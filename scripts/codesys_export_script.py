"""
CODESYS ScriptEngine Program
Checks every component in the project tree of the currently loaded project
and saves all POUs and DUTs (all components, that have a `textual_declaration`).
"""
from __future__ import print_function
import os


EXCLUDE_NAMES = ['Device', 'Plc Logic', 'Application', 'Task Configuration', 'MainTask']
DUT_FILE_ENDING = '.IEC'
POU_FILE_ENDING = '.ST'
DUT_FORMAT = "{declaration}"
POU_FORMAT = """(*@PROPERTIES_EX@
TYPE: {object_type}
LOCALE: 0
IEC_LANGUAGE: ST
PLC_TYPE: independent
PROC_TYPE: independent
*)
(*@KEY@:DESCRIPTION*)

(*@KEY@:END_DESCRIPTION*)
{declaration}

(*@KEY@: WORKSHEET
NAME: {name}
IEC_LANGUAGE: ST
*)
{implementation}
(*@KEY@: END_WORKSHEET *)
END_{function_type}
"""


def save_mkdir(path):
    if not os.path.exists(path):
        os.mkdir(path)


def get_project():
    return projects.primary


def get_project_dir():
    project_path = get_project().path
    last_dir = project_path.rfind('\\')
    return project_path[:last_dir]


def write_to_file(text, full_path):
    with open(full_path, 'wb') as file:
        file.write(text.replace('\r\n', '\n').replace('\r', '\n'))


def get_node_info(node):
    """
    Gets the node's name, object_type, function_type, declaration and implementation
    :param node: a POU or DUT node
    :return: the node's name, object_type, function_type, declaration and implementation as a dictionary
    """
    node_info = {
        "name": node.get_name(),
        "object_type": 'POU' if node.has_textual_declaration and node.has_textual_implementation else \
            'DUT' if node.has_textual_declaration else '',
        "declaration": node.textual_declaration.text if node.has_textual_declaration else None,
        "implementation": node.textual_implementation.text if node.has_textual_implementation else None
    }
    declaration_end = min(node_info["declaration"].find(' '), node_info["declaration"].find('\n'))
    node_info["function_type"] = node_info["declaration"][:declaration_end]
    return node_info


def save_dut_or_pou(node, file_path):
    """
    Tries to save the node, what will succeed if it is a POU or DUT
    :param node: a POU or DUT node
    :param file_path: where to store the node
    :return: nothing
    """
    try:
        node_info = get_node_info(node)
        if node_info["object_type"] == 'POU':
            text = POU_FORMAT.format(**node_info)
            write_to_file(text, file_path + POU_FILE_ENDING)
        else:
            text = DUT_FORMAT.format(**node_info)
            write_to_file(text, file_path + DUT_FILE_ENDING)
        print("{name} - {object_type} ({function_type})".format(**node_info))
    except Exception:
        pass


def save_text_nodes(node, base_path):
    name = node.get_name(False)
    if name not in EXCLUDE_NAMES:
        base_path = os.path.join(base_path, name)
        save_dut_or_pou(node, base_path)
    return base_path


def save_child_nodes(root_node, base_path):
    child_nodes = root_node.get_children()
    if child_nodes is not None and len(child_nodes) > 0:
        save_mkdir(base_path)
        for node in child_nodes:
            child_path = save_text_nodes(node, base_path)
            save_child_nodes(node, child_path)


if __name__ == '__main__':
    root_path = os.path.join(get_project_dir(), '../export')
    print('Save raw text export to ' + root_path)
    save_mkdir(root_path)
    save_child_nodes(get_project(), root_path)
    print('Finished')
