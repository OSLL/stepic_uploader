from argparse import ArgumentParser
from step_generate_api.config_reader import getTextQuestionForStringStep, getTextAnswerForStringStep
import json


BLOCK = "block"
NAME = "name"
TEXT = "text"
STRING = "string"
SOURCE = "source"
OPTIONS = "options"
PATTERN = "pattern"
MATCH_SUBSTR = "match_substring"
USE_RE = "use_re"
CASE_SENS = "case_sensitive"
FALSE = "false"


FILE_NAME = "step_string"


def generate_step_json(config, number):
    step = {}
    block = {}
    source = {}
    question = getTextQuestionForStringStep(config, number)
    if question != '':
        source.update({PATTERN:getTextAnswerForStringStep(config, number)})
        source.update({MATCH_SUBSTR:FALSE})
        source.update({USE_RE: FALSE})
        source.update({CASE_SENS:FALSE})

        block.update({NAME:STRING})
        block.update({TEXT:question})
        block.update({SOURCE:source})

        step.update({BLOCK:block})
        json_data = json.dumps(step)
        return json_data
    else:
        return ''


def save_steps(config, output_folder):
    i = 1
    while True:
        step = generate_step_json(config, i)
        if step == '':
            break
        with open(output_folder + '/' + FILE_NAME + "_" + str(i) + ".step", "w") as step_file:
            step_file.write(step)
        i += 1


def parse_arguments():
    parser = ArgumentParser(description='output folder for generated steps')
    parser.add_argument(
        '--output',
        help='output folder for steps',
        type=str,
        default='string_steps',
        required=False)
    parser.add_argument(
        '--config',
        help='path to config ini file',
        type=str,
        default='string_step_config.ini',
        required=False)
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_arguments()
    save_steps(args.config, args.output)
