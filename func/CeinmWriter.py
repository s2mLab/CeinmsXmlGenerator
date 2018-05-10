import os

from sys import exit

import lxml.etree as etree

from func import xml_writer, utils

from func.Analyses_lifting import compare_msk


class SetupCalib:
    def __init__(self):
        self.uncalibrated_model = None
        self.excitation = None
        self.calibration = None
        self.force_calibration = False


class SetupTrial:
    def __init__(self):
        self.trial = None
        self.execute = None
        self.allow_override = False


class Writer:
    def __init__(self, base_output_path, setup_calib, ceinms_path):
        self.setup_calib = setup_calib
        self.ceinms_path = ceinms_path

        # Define a nice output name for the folder
        self.base_path = base_output_path
        self.output_calib_path = self.determine_output_calib_path()
        if not os.path.exists(self.output_calib_path):
            self.should_force_calibration = True
            os.makedirs(self.output_calib_path)
        else:
            self.should_force_calibration = setup_calib.force_calibration

        # Calibration path
        self.calibration_path = os.path.join(self.output_calib_path, "calibration.xml")
        self.calibrated_model_path = os.path.join(self.output_calib_path, "calibrated_model.xml")
        self.uncalibrated_model_path = os.path.join(self.output_calib_path, "uncalibrated_model.xml")
        self.excitation_generator_path = os.path.join(self.output_calib_path, "excitation_generator.xml")
        self.calibration_configuration_path = os.path.join(self.output_calib_path, "calibration_config.xml")

        # Trial path declaration
        self.model_path = self.calibrated_model_path
        self.trial_path = None
        self.execution = None
        self.output_run_path = None
        self.setup_path = None
        self.execution_path = None
        self.output_results = None

    def calibrate(self):
        if self.should_force_calibration:
            # Calibrate the model
            self.write_model_file(self.setup_calib.uncalibrated_model.uncalibrated_model)
            self.write_calibration_file()
            self.write_excitation_generator_file(self.setup_calib.excitation)
            self.write_calibration_configuration_file(self.setup_calib.calibration)

            if os.path.isfile(self.calibrated_model_path):
                os.remove(self.calibrated_model_path)
            os.system(self.ceinms_path + os.sep + "CEINMScalibrate -S " + self.calibration_path)
            if not os.path.isfile(self.calibrated_model_path):
                exit("************* ERROR CEINMScalibration cannot calibrate the model *************")

            # Write the calibrated model
            utils.write_model(self.setup_calib, self.calibrated_model_path)

    def run(self, setup_trial, excitations_type):
        # Trials path
        for trial in setup_trial.trials:
            print('****** ' + trial + ' ********')
            setup_trial.trial = trial
            self.trial_path = setup_trial.trial
            self.execution = setup_trial.execution
            self.output_run_path = self.determine_output_run_path()
            if not os.path.exists(self.output_run_path):
                os.makedirs(self.output_run_path)
            else:
                if not setup_trial.allow_override:
                    raise PermissionError("File already exists, modify the parameters of allow override")

            self.setup_path = os.path.join(self.output_run_path, "setup.xml")
            self.execution_path = os.path.join(self.output_run_path, "execution.xml")
            self.output_results = self.determine_result_path()
            if not os.path.exists(self.output_results):
                os.makedirs(self.output_results)

            self.write_setup_file()
            self.write_execution_file(self.execution)
            os.system(self.ceinms_path + os.sep + "CEINMS -S " + self.setup_path)

            #Analyses_lifting
            compare_msk(self.trial_path, self.output_results, excitations_type)



    def write_calibration_file(self):
        tree = {
            "subjectFile": self.uncalibrated_model_path,
            "excitationGeneratorFile": self.excitation_generator_path,
            "calibrationFile": self.calibration_configuration_path,
            "outputSubjectFile": self.calibrated_model_path
        }
        et_ceinms_calibration = etree.Element('ceinmsCalibration')
        self._write_simple_tree(et_ceinms_calibration, tree)
        xml_writer.write_xml_file(self.calibration_path, et_ceinms_calibration, pretty_print=True)

    def write_setup_file(self):
        tree = {
            "subjectFile": self.model_path,
            "excitationGeneratorFile": self.excitation_generator_path,
            "executionFile": self.execution_path,
            "inputDataFile": self.trial_path,
            "outputDirectory": self.output_results
        }
        et_ceinms_calibration = etree.Element('ceinms', xmlns__COLON__xsi="http://www.w3.org/2001/XMLSchema-instance",
                                              xsi__COLON__noNamespaceSchemaLocation="ceinmsSetup.xsd")
        self._write_simple_tree(et_ceinms_calibration, tree)
        xml_writer.write_xml_file(self.setup_path, et_ceinms_calibration, pretty_print=True)

    def write_execution_file(self, execution):
        et_execution = etree.Element('execution', xmlns__COLON__xsi="http://www.w3.org/2001/XMLSchema-instance",
                                     xsi__COLON__noNamespaceSchemaLocation="execution.xsd")
        self._write_simple_tree(et_execution, execution.dict())
        xml_writer.write_xml_file(self.execution_path, et_execution, pretty_print=True)

    def write_excitation_generator_file(self, excitation):
        et_excitation_generator = etree.Element('excitationGenerator',
                                                xmlns__COLON__xsi="http://www.w3.org/2001/XMLSchema-instance",
                                                xsi__COLON__noNamespaceSchemaLocation="excitationGenerator.xsd")
        for signal in excitation.excitation()["input_signals"]:
            et_input_signals = etree.SubElement(et_excitation_generator, 'inputSignals', type=signal)
            et_input_signals.text = self._get_values(excitation.excitation()["input_signals"][signal])

        et_mapping = etree.SubElement(et_excitation_generator, 'mapping')
        for key, el in excitation.excitation()["mapping"].items():
            et_excitation = etree.SubElement(et_mapping, 'excitation', id=key)
            for i in range(int(len(el)/2)):
                et_input = etree.SubElement(et_excitation, 'input', weight=str(el[2*i]))
                et_input.text = el[2*i+1]

        xml_writer.write_xml_file(self.excitation_generator_path, et_excitation_generator, pretty_print=True)

    def write_calibration_configuration_file(self, algo):
        et_calibration = etree.Element('calibration',
                                       xmlns__COLON__xsi="http://www.w3.org/2001/XMLSchema-instance",
                                       xsi__COLON__noNamespaceSchemaLocation="calibration.xsd")
        self._write_simple_tree(et_calibration, algo.calib())
        xml_writer.write_xml_file(self.calibration_configuration_path, et_calibration, pretty_print=True)

    def write_model_file(self, subject):
        et_subject = etree.Element('subject', xmlns__COLON__xsi="http://www.w3.org/2001/XMLSchema-instance",
                                   xsi__COLON__noNamespaceSchemaLocation="subject.xsd")

        self._write_simple_tree(et_subject, subject)
        xml_writer.write_xml_file(self.uncalibrated_model_path, et_subject, pretty_print=True)

    def _write_simple_tree(self, parent, tree):
        for branch in tree:
            #  print(branch)
            if tree[branch] is not None:  # is not None is necessary so 0 is tag and not skipped
                if isinstance(tree[branch], dict):
                    b = etree.SubElement(parent, branch)
                    self._write_simple_tree(b, tree[branch])
                else:
                    if isinstance(tree[branch], tuple) and isinstance(tree[branch][0], dict):
                        for leaf in tree[branch]:
                            b = etree.SubElement(parent, branch)
                            self._write_simple_tree(b, leaf)
                    else:
                        b = etree.SubElement(parent, branch)
                        b.text = self._get_values(tree[branch])
            else:
                etree.SubElement(parent, branch)

    @staticmethod
    def generate_trial_xml(model, directory, fname):
        et_trial = etree.Element('inputData', xmlns__COLON__xsi="http://www.w3.org/2001/XMLSchema-instance",
                                 xsi__COLON__noNamespaceSchemaLocation="inputData.xsd")

        # ToDo modify the names according to Romain ... perhaps store names in utils to be used later?

        file_name = directory + "/_MuscleAnalysis_Length.sto"
        if not os.path.isfile(file_name):
            print("File " + file_name + " does not exist")
        etree.SubElement(et_trial, "muscleTendonLengthFile").text = file_name

        file_name = directory + "/EMG.sto"
        if not os.path.isfile(file_name):
            print("File " + file_name + " does not exist")
        etree.SubElement(et_trial, "excitationsFile").text = file_name

        file_name = directory + "/InvDyn.sto"
        if not os.path.isfile(file_name):
            print("File " + file_name + " does not exist")
        etree.SubElement(et_trial, "externalTorquesFile").text = file_name

        branch = etree.SubElement(et_trial, 'momentArmsFiles')
        dof_name = model["DoFName"]
        for dof in dof_name:
            tp = etree.SubElement(branch, "momentArmsFile")
            tp.set("dofName", dof)
            file_name = directory + "/_MuscleAnalysis_MomentArm_" + dof + ".sto"
            if not os.path.isfile(file_name):
                print("File " + file_name + " does not exist")
            tp.text = file_name

        xml_writer.write_xml_file(fname, et_trial, pretty_print=True)

    @staticmethod
    def _get_values(values):

        if isinstance(values, list) or isinstance(values, tuple):
            val_text = ""
            for trial in values:
                val_text += " " + str(trial)
            return val_text[1:]  # remove the first " "

        elif isinstance(values, str):
            return values

        else:
            return str(values)

    def _determine_output_common(self):
        return self.setup_calib.uncalibrated_model.type() + self.setup_calib.uncalibrated_model.name() + "_" + \
               str(len(self.setup_calib.uncalibrated_model.uncalibrated_model["dofSet"])) + "dofs_" + \
               self.setup_calib.calibration.name() + "_" + self.setup_calib.excitation.name()

    def determine_output_calib_path(self):
        return os.path.join(self.base_path, self._determine_output_common(), "calib")

    def determine_output_run_path(self):
        new_dir = "Trials_Exec" + self.execution.name()
        return os.path.join(self.base_path, self._determine_output_common(), new_dir)

    def determine_result_path(self):
        new_dir = "results_" + os.path.splitext(os.path.basename(self.trial_path))[0]
        return os.path.join(self.base_path, self.determine_output_run_path(), new_dir)
