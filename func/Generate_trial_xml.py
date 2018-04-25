import lxml.etree as etree
from func import xml_writer


def generate_trial_xml(model, subdir, fname):
    et_trial = etree.Element('inputData', xmlns__COLON__xsi="http://www.w3.org/2001/XMLSchema-instance",
                             xsi__COLON__noNamespaceSchemaLocation="inputData.xsd")

    etree.SubElement(et_trial, "muscleTendonLengthFile").text = "./%s/_MuscleAnalysis_Length.sto" % subdir
    etree.SubElement(et_trial, "excitationsFile").text = "./%s/EMG.sto" % subdir
    etree.SubElement(et_trial, "externalTorquesFile").text = "./%s/_InvDyn.sto" % subdir
    branch = etree.SubElement(et_trial, 'momentArmsFiles')
    DoFName = model["DoFName"]
    for dof in DoFName:
        tp = etree.SubElement(branch, "momentArmsFile")
        tp.set("dofName", dof)
        tp.text = "./%s/_MuscleAnalysis_MomentArm_%s.sto" % (subdir, dof)

    xml_writer.write_xml_file(fname, et_trial, pretty_print=True)
