import xml 
import os

def find_omc_interface(root_tree):
    finded_models = list()
    for model_element in root_tree.getiterator():
        if model_element.tag == "ScalarVariable" and \
            "name" in model_element.attrib and "fileName" in model_element.attrib:

            splited_name = model_element.attrib["name"].split(".")

            if len(splited_name)!=2: # Need a <parent>.t shape
                continue
            
            if splited_name[1] != 't':
                continue

            if os.path.split(os.path.dirname(model_element.attrib["fileName"]))[1] != "omc_gym_lib":
                continue
            
            finded_models.append(splited_name[0])

    return list(set(finded_models))
