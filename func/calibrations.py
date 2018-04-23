
class SimulatedAnnealing:
    def __init__(self, calib_trials, dofs, vTendon):
        self.calib_trials = calib_trials
        self.dofs = dofs
        self.vTendon = vTendon

        Wu_Muscles = ["LVS", "SBCL",
                      "TRP1", "TRP2", "TRP3", "TRP4",
                      "RMN", "RMJ1", "RMJ2",
                      "SRA1", "SRA2", "SRA3", "PMN",
                      "DELT1", "DELT2", "DELT3",
                      "SUPSP", "INFSP", "SUBSC", "TMIN",
                      "TMAJ", "PECM1", "PECM2", "PECM3", "LAT", "CORB"]



@staticmethod
    def name():
        return "Wu_GH_v1"

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
                    "dofs": self.dofs, #("shoulder_plane", "shoulder_ele", "shoulder_rotation"),
                    "objectiveFunction": {"minimizeTorqueError": None},
                    "parameterSet": {
                        "parameter": (
                            {"name": "c1", "global": None, "absolute": {"range": (-0.95, -0.05)}},
                            {"name": "c2", "global": None, "absolute": {"range": (-0.95, -0.05)}},
                            {"name": "shapeFactor",
                             "muscleGroups": {"muscles__RM_BEGIN__0__RM_END__": ("DELT1", "DELT2", "DELT3"),
                                              "muscles__RM_BEGIN__1__RM_END__": ("SUPSP", "INFSP", "SUBSC", "TMIN"),
                                              "muscles__RM_BEGIN__2__RM_END__": ("PECM1", "PECM2", "PECM3"),
                                              "muscles__RM_BEGIN__3__RM_END__": ("LAT", "")},
                             "absolute": {"range": (-2.999, -0.001)}},
                            {"name": "tendonSlackLength",   "single": None, "relativeToSubjectValue": {"range": (0.9, 1.1)}},
                            {"name": "optimalFibreLength",  "single": None, "relativeToSubjectValue": {"range": (0.9, 1.1)}},
                            {"name": "strengthCoefficient", "single": None, "absolute": {"range": (0.3, 6)}},
                        ),
                    }
                }
            },
            "trialSet": self.calib_trials
        }

