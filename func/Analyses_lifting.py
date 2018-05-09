import opensim as osim

#import matplotlib
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

import numpy as np

from sklearn.metrics import mean_squared_error
from math import sqrt

from scipy.interpolate import interp1d

import os




def compare_emg(dir_trial, dir_result, excitations_type, name, units):

    emgCEINMS = read_STO(dir_result, 'AdjustedEmgs')
    emg = read_STO(dir_trial, 'EMG')
    mapping = excitations_type.excitation()['mapping']

    nMTU = emgCEINMS.getColumnLabels().__len__()
    nrows = np.floor(sqrt(nMTU))
    ncols = np.ceil(nMTU/nrows)

    fig, ax = plt.subplots(int(nrows), int(ncols), sharex=True)
    manager = plt.get_current_fig_manager()
    manager.window.showMaximized()

    count = 0
    row = 0
    col = 0

    rmsEMG = np.zeros(nMTU)*np.nan
    time_emgCEINMS = emgCEINMS.getIndependentColumn()
    time_emg = np.asarray(emg.getIndependentColumn())+0.015 # emgDelay TODO could be read in calibrated model


    for MTU in emgCEINMS.getColumnLabels():
        print(MTU)
        if mapping.__contains__(MTU):
            muscle_names = mapping[MTU]

            x = emgCEINMS.getDependentColumn(MTU)
            npx = osim2np(x)

            y = emg.getDependentColumn(muscle_names[1])
            npy = osim2np(y)
            for i in range(2,muscle_names.__len__(),2):
                npy = npy + osim2np(emg.getDependentColumn(muscle_names[i+1]))

            f = interp1d(time_emg, npy, 'nearest') # nearest in this case since emg high frequency
            npy_tnorm = f(time_emgCEINMS)

            rmsEMG[count] = sqrt(mean_squared_error(npx, npy_tnorm))
            print('RMS error in %s: %f %%max Excitation' % (MTU, rmsEMG[count]))

            ax[row, col].plot(time_emg, npy, 'k', label='mesured')
            ax[row, col].plot(time_emgCEINMS, npy_tnorm, 'k.', label='interp')
            ax[row, col].plot(time_emgCEINMS, npx, 'b', label='ceinms')
            ax[row, col].set_title(MTU + '_rms(%f)' % (rmsEMG[count]))

            if col == 0:
                ax[row, col].set_ylabel('%s [%s]' % (name, units))
            if row == nrows - 1:
                ax[row, col].set_xlabel('time [s]')

            count = count+1
            col = col + 1
            if col == ncols:
                col = 0
                row = row + 1

        else:
            print('no EMG')

    return rmsEMG, fig


def compare_msk(trial_path, dir_result, excitations_type):
    dir_trial = trial_path[:-4]+os.sep
    # TODO change names according to Romain's code

    pp = PdfPages(dir_result + os.sep + 'results.pdf')

    rmsTorque,figTorque = compare_xy(dir_result, 'Torques', dir_trial, 'InvDyn', 'Torques','Nm','_moment')
    rmsActivation, figActivation = compare_xy(dir_result, 'Activations', dir_trial, 'StaticOptimization_activation', 'Activation','0-1')
    rmsForce, figForce = compare_xy(dir_result, 'MuscleForces', dir_trial, 'StaticOptimization_force', 'Muscle Forces','N')
    #rmsJRF, figJRF = compare_xy(dir_result, '', dir_trial, '_JointReaction_ReactionLoads', 'GH force','N') # warning : only the first 3 columns
    rmsEMG, figEMG = compare_emg(dir_trial, dir_result, excitations_type, 'excitation', '0-1')

    figGH = compare_gh_forces(trial_path, dir_result)

    pp.savefig(figEMG)
    pp.savefig(figTorque)
    pp.savefig(figActivation)
    pp.savefig(figForce)
    pp.savefig(figGH)

    pp.close()

    return rmsTorque, rmsActivation, rmsForce, #rmsJRF



