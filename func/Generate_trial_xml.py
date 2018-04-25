import os
import lxml.etree as etree
from func import xml_writer


def generate_trial_xml(model, directory, fname):
    et_trial = etree.Element('inputData', xmlns__COLON__xsi="http://www.w3.org/2001/XMLSchema-instance",
                             xsi__COLON__noNamespaceSchemaLocation="inputData.xsd")

    FileName = "%s/_MuscleAnalysis_Length.sto" % directory
    if not os.path.isfile(FileName):
        print("File %s does not exist" % FileName)
    etree.SubElement(et_trial, "muscleTendonLengthFile").text = FileName

    FileName = "%s/EMG.sto" % directory
    if not os.path.isfile(FileName):
        print("File %s does not exist" % FileName)
    etree.SubElement(et_trial, "excitationsFile").text = FileName

    FileName = "%s/InvDyn.sto" % directory
    if not os.path.isfile(FileName):
        print("File %s does not exist" % FileName)
    etree.SubElement(et_trial, "externalTorquesFile").text = FileName



    branch = etree.SubElement(et_trial, 'momentArmsFiles')
    DoFName = model["DoFName"]
    for dof in DoFName:
        tp = etree.SubElement(branch, "momentArmsFile")
        tp.set("dofName", dof)
        FileName = "%s/_MuscleAnalysis_MomentArm_%s.sto" % (directory, dof)
        if not os.path.isfile(FileName):
            print("File %s does not exist" % FileName)
        tp.text = FileName

    xml_writer.write_xml_file(fname, et_trial, pretty_print=True)
