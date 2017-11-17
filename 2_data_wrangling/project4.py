import xml.etree.cElementTree as ET
from collections import defaultdict
import re
import pprint
import codecs
import json

OSMFILE = "san-diego-tijuana_mexico.osm"

street_type_re = re.compile(r'\b\S+\.?$', re.IGNORECASE)
street_type_re_spanish = re.compile(r'^\S+\b', re.IGNORECASE)
postcode_re = re.compile(r'\d{5}', re.IGNORECASE)

expected_spanish = ["Camino", "Caminito", "Via", "Calle", "Plaza", "Rancho", "Senda", "Corte", "Circulo", "Avenida"]
expected = ["Street", "Avenue", "Boulevard", "Drive", "Court", "Place", "Square", "Lane", "Road", 
            "Trail", "Parkway", "Commons", "Circle", "Cove", "Creek", "Glen", "Terrace", "View", "Way", "Loop", "Pass", "Point", "Row", "Run"]

#expected_postcode = ["91901","91902","91903","91905","91906","91908","91909","91910","91911","91912","91913","91914","91915","91916","91917","91921","91931","91932","91933","91934","91935","91941","91942","91943","91944","91945","91946","91947","91948","91950","91951","91962","91963","91976","91977","91978","91979","91980","91987","92003","92004","92007","92008","92009","92010","92011","92013","92014","92018","92019","92020","92021","92022","92023","92024","92025","92026","92027","92028","92029","92030","92033","92036","92037","92038","92039","92040","92046","92049","92051","92052","92054","92055","92056","92058","92057","92059","92060","92061","92064","92065","92066","92067","92068","92069","92070","92071","92072","92074","92075","92078","92079","92081","92082","92083","92084","92085","92086","92088","92090","92091","92092","92093","92096","92101","92102","92103","92104","92105","92106","92107","92108","92109","92110","92111","92112","92113","92114","92115","92116","92117","92118","92119","92120","92121","92122","92123","92124","92126","92127","92128","92129","92130","92131","92132","92134","92135","92136","92137","92138","92139","92140","92142","92143","92145","92147","92149","92150","92152","92153","92154","92155","92158","92159","92160","92161","92162","92163","92164","92165","92166","92167","92168","92169","92170","92171","92172","92173","92174","92175","92176","92177","92178","92179","92182","92184","92186","92187","92190","92191","92192","92193","92194","92195","92196","92197","92198","92199"]
expected_postcode = [] #checking cleaning function by allowing all postcodes to be printed

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
            "highway": "Highway",
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
            "Wl": "Well",
            "Gre": "Green",
            "Lo": "Loop",
            "Pa": "Pass",
            "tre": "Terrace"
            }

mapping_spanish = { "Cam": "Camino",
                    "Camto": "Caminito",
                    "Cte": "Corte",
                    "Trza": "Terraza",
                    "Avnda": "Avenida",
                    "Camta": "Caminito",
                    }

def audit_street_type(street_types, street_name):
    """Add street type and name to street_types dictionary 
    if it is not in 'expected' or 'expected_spanish' lists.
    """
    m = street_type_re.search(street_name)
    if m:
        street_type = m.group()
        if street_type not in expected:
            n = street_type_re_spanish.search(street_name)
            if n:
                street_type_spanish = n.group()
                if street_type_spanish not in expected_spanish:
                    street_types[street_type].add(street_name)

def audit_postcodes(postcodes, postcode_name):
    """ Add postcode and postcode name to postcodes dictionary if
    the postcode is not in expected_postcode list.
    """
    m = postcode_re.search(postcode_name)
    if m:
        postcode = m.group()
        if postcode not in expected_postcode:
            postcodes[postcode].add(postcode_name)
        
def is_street_name(elem):
    return (elem.attrib['k'] == "addr:street")

def is_postcode_name(elem):
    return (elem.attrib['k'] == "addr:postcode")

def audit(osmfile):
    """ Parses data file and audits street name types and postcodes. """
    osm_file = open(osmfile, "r")
    street_types = defaultdict(set)
    postcode_types = defaultdict(set)
    for event, elem in ET.iterparse(osm_file, events=("start",)):
        if elem.tag == "node" or elem.tag == "way":
            for tag in elem.iter("tag"):
                if is_street_name(tag):
                    audit_street_type(street_types, tag.attrib['v'])
                if is_postcode_name(tag):
                    audit_postcodes(postcode_types, tag.attrib['v'])
    return street_types, postcode_types


