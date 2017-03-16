from configparser import SafeConfigParser, NoSectionError

import os
CHOICE_STEP_CONFIG_PATH = os.path.dirname(os.path.realpath(__file__)) + "/step_generate_api/choice_step_config.ini"
STRING_STEP_CONFIG_PATH = os.path.dirname(os.path.realpath(__file__)) + "/step_generate_api/string_step_config.ini"

SECTION_QUESTION = "question_"
OPTION_TEXT = "text"
OPTION_IS_ALWAYS_CORRECT = "is_always_correct"
OPTION_PRESERVE_ORDER = "preserve_order"
OPTION_SAMPLE_SIZE = "sample_size"
OPTION_IS_MULTIPLE_CHOICE = "is_multiple_choice"
OPTION_NAME = "name"
OPTION_PATTERN = "pattern"
OPTION_FEEDBACK = "feedback"

TEXT = ""
IS_ALWAYS_CORRECT = "false"
PRESERVE_ORDER = "false"
SAMPLE_SIZE = 3
IS_MULTIPLE_CHOICE = "false"

SECTION_OPTION = "options_"
OPTION_TEXT_ANSWER = "text"
OPTION_IS_CORRECT = "is_correct"
TEXT_ANSWER = ""
IS_CORRECT = "false"
STRING = "string"


def getConfigParserForChoiceConfig(config_file):
    config = SafeConfigParser({OPTION_TEXT: TEXT,
                               OPTION_IS_ALWAYS_CORRECT: IS_ALWAYS_CORRECT,
                               OPTION_PRESERVE_ORDER: PRESERVE_ORDER,
                               OPTION_SAMPLE_SIZE: SAMPLE_SIZE,
                               OPTION_IS_MULTIPLE_CHOICE: IS_MULTIPLE_CHOICE,
                               OPTION_TEXT_ANSWER: TEXT_ANSWER,
                               OPTION_IS_CORRECT: IS_CORRECT,
                               })
    config.read(config_file)
    return config


def getConfigParserForStringConfig(config_file):
    config = SafeConfigParser({OPTION_TEXT: TEXT,
                               OPTION_NAME: STRING,
                               OPTION_PATTERN: TEXT_ANSWER,
                               })
    config.read(config_file)
    return config


def getTextQuestionForChoiceStep(config_file, question_number):
    try:
        question = unicode(getConfigParserForChoiceConfig(config_file).get(SECTION_QUESTION + str(question_number), OPTION_TEXT))
    except NoSectionError:
        return ''
    return question


def getTextQuestionForStringStep(config_file, question_number):
    try:
        question = unicode(getConfigParserForStringConfig(config_file).get(SECTION_QUESTION + str(question_number), OPTION_TEXT))
    except NoSectionError:
        return ''
    return question


def getIsAlwaysCorrectForChoiceStep(config_file, question_number):
    return unicode(getConfigParserForChoiceConfig(config_file).get(SECTION_QUESTION + str(question_number), OPTION_IS_ALWAYS_CORRECT))


def getPreserveOrderForChoiceStep(config_file, question_number):
    return unicode(getConfigParserForChoiceConfig(config_file).get(SECTION_QUESTION + str(question_number), OPTION_PRESERVE_ORDER))


def getSampleSizeForChoiceStep(config_file, question_number):
    return getConfigParserForChoiceConfig(config_file).get(SECTION_QUESTION + str(question_number), OPTION_SAMPLE_SIZE)


def getIsMultipleChoiceForChoiceStep(config_file, question_number):
    return unicode(getConfigParserForChoiceConfig(config_file).get(SECTION_QUESTION + str(question_number), OPTION_IS_MULTIPLE_CHOICE))


def getAnswersForChoiceStep(config_file, question_number):
    sample_size = int(getSampleSizeForChoiceStep(config_file, question_number))
    answers = []
    for i in range(1, sample_size+1):
        answer_text = unicode(getConfigParserForChoiceConfig(config_file).get(SECTION_OPTION + str(question_number) + str(i), OPTION_TEXT_ANSWER))
        answers_is_correct = unicode(getConfigParserForChoiceConfig(config_file).get(SECTION_OPTION + str(question_number) + str(i), OPTION_IS_CORRECT))
        answers.append({OPTION_TEXT_ANSWER:answer_text, OPTION_IS_CORRECT:answers_is_correct, OPTION_FEEDBACK:""})
    return answers


def getTextAnswerForStringStep(config_file, question_number):
    try:
        answer = unicode(getConfigParserForStringConfig(config_file).get(SECTION_QUESTION + str(question_number), OPTION_PATTERN))
    except NoSectionError:
        return ''
    return answer
