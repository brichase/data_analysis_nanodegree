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
#street_type_re = re.compile(r'^\S+\b', re.IGNORECASE)

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


def audit_street_type(street_types, street_name):
    m = street_type_re.search(street_name)
    if m:
        street_type = m.group()
        if street_type not in expected:
            street_types[street_type].add(street_name)


def is_street_name(elem):
    return (elem.attrib['k'] == "addr:street")


def audit(osmfile):
    osm_file = open(osmfile, "r")
    street_types = defaultdict(set)
    for event, elem in ET.iterparse(osm_file, events=("start",)):

        if elem.tag == "node" or elem.tag == "way":
            for tag in elem.iter("tag"):
                if is_street_name(tag):
                    audit_street_type(street_types, tag.attrib['v'])

    return street_types


def update_name(name, mapping):

    # YOUR CODE HERE
    #print mapping
    for case in mapping:
        if mapping[case] in name:
            continue
        name = name.replace(case,mapping[case])

    return name

def write_updates(st_name_dict, osmfile, outosmfile):
    # Open the input and output files 
    with open(osmfile, 'r') as infile, open(outosmfile, 'w') as outfile:
        # Interate through the file tags for node or way tags 
        for event, elem in ET.iterparse(infile, events=("start",)):
            if elem.tag == "node" or elem.tag == "way":
                for tag in elem.iter("tag"):
                    #if it is a street name and matches the list
                    #if is_street_name(tag) and any(street in tag.attrib['v'] for street in st_name_dict.keys()):
                    if is_street_name(tag):
                        street_name = tag.attrib['v'] 
                        m = street_type_re.search(street_name)
                        if m:
                            street_type = m.group()
                            if street_type not in expected:
                                for case in mapping:
                                    if mapping[case] in tag.attrib['v']:
                                        continue
                                    tag.attrib['v'] = tag.attrib['v'].replace(case,mapping[case])
            outfile.write(ET.tostring(elem))
            
def test():
    st_types = audit(OSMFILE)
 #   st_type_dict = dict(st_types)
    

 #   with open("audit_streetnames.txt", "w") as f:
#       pprint.pprint(st_type_dict, f)
        
    st_name_dict = {}
    for st_type, ways in st_types.iteritems():
        for name in ways:

            better_name = update_name(name, mapping)
            #print name, "=>", better_name
            st_name_dict[name] = better_name
            write_updates(st_name_dict, 'example.osm',  'san-diego-tijuana_mexico_update.osm')


if __name__ == '__main__':
    test()