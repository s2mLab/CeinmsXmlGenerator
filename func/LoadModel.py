def LoadModel(ModelName):

    if ModelName.lower() == "wu":
        Model = {"ModelName": "Wu",
            "DoFName" : ("sternoclavicular_r1", "sternoclavicular_r2", "sternoclavicular_r3",
                         "Acromioclavicular_r1", "Acromioclavicular_r2", "Acromioclavicular_r3",
                         "shoulder_plane", "shoulder_ele", "shoulder_rotation"),
            "MTUNames" : ("LVS", "SBCL",
                          "TRP1", "TRP2", "TRP3", "TRP4",
                          "RMN", "RMJ1", "RMJ2",
                          "SRA1", "SRA2", "SRA3", "PMN",
                          "DELT1", "DELT2", "DELT3",
                          "SUPSP", "INFSP", "SUBSC", "TMIN",
                          "TMAJ", "PECM1", "PECM2", "PECM3", "LAT", "CORB"),
            "MTUgroups" : {"g1": ("LVS", "SBCL"),
                           "g2": ("TRP1", "TRP2", "TRP3", "TRP4"),
                           "g3": ("RMN", "RMJ1", "RMJ2"),
                           "g4": ("SRA1", "SRA2", "SRA3"),
                           "g5": ("DELT1", "DELT2", "DELT3"),
                           "g6": ("SUPSP", "INFSP", "SUBSC", "TMIN"),
                           "g7": ("PECM1", "PECM2", "PECM3"},
                           "g8": ( "PMN","LAT", "TMAJ"),
                           "g9": ("CORB")}
                 } #ADD BICEPS and TRICEPS
    elif ModelName.lower() == "das3":
        Model = {"ModelName": "DAS3",
            "DoFName" : ("SC_x", "SC_y", "SC_z", "AC_x", "AC_y", "AC_z", "GH_x", "GH_y", "GH_z"),
            "MTUNames": (
            "trap_scap_1", "trap_scap_2", "trap_scap_3", "trap_scap_4", "trap_scap_5", "trap_scap_6", "trap_scap_7", "trap_scap_8", "trap_scap_9", "trap_scap_10", "trap_scap_11", "trap_clav_1", "trap_clav_2",
            "lev_scap_1", "lev_sca_2", "rhomboid_1", "rhomboid_2", "rhomboid_3", "rhomboid_4", "rhomboid_5",
            "serr_ant_1", "serr_ant2", "serr_ant3", "serr_ant4", "serr_ant5", "serr_ant6", "serr_ant_7", "serr_ant8", "serr_ant9", "serr_ant10", "serr_ant11", "serr_ant12",
            "delt_scap_1", "delt_scap_2", "delt_scap_3", "delt_scap_4", "delt_scap_5", "delt_scap_6", "delt_scap_7",  "delt_scap_8", "delt_scap_9", "delt_scap_10", "delt_scap_11", "delt_clav_1", "delt_clav_2", "delt_clav_3", "delt_clav_4",
            "infra_1", "infra_2", "infra_3", "infra_4", "infra_5", "infra_6",
            "ter_min_1", "ter_min_2", "ter_min_3",
            "supra_1", "supra_2", "supra_3", "supra_4",
            "subscap_1", "subscap_2", "subscap_3", "subscap_4", "subscap_5", "subscap_6", "subscap_7", "subscap_8",
            "subscap_9", "subscap_10", "subscap_11",
            "ter_maj_1", "ter_maj_2", "ter_maj_3", "ter_maj_4",
            "bic_l", "bic_b_1", "bic_b_2",
            "tric_long_1", "tric_long_2", "tric_long_3", "tric_long_4", "tric_med_1", "tric_med_2", "tric_med_3", "tric_med_4", "tric_med_5", "tric_lat_1", "tric_lat_2", "tric_lat_3", "tric_lat_4", "tric_lat_5",
            "lat_dorsi_1", "lat_dorsi_2", "lat_dorsi_3", "lat_dorsi_4", "lat_dorsi_5", "lat_dorsi_6",
            "pect_maj_t_1", "pect_maj_t_2", "pect_maj_t_3", "pect_maj_t_4", "pect_maj_t_5", "pect_maj_t_6", "pect_maj_c_1", "pect_maj_c_2",
            "pect_min_1", "pect_min_2", "pect_min_3", "pect_min_4",
            "brachialis_1", "brachialis_2", "brachialis_3", "brachialis_4", "brachialis_5", "brachialis_6", "brachialis_7", "brachiorad_1", "brachiorad_2",
            "coracobr_1", "coracobr_2", "coracobr_3")} ## pourrait être plus efficace de lire un fichier osim


        print("Model : " + Model["ModelName"])
        return Model