def update_name(name, mapping):
    """Changes name to accepted value in dictionary."""
    for case in mapping:
        if mapping[case] in name:
            continue
        name = name.replace(case,mapping[case])

    return name

def clean_streetname(street_name):
    """Replace incorrect english street type (usually at the end of the string) 
    with acceptable stored dictionary value. 
    Then replace any spanish street name types (usually at the beginning)
    with the acceptable stored dictionary value.
    """
    m = street_type_re.search(street_name)
    if m:
        street_type = m.group()
        if street_type not in expected:
            for case in mapping:
                if case == street_type:
                    street_name = street_name.replace(case,mapping[case])
    n = street_type_re_spanish.search(street_name)
    if n:
        street_type = n.group()
        if street_type not in expected_spanish:
            for case in mapping_spanish:
                if case == street_type:
                    street_name = street_name.replace(case,mapping_spanish[case])                            
    return street_name

def clean_postcode(postcode_name):
    """If postcode_name is not the 5 digit postal code, return the 5 digit form.
    """
    m = postcode_re.search(postcode_name)
    if m:
        postcode = m.group()
        if postcode_name != postcode:
            postcode_name = postcode
    return postcode_name

def test():
    """Main program. Audit osm file. Then convert osm to JSON format
    while cleaning street names and postal codes.
    """
    st_types, pc_types = audit(OSMFILE)
    st_type_dict = dict(st_types)
    pc_type_dict = dict(pc_types)
    
    process_map(OSMFILE, True)

    with open("audit_streetnames.txt", "w") as f:
        pprint.pprint(st_type_dict, f)
        
    with open("audit_postcodes.txt", "w") as f:
        pprint.pprint(pc_type_dict, f)


lower = re.compile(r'^([a-z]|_)*$')
lower_colon = re.compile(r'^([a-z]|_)*:([a-z]|_)*$')
problemchars = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')

CREATED = [ "version", "changeset", "timestamp", "user", "uid"]


def shape_element(element):
    """Reshape data to desired JSON format and clean streetnames and postalcodes found in audit"""
    node = {}
    
    if element.tag == "node" or element.tag == "way" :
        node['type'] = element.tag
        
        if element.tag == "way": 
            ndtags = element.findall('nd')
            node['node_refs'] = []
            for index, ndtag in enumerate(ndtags):
                node['node_refs'].append(ndtag.attrib.get('ref'))
                
        for element2 in element.iter():
            tag_keys = element2.keys()
            for key in tag_keys:
                
                if key == 'v':
                    continue
                
                elif key in CREATED:
                    try:
                        node['created'][key] = element.attrib.get(key)
                    except KeyError:
                        node['created'] = {}
                        node['created'][key] = element.attrib.get(key)
                        
                elif key == 'lon' or key == 'lat':
                    node['pos'] = [ float(element.attrib.get('lat')) , float(element.attrib.get('lon')) ]
                    
                elif key == 'k':
                    k_tag = element2.attrib.get('k') # save attribute of k tag
                    if problemchars.search(k_tag) != None: # ignore tags with problem characters
                        continue 
                    if k_tag.startswith('addr:street:'):
                        continue
                    if k_tag.startswith('addr:'):
                        try:
                            if k_tag == 'addr:street':
                                node['address'][k_tag[5:]] = clean_streetname(element2.attrib.get('v')) 
                            elif k_tag == 'addr:postcode':
                                node['address'][k_tag[5:]] = clean_postcode(element2.attrib.get('v')) 
                            else:
                                node['address'][k_tag[5:]] = element2.attrib.get('v')
                        except KeyError:
                                node['address'] = {}
                                if k_tag == 'addr:street':
                                    node['address'][k_tag[5:]] = clean_streetname(element2.attrib.get('v'))
                                elif k_tag == 'addr:postcode':
                                    node['address'][k_tag[5:]] = clean_postcode(element2.attrib.get('v'))
                                else:
                                    node['address'][k_tag[5:]] = element2.attrib.get('v')
                    else:
                        node[k_tag] = element2.attrib.get('v')                    
                else:
                    node[key] = element.attrib.get(key)
        return node
    else:
        return None


def process_map(file_in, pretty = False):
    # You do not need to change this file
    file_out = "{0}.json".format(file_in)
    data = []   
    with codecs.open(file_out, "w") as fo:
        for _, element in ET.iterparse(file_in):
            el = shape_element(element)
            if el:
                data.append(el)
                if pretty:
                    fo.write(json.dumps(el, indent=2)+"\n")
                else:
                    fo.write(json.dumps(el) + "\n")
    return data

if __name__ == '__main__':
    test()