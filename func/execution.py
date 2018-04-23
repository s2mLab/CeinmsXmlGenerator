
class EMG_driven_Stiff:
    @staticmethod
    def name():
        return "EMG_driven_Stiff"

    @staticmethod
    def dict():
        return {
            "NMSmodel": {
                "type": {"openLoop": None},
                "tendon": {"stiff": None},
                "activation": {"exponential": None}
            },
            "online": None,
            "elaboratedDoFs": {}
        }


class EMG_driven_Elastic:
    @staticmethod
    def name():
        return "EMG_driven_Elastic"

    @staticmethod
    def dict():
        return {
            "NMSmodel": {
                "type": {"openLoop": None},
                "tendon": {"equilibriumElastic": None},
                "activation": {"exponential": None}
            },
            "online": None,
            "elaboratedDoFs": {}
        }


class Hybrid_Sitff:
    @staticmethod
    def name():
        return "Hybrid_Sitff"

    @staticmethod
    def dict():
        return {
            "NMSmodel": {
                "type": {"hybrid": {
                    "dofSet": ("sternoclavicular_r1", "sternoclavicular_r2", "Acromioclavicular_r1",
                               "Acromioclavicular_r2", "Acromioclavicular_r3", "shoulder_plane", "shoulder_ele",
                               "shoulder_rotation"),
                    "alpha": 1,
                    "beta": 5,
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
            "elaboratedDoFs": ("sternoclavicular_r1", "sternoclavicular_r2", "Acromioclavicular_r1",
                               "Acromioclavicular_r2", "Acromioclavicular_r3", "shoulder_plane",
                               "shoulder_ele", "shoulder_rotation")
        }
