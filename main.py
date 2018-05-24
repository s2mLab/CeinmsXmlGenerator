from func import models, excitations, calibrations, utils, execution
from func.CeinmWriter import Writer

# Define base path
base_path, ceinms_path = utils.determine__base_paths()


# # # DEFINE DoF, MODELS and SUBJECT, vCalibTrials, Trials # # #
subject = 'DapO'
uncalib_model_path = f"{base_path}/{subject}/models/wu.osim"
model_to_add = f"{base_path}/{subject}/models/box.osim"

model_name = 'Wu'  # "Wu"| 'DAS3'
v_tendon = 'stiff'  # 'stiff' | 'equilibriumElastic'
trials = 'All'  # | 'All' | 'AllButCalib' | 'Calib'
force_recalib = True
v_calib_trials = 1
joints = 'G'  # 'G' | 'SAG"
excitation_version = 3
exec_type = 'hybrid'

model_type = models.choose(model_name)
excitations_type = excitations.choose(model_name, excitation_version)
calibrations_type = calibrations.choose(model_name, joints, v_calib_trials)
execution_type = execution.choose(model_name, joints, exec_type)  # TODO with Benjamin improve approach # EMGdriven | Hydrib | Static_optim

# # # END OF THE MAIN VARIABLES # # #
# Setup the trials
model, setup_calib, setup_trials = utils.build_and_setup_model(base_path, subject, model_name, uncalib_model_path,
                                                               joints, trials, v_calib_trials, v_tendon,
                                                               model_type, excitations_type, calibrations_type,
                                                               execution_type, force_recalib)

# Write configuration and calibration files
cw = Writer(base_path, setup_calib, ceinms_path)

# Run calibration process if needed
cw.calibrate()

# Add the box to the model
models.OsimModel.combine_models(cw.calibrated_model_path, model_to_add)

# Run
cw.run(setup_trials, excitations_type)
