DUT_HEADER = """
(*@PROPERTIES_EX@
TYPE: DATA_TYPE
LOCALE: 0
*)
"""


def get_file_contents(path_to_file):
    with open(path_to_file, 'r') as file:
        return file.read()


def concat_dut_definitions(dut_file_list, base_path = ''):
    result = ''
    for path in dut_file_list:
        result += get_file_contents(base_path + path).replace('END_STRUCT', 'END_STRUCT;') + '\n'
    return result


def sys_flag_types(base_path, persist=False):
    export = 'SYS_FLAG_TYPE.IEC'
    data_types = [ # Data types
        'misc/data/STRING1.IEC',
        'misc/data/StringKeySize.IEC',
        'misc/data/StringTextSize.IEC',
        'misc/data/ArrayOfByte255.IEC',
        'misc/data/NestedKeys.IEC',
        'json/data/JsonPosition.IEC',
        'json/data/JsonKey.IEC',
        'json/data/JsonValue.IEC',
        'json/data/JsonProperty.IEC',
    ]
    constants = [ # Constants
        'misc/data/GeneralConstants.IEC',
        'json/data/JsonConstants.IEC',
    ]
    result = DUT_HEADER \
            + '\n(* DATA TYPES DEFINITIONS *)\n\n' + concat_dut_definitions(data_types, base_path) \
            + '\n(* CONSTANTS VARIABLES *)\n\n' + concat_dut_definitions(constants, base_path)
    if persist:
        with open(base_path + export, 'w') as file:
            file.write(result)
    else:
        print(result)


if __name__ == '__main__':
    base_path = '../export/'
    sys_flag_types(base_path, True)
