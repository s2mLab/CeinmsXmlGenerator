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
DoF = 'G' # |'SAG"
Model = 'Wu' # | 'DAS3' #... WuModel | DAS3Model
Subject = 'DapO'; SubjectPath = "../%s/Trials" % (Subject)
vCalibTrials = 1
Trials = 'AllButCalib' # | 'AllButCalib' | 'Calib'
vTendon = 'stiff' #| 'elastic'


# # # END OF THE MAIN VARIABLES # # #

# READ THAT AT THE BEGINNING
WuModel = {"Model" : "Wu",
    "DoFName" : ("sternoclavicular_r1", "sternoclavicular_r2",  "sternoclavicular_r3",
                 "Acromioclavicular_r1","Acromioclavicular_r2", "Acromioclavicular_r3",
                 "shoulder_plane", "shoulder_ele", "shoulder_rotation"),
    "MTUNames" : ("LVS", "SBCL",
                  "TRP1", "TRP2", "TRP3", "TRP4",
                  "RMN", "RMJ1", "RMJ2",
                  "SRA1", "SRA2", "SRA3", "PMN",
                  "DELT1", "DELT2", "DELT3",
                  "SUPSP", "INFSP", "SUBSC", "TMIN",
                  "TMAJ", "PECM1", "PECM2", "PECM3", "LAT", "CORB")}

DAS3Model = {"Model" : "DAS3",
    "DoFName" : ("SC_y", "SC_z","AC_x", "AC_y", "AC_z","GH_x", "GH_y", "GH_z"),
    "MTUNames" : (  "trap_scap_1","trap_scap_2","trap_scap_3","trap_scap_4","trap_scap_5","trap_scap_6","trap_scap_7","trap_scap_8","trap_scap_9","trap_scap_10","trap_scap_11","trap_clav_1","trap_clav_2",
                    "lev_scap_1","lev_sca_2","rhomboid_1","rhomboid_2","rhomboid_3","rhomboid_4","rhomboid_5",
                    "serr_ant_1","serr_ant2","serr_ant3","serr_ant4","serr_ant5","serr_ant6","serr_ant_7","serr_ant8","serr_ant9","serr_ant10","serr_ant11","serr_ant12",
                    "delt_scap_1","delt_scap_2","delt_scap_3","delt_scap_4","delt_scap_5","delt_scap_6","delt_scap_7","delt_scap_8","delt_scap_9","delt_scap_10","delt_scap_11","delt_clav_1","delt_clav_2","delt_clav_3","delt_clav_4",
                    "infra_1","infra_2","infra_3","infra_4","infra_5","infra_6",
                    "ter_min_1","ter_min_2","ter_min_3",
                    "supra_1","supra_2","supra_3","supra_4",
                    "subscap_1","subscap_2","subscap_3","subscap_4","subscap_5","subscap_6","subscap_7","subscap_8","subscap_9","subscap_10","subscap_11",
                    "ter_maj_1","ter_maj_2","ter_maj_3","ter_maj_4",
                    "bic_l","bic_b_1","bic_b_2",
                    "tric_long_1","tric_long_2","tric_long_3","tric_long_4","tric_med_1","tric_med_2","tric_med_3","tric_med_4","tric_med_5","tric_lat_1","tric_lat_2","tric_lat_3","tric_lat_4","tric_lat_5",
                    "lat_dorsi_1","lat_dorsi_2","lat_dorsi_3","lat_dorsi_4","lat_dorsi_5","lat_dorsi_6",
                    "pect_maj_t_1","pect_maj_t_2","pect_maj_t_3","pect_maj_t_4","pect_maj_t_5","pect_maj_t_6","pect_maj_c_1","pect_maj_c_2",
                    "pect_min_1","pect_min_2","pect_min_3","pect_min_4",
                    "brachialis_1","brachialis_2","brachialis_3","brachialis_4","brachialis_5","brachialis_6","brachialis_7","brachiorad_1","brachiorad_2",
                    "coracobr_1","coracobr_2","coracobr_3")} ## pourrait être plus efficace de lire un fichier osim


if Model.lower() == 'wu':
    if DoF.lower() == 'g': DoFName = WuModel["DoFName"][-3:]
elif DoF.lower() =='sag':  DoFName = WuModel["DoFName"][0:2] + WuModel["DoFName"][3:] #improve?
elif Model.lower() == 'das3':
    if DoF.lower() == 'g':     DoFName = DAS3Model["DoFName"][-3:]
    elif DoF.lower() =='sag':  DoFName = DAS3Model["DoFName"][0:2] + DAS3Model["DoFName"][3:] #improve?

# # # GENERATE trials.xml # # #
for subdir in  next(os.walk(SubjectPath))[1]: #regarder tous les dossiers et générer les xml
    print(subdir)
    Generate_trial_xml(Model,subdir)





# # # CHOOSE CalibTrials and Trials # # #
# xHy_z   with x=6|12|18 y=1-6  z=1-3
if vCalibTrials == 1:
    calib_trials = [] #initialiser avec un mouvement fonctionnel
    x=[6, 12, 18] #kg
    y=1 #changer pour excentric yeux -> hanches
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
