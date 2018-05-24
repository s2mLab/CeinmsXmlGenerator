import opensim
import math

from func.xml_writer import remove_begin, remove_end


def choose(model_name):
    if model_name.lower() == 'wu':
        return Wu
    else:
        raise NotImplementedError("Model cannot be chosen")


class OsimModel:
    def __init__(self, model_path, dof_list):
        self.osim_path = model_path
        self.dof_list = dof_list
        self.uncalibrated_model = self.setup_model(self.osim_path, self.dof_list)

    def name(self):
        return self.uncalibrated_model["calibrationInfo"]["uncalibrated"]["subjectID"]

    @staticmethod
    def setup_model(path, dof_list):
        raise TypeError("Model should be derived and never called directly")

    @staticmethod
    def extract_dof_set_from_osim(dof_list, dof_to_muscles):
        dof_set = {}
        for dof in dof_list:
            full_dof_name = "dof" + remove_begin + dof + remove_end
            muscles = ''
            for m in dof_to_muscles[dof]:
                muscles += " " + m
            muscles = muscles[1:]

            dof_set[full_dof_name] = {
                "name": dof,
                "mtuNameSet": muscles
            }
        return dof_set

    @staticmethod
    def get_joints_spanned_by_muscle(osim_model, muscle):
        # useful initializations
        body_set = osim_model.getBodySet()
        joint_set = osim_model.getJointSet()

        # Extracting the PathPointSet via GeometryPath
        muscle_path = muscle.getGeometryPath()
        muscle_path_point_set = muscle_path.getPathPointSet()

        # for loops to get the attachment bodies
        muscle_attach_bodies = []
        muscle_attach_index = []
        previous_attach_body = ''
        for point_set in muscle_path_point_set:
            # get the current muscle point
            current_attach_body = point_set.getBodyName()

            # building a vectors of the bodies attached to the muscles
            if not previous_attach_body or current_attach_body != previous_attach_body[0:len(current_attach_body)]:
                muscle_attach_bodies.append(current_attach_body)
                muscle_attach_index.append(body_set.getIndex(current_attach_body))
                previous_attach_body = current_attach_body
        # From distal body checking the joint names going up until the desired
        # OSJointName is found or the proximal body is reached as parent body.
        proximal_body_name = muscle_attach_bodies[0]
        distal_body_name = muscle_attach_bodies[-1]

        body_name = distal_body_name
        spanned_joint_name_old = ''
        joint_name_set = []
        while body_name != proximal_body_name:
            for joint in joint_set:
                # We must test for both, because for some reason, opensim sometimes add "_offset" to child name
                if joint.getChildFrame().getName() == body_name or joint.getChildFrame().getName()[0:-7] == body_name:
                    spanned_joint_name = joint.getName()
                    if joint.numCoordinates() != 0 and spanned_joint_name_old != spanned_joint_name:
                        joint_name_set.append(spanned_joint_name)
                        spanned_joint_name_old = spanned_joint_name
                    body_name = joint.getParentFrame().getName()
                    if body_name[-7:] == "_offset":
                        body_name = body_name[0:-7]
                    break

        if not joint_name_set:
            raise IndexError('No joint detected for muscle ' + muscle.getName())

        return joint_name_set

    @staticmethod
    def get_all_implied_muscles(osim_model, dof_name):

        current_state = osim_model.initSystem()
        muscles = osim_model.getMuscles()
        muscle_list = []
        print(f"******** FOR DOF: {dof_name} *********")
        for muscle in muscles:
            # if muscle.isDisabled() == True:  # NOTE For some reason, isDisabled doesn't work
            print("Test muscle: " + muscle.getName())
            muscle_crossed_joint_set = Wu.get_joints_spanned_by_muscle(osim_model, muscle)

            for curr_joint in muscle_crossed_joint_set:
                # Initial estimation of the nr of Dof of the CoordinateSet for that
                # joint before checking for locked and constraint dofs.
                # skip welded joint and remove welded joint from muscleCrossedJointSet
                if osim_model.getJointSet().get(curr_joint).numCoordinates() == 0:
                    continue

                # calculating effective dof for that joint
                for curr_coord_idx in range(osim_model.getJointSet().get(curr_joint).numCoordinates()):
                    curr_coord = osim_model.getJointSet().get(curr_joint).get_coordinates(curr_coord_idx)
                    curr_coord_name = curr_coord.getName()

                    # skip dof if locked
                    if curr_coord.getLocked(current_state):
                        continue

                    # if coordinate is constrained then the independent coordinate and
                    # associated joint will be listed in the sampling "map"
                    if curr_coord.isConstrained(current_state):
                        # finding the independent coordinate
                        raise NotImplementedError("get_independent_coord_and_joint was not implemented yet")
                        # # curr_coord_name, ~ = getIndipCoordAndJoint(osimModel, curr_coord_name);

                        # # skip dof if independent coordinate locked(the coord
                        # # correspondent to the name needs to be extracted)
                        # if osim_model.getCoordinateSet.get(curr_coord_name).getLocked(current_state):
                        #     continue

                    if dof_name == curr_coord_name:
                        muscle_list.append(muscle.getName())
                        print("** muscle included: " + muscle.getName())
        return muscle_list

    @staticmethod
    def read_osim_file(osim_path, dof_list):
        osim_model = opensim.Model(osim_path)
        osim_model.initSystem()
        model_name = osim_model.getModel().getName()

        dof_to_muscles = {}
        all_muscles = []
        muscles = []
        for dof in dof_list:
            muscles = Wu.get_all_implied_muscles(osim_model, dof)
            dof_to_muscles[dof] = muscles
            all_muscles += muscles

        if not muscles:
            raise ValueError("No muscles found")

        # Remove duplicates and sorts
        all_muscles = sorted(list(set(all_muscles)))

        mtu_set = Wu.extract_mtu_from_osim(osim_model, all_muscles)
        dof_set = Wu.extract_dof_set_from_osim(dof_list, dof_to_muscles)

        return model_name, mtu_set, dof_set

    @staticmethod
    def write_model(osim_old_model_path, osim_new_model_path, new_params):
        osim_model = opensim.Model(osim_old_model_path)
        osim_model.initSystem()
        model_name = osim_model.getModel().getName()

        for mtu in new_params.xpath('mtuSet/mtu'):
            mtu_name = mtu.xpath('name')[0].text
            muscle = osim_model.getMuscles().get(mtu_name)
            muscle.set_optimal_fiber_length(float(mtu.xpath('optimalFibreLength')[0].text))
            muscle.set_tendon_slack_length(float(mtu.xpath('tendonSlackLength')[0].text))
            muscle.set_max_isometric_force(float(mtu.xpath('strengthCoefficient')[0].text) * float(mtu.xpath('maxIsometricForce')[0].text))
            muscle.set_pennation_angle_at_optimal(float(mtu.xpath('pennationAngle')[0].text) * 180.0 / math.pi)  # warning in rad

        osim_model.setName(model_name + '_optCEINMS')
        osim_model.printToXML(osim_new_model_path)

    @staticmethod
    def sort_muscle_dict(to_sort):
        sorted_key = sorted(to_sort, key=str.lower)
        to_sort_sorted = {}
        for key in sorted_key:
            to_sort_sorted[key] = to_sort[key]
        return to_sort_sorted

    @staticmethod
    def combine_models(base_model, model_to_add):
        # Open the models
        osim_base = opensim.Model(base_model)
        osim_to_add = opensim.Model(model_to_add)

        bodies = osim_to_add.getBodySet()
        joints = osim_to_add.getJointSet()
        controls = osim_to_add.getControllerSet()
        constraints = osim_to_add.getConstraintSet()
        markers = osim_to_add.getMarkerSet()
        for body in bodies:
            osim_base.addBody(body)

        for joint in joints:
            osim_base.addJoint(joint)

        for control in controls:
            osim_base.addControl(control)

        for constraint in constraints:
            osim_base.addConstraint(constraint)

        for marker in markers:
            osim_base.addMarker(marker)

        osim_base.initSystem()
        osim_base.printToXML(base_model)