def compare_gh_forces(trial_path, dir_result):
    dir_trial = trial_path[:-4] + os.sep

    GHosim = read_STO(dir_trial, '_JointReaction_ReactionLoads')
    Fx = osim2np(GHosim.getDependentColumnAtIndex(0))
    Fy = osim2np(GHosim.getDependentColumnAtIndex(1))
    Fz = osim2np(GHosim.getDependentColumnAtIndex(2))
    F = np.vstack( (Fx, Fy, Fz) )
    # var = GHosim.getColumnLabels()
    # mx, my, mz, x, y, z for index 3 to 8

    # calculate norm of GH force
    normF = np.linalg.norm(F, axis=0)
    unitF = F / normF # TODO: check may be wrong

    # TODO: validate in opensim the directions of the forces ... 0 deg being forward

    # Lippitt, S., & Matsen, F. (1993). Mechanisms of glenohumeral joint stability. Clinical orthopaedics and related research, (291), 20-28.
    angles = np.arange(0, 2.1*np.pi, np.pi / 4)
    coefMEAN = np.array([17, 19, 29, 20, 17, 25, 32, 23, 17]) / 50
    coefSD = np.array([6, 6, 7, 8, 6, 9, 4, 4, 6]) / 50
    xp = np.cos(angles) * (coefMEAN + coefSD)
    yp = np.sin(angles) * (coefMEAN + coefSD)
    xm = np.cos(angles) * (coefMEAN - coefSD)
    ym = np.sin(angles) * (coefMEAN - coefSD)

    fig, ax = plt.subplots(1,2, sharex=True)
    manager = plt.get_current_fig_manager()
    manager.window.showMaximized()

    for i in [0, 1]:
        ax[i].plot(xp,yp,'k-', xm, ym,'k--')
        ax[i].axis('equal')

    ax[0].plot(unitF[0, :], unitF[1, :], '.')

    return fig


def compare_xy(dir1name, param1name, dir2name, param2name, name, units, suffix=''):

    param1 = read_STO(dir1name, param1name)
    param2 = read_STO(dir2name, param2name)

    nb = param1.getColumnLabels().__len__()
    ncols = np.ceil(sqrt(nb))
    nrows = np.ceil(nb / ncols)

    #matplotlib.is_interactive()  # est-ce utile?
    fig, ax = plt.subplots(int(nrows), int(ncols), sharex=True)
    manager = plt.get_current_fig_manager()
    manager.window.showMaximized()


    count = 0
    row = 0
    col = 0

    time_x = np.asarray(param1.getIndependentColumn())
    time_y = np.asarray(param2.getIndependentColumn())
    #rmsValue = np.zeros(nb) * np.nan
    rmsValue = []

    for i in param1.getColumnLabels():
        x = osim2np(param1.getDependentColumn(i))
        y = osim2np(param2.getDependentColumn(i + suffix)) # TODO modify to work in many cases

        # TODO check that time are simular
        if not all(time_x[1:] == time_y[1:]):  # time[0] not always 0
            print('TODO')


        #rmsValue[count] = sqrt(mean_squared_error(x, y))
        err = sqrt(mean_squared_error(x, y))
        rmsValue.append([i, err])

        print('RMS error in %s: %f Nm' % (i, err))

        ax[row, col].plot(time_y, y, 'k', label='osim')
        ax[row, col].plot(time_x, x, 'b', label='ceinms')
        ax[row, col].set_title(i + '_rms(%f)' % (err))

        if col == 0:
            ax[row, col].set_ylabel( '%s [%s]' % (name, units))
        if row == nrows-1:
            ax[row, col].set_xlabel('time [s]')

        count = count + 1
        col = col + 1
        if col == ncols:
            col = 0
            row = row + 1


    ax[0, 0].legend()
    plt.tight_layout()
    #plt.show()

    return rmsValue, fig


def osim2np(x):
    # totaly ineffcient TODO improve translation vectorSIMTK to np
    npx = np.zeros(x.nrow())
    for i in range(0, x.nrow()):
        npx[i] = x.getElt(i, 0)

    return npx


def time_normalization(x, time_vector=np.linspace(0, 100, 101), axis=-1):
    """
    Time normalization used for temporal alignment of data

    Parameters
    ----------
    x : np.ndarray
        matrix or vector to interpolate over
    time_vector : np.ndarray
        desired time vector (0 to 100 by step of 1 by default)
    axis : int
        specifies the axis along which to interpolate. Interpolation defaults to the last axis (over frames)

    Returns
    -------
    np.ndarray
    """
    original_time_vector = np.linspace(time_vector[0], time_vector[-1], x.shape[axis])
    f = interp1d(original_time_vector, x, axis=axis)
    return f(time_vector)


