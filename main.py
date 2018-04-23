import os, glob
from func import calibrations, excitations, execution, models
from func.CeinmWriter import CeinmWriter, SetupCalib, SetupTrial

if os.environ['COMPUTERNAME'] =='DESKTOP-4KTED5M':
    base_path = "C:/Users/micka/Dropbox/Projet_EMGdriven/test_1/test_hierarchie/"
    ceinms_path = "C:/Programming/CEINMS_dev/bin"
else:
    ceinms_path = "~/Documents/Laboratoire/Programmation/CEINMS/ceinms/release/bin"
    base_path = "TODO"


# # # DEFINE DoF, MODELS and SUBJECT, vCalibTrials, Trials # # #
DoF = 'G' # 'G' | 'SAG"
ModelName = 'Wu' # "Wu"| 'DAS3'
Subject = 'DapO'
vCalibTrials = 1
Trials = 'AllButCalib' # | 'All' | 'AllButCalib' | 'Calib'
vTendon = 'stiff' #| 'elastic'
# # # END OF THE MAIN VARIABLES # # #



SubjectPath = "../%s/Trials" % (Subject)
LoadModel(ModelName)

if Model["ModelName"].lower() == 'wu' or Model["ModelName"].lower() == 'das3':
    if DoF.lower() == 'g': DoFName = Model["DoFName"][-3:]
elif DoF.lower() =='sag':  DoFName = Model["DoFName"][0:2] + Model["DoFName"][3:] #improve?

print("DoF for CEINMS are: "); print(DoFName)

# # # GENERATE trials.xml # # #
for subdir in  next(os.walk(SubjectPath))[1]: #regarder tous les dossiers et générer les xml
    print("Generate xml for trial: " + subdir)
    Generate_trial_xml(Model, subdir)


# # # CHOOSE CalibTrials and Trials # # #
# xHy_z   with x=6|12|18 y=1-6  z=1-3
if vCalibTrials == 1:
    calib_trials = [] #initialiser avec un mouvement fonctionnel
    x=[6, 12, 18] #kg
    y=1 #changer pour excentric yeux -> hanches qd tout généré par Romain
    z=1 #x= all,
    for i in x: calib_trials = calib_trials + glob.glob("%s/*%d*%d_%d.xml" %(SubjectPath,i,y,z))
else:
    print("%d: HAS TO BE DONE" %(vCalibTrials))


if Trials.lower() == 'all':
    trials = glob.glob("%s/*.xml" %(SubjectPath))
elif Trials.lower() == 'allbutcalib':
    trials = glob.glob("%s/*.xml" %(SubjectPath))
    for i in calib_trials: trials.remove(i)
elif Trials.lower() == 'calib':
    trials = calib_trials

calib_trials = tuple(calib_trials) #calib_trials = ("../../../DapO/Trials/F6H1_1.xml", "../../../DapO/Trials/F6H1_1.xml")
print(calib_trials)
trials = tuple(trials)
print(trials) #trials = ("../../Trials/F6H1_1.xml", "../../Trials/F6H1_1.xml")


# # # CALIB # # #
setup_calib = SetupCalib()
setup_calib.uncalibrated_model = GenerateSubject(dofs)
setup_calib.excitation = excitations.Wu_v3(dofs, vTendon)
setup_calib.calibration = calibrations.Wu_GH_v1(calib_trials, dofs, vTendon, Model)
setup_calib.force_calibration = True
#################

# # # TRIALS # # #
setup_trials = SetupTrial()
setup_trials.execution = execution.EMG_driven # EMG_driven Hybrid
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
