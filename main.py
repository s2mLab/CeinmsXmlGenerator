from func import models, excitations, calibrations, utils, execution
from func.CeinmWriter import Writer

# Define base path
base_path, ceinms_path = utils.determine__base_paths()


# # # DEFINE DoF, MODELS and SUBJECT, vCalibTrials, Trials # # #
subject = 'DapO'
uncalib_model_path = base_path + "%s/models/1_generic_MICK_Wu_v5_test2.osim" % (subject)
model_name = 'Wu'  # "Wu"| 'DAS3'
joints = 'SAG'  # 'G' | 'SAG"
v_calib_trials = 1
v_tendon = 'stiff' #'stiff' | 'equilibriumElastic'
trials = 'All'  # | 'All' | 'AllButCalib' | 'Calib'
force_recalib = False

model_type = models.Wu
excitations_type = excitations.Wu_v3
calibrations_type = calibrations.Wu_SAG_v1 # Wu_GH_v1 Wu_SAG_v1
execution_type = []  # TODO with Benjamin execution.EMGdriven # EMGdriven | Hydrib | Static_optim
# # # END OF THE MAIN VARIABLES # # #

# Setup the trials
model, setup_calib, setup_trials = utils.build_and_setup_model(base_path, subject, model_name, uncalib_model_path,
                                                               joints, trials, v_calib_trials, v_tendon,
                                                               model_type, excitations_type, calibrations_type, execution_type,
                                                               force_recalib)

# Write configuration and calibration files
cw = Writer(base_path, setup_calib, ceinms_path)

# Run calibration process if needed
cw.calibrate()

# Run
cw.run(setup_trials, excitations_type)
