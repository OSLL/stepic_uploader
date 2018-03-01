from argparse import ArgumentParser


SOURCE_FILE = 'string_step_api/string_source.txt'
CONFIG_FILE = 'string_step_config.ini'

SECTION_QUESTION_TEMPLATE = "[question_{}]\n" + \
"text={}\n"+ \
"name=string\n"+ \
"pattern={}\n"


def generate_config_section_template(question, i, answer):
    QUESTION = SECTION_QUESTION_TEMPLATE.format(str(i+1), question, answer)
    return QUESTION


def generate_config_file(source):
    sections = ""
    with open(source, "r") as source_file:
        for count, line in enumerate(source_file.readlines()):
            question, answer = line.split(';')
            sections += generate_config_section_template(question, count, answer)
    config_file_name = get_config_name(source)
    with open(config_file_name, "w") as config_file:
        config_file.write(sections)


def get_config_name(source):
    index_first_literal_of_source_file = source.rfind('/')
    if index_first_literal_of_source_file != -1:
        return source[:index_first_literal_of_source_file+1] + CONFIG_FILE
    return CONFIG_FILE


def parse_arguments():
    parser = ArgumentParser(description='source for generate config file')
    parser.add_argument(
        '--source',
        help='source for generate config file',
        type=str,
        default=SOURCE_FILE,
        required=False)
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_arguments()
    generate_config_file(args.source)