def read_STO(dirname, filename):
    adapter = osim.STOFileAdapter()
    return adapter.read(dirname + os.sep + filename + '.sto')
















### OLD STUFF ###

# def read_all_STO(dir_raw, dir_result, dir_osim):
#
#     adapter = osim.STOFileAdapter()
#
#     ## Opensim Files #
#     filename = dir_osim+os.sep + 'StaticOptimization_activation.sto'
#     activationOSIM = adapter.read(filename)
#
#     filename = dir_osim+os.sep + 'StaticOptimization_force.sto'
#     muscleforceOSIM = adapter.read(filename)
#
#     filename = dir_osim+os.sep + 'InvDyn.sto'
#     torqueOSIM = adapter.read(filename)
#
#     filename = dir_raw+os.sep + 'EMG.sto'
#     emg = adapter.read(filename)
#
#     filename = dir_raw + os.sep + '_JointReaction_ReactionLoads.sto'
#     jrfOSIM = adapter.read(filename)
#
#     ## CEINMS Files ##
#     filename = dir_result+os.sep + 'Activations.sto'
#     activationCEINMS = adapter.read(filename)
#
#     filename = dir_result+os.sep + 'AdjustedEmgs.sto'
#     if os.path.isfile(filename):  # generated in hydrid mode only
#         emgCEINMS = adapter.read(filename)
#     else:
#         emgCEINMS = []
#
#     filename = dir_result+os.sep + 'MuscleForces.sto'
#     muscleforceCEINMS = adapter.read(filename)
#
#     filename = dir_result+os.sep + 'Torques.sto'
#     torqueCEINMS = adapter.read(filename)
#
#     return emg, activationCEINMS, emgCEINMS, muscleforceCEINMS, torqueCEINMS, activationOSIM, muscleforceOSIM, torqueOSIM, jrfOSIM


