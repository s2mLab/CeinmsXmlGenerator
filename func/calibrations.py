def choose(model_name, joints, v_calib_trials):
    if model_name.lower() == 'wu' and joints.lower() == 'g' and v_calib_trials == 1:
        return Wu_G_v1
    elif model_name.lower() == 'wu' and joints.lower() == 'sag' and v_calib_trials == 1:
        return Wu_SAG_v1
    else:
        raise NotImplementedError("Model cannot be chosen")


class Wu_G_v1:
    def __init__(self, calib_trials, dofs, vtendon, model):
        self.calib_trials = calib_trials
        self.dofs = dofs
        self.vTendon = vtendon
        self.groups = model["MTUgroups"]

    @staticmethod
    def name():
        return "Wu_G_v1"

    def calib(self):
        return {
            "algorithm": {
                "simulatedAnnealing": {
                    "noEpsilon": 4,
                    "rt": 0.05,
                    "T": 200000,
                    "NS": 10,
                    "NT": 4,
                    "epsilon": "1.E-3",
                    "maxNoEval": 2000000
                }
            },
            "NMSmodel": {
                "type": {"openLoop": None},
                "tendon": {self.vTendon: None},
                "activation": {"exponential": None}
            },
            "calibrationSteps": {
                "step": {
                    "dofs": self.dofs,  # ("shoulder_plane", "shoulder_ele", "shoulder_rotation"),
                    "objectiveFunction": {"minimizeTorqueError": None},
                    "parameterSet": {
                        "parameter": (
                            {"name": "c1", "global": None, "absolute": {"range": (-0.95, -0.05)}},
                            {"name": "c2", "global": None, "absolute": {"range": (-0.95, -0.05)}},
                            {"name": "shapeFactor",
                             "muscleGroups": {
                                 "muscles__RM_BEGIN__0__RM_END__": self.groups["g5"],  # ("DELT1", "DELT2", "DELT3"),
                                 "muscles__RM_BEGIN__1__RM_END__": self.groups["g6"],  # ("SUPSP", "INFSP",
                                                                                       # "SUBSC", "TMIN"),
                                 "muscles__RM_BEGIN__2__RM_END__": self.groups["g7"],  # ("PECM1", "PECM2", "PECM3"),
                                 "muscles__RM_BEGIN__3__RM_END__": ("LAT", ""),
                                 "muscles__RM_BEGIN__4__RM_END__": ("tric_long", ""),
                                 "muscles__RM_BEGIN__5__RM_END__": self.groups["g10"]},  # ("bic_l","bic_b"),
                             "absolute": {"range": (-2.999, -0.001)}}, {
                                "name": "tendonSlackLength",
                                "single": None,
                                "relativeToSubjectValue": {
                                    "range": (0.9, 1.1)
                                }
                            }, {
                                "name": "optimalFibreLength",
                                "single": None,
                                "relativeToSubjectValue": {
                                    "range": (0.9, 1.1)
                                }
                            }, {
                                "name": "strengthCoefficient",
                                "single": None,
                                "absolute": {
                                    "range": (0.2, 6)
                                }
                            },
                        ),
                    }
                }
            },
            "trialSet": self.calib_trials
        }

class Wu_SAG_v1:
    def __init__(self, calib_trials, dofs, vtendon, model):
        self.calib_trials = calib_trials
        self.dofs = dofs
        self.vTendon = vtendon
        self.groups = model["MTUgroups"]

    @staticmethod
    def name():
        return "Wu_SAG_v1"

    def calib(self):
        return {
            "algorithm": {
                "simulatedAnnealing": {
                    "noEpsilon": 4,
                    "rt": 0.05,
                    "T": 200000,
                    "NS": 10,
                    "NT": 4,
                    "epsilon": "1.E-3",
                    "maxNoEval": 2000000
                }
            },
            "NMSmodel": {
                "type": {"openLoop": None},
                "tendon": {self.vTendon: None},
                "activation": {"exponential": None}
            },
            "calibrationSteps": {
                "step": {
                    "dofs": self.dofs,  # ("shoulder_plane", "shoulder_ele", "shoulder_rotation"),
                    "objectiveFunction": {"minimizeTorqueError": None},
                    "parameterSet": {
                        "parameter": (
                            {"name": "c1", "global": None, "absolute": {"range": (-0.95, -0.05)}},
                            {"name": "c2", "global": None, "absolute": {"range": (-0.95, -0.05)}},
                            {"name": "shapeFactor",
                             "muscleGroups": {
                                 "muscles__RM_BEGIN__0__RM_END__": self.groups["g1"],  # ("LVS", "SBCL"),
                                 "muscles__RM_BEGIN__1__RM_END__": self.groups["g2"],  # ("TRP1", "TRP2", "TRP3", "TRP4"),
                                 "muscles__RM_BEGIN__2__RM_END__": self.groups["g3"],  # ("RMN", "RMJ1", "RMJ2"),
                                 "muscles__RM_BEGIN__3__RM_END__": self.groups["g4"],  # ("SRA1", "SRA2", "SRA3")
                                 "muscles__RM_BEGIN__4__RM_END__": self.groups["g5"],  # ("DELT1", "DELT2", "DELT3"),
                                 "muscles__RM_BEGIN__5__RM_END__": self.groups["g6"],  # ("SUPSP", "INFSP", "SUBSC", "TMIN"),
                                 "muscles__RM_BEGIN__6__RM_END__": self.groups["g7"],  # ("PECM1", "PECM2", "PECM3"),
                                 "muscles__RM_BEGIN__7__RM_END__": ("LAT", ""),
                                 "muscles__RM_BEGIN__8__RM_END__": ("tric_long", ""),
                                 "muscles__RM_BEGIN__9__RM_END__": self.groups["g10"]},  # ("bic_l","bic_b"),
                             "absolute": {"range": (-2.999, -0.001)}}, {
                                "name": "tendonSlackLength",
                                "single": None,
                                "relativeToSubjectValue": {
                                    "range": (0.9, 1.1)
                                }
                            }, {
                                "name": "optimalFibreLength",
                                "single": None,
                                "relativeToSubjectValue": {
                                    "range": (0.9, 1.1)
                                }
                            }, {
                                "name": "strengthCoefficient",
                                "single": None,
                                "absolute": {
                                    "range": (0.2, 6)
                                }
                            },
                        ),
                    }
                }
            },
            "trialSet": self.calib_trials
        }