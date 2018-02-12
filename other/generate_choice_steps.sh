#!/usr/bin/env bash

OUTPUT_FOLDER='choice_steps'
CONFIG='step_generate_api/choice_step_api/choice_step_config.ini'
SOURCE_FILE='step_generate_api/choice_step_api/choice_source.txt'

mkdir $OUTPUT_FOLDER

python step_generate_api/choice_step_api/generate_choice_step_config_file.py --source $SOURCE_FILE
python step_generate_api/choice_step_api/generate_choice_steps_json.py --output $OUTPUT_FOLDER --config $CONFIG

sed -i 's/\"false\"/false/g' $OUTPUT_FOLDER/*.step
sed -i 's/\"true\"/true/g' $OUTPUT_FOLDER/*.step