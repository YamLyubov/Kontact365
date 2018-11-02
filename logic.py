import xml.etree.ElementTree as etr


def get_date(ip):
    tree = etr.parse('UsersTest.xml')
    root = tree.getroot()
    for elem in root:
        current_ip = elem.attrib['UserIPAddr']
        if current_ip == ip:
            preresult = elem.attrib['Date2']
            result = preresult[8:10] + '.'\
             + preresult[5:7] + '.'\
             + preresult[:4]
            return result
        return None
print(get_date('10.11.6.206'))