# -*- coding: utf-8 -*-
import os
from argparse import ArgumentParser
from login import StepicAPILogin
from request import StepicApiRequest



clientId = ""
clientSecret = ""

client = StepicAPILogin(clientId, clientSecret)
#lesson = "54019"

def import_all_course_from_folder(folder):
    dir = os.path.abspath(folder)
    for d, dirs, files in os.walk(dir):
        for f in files:
            #print(f)
            fullname = os.path.join(os.path.abspath(d),f)
            temp_array = f.split("_")
            lesson = int(temp_array[0])
            step = int(temp_array[1])
            #print(fullname)
            StepicApiRequest(client).import_step(
                fullname,
                lesson,
                step
            )
            

def parse_arguments():
    parser = ArgumentParser(description='source for generate config file')
    parser.add_argument(
        '--source',
        help='folder for uploading',
        type=str,
        required=True)
    parser.add_argument(
        '--step_number',
        help='step number, which we will use for first file in folder',
        type=str,
        required=False,
        default="1"
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_arguments()
    import_all_course_from_folder(args.source)
