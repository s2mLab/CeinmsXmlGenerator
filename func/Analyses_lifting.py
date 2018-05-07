import opensim as osim

import matplotlib
import matplotlib.pyplot as plt  # conda install matplotlib

import numpy as np

from sklearn.metrics import mean_squared_error
from math import sqrt



import os


def read_STO(dir_raw, dir_result, dir_osim):

    adapter = osim.STOFileAdapter()


    ## Opensim Files ## TODO uncomment when files generated ... and change names according to Romain's code
    filename = dir_osim+os.sep + 'StaticOptimization_activation.sto'
    activationOSIM = [] # adapter.read(filename)

    filename = dir_osim+os.sep + 'StaticOptimization_force.sto'
    muscleforceOSIM = [] # adapter.read(filename)

    filename = dir_osim+os.sep + 'InvDyn.sto'
    torqueOSIM = adapter.read(filename)

    filename = dir_raw+os.sep + 'EMG.sto'
    emg = adapter.read(filename)

    ## CEINMS Files ##
    filename = dir_result+os.sep + 'Activations.sto'
    activationCEINMS = adapter.read(filename)


    filename = dir_result+os.sep + 'AdjustedEmgs.sto'
    if os.path.isfile(filename):  # generated in hydrid mode only
        emgCEINMS = adapter.read(filename)
    else:
        emgCEINMS = []


    filename = dir_result+os.sep + 'MuscleForces.sto'
    muscleforceCEINMS = adapter.read(filename)

    filename = dir_result+os.sep + 'Torques.sto'
    torqueCEINMS = adapter.read(filename)

    return emg, activationCEINMS, emgCEINMS, muscleforceCEINMS, torqueCEINMS, activationOSIM, muscleforceOSIM, torqueOSIM




def result1(trial_path, dir_result, excitations_type):
    dir_trial = trial_path[:-4]+os.sep
    emg, _, emgCEINMS, _, torqueCEINMS, _, _, torqueOSIM = read_STO(dir_trial, dir_result, dir_trial)


    # emg_names = emg.getColumnLabels()
    # emgEINMS_names = emgCEINMS.getColumnLabels()

    mapping = excitations_type.excitation()['mapping']



    nMTU = emgCEINMS.getColumnLabels().__len__()
    nrows = np.floor(sqrt(nMTU))
    ncols = np.ceil(nMTU/nrows)

    _, ax = plt.subplots(int(nrows), int(ncols), sharex=True)

    count = 0
    row = 0
    col = 0

    rmsEMG = np.zeros(nMTU)*np.nan
    time_emgCEINMS = emgCEINMS.getIndependentColumn()
    time_emg =  emg.getIndependentColumn()


    for MTU in emgCEINMS.getColumnLabels():
        print(MTU)
        if mapping.__contains__(MTU):
            muscle_names = mapping[MTU]



            x = emgCEINMS.getDependentColumn(MTU)
            npx = np.zeros(x.nrow())
            for i in range(0, x.nrow()):
                npx[i] = x.getElt(i, 0)


            y = emg.getDependentColumn(muscle_names[1])
            npy = np.zeros(y.nrow())
            for i in range(0, y.nrow()):
                npy[i] = muscle_names[0] * y.getElt(i, 0)
            for i in range(2,muscle_names.__len__(),2):
                print(i)
                y = emg.getDependentColumn(muscle_names[i+1])
                for i in range(0, y.nrow()):
                    npy[i] = muscle_names[i] * y.getElt(i, 0)



#           rmsTorques[count] = sqrt(mean_squared_error(npx, npy))


            ax[row, col].plot(time_emgCEINMS, npx, label='ceinms')
            ax[row, col].plot(time_emg, npy, label='mesured')
            ax[row, col].set_title(MTU)
            #       ax[row, col].set_title(MTU+ '_rms(%f)' % (rmsMTU[count]) )

            if col == 0:
                plt.ylabel('Excitation [%]')
            if row == nrows:
                plt.xlabel('time [samples]')

            count = count+1
            col = col + 1
            if col == ncols:
                col = 0
                row = row + 1

        else:
            print('no EMG')




    ndof = torqueCEINMS.getColumnLabels().__len__()
    ncols = np.ceil(sqrt(ndof))
    nrows = np.ceil(ndof/ncols)

    # if ndof < 5:
    #     nrows = 2
    #     ncols = 2
    # elif ndof < 10:
    #     nrows = 3
    #     ncols = 3
    # else:
    #     nrows = 4
    #     ncols = np.ceil(ndof / 4)

    matplotlib.is_interactive()
    _, ax = plt.subplots(int(nrows), int(ncols), sharex=True)

    count = 0
    row = 0
    col = 0

    rmsTorques = np.zeros(ndof)*np.nan
    for dof in torqueCEINMS.getColumnLabels():
        x = torqueCEINMS.getDependentColumn(dof)
        y = torqueOSIM.getDependentColumn(dof + '_moment')

        # totaly ineffcient TODO improve translation vectorSIMTK to np
        npx = np.zeros(x.nrow())
        for i in range(0, x.nrow()):
            npx[i] = x.getElt(i, 0)

        npy = np.zeros(y.nrow())
        for i in range(0, y.nrow()):
            npy[i] = y.getElt(i, 0)

        rmsTorques[count] = sqrt(mean_squared_error(npx, npy))

        print('RMS error in %s: %f Nm' % (dof, rmsTorques[count]))

        ax[row, col].plot(npx, label='ceinms')
        ax[row, col].plot(npy, label='osim')
        ax[row, col].set_title(dof+ '_rms(%f)' % (rmsTorques[count]) )

        if col==0:
            plt.ylabel('Torques [Nm]')
        if row==nrows:
            plt.xlabel('time [samples]')

        count=count+1
        col = col + 1
        if col == ncols:
            col = 0
            row = row + 1

    ax[0,0].legend()
    plt.tight_layout()

    return rmsTorques  #  rmsEMG,







