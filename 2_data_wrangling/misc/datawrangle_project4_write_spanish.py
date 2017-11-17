"""
Your task in this exercise has two steps:

- audit the OSMFILE and change the variable 'mapping' to reflect the changes needed to fix 
    the unexpected street types to the appropriate ones in the expected list.
    You have to add mappings only for the actual problems you find in this OSMFILE,
    not a generalized solution, since that may and will depend on the particular area you are auditing.
- write the update_name function, to actually fix the street name.
    The function takes a string with street name as an argument and should return the fixed name
    We have provided a simple test so that you see what exactly is expected
"""
import xml.etree.cElementTree as ET
from collections import defaultdict
import re
import pprint


OSMFILE = "san-diego-tijuana_mexico.osm"
street_type_re = re.compile(r'\b\S+\.?$', re.IGNORECASE)
street_type_re_spanish = re.compile(r'^\S+\b', re.IGNORECASE)

expected_spanish = ["Camino", "Caminito", "Via", "Calle", "Plaza", "Rancho", "Senda", "Corte", "Circulo", "Avenida"]
expected = ["Street", "Avenue", "Boulevard", "Drive", "Court", "Place", "Square", "Lane", "Road", 
            "Trail", "Parkway", "Commons"]

# UPDATE THIS VARIABLE
mapping = { "St": "Street",
            "St.": "Street",
            "Rd": "Road",
            "Rd.": "Road",
            "Ro": "Road",
            "Ave": "Avenue",
            "Ave.": "Avenue",
            "Av": "Avenue",
            "Bl": "Boulevard",
            "Blvd": "Boulevard",
            "Blvd.": "Boulevard",
            "Ci": "Circle",
            "Cr": "Creek",
            "Ct": "Court",
            "Ct.": "Court",
            "Cte": "Court",
            "Cv": "Cove",
            "DRIVE": "Drive",
            "Dr": "Drive",
            "Dy": "",
            "Gl": "Glen",
            "Hw": "Highway",
            "Hwy": "Highway",
            "Hy": "Highway",
            "La": "Lane",
            "Ln": "Lane",
            "Lo": "Loop",
            "Pk": "Parkway",
            "Pkwy": "Parkway",
            "Pkwy.": "Parkway",
            "Pl": "Place",
            "Ps": "Pass",
            "Pt": "Point",
            "Pw": "Parkway",
            "Py": "Parkway",
            "Pz": "Parkway",
            "Ru": "Run",
            "Rw": "Row",
            "Te": "Terrace",
            "Ter": "Terrace",
            "Tl": "Trail",
            "Tr": "Trail",
            "Vw": "View",
            "Wa": "Way",
            "Wk": "Walk",
            "Wy": "Way",
            "street": "Street",
            "street)": "Street",
            "Wl": "Well"
            }

mapping_spanish = { "Cam": "Camino",
                    "Camto": "Caminito",
                    "Cte": "Corte",
                    "Trza": "Terraza",
                    "Avnda": "Avenida",
                    "Camta": "Caminito",
                    "S": "South",
                    "N": "North",
                    "W": "West",
                    "E": "East"
                    }

def is_street_name(elem):
    return (elem.attrib['k'] == "addr:street")

def write_updates(osmfile, outosmfile, logfilename):
    # Open the input and output files 
    with open(osmfile, 'r') as infile, open(outosmfile, 'w') as outfile, open(logfilename, 'w') as logfile:
        # Interate through the file tags for node or way tags 
        #for event, elem in ET.iterparse(infile, events=("start",)):
        outfile.write("<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n")
        for event, elem in ET.iterparse(infile):
            if elem.tag == "node" or elem.tag == "way":
                for tag in elem.iter("tag"):
                    #if it is a street name and matches the list
                    #if is_street_name(tag) and any(street in tag.attrib['v'] for street in st_name_dict.keys()):
                    if is_street_name(tag):
                        street_name = tag.attrib['v'] 
                        m = street_type_re_spanish.search(street_name)
                        if m:
                            street_type = m.group()
                            if street_type not in expected_spanish:
                                for case in mapping_spanish:
                                    if case == street_type:
                                        #before_change = tag.attrib['v']
                                        tag.attrib['v'] = tag.attrib['v'].replace(case,mapping_spanish[case])
                                        #try:
                                        #    logfile.write("Before: %s After: %s \n" % (str(before_change), str(tag.attrib['v'])) )
                                        #except UnicodeEncodeError:
                                        #    logfile.write("Before: %s After: %s \n" % (before_change, tag.attrib['v']).encode("utf-8") )
                                        break
                                        
                                    #logfile.write(tag.attrib['v'])
                                    
        outfile.write(ET.tostring(elem, encoding='utf-8'))

            
def test():
    write_updates('san-diego-tijuana_mexico_update2.osm',  'san-diego-tijuana_mexico_update3.osm', 'san-diego-tijuana_mexico_update.log')
    #write_updates('example_spanish.osm',  'example_update.osm', 'example.log')

if __name__ == '__main__':
    test()