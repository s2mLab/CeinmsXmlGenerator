import os.path

def Generate_trial_xml(Model, subdir):



    @staticmethod
    def dict():
       DoFName = Model["DoFName"]
       MomentArm = {}
       for dof in DoFName:
          tp0 = "momentArmsFile dofName= %s" % (dof)
          tp1 = "./%s/_MuscleAnalysis_MomentArm_%s.sto" % (subdir, dof)
          MomentArm[tp0] = tp1

#   example:    <momentArmsFile dofName="shoulder_plane">./F6H1_1_MICK/_MuscleAnalysis_MomentArm_shoulder_plane.sto</momentArmsFile>
       return {"muscleTendonLengthFile" : "./%s/_MuscleAnalysis_Length.sto" %(subdir),
           "excitationsFile" : "./%s/EMG.sto" %(subdir),
           "externalTorquesFile" : "./%s/_InvDyn.sto" % (subdir)
           "momentArmsFiles"  :  MomentArm}


    def write_Trial_file(self, xxxx):
       fname = ''
       if not os.path.isfile(fname):
          et_trial = etree.Element('inputData', xmlns__COLON__xsi="http://www.w3.org/2001/XMLSchema-instance",
                                        xsi__COLON__noNamespaceSchemaLocation="inputData.xsd")
           self._write_simple_tree(et_trial, trial.dict())
           xml_writer.write_xml_file(fname, et_trial, pretty_print=True)