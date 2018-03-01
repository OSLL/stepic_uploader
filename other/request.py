# -*- coding: utf-8 -*-

import json
import os


class StepicApiRequest:
    def __init__(self, stepic_api_login):
        self.stepic_api_login = stepic_api_login

    def make_request(self, method, url, data=None, json_data=None, files=None):
        kwargs = {
            'verify': False,
            'allow_redirects': True
        }
        if data is not None:
            kwargs['data'] = data
        if json_data is not None:
            kwargs['json'] = json_data
        if files is not None:
            files_payload = {}
            if type(files) is not dict:
                files = [files]
            for f in files:
                files_payload.update({os.path.basename(f): open(f, 'rb')})
            kwargs['files'] = files_payload
        self.stepic_api_login.client.headers.update({'Authorization': 'Bearer ' + self.stepic_api_login.token})
        return self.stepic_api_login.client.request(method, url, **kwargs)


    def import_step(self, path_to_step_file, lesson, step):
        lessons_info = self.make_request('GET', 'https://stepik.org/api/lessons/{}'.format(lesson)).json()
        step_id = None
        lesson = int(lesson)
        step = int(step)
        print(step)
        for lsn in lessons_info['lessons']:
            if lsn['id'] == lesson:
                if (step - 1) < len(lsn['steps']):
                    step_id = lsn['steps'][step - 1]
        if step_id is None:
            raise RuntimeError('Step {} not found for lesson {}'.format(step, lesson))
        template_payload = json.loads(
            '{"stepSource":{"block":{}, "lesson_id":"' + str(lesson) + '",' +
            '"position":' + str(step) + ',' +
            '"lesson":"' + str(lesson) + '"}}'
        )
        template_payload['stepSource']['block'] = \
            json.loads(open(os.path.abspath(path_to_step_file), 'r').read())['block']
        return self.make_request(
            'PUT',
            "https://stepik.org/api/step-sources/{}".format(step_id),
            None,
            template_payload
        )

    def upload_images(self, image_files):
        payload = {
            'UPLOADCARE_PUB_KEY': 'e7a075ad8dc9e3a1ec61',
            'UPLOADCARE_STORE': 'auto'
        }
        image_link_template = "https://ucarecdn.com/{}/-/crop/235x192/0,0/-/preview//"
        for image_file in image_files.split(','):
            response = self.make_request(
                'POST',
                'https://upload.uploadcare.com/base/?jsonerrors=1',
                payload,
                None,
                os.path.abspath(image_file.strip())
            )
            print(image_link_template.format(
                json.loads(response.text)[os.path.basename(image_file.strip())]
            ))
