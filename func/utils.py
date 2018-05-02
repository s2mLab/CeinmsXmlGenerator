import os
import glob

from func import execution, CeinmWriter
from func.CeinmWriter import CeinmWriter


def determine__base_paths():
    if os.uname()[1] == 'DESKTOP-4KTED5M':
        base_path = "C:/Users/micka/Dropbox/Projet_EMGdriven/test_1/"
        ceinms_path = "C:/Programming/CEINMS_dev/bin"
    elif os.uname()[1] == 'bimec29-kinesio':
        base_path = "/home/pariterre/Dropbox/test_1/"
        ceinms_path = "~/Documents/Laboratoire/Programmation/CEINMS/ceinms/release/bin"
    else:
        raise NotImplementedError("Please add your computer to determine_path.py script")
    return base_path, ceinms_path


def build_and_setup_model(base_path, subject, model_name, uncalib_model_path,
                          dof_list, dof, trials, v_calib_trials, v_tendon,
                          model_type, excitations_type, calibrations_type, force_recalib):
    uncalib_model = model_type(uncalib_model_path, dof_list)
    excitation = excitations_type()
    model, subject_path, dof_name, calib_trials, trials = prepare_model_and_trials(subject, base_path,
                                                                                   model_name, dof,
                                                                                   v_calib_trials, trials)
    calib = calibrations_type(calib_trials, dof_name, v_tendon, model)
    setup_calib, setup_trials = prepare_setup(uncalib_model, dof_name, trials, excitation,
                                              calib, v_tendon, force_recalib)

    return model, setup_calib, setup_trials


def prepare_model_and_trials(subject, base_path, model_name, dof, v_calib_trials, trials):
    subject_path = "./" + subject + "/Trials/"
    model = load_model(model_name)

    if model["ModelName"].lower() == 'wu' or model["ModelName"].lower() == 'das3':
        if dof.lower() == 'g':
            dof_name = model["DoFName"][-3:]
        else:
            raise ValueError("Wrong value for dof")
    elif dof.lower() == 'sag':
        dof_name = model["DoFName"][0:2] + model["DoFName"][3:]  # improve?
    else:
        raise ValueError("Wrong value for model")
    print("DoF for CEINMS are: " + str(dof_name))

    # # # CHOOSE CalibTrials and Trials # # #
    # xHy_z   with x=6|12|18 y=1-6  z=1-3
    if v_calib_trials == 1:
        calib_trials = []  # initialiser avec un mouvement fonctionnel
        x = [6, 12, 18]  # kg
        y = 1  # changer pour excentric yeux -> hanches qd tout généré par Romain
        z = 1  # x= all,
        for i in x:
            calib_trials += glob.glob(os.path.join(base_path, subject_path) + "/" + model_name.lower() + "*" + str(i) +
                                      "*" + str(y) + "_" + str(z) + ".xml")
    else:
        raise ValueError("Wrong value for v_calib_trials")

    # regarder tous les dossiers et générer les xml
    for subdir in next(os.walk(os.path.join(base_path, subject_path)))[1]:
        fname = os.path.join(base_path, subject_path, subdir + '.xml')
        if subdir.startswith(model["ModelName"].lower()) and not os.path.isfile(fname):
            print("Generate xml for trial: " + subdir)
            CeinmWriter.generate_trial_xml(model, os.path.join(base_path, subject_path, subdir), fname)

    # # # GENERATE trials.xml # # #
    if trials.lower() == 'all':
        _trials = glob.glob(os.path.join(base_path, subject_path) + "/" + model_name.lower() + "*.xml")
    elif trials.lower() == 'allbutcalib':
        _trials = glob.glob(os.path.join(base_path, subject_path) + "/" + model_name.lower() + "*.xml")
        for i in calib_trials:
            _trials.remove(i)
    elif trials.lower() == 'calib':
        _trials = calib_trials
    else:
        raise ValueError("wrong value for trials")

    calib_trials = tuple(calib_trials)
    print('********* Calibration Files **********')
    print(calib_trials)
    _trials = tuple(_trials)
    print('********* Files of Interest **********')
    print(_trials)

    return model, subject_path, dof_name, calib_trials, trials


def prepare_setup(uncalibrated_model, dof_name, trials, excitations, calibration, v_tendon,  force_recalib):

    # # # CALIB # # #
    setup_calib = CeinmWriter.SetupCalib()
    setup_calib.uncalibrated_model = uncalibrated_model
    setup_calib.excitation = excitations
    setup_calib.calibration = calibration
    setup_calib.force_calibration = force_recalib

    # # # TRIALS # # #
    setup_trials = CeinmWriter.SetupTrial()
    setup_trials.execution = execution.EMG_driven(dof_name, v_tendon)  # EMG_driven Hybrid
    setup_trials.allow_override = True
    setup_trials.trials = trials
    ##################
    return setup_calib, setup_trials