class Wu(OsimModel):
    def __init__(self, model_path, dof_list):
        super(Wu, self).__init__(model_path, dof_list)

    @staticmethod
    def type():
        return "Wu"

    @staticmethod
    def extract_mtu_from_osim(osim_model, all_muscles):
        mtu_set = {}
        for muscle in osim_model.getMuscles():
            if muscle.getName() not in all_muscles:
                continue
            if muscle.getConcreteClassName() != 'Thelen2003Muscle':
                raise NotImplementedError(muscle.getConcreteClassName() + " is not implemented for automatic xlm write")
            full_mtu_name = "mtu" + remove_begin + muscle.getName() + remove_end
            mtu_set[full_mtu_name] = {
                "name": muscle.getName(),
                "c1": -0.5,
                "c2": -0.5,
                "shapeFactor": 0.1,
                "optimalFibreLength": muscle.getOptimalFiberLength(),
                "pennationAngle": muscle.getPennationAngleAtOptimalFiberLength(),
                "tendonSlackLength": muscle.getTendonSlackLength(),
                "maxIsometricForce": muscle.getMaxIsometricForce(),
                "strengthCoefficient": 1.5
            }
        # Sort in alphabetical order
        return Wu.sort_muscle_dict(mtu_set)

    @staticmethod
    def mtu_default():
        return {
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
        }

    @staticmethod
    def calibration_info(model_name):
        return {
            "uncalibrated": {
                "subjectID": model_name,
                "additionalInfo": ""
            }
        }

    @staticmethod
    def setup_model(osim_path, dof_list):
        model_name, mtu_set, dof_set = Wu.read_osim_file(osim_path, dof_list)

        return {
            "mtuDefault": Wu.mtu_default(),
            "mtuSet": mtu_set,
            "dofSet": dof_set,
            "calibrationInfo": Wu.calibration_info(model_name)
        }
