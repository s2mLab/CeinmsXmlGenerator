from func.CeinmWriter import CeinmWriter
from func import utils

# Define base path
base_path, ceinms_path = utils.determine__base_paths()


# # # DEFINE DoF, MODELS and SUBJECT, vCalibTrials, Trials # # #
uncalib_model_path = base_path + "DapO/models/1_scaled_and_markersMICK.osim"
model_name = 'Wu'  # "Wu"| 'DAS3'
subject = 'DapO'
dof = 'G'  # 'G' | 'SAG"
dof_list = ("shoulder_ele", "shoulder_plane", "shoulder_rotation")
v_calib_trials = 1
v_tendon = 'stiff'  # | 'elastic'
trials = 'All'  # | 'All' | 'AllButCalib' | 'Calib'
force_recalib = False
# # # END OF THE MAIN VARIABLES # # #

# Setup the trials
setup_calib, setup_trials = utils.prepare_setup(base_path, model_name, subject, uncalib_model_path,
                                                v_calib_trials, dof_list, dof, v_tendon, trials, force_recalib)


# Write configuration and calibration files
cw = CeinmWriter(base_path, setup_calib, ceinms_path)

# Run calibration process if needed
cw.calibrate()

# Run
cw.run(setup_trials)
