class Execution:
    def __init__(self, dofs, v_tendon): #TODO add list of muscles to check if all muscles are here in hybrid
        self.dofs = dofs
        self.v_tendon = v_tendon

class EMG_driven(Execution):
    def __init__(self, dofs, v_tendon):
        super(EMG_driven, self).__init__(dofs, v_tendon)

    @staticmethod
    def name():
        return "EMG_driven"

    def dict(self):
        return {
            "NMSmodel": {
                "type": {"openLoop": None},
                "tendon": {self.v_tendon: None},
                "activation": {"exponential": None}
            },
            "online": None,
            "elaboratedDoFs": self.dofs
        }


class Hybrid(Execution):
    def __init__(self, dofs, v_tendon):
        super(Hybrid, self).__init__(dofs, v_tendon)

    @staticmethod
    def name():
        return "Hybrid"
        # calculate the rms activation from staticoptim (process in Opensim)
        # calculate the rms emg excitation (only muscles used)
        # calculate the rms join torques (only joint used)
        # ensure that 1% rms on joint torque = 1% rms on emgs and 10-20% rms of least excitations

    def dict(self):
        return {
            "NMSmodel": {
                "type": {"hybrid": {
                    "dofSet": self.dofs,
                    "alpha": 5, #TODO: determine way to automatically weight alpha, beta, gamma
                    "beta":  1,#alpha: torque fitting, beta: least excitations; gamma: emg fitting
                    "gamma": 50,
                    "synthMTUs": ("CORB", "LVS", "PECM1", "PECM3", "PMN", "RMJ1", "RMJ2", "RMN", "SBCL", "SRA2", "SRA3",
                                  "TMAJ", "TMIN"),
                    "adjustMTUs": ("DELT1", "DELT2", "DELT3", "INFSP", "LAT", "PECM2", "SRA1", "SUBSC", "SUPSP", "TRP1",
                                   "TRP2", "TRP3", "TRP4", "bic_l", "bic_b", "tric_long"),
                    "algorithm": {
                        "simulatedAnnealing": {
                            "noEpsilon": 4,
                            "rt": 0.05,
                            "T": 200000,
                            "NS": 30,
                            "NT": 10,
                            "epsilon": "1.E-3",
                            "maxNoEval": 2000000
                        }
                    }
                }},
                "tendon": {self.v_tendon: None},
                "activation": {"exponential": None}
            },
            "online": None,
            "elaboratedDoFs": self.dofs
        }

class Static_optim(Execution):
    def __init__(self, dofs, v_tendon):
        super(static_optim, self).__init__(dofs, v_tendon)

    @staticmethod
    def name():
        return "Static_optim"

    def dict(self):
        return {
            "NMSmodel": {
                "type": {"hybrid": {
                    "dofSet": self.dofs,
                    "alpha": 1,
                    "beta":  5,
                    "gamma": 0,
                    "synthMTUs": ("CORB", "LVS", "PECM1", "PECM3", "PMN", "RMJ1", "RMJ2", "RMN", "SBCL", "SRA2", "SRA3",
                                  "TMAJ", "TMIN","DELT1", "DELT2", "DELT3", "INFSP", "LAT", "PECM2", "SRA1", "SUBSC", "SUPSP", "TRP1",
                                   "TRP2", "TRP3", "TRP4", "bic_l", "bic_b", "tric_long"),
                    "adjustMTUs": (),
                    "algorithm": {
                        "simulatedAnnealing": {
                            "noEpsilon": 4,
                            "rt": 0.05,
                            "T": 200000,
                            "NS": 30,
                            "NT": 10,
                            "epsilon": "1.E-3",
                            "maxNoEval": 2000000
                        }
                    }
                }},
                "tendon": {self.v_tendon: None},
                "activation": {"exponential": None}
            },
            "online": None,
            "elaboratedDoFs": self.dofs
        }