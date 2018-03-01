# -*- coding: utf-8 -*-
import os
from argparse import ArgumentParser
from login import StepicAPILogin
from request import StepicApiRequest



clientId = ""
clientSecret = ""

client = StepicAPILogin(clientId, clientSecret)
lesson = "39228"

def import_all_choice_steps_in_folder(folder, step_number):
    names = os.listdir(folder)
    step = int(step_number)
    for name in names:
        fullname = os.path.join(folder, name)
        if os.path.isfile(fullname):

            StepicApiRequest(client).import_step(
                fullname,
                lesson,
                step
            )
            step += 1


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
    import_all_choice_steps_in_folder(args.source, args.step_number)
