from func import calibrations, excitations, execution, models
from func.CeinmWriter import CeinmWriter, SetupCalib, SetupTrial

base_path = "/home/pariterre/Dropbox/test_1/test_hierarchie/"
calib_trials = ("../../../DapO/Trials/F6H1_1.xml", "../../../DapO/Trials/F6H1_1.xml")
trials = ("../../Trials/F6H1_1.xml", "../../Trials/F6H1_1.xml")
ceinms_path = "~/Documents/Laboratoire/Programmation/CEINMS/ceinms/release/bin"

# # # CALIB # # #
setup_calib = SetupCalib()
setup_calib.uncalibrated_model = models.Wu
setup_calib.excitation = excitations.EMG
setup_calib.calibration = calibrations.SimulatedAnnealing(calib_trials)
setup_calib.force_calibration = True
#################

# # # TRIALS # # #
setup_trials = SetupTrial()
setup_trials.execution = execution.Stiff
setup_trials.allow_override = True
##################

# Write configuration and calibration files
cw = CeinmWriter(base_path, setup_calib, ceinms_path)

# Run calibration process if needed
cw.calibrate()

# Run
if isinstance(trials, tuple):
    for trial in trials:
        setup_trials.trial = trial
        cw.run(setup_trials)
else:
    setup_trials.trial = trials
    cw.run(setup_trials)
