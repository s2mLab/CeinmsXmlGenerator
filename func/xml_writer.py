import lxml.etree as etree


def write_xml_file(file, xml_root_element, xml_declaration=False, pretty_print=False, encoding='unicode', indent='  '):
    s = etree.tostring(xml_root_element, xml_declaration=xml_declaration, pretty_print=pretty_print, encoding=encoding)
    if pretty_print:
        s = s.replace('  ', indent)
    try:
        s = s.replace('__COLON__', ":")
        while s.find('__RM_BEGIN__') >= 0:
            s = s[:s.find('__RM_BEGIN__')] + s[s.find('__RM_END__') + len('__RM_END__'):]

        with open(file, 'w') as f:
            f.write('<?xml version="1.0" encoding="UTF-8" standalone="no" ?>\n')
            f.write(s)
    except IOError:
        print("Error while writing in log file!")
