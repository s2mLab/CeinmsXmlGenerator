
class EMG_driven:
    def __init__(self, dofs, vTendon):
        self.dofs = dofs
        self.vTendon = vTendon



    @staticmethod
    def name():
        return "EMG_driven"

    @staticmethod
    def dict():
        return {
            "NMSmodel": {
                "type": {"openLoop": None},
                "tendon": {self.vTendon: None},
                "activation": {"exponential": None}
            },
            "online": None,
            "elaboratedDoFs": self.dofs
        }



class Hybrid:
    def __init__(self, dofs, vTendon):
        self.dofs = dofs
        self.vTendon = vTendon

    @staticmethod
    def name():
        return "Hybrid"

    @staticmethod
    def dict():
        return {
            "NMSmodel": {
                "type": {"hybrid": {
                    "dofSet": self.dofs,
                    "alpha": 1,
                    "beta":  5,
                    "gamma": 5,
                    "synthMTUs": ("CORB", "LVS", "PECM1", "PECM3", "PMN", "RMJ1", "RMJ2", "RMN", "SBCL", "SRA2", "SRA3",
                                  "TMAJ", "TMIN"),
                    "adjustMTUs": ("DELT1", "DELT2", "DELT3", "INFSP", "LAT", "PECM2", "SRA1", "SUBSC", "SUPSP", "TRP1",
                                   "TRP2", "TRP3", "TRP4"),
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
                "tendon": {"stiff": None},
                "activation": {"exponential": None}
            },
            "online": None,
            "elaboratedDoFs": self.dofs
        }
