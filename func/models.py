
class Wu:
    @staticmethod
    def name():
        return "Wu"

    @staticmethod
    def uncalibrated_model():
        return {
            "mtuDefault": {
                "emDelay": 0.015,
                "percentageChange": 0.15,
                "damping": 0.1,
                "curve__RM_BEGIN__0__RM_END__": {
                    "name": "activeForceLength",
                    "xPoints": [0.4035, 0.52725, 0.62875, 0.71875, 0.86125, 1.045, 1.2175, 1.43875, 1.61875],
                    "yPoints": [0, 0.226667, 0.636667, 0.856667, 0.95, 0.993333, 0.77, 0.246667, 0]
                },
                "curve__RM_BEGIN__1__RM_END__": {
                    "name": "passiveForceLength",
                    "xPoints": [1, 1.1, 1.2, 1.3, 1.4, 1.5, 1.6],
                    "yPoints": [0, 0.035, 0.12, 0.26, 0.55, 1.17, 2]
                },
                "curve__RM_BEGIN__2__RM_END__": {
                    "name": "forceVelocity",
                    "xPoints": [-1, -0.6, -0.3, -0.1, 0, 0.1, 0.3, 0.6, 0.8],
                    "yPoints": [0, 0.08, 0.2, 0.55, 1, 1.4, 1.6, 1.7, 1.75]
                },
                "curve__RM_BEGIN__3__RM_END__": {
                    "name": "tendonForceStrain",
                    "xPoints": [0, 0.00131, 0.00281, 0.00431, 0.00581, 0.00731, 0.00881, 0.0103, 0.0118, 0.0123, 9.2],
                    "yPoints": [0, 0.0108, 0.0257, 0.0435, 0.0652, 0.0915, 0.123, 0.161, 0.208, 0.227, 345]
                },
            },
            "mtuSet": {
                "mtu__RM_BEGIN__CORB__RM_END__": {
                    "name": "CORB",
                    "c1": -0.5,
                    "c2": -0.5,
                    "shapeFactor": 0.1,
                    "optimalFibreLength": 0.0880530152660019,
                    "pennationAngle": 0,
                    "tendonSlackLength": 0.0650872648901336,
                    "maxIsometricForce": 306.9,
                    "strengthCoefficient": 1.5
                },
                "mtu__RM_BEGIN__DELT1__RM_END__": {
                    "name": "DELT1",
                    "c1": -0.5,
                    "c2": -0.5,
                    "shapeFactor": 0.1,
                    "optimalFibreLength": 0.181156791151782,
                    "pennationAngle": 0.383972435439,
                    "tendonSlackLength": 0.0323641984192398,
                    "maxIsometricForce": 556.8,
                    "strengthCoefficient": 1.5
                },
                "mtu__RM_BEGIN__DELT2__RM_END__": {
                    "name": "DELT2",
                    "c1": -0.5,
                    "c2": -0.5,
                    "shapeFactor": 0.1,
                    "optimalFibreLength": 0.141050311287921,
                    "pennationAngle": 0.261799387799,
                    "tendonSlackLength": 0.0499776140906367,
                    "maxIsometricForce": 1098.4,
                    "strengthCoefficient": 1.5
                },
                "mtu__RM_BEGIN__DELT3__RM_END__": {
                    "name": "DELT3",
                    "c1": -0.5,
                    "c2": -0.5,
                    "shapeFactor": 0.1,
                    "optimalFibreLength": 0.133817175908073,
                    "pennationAngle": 0.314159265359,
                    "tendonSlackLength": 0.106247350578478,
                    "maxIsometricForce": 944.7,
                    "strengthCoefficient": 1.5
                },
                "mtu__RM_BEGIN__INFSP__RM_END__": {
                    "name": "INFSP",
                    "c1": -0.5,
                    "c2": -0.5,
                    "shapeFactor": 0.1,
                    "optimalFibreLength": 0.148326196518162,
                    "pennationAngle": 0.322885911619,
                    "tendonSlackLength": 0.0377822586746943,
                    "maxIsometricForce": 864.6,
                    "strengthCoefficient": 1.5
                },
                "mtu__RM_BEGIN__LAT__RM_END__": {
                    "name": "LAT",
                    "c1": -0.5,
                    "c2": -0.5,
                    "shapeFactor": 0.1,
                    "optimalFibreLength": 0.2479168519676,
                    "pennationAngle": 0.331612557879,
                    "tendonSlackLength": 0.0823892861523746,
                    "maxIsometricForce": 1129.7,
                    "strengthCoefficient": 1.5
                },
                "mtu__RM_BEGIN__PECM1__RM_END__": {
                    "name": "PECM1",
                    "c1": -0.5,
                    "c2": -0.5,
                    "shapeFactor": 0.1,
                    "optimalFibreLength": 0.104235736488706,
                    "pennationAngle": 0.296705972839,
                    "tendonSlackLength": 0.04881283269715,
                    "maxIsometricForce": 983.4,
                    "strengthCoefficient": 1.5
                },
                "mtu__RM_BEGIN__PECM2__RM_END__": {
                    "name": "PECM2",
                    "c1": -0.5,
                    "c2": -0.5,
                    "shapeFactor": 0.1,
                    "optimalFibreLength": 0.139769338714534,
                    "pennationAngle": 0.436332312999,
                    "tendonSlackLength": 0.0953426560517004,
                    "maxIsometricForce": 699.7,
                    "strengthCoefficient": 1.5
                },
                "mtu__RM_BEGIN__PECM3__RM_END__": {
                    "name": "PECM3",
                    "c1": -0.5,
                    "c2": -0.5,
                    "shapeFactor": 0.1,
                    "optimalFibreLength": 0.187065821832059,
                    "pennationAngle": 0.436332312999,
                    "tendonSlackLength": 0.101942102575882,
                    "maxIsometricForce": 446.7,
                    "strengthCoefficient": 1.5
                },
                "mtu__RM_BEGIN__SUBSC__RM_END__": {
                    "name": "SUBSC",
                    "c1": -0.5,
                    "c2": -0.5,
                    "shapeFactor": 0.1,
                    "optimalFibreLength": 0.181497898584421,
                    "pennationAngle": 0.349065850399,
                    "tendonSlackLength": 0.00834089607465166,
                    "maxIsometricForce": 944.3,
                    "strengthCoefficient": 1.5
                },
                "mtu__RM_BEGIN__SUPSP__RM_END__": {
                    "name": "SUPSP",
                    "c1": -0.5,
                    "c2": -0.5,
                    "shapeFactor": 0.1,
                    "optimalFibreLength": 0.130385807546346,
                    "pennationAngle": 0.12217304764,
                    "tendonSlackLength": 0.027755948730896,
                    "maxIsometricForce": 410.7,
                    "strengthCoefficient": 1.5
                },
                "mtu__RM_BEGIN__TMAJ__RM_END__": {
                    "name": "TMAJ",
                    "c1": -0.5,
                    "c2": -0.5,
                    "shapeFactor": 0.1,
                    "optimalFibreLength": 0.156714909037499,
                    "pennationAngle": 0.279252680319,
                    "tendonSlackLength": 0.0606310563062945,
                    "maxIsometricForce": 234.9,
                    "strengthCoefficient": 1.5
                },
                "mtu__RM_BEGIN__TMIN__RM_END__": {
                    "name": "TMIN",
                    "c1": -0.5,
                    "c2": -0.5,
                    "shapeFactor": 0.1,
                    "optimalFibreLength": 0.0502009742043238,
                    "pennationAngle": 0.418879020479,
                    "tendonSlackLength": 0.115030046852291,
                    "maxIsometricForce": 605.4,
                    "strengthCoefficient": 1.5
                },
            },
            "dofSet": {
                "dof__RM_BEGIN__SHOULDER_ELEV__RM_END__": {
                    "name": "shoulder_ele",
                    "mtuNameSet": ["DELT1", "DELT2", "DELT3", "SUPSP", "INFSP", "SUBSC", "TMIN", "TMAJ", "PECM1", "PECM2",
                                   "PECM3", "LAT", "CORB"]
                },
                "dof__RM_BEGIN__SHOULDER_PLANE__RM_END__": {
                    "name": "shoulder_plane",
                    "mtuNameSet": ["DELT1", "DELT2", "DELT3", "SUPSP", "INFSP", "SUBSC", "TMIN", "TMAJ", "PECM1", "PECM2",
                                   "PECM3", "LAT", "CORB"]
                },
                "dof__RM_BEGIN__SHOULDER_ROTATION__RM_END__": {
                    "name": "shoulder_rotation",
                    "mtuNameSet": ["DELT1", "DELT2", "DELT3", "SUPSP", "INFSP", "SUBSC", "TMIN", "TMAJ", "PECM1", "PECM2",
                                   "PECM3", "LAT", "CORB"]
                },
            },
            "calibrationInfo": {
                "uncalibrated": {
                    "subjectID": "model_scaled",
                    "additionalInfo": "TendonSlackLength and OptimalFibreLength scaled with Winby-Modenese"
                }
            }
        }
