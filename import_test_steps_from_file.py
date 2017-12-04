# -*- coding: utf-8 -*-
# Run with Python 3

import os
from argparse import ArgumentParser
from login import StepicAPILogin
from request import StepicApiRequest

import json
import requests

# Get your keys at https://stepic.org/oauth2/applications/ (client type = confidential, authorization grant type = client credentials)
clientId = ""
clientSecret = ""

client = StepicAPILogin(clientId, clientSecret)
lesson = ""



def parse_answers_options(answers_array):
    answers = []
    is_multiple_choice = False
    
    right_choice_count = 0
    rangeTo = len(answers_array)
    for i in range(rangeTo):
        is_correct = False
        text = answers_array[i]
        
        if (answers_array[i][0]=='+'):
            is_correct = True
            right_choice_count = right_choice_count + 1
            text = answers_array[i][1:]
            #print(answers_array[i][1:])    
            
        d = {'is_correct': is_correct, 'text': text, 'feedback': ''}
        
        answers.append(d)
    
    if (right_choice_count > 1):
        is_multiple_choice = True
    
    answers_data = {"answers": answers, "is_multiple_choice": is_multiple_choice}
    return answers_data
       
def upload_step(question, answers_array, position):

    api_url = 'https://stepic.org/api/step-sources'
    lesson_id  = lesson
        
    sample_size = len(answers_array)
    answers_data = parse_answers_options(answers_array)
    answers = answers_data["answers"]
    is_multiple_choice = answers_data["is_multiple_choice"]
    
    # https://github.com/npatyur/Stepik-API/blob/master/examples/create_content.py#L69 
	# 3.4. Add new multiple (single) choice step to this lesson

    data = {
        'stepSource': {
            'block': {
                'name': 'choice',
                'text': question,
                'source': {
                    'options': answers,
                    'is_always_correct': False,
                    'is_html_enabled': True,
                    'sample_size': sample_size,
                    'is_multiple_choice': is_multiple_choice,
                    'preserve_order': False,
                    'is_options_feedback': False
                }
            },
            'lesson': lesson_id,
            'position': position
        }
        
    }
    #print(data)
    r = StepicApiRequest(client).make_request('POST', api_url, json_data=data)
    #print(r.json())
    step_id = r.json()['step-sources'][0]['id']
    print('Step ID:', step_id)

    ###

    # Your lesson is ready!
    print('--> Check https://stepic.org/lesson/{}'.format(lesson_id))

    ###

def import_test_steps_from_file(file, start_position):
    handle = open(os.path.abspath(file), "r")
    data = handle.read()    
    handle.close()
    
    #Sample: 
    #question_string?;+correct_answer; uncorrect_answer; ...;
    #question_string?;uncorrect_answer; +correct_answer; ...;
    #question_string?;+correct_answer; +correct_answer; ...;
    #....;
	
    data_array = data.split(';')
    
    question = None
    answers = []
    position = start_position
    rangeTo = len(data_array) - 1
    for i in range(rangeTo):
        if (data_array[i][-1]=='?'):
            if (question != None):
                upload_step(question, answers, position)
            question = data_array[i]    
            answers = []
            position = position + 1
        else:
            answers.append(data_array[i])
        
        if(i == rangeTo - 1):
            upload_step(question, answers, position)        
    

def parse_arguments():
    parser = ArgumentParser(description='source for generate config file')
    parser.add_argument(
        '--source',
        help='file for uploading',
        type=str,
        required=True)
    parser.add_argument(
        '--position',
        help='start step number in lesson for uploading from',
        type=int,
        required=False,
        default="1"
    )
    parser.add_argument(
        '--lesson',
        help='lesson id',
        type=int,
        required=True,
    )
    
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_arguments()
    lesson = args.lesson
    import_test_steps_from_file(args.source, args.position)

