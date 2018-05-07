from func import models, excitations, calibrations, utils, execution
from func.CeinmWriter import Writer

# Define base path
base_path, ceinms_path = utils.determine__base_paths()


# # # DEFINE DoF, MODELS and SUBJECT, vCalibTrials, Trials # # #
uncalib_model_path = base_path + "DapO/models/1_scaled_and_markersMICK.osim"
model_name = 'Wu'  # "Wu"| 'DAS3'
subject = 'DapO'
dof = 'G'  # 'G' | 'SAG"
#dof_list = ("shoulder_ele", "shoulder_plane", "shoulder_rotation")
v_calib_trials = 1
v_tendon = 'stiff'  # | 'elastic'
trials = 'All'  # | 'All' | 'AllButCalib' | 'Calib'
force_recalib = False

model_type = models.Wu
excitations_type = excitations.Wu_v3
calibrations_type = calibrations.Wu_GH_v1
execution_type = []  # TODO execution.EMGdriven # EMGdriven | Hydrib | Static_optim
# # # END OF THE MAIN VARIABLES # # #

# Setup the trials
model, setup_calib, setup_trials = utils.build_and_setup_model(base_path, subject, model_name, uncalib_model_path,
                                                               dof, trials, v_calib_trials, v_tendon,
                                                               model_type, excitations_type, calibrations_type, execution_type,
                                                               force_recalib)

# Write configuration and calibration files
cw = Writer(base_path, setup_calib, ceinms_path)

# Run calibration process if needed
cw.calibrate()

# Run
cw.run(setup_trials, excitations_type)
