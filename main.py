from func import models, excitations, calibrations, utils, execution
from func.CeinmWriter import Writer

# Define base path
base_path, ceinms_path = utils.determine__base_paths()


# # # DEFINE DoF, MODELS and SUBJECT, vCalibTrials, Trials # # #
subject = 'DapO'
uncalib_model_path = base_path + "%s/models/1_generic_MICK_Wu_v5_test2.osim" % (subject)
model_name = 'Wu'  # "Wu"| 'DAS3'
joints = 'G'  # 'G' | 'SAG"
v_calib_trials = 1
v_tendon = 'stiff' #'stiff' | 'equilibriumElastic'
trials = 'All'  # | 'All' | 'AllButCalib' | 'Calib'
force_recalib = False

excitations_type = eval('excitations.%s_v%d' % (model_name, 3) )# use v3
calibrations_type = eval('calibrations.%s_%s_v%d' % (model_name, joints, 1) ) # used v1
execution_type = 'Hybrid'  # TODO with Benjamin improve approach # EMGdriven | Hydrib | Static_optim

# # # END OF THE MAIN VARIABLES # # #
model_type = eval('models.%s' % model_name)
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