# def compare_torque(trial_path, dir_result):
#
#     torqueCEINMS = read_STO(dir_result, 'Torques')
#     torqueOSIM = read_STO(trial_path, 'InvDyn')
#
#     ndof = torqueCEINMS.getColumnLabels().__len__()
#     ncols = np.ceil(sqrt(ndof))
#     nrows = np.ceil(ndof/ncols)
#
#     matplotlib.is_interactive() # est-ce utile?
#     _, ax = plt.subplots(int(nrows), int(ncols), sharex=True)
#
#     count = 0
#     row = 0
#     col = 0
#
#
#     time_x = torqueCEINMS.getIndependentColumn()
#     time_y = torqueOSIM.getIndependentColumn()
#     rmsTorques = np.zeros(ndof)*np.nan
#     for dof in torqueCEINMS.getColumnLabels():
#         x = torqueCEINMS.getDependentColumn(dof)
#         y = torqueOSIM.getDependentColumn(dof + '_moment')
#         npx = osim2np(x)
#         npy = osim2np(y)
#
#         rmsTorques[count] = sqrt(mean_squared_error(npx, npy))
#         print('RMS error in %s: %f Nm' % (dof, rmsTorques[count]))
#
#         ax[row, col].plot(time_y, npy,'k', label='osim')
#         ax[row, col].plot(time_x, npx,'b', label='ceinms')
#         ax[row, col].set_title(dof + '_rms(%f)' % (rmsTorques[count]))
#
#         if col==0:
#             plt.ylabel('Torques [Nm]')
#         if row==nrows:
#             plt.xlabel('time [samples]')
#
#         count=count+1
#         col = col + 1
#         if col == ncols:
#             col = 0
#             row = row + 1
#
#     ax[0,0].legend()
#     plt.tight_layout()
#
#     return rmsTorques
#
#
#
# def result1(trial_path, dir_result, excitations_type):
#     dir_trial = trial_path[:-4]+os.sep
#     emg, activationCEINMS, emgCEINMS, muscleforceCEINMS, torqueCEINMS, activationOSIM, muscleforceOSIM, torqueOSIM, jrfOSIM = read_all_STO(dir_trial, dir_result, dir_trial)
#
#
#     # emg_names = emg.getColumnLabels()
#     # emgEINMS_names = emgCEINMS.getColumnLabels()
#
#     mapping = excitations_type.excitation()['mapping']
#
#     nMTU = emgCEINMS.getColumnLabels().__len__()
#     nrows = np.floor(sqrt(nMTU))
#     ncols = np.ceil(nMTU/nrows)
#
#     _, ax = plt.subplots(int(nrows), int(ncols), sharex=True)
#
#     count = 0
#     row = 0
#     col = 0
#
#     rmsEMG = np.zeros(nMTU)*np.nan
#     time_emgCEINMS = emgCEINMS.getIndependentColumn()
#     time_emg = np.asarray(emg.getIndependentColumn())+0.015 # emgDelay
#
#
#     for MTU in emgCEINMS.getColumnLabels():
#         print(MTU)
#         if mapping.__contains__(MTU):
#             muscle_names = mapping[MTU]
#
#
#             x = emgCEINMS.getDependentColumn(MTU)
#             npx = osim2np(x)
#
#
#             y = emg.getDependentColumn(muscle_names[1])
#             npy = np.zeros(y.nrow())
#             for i in range(0, y.nrow()):
#                 npy[i] = muscle_names[0] * y.getElt(i, 0)
#             for i in range(2,muscle_names.__len__(),2):
#                 print(i)
#                 y = emg.getDependentColumn(muscle_names[i+1])
#                 for i in range(0, y.nrow()):
#                     npy[i] = muscle_names[i] * y.getElt(i, 0)
#
#
#             f = interp1d(time_emg, npy, 'nearest') # nearest in this case since emg high frequency
#             npy_tnorm = f(time_emgCEINMS)
#             rmsEMG[count] = sqrt(mean_squared_error(npx, npy_tnorm))
#             print('RMS error in %s: %f %%max Excitation' % (MTU, rmsEMG[count]))
#
#             ax[row, col].plot(time_emg, npy, 'k', label='mesured')
#             ax[row, col].plot(time_emgCEINMS, npy_tnorm, 'k.', label='interp')
#             ax[row, col].plot(time_emgCEINMS, npx, 'b', label='ceinms')
#             ax[row, col].set_title(MTU + '_rms(%f)' % (rmsEMG[count]))
#
#             if col == 0:
#                 plt.ylabel('Excitation [%]')
#             if row == nrows:
#                 plt.xlabel('time [samples]')
#
#             count = count+1
#             col = col + 1
#             if col == ncols:
#                 col = 0
#                 row = row + 1
#
#         else:
#             print('no EMG')
#
#
#
#
#     ndof = torqueCEINMS.getColumnLabels().__len__()
#     ncols = np.ceil(sqrt(ndof))
#     nrows = np.ceil(ndof/ncols)
#
#     matplotlib.is_interactive()
#     _, ax = plt.subplots(int(nrows), int(ncols), sharex=True)
#
#     count = 0
#     row = 0
#     col = 0
#
#
#     time_x = torqueCEINMS.getIndependentColumn()
#     time_y = torqueOSIM.getIndependentColumn()
#     rmsTorques = np.zeros(ndof)*np.nan
#     for dof in torqueCEINMS.getColumnLabels():
#         x = torqueCEINMS.getDependentColumn(dof)
#         y = torqueOSIM.getDependentColumn(dof + '_moment')
#         npx = osim2np(x)
#         npy = osim2np(y)
#
#         rmsTorques[count] = sqrt(mean_squared_error(npx, npy))
#         print('RMS error in %s: %f Nm' % (dof, rmsTorques[count]))
#
#         ax[row, col].plot(time_y, npy,'k', label='osim')
#         ax[row, col].plot(time_x, npx,'b', label='ceinms')
#         ax[row, col].set_title(dof + '_rms(%f)' % (rmsTorques[count]))
#
#         if col==0:
#             plt.ylabel('Torques [Nm]')
#         if row==nrows:
#             plt.xlabel('time [samples]')
#
#         count=count+1
#         col = col + 1
#         if col == ncols:
#             col = 0
#             row = row + 1
#
#     ax[0,0].legend()
#     plt.tight_layout()
#
#     return rmsTorques, rmsEMG,

