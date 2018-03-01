# -*- coding: utf-8 -*-

from login import StepicAPILogin
from request import StepicApiRequest
from argparse import ArgumentParser


class StepicAPI:
    def __init__(self):
        parser = self.parse_arguments()
        client = StepicAPILogin(parser.clientId, parser.clientSecret)

        if parser.importStep:
            if parser.lesson is None or parser.step is None or parser.stepSnapshotFile is None:
                raise RuntimeError('--lesson, --stepSnapshotFile and --step must be specified')
            StepicApiRequest(client).import_step(
                parser.stepSnapshotFile,
                parser.lesson,
                parser.step
            )
        if parser.uploadImages:
            if parser.images is None:
                raise RuntimeError('--images must be specified')
            StepicApiRequest(client).upload_images(parser.images)

    def parse_arguments(self):
        parser = ArgumentParser(description='stepic cli api parameters')
        parser.add_argument(
            '--clientId',
            help='oauth client id for stepic.org',
            type=str,
            required=True)
        parser.add_argument(
            '--clientSecret',
            help='oauth client secret for stepic.org',
            type=str,
            required=True)
        parser.add_argument(
            '--stepSnapshotFile',
            help='step snapshot file path to import',
            type=str,
            required=False)
        parser.add_argument(
            '--importStep',
            help='perform step import --stepSnapshotFile, --lesson and --step required',
            action='store_true',
            required=False)
        parser.add_argument(
            '--lesson',
            help='lesson id',
            type=int,
            required=False)
        parser.add_argument(
            '--step',
            help='step number (starting from 1)',
            type=int,
            required=False)
        parser.add_argument(
            '--uploadImages',
            help='perform upload images to stepic related server(uploadcare.com), --images required',
            action='store_true',
            required=False)
        parser.add_argument(
            '--images',
            help='paths to images (divided with coma). Example: \'--images path1,path2,...\'',
            type=str,
            required=False)
        return parser.parse_args()


if __name__ == "__main__":
    StepicAPI()
