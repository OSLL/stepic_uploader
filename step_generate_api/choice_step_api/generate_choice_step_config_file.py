from argparse import ArgumentParser


CONFIG_FILE = 'choice_step_config.ini'

SECTION_QUESTION_TEMPLATE = "[question_{}]\n" + \
"text={}\n"+ \
"is_always_correct=false\n"+ \
"preserve_order=false\n"+ \
"is_html_enabled=true\n" + \
"sample_size={}\n"+ \
"is_multiple_choice={}\n"

SECTION_OPTIONS_TEMPLATE = "[options_{}]\n"

SECTION_ANSWERS_TEMPLATE = "text={}\n"+ \
"is_correct={}\n"

def generate_config_file(source):
    sections = ""
    with open(source, "r") as source_file:
        for count, line in enumerate(source_file.readlines()):
            question = line.split(';')[0]
            answers = line.split(';')[1:]
            sections += generate_config_section_template(question, count, answers)
    config_file_name = get_config_name(source)
    with open(config_file_name, "w") as config_file:
        config_file.write(sections)


def generate_config_section_template(question, i, answers):
    SAMPLE_SIZE = len(answers)
    correct_answers = 0
    ANSWERS = ""
    for number, answer in enumerate(answers):
        OPTIONS = SECTION_OPTIONS_TEMPLATE.format(str(i+1) + str(number+1))
        if answer[0] == '_':
            correct_answers += 1
            ANSWER = SECTION_ANSWERS_TEMPLATE.format(answer[1:], "true")
        else:
            ANSWER = SECTION_ANSWERS_TEMPLATE.format(answer, "false")
        ANSWERS += OPTIONS + ANSWER

    if correct_answers > 1:
        IS_MULTIPLE_CHOICE = "true"
    else:
        IS_MULTIPLE_CHOICE = "false"

    QUESTION = SECTION_QUESTION_TEMPLATE.format(str(i+1), question, SAMPLE_SIZE, IS_MULTIPLE_CHOICE)
    return QUESTION + ANSWERS


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
        default='choice_step_api/choice_source.txt',
        required=False)
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_arguments()
    generate_config_file(args.source)