def load_model(model_name):
    # TODO : pourrait être plus efficace de lire un fichier osim
    print("Model : " + model_name)
    if model_name.lower() == "wu":
        return {"ModelName": "Wu",
                "DoFName": ("sternoclavicular_r1", "sternoclavicular_r2", "sternoclavicular_r3",
                            "Acromioclavicular_r1", "Acromioclavicular_r2", "Acromioclavicular_r3",
                            "shoulder_plane", "shoulder_ele", "shoulder_rotation"),
                "MTUNames": ("LVS", "SBCL",
                             "TRP1", "TRP2", "TRP3", "TRP4",
                             "RMN", "RMJ1", "RMJ2",
                             "SRA1", "SRA2", "SRA3", "PMN",
                             "DELT1", "DELT2", "DELT3",
                             "SUPSP", "INFSP", "SUBSC", "TMIN",
                             "TMAJ", "PECM1", "PECM2", "PECM3", "LAT", "CORB"),
                "MTUgroups": {"g1": ("LVS", "SBCL"),
                              "g2": ("TRP1", "TRP2", "TRP3", "TRP4"),
                              "g3": ("RMN", "RMJ1", "RMJ2"),
                              "g4": ("SRA1", "SRA2", "SRA3"),
                              "g5": ("DELT1", "DELT2", "DELT3"),
                              "g6": ("SUPSP", "INFSP", "SUBSC", "TMIN"),
                              "g7": ("PECM1", "PECM2", "PECM3"),
                              "g8": ("PMN", "LAT", "TMAJ"),
                              "g9": "CORB"}
                }  # ADD BICEPS and TRICEPS
    elif model_name.lower() == "das3":
        return {"ModelName": "DAS3",
                "DoFName": ("SC_x", "SC_y", "SC_z", "AC_x", "AC_y", "AC_z", "GH_x", "GH_y", "GH_z"),
                "MTUNames": (
                     "trap_scap_1", "trap_scap_2", "trap_scap_3", "trap_scap_4", "trap_scap_5", "trap_scap_6",
                     "trap_scap_7", "trap_scap_8", "trap_scap_9", "trap_scap_10", "trap_scap_11", "trap_clav_1",
                     "trap_clav_2",
                     "lev_scap_1", "lev_sca_2", "rhomboid_1", "rhomboid_2", "rhomboid_3", "rhomboid_4",
                     "rhomboid_5",
                     "serr_ant_1", "serr_ant2", "serr_ant3", "serr_ant4", "serr_ant5", "serr_ant6", "serr_ant_7",
                     "serr_ant8", "serr_ant9", "serr_ant10", "serr_ant11", "serr_ant12",
                     "delt_scap_1", "delt_scap_2", "delt_scap_3", "delt_scap_4", "delt_scap_5", "delt_scap_6",
                     "delt_scap_7", "delt_scap_8", "delt_scap_9", "delt_scap_10", "delt_scap_11", "delt_clav_1",
                     "delt_clav_2", "delt_clav_3", "delt_clav_4",
                     "infra_1", "infra_2", "infra_3", "infra_4", "infra_5", "infra_6",
                     "ter_min_1", "ter_min_2", "ter_min_3",
                     "supra_1", "supra_2", "supra_3", "supra_4",
                     "subscap_1", "subscap_2", "subscap_3", "subscap_4", "subscap_5", "subscap_6", "subscap_7",
                     "subscap_8",
                     "subscap_9", "subscap_10", "subscap_11",
                     "ter_maj_1", "ter_maj_2", "ter_maj_3", "ter_maj_4",
                     "bic_l", "bic_b_1", "bic_b_2",
                     "tric_long_1", "tric_long_2", "tric_long_3", "tric_long_4", "tric_med_1", "tric_med_2",
                     "tric_med_3", "tric_med_4", "tric_med_5", "tric_lat_1", "tric_lat_2", "tric_lat_3",
                     "tric_lat_4",
                     "tric_lat_5",
                     "lat_dorsi_1", "lat_dorsi_2", "lat_dorsi_3", "lat_dorsi_4", "lat_dorsi_5", "lat_dorsi_6",
                     "pect_maj_t_1", "pect_maj_t_2", "pect_maj_t_3", "pect_maj_t_4", "pect_maj_t_5", "pect_maj_t_6",
                     "pect_maj_c_1", "pect_maj_c_2",
                     "pect_min_1", "pect_min_2", "pect_min_3", "pect_min_4",
                     "brachialis_1", "brachialis_2", "brachialis_3", "brachialis_4", "brachialis_5", "brachialis_6",
                     "brachialis_7", "brachiorad_1", "brachiorad_2",
                     "coracobr_1", "coracobr_2",
                     "coracobr_3")
                }
    else:
        raise NotImplementedError("Wrong model_name")


def write_model(model, ):
    pass
