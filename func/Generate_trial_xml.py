
def Generate_trial_xml(Model, subdir):



if Model.lower() == 'wu':
    @staticmethod
    def dict():
       DoFName = ("sternoclavicular_r1", "sternoclavicular_r2",
                  "Acromioclavicular_r1", "Acromioclavicular_r2", "Acromioclavicular_r3",
                  "shoulder_plane", "shoulder_ele", "shoulder_rotation")
        return {
           "muscleTendonLengthFile" : "./%s/_MuscleAnalysis_Length.sto" %(subdir),
           "excitationsFile" : "./%s/EMG.sto" %(subdir),
           "momentArmsFiles"  :  {
            for dof in DoFName:
               "momentArmsFile dofName= %s" &(dof) : "./%s/_MuscleAnalysis_MomentArm_%s.sto" %(subdir, dof)
            }
            "externalTorquesFile" : "./%s/_InvDyn.sto" % (subdir)
       }


elif Model.lower() == 'das3':




    def write_Trial_file(self, xxxx):
        et_trial = etree.Element('inputData', xmlns__COLON__xsi="http://www.w3.org/2001/XMLSchema-instance",
                                     xsi__COLON__noNamespaceSchemaLocation="inputData.xsd")
        self._write_simple_tree(et_trial, trial.dict())
        xml_writer.write_xml_file(self.trial_path, et_trial, pretty_print=True)