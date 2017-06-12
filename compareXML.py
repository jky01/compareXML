import sys
import xml.etree.ElementTree as ET
from collections import namedtuple

#from Tkinter import Tk
#from tkFileDialog import askopenfilename

Pair = namedtuple("Pair", ["version", "distName"])

distName_list={}
distName_all ={}

def process(file1,file2):

    tree_1 = ET.ElementTree(file=file1)
    tree_2 = ET.ElementTree(file=file2)
    for root_1 in tree_1.findall('{raml20.xsd}cmData/{raml20.xsd}managedObject'):
        distName_all[root_1.get('version')+root_1.get('distName') ] = root_1.get('version')+root_1.get('distName');

        if (len(root_1.get('distName')) - root_1.get('distName').rfind('-',root_1.get('distName').rfind('/')) <= 3 ):
            distName_list[root_1.get('version')+root_1.get('distName')[0:root_1.get('distName').rfind('-',root_1.get('distName').rfind('/'))]] = (Pair(root_1.get('version'),root_1.get('distName')))
        check_str = '{raml20.xsd}cmData/{raml20.xsd}managedObject[@version=\"' + root_1.get('version') + '\"][@distName=\"' + root_1.get('distName') + '\"]'

        root_2 = tree_2.find(check_str)

        for elem_1 in root_1:
            if( elem_1.attrib.get('name') == "System"): continue

            isFound = False;
            for elem_2 in root_2:
                if( elem_1.attrib.get('name') == elem_2.attrib.get('name') ):
                    isFound=True
                    if( elem_1.text != elem_2.text ):
                        print(root_1.get('version'), root_1.get('distName'), elem_1.attrib.get('name') , elem_1.text , elem_2.text + " is unmatch")

            if( isFound == False ):
                print ( root_1.get('version'), root_1.get('distName'), elem_1.attrib.get('name') + "is not found")

    print ( "first loop is finished.")
    for root_2 in tree_2.findall('{raml20.xsd}cmData/{raml20.xsd}managedObject'):
        if (len(root_2.get('distName')) - root_2.get('distName').rfind('-',root_2.get('distName').rfind('/')) <= 3 ):
            if ( root_2.get('version')+root_2.get('distName')[0:root_2.get('distName').rfind('-',root_2.get('distName').rfind('/'))] in distName_list ):
                if(  root_2.get('version')+root_2.get('distName') not in distName_all ):
                    print ( root_2.get('version'), root_2.get('distName') + " is not found" )

    print("second loop is finished.")


if( len(sys.argv) > 2 ):
    process(sys.argv[1],sys.argv[2])
else:
    print("compareXML.py [modify_XML] [dump_XML]")

#else:
#    Tk().withdraw()
#    filename1 = askopenfilename()
#    Tk().withdraw()
#    filename2 = askopenfilename()
#    process(filename1,filename1)
