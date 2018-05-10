
def choose(model_name, version):
    if model_name.lower() == 'wu' and version == 1:
        return Wu_v1
    elif model_name.lower() == 'wu' and version == 3:
        return Wu_v3
    else:
        raise NotImplementedError("Model cannot be chosen")


class Wu_v1:
    @staticmethod
    def name():
        return "Wu_v1"

    @staticmethod
    def excitation():
        return {
            "input_signals": {
                "EMG": (
                    "Delt_ant", "Delt_med", "Delt_post", "Biceps", "Triceps", "Trap_sup", "Trap_inf", "Gd_dent",
                    "Supra", "Infra", "Subscap", "Pec", "Gd_dors")
            },
            "mapping": {
                'TRP1': (1, "Trap_sup"), 
                'TRP2': (1, "Trap_sup"),
                'TRP4': (1, "Trap_inf"),
                'SRA2': (1, "Gd_dent"),
                'SRA3': (1, "Gd_dent"),
                'DELT1': (1, "Delt_ant"),
                'DELT2': (1, "Delt_med"),
                'DELT3': (1, "Delt_post"),
                'SUPSP': (1, "Supra"),
                'INFSP': (1, "Infra"),
                'SUBSC': (1, "Subscap"),
                'PECM2': (1, "Pec"),
                'LAT': (1, "Gd_dors"),
            }
        }


class Wu_v3:
    @staticmethod
    def name():
        return "Wu_v3"

    @staticmethod
    def excitation():
        return {
            "input_signals": {
                "EMG": (
                    "Delt_ant", "Delt_med", "Delt_post", "Biceps", "Triceps", "Trap_sup", "Trap_inf", "Gd_dent",
                    "Supra", "Infra", "Subscap", "Pec", "Gd_dors")
            },
            "mapping": {
                'TRP1': (1, "Trap_sup"),
                'TRP2': (1, "Trap_sup"),
                'TRP3': (0.5, "Trap_inf", 0.5, "Trap_sup"),
                'TRP4': (1, "Trap_inf"),
                'SRA2': (1, "Gd_dent"),
                'SRA3': (1, "Gd_dent"),
                'DELT1': (1, "Delt_ant"),
                'DELT2': (1, "Delt_med"),
                'DELT3': (1, "Delt_post"),
                'SUPSP': (1, "Supra"),
                'INFSP': (1, "Infra"),
                'TMIN': (1, "Infra"),
                'SUBSC': (1, "Subscap"),
                'PECM1': (1, "Pec"),
                'PECM2': (1, "Pec"),
                'PECM3': (1, "Pec"),
                'LAT': (1, "Gd_dors"),
                'bic_l': (1, "Biceps"),
                'bic_b': (1, "Biceps"),
                'tric_long': (1, "Triceps"),
            }
        }
