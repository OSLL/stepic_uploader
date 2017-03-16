import json
from argparse import ArgumentParser
from step_generate_api.config_reader import getTextQuestionForChoiceStep, getIsAlwaysCorrectForChoiceStep, \
getPreserveOrderForChoiceStep, getSampleSizeForChoiceStep, getIsMultipleChoiceForChoiceStep, getAnswersForChoiceStep

BLOCK = "block"
NAME = "name"
TEXT = "text"
SOURCE = "source"
OPTIONS = "options"
IS_ALWAYS_CORRECT = "is_always_correct"
PRESERVE_ORDER = "preserve_order"
SAMPLE_SIZE = "sample_size"
IS_MULTIPLE_CHOICE = "is_multiple_choice"
CHOICE = "choice"
IS_HTML_ENABLED = "is_html_enabled"
IS_OPTIONS_FEEDBACK = "is_options_feedback"
TRUE = "true"
FALSE = "false"

FILE_NAME = "step"


def generate_step_json(config, number):
    step = {}
    block = {}
    source = {}
    question = getTextQuestionForChoiceStep(config, number)
    if question != '':
        source.update({IS_ALWAYS_CORRECT:getIsAlwaysCorrectForChoiceStep(config, number)})
        source.update({PRESERVE_ORDER:getPreserveOrderForChoiceStep(config, number)})
        source.update({SAMPLE_SIZE:getSampleSizeForChoiceStep(config, number)})
        source.update({IS_MULTIPLE_CHOICE:getIsMultipleChoiceForChoiceStep(config, number)})
        source.update({IS_HTML_ENABLED:TRUE})
        source.update({IS_OPTIONS_FEEDBACK:FALSE})
        source.update({OPTIONS:getAnswersForChoiceStep(config, number)})

        block.update({NAME:CHOICE})
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
        default='choice_steps',
        required=False)
    parser.add_argument(
        '--config',
        help='path to config ini file',
        type=str,
        default='choice_step_config.ini',
        required=False)
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_arguments()
    save_steps(args.config, args.output)
