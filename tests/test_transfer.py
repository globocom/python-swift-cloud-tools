# Copyright 2021 Grupo Globo
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import json

from unittest import TestCase
from unittest.mock import Mock, MagicMock, patch

from swift_cloud_tools.client import SCTClient


class TestTransfer(TestCase):

    def setUp(self):
        self.sct_host = 'http://swift-cloud-tools-dev.gcloud.dev.globoi.com'
        self.sct_api_key = 'd003d7dc6e2a48e99aed5082160de1fa'

        self.client = SCTClient(
            self.sct_host,
            self.sct_api_key
        )

    @patch('swift_cloud_tools.client.requests.post')
    def test_transfer_create(self, mock_request):
        project_id = '64b10d56454c4b1eb91b46b62d27c8b2'
        project_name = 'alan'
        environment = 'dev'

        headers = {
            'Content-type': 'application/json',
            'X-Auth-Token': self.sct_api_key
        }

        data = {
            "project_id": project_id,
            "project_name": project_name,
            "environment": environment
        }

        status = 201
        content = "Transfer project '{}' environment '{}' created".format(project_name, environment)

        mock = Mock()
        mock.content = content
        mock.status_code = status
        mock_request.return_value = mock

        response = self.client.transfer_create(project_id, project_name, environment)
        mock_request.assert_called_once_with(
            '{}/v1/transfer/'.format(self.sct_host),
            data=json.dumps(data),
            headers=headers
        )
        self.assertEqual(response.status_code, status)
        self.assertEqual(response.content, content)

    @patch('swift_cloud_tools.client.requests.post')
    def test_transfer_create_unauthenticated(self, mock_request):
        project_id = '64b10d56454c4b1eb91b46b62d27c8b2'
        project_name = 'alan'
        environment = 'dev'

        headers = {
            'Content-type': 'application/json',
            'X-Auth-Token': '123456789'
        }

        data = {
            "project_id": project_id,
            "project_name": project_name,
            "environment": environment
        }

        status = 401
        content = 'Unauthenticated'

        mock = Mock()
        mock.content = content
        mock.status_code = status
        mock_request.return_value = mock

        client = SCTClient(
            self.sct_host,
            '123456789'
        )

        response = client.transfer_create(project_id, project_name, environment)
        mock_request.assert_called_once_with(
            '{}/v1/transfer/'.format(self.sct_host),
            data=json.dumps(data),
            headers=headers
        )
        self.assertEqual(response.status_code, status)
        self.assertEqual(response.content, content)

    @patch('swift_cloud_tools.client.requests.post')
    def test_transfer_create_incorrect_parameters(self, mock_request):
        project_id = '64b10d56454c4b1eb91b46b62d27c8b2'
        project_name = 'alan'
        environment = ''

        headers = {
            'Content-type': 'application/json',
            'X-Auth-Token': self.sct_api_key
        }

        data = {
            "project_id": project_id,
            "project_name": project_name,
            "environment": environment
        }

        status = 422
        content = 'incorrect parameters'

        mock = Mock()
        mock.content = content
        mock.status_code = status
        mock_request.return_value = mock

        response = self.client.transfer_create(project_id, project_name, environment)
        mock_request.assert_called_once_with(
            '{}/v1/transfer/'.format(self.sct_host),
            data=json.dumps(data),
            headers=headers
        )
        self.assertEqual(response.status_code, status)
        self.assertEqual(response.content, content)

    @patch('swift_cloud_tools.client.requests.get')
    def test_transfer_get(self, mock_request):
        project_id = '64b10d56454c4b1eb91b46b62d27c8b2'
        project_name = 'alan'
        environment = 'dev'

        headers = {
            'Content-type': 'application/json',
            'X-Auth-Token': self.sct_api_key
        }

        status = 200
        content = {
            'id': 22,
            'project_id': project_id,
            'project_name': project_name,
            'environment': environment,
            'container_count_swift': 0,
            'object_count_swift': 0,
            'bytes_used_swift': 0,
            'last_object': '',
            'count_error': 0,
            'container_count_gcp': 0,
            'object_count_gcp': 0,
            'bytes_used_gcp': 0,
            'initial_date': '2021-10-07 11:05:00',
            'final_date': '2021-10-07 11:29:00'
        }

        mock = Mock()
        mock.json = content
        mock.status_code = status
        mock_request.return_value = mock

        response = self.client.transfer_get(project_id)
        mock_request.assert_called_once_with(
            '{}/v1/transfer/{}'.format(self.sct_host, project_id),
            headers=headers
        )
        self.assertEqual(response.status_code, status)
        self.assertEqual(response.json, content)

    @patch('swift_cloud_tools.client.requests.get')
    def test_transfer_get_unauthenticated(self, mock_request):
        project_id = '64b10d56454c4b1eb91b46b62d27c8b2'

        headers = {
            'Content-type': 'application/json',
            'X-Auth-Token': self.sct_api_key
        }

        status = 401
        content = 'Unauthenticated'

        mock = Mock()
        mock.content = content
        mock.status_code = status
        mock_request.return_value = mock

        response = self.client.transfer_get(project_id)
        mock_request.assert_called_once_with(
            '{}/v1/transfer/{}'.format(self.sct_host, project_id),
            headers=headers
        )
        self.assertEqual(response.status_code, status)
        self.assertEqual(response.content, content)

    @patch('swift_cloud_tools.client.requests.get')
    def test_transfer_get_not_found(self, mock_request):
        project_id = '64b10d56454c4b1eb91b46b62d27c8b2'

        headers = {
            'Content-type': 'application/json',
            'X-Auth-Token': self.sct_api_key
        }

        status = 404
        content = '<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 3.2 Final//EN">\n<title>404 Not Found</title>\n<h1>Not Found</h1>\n<p>The requested URL was not found on the server.  If you entered the URL manually please check your spelling and try again.</p>\n'

        mock = Mock()
        mock.content = content
        mock.status_code = status
        mock_request.return_value = mock

        response = self.client.transfer_get(project_id)
        mock_request.assert_called_once_with(
            '{}/v1/transfer/{}'.format(self.sct_host, project_id),
            headers=headers
        )
        self.assertEqual(response.status_code, status)
        self.assertEqual(response.content, content)

    @patch('swift_cloud_tools.client.requests.get')
    def test_transfer_status_uninitialized(self, mock_request):
        project_id = '64b10d56454c4b1eb91b46b62d27c8b_'

        headers = {
            'Content-type': 'application/json',
            'X-Auth-Token': self.sct_api_key
        }

        status = 200
        content = {'status': 'Migração não inicializada'}

        mock = Mock()
        mock.json = content
        mock.status_code = status
        mock_request.return_value = mock

        response = self.client.transfer_status(project_id)
        mock_request.assert_called_once_with(
            '{}/v1/transfer/status/{}'.format(self.sct_host, project_id),
            headers=headers
        )
        self.assertEqual(response.status_code, status)
        self.assertEqual(response.json, content)

    @patch('swift_cloud_tools.client.requests.get')
    def test_transfer_status_completed(self, mock_request):
        project_id = '64b10d56454c4b1eb91b46b62d27c8b2'

        headers = {
            'Content-type': 'application/json',
            'X-Auth-Token': self.sct_api_key
        }

        status = 200
        content = {'status': 'Migração concluída'}

        mock = Mock()
        mock.json = content
        mock.status_code = status
        mock_request.return_value = mock

        response = self.client.transfer_status(project_id)
        mock_request.assert_called_once_with(
            '{}/v1/transfer/status/{}'.format(self.sct_host, project_id),
            headers=headers
        )
        self.assertEqual(response.status_code, status)
        self.assertEqual(response.json, content)

    @patch('swift_cloud_tools.client.requests.get')
    def test_transfer_status_waiting(self, mock_request):
        project_id = '64b10d56454c4b1eb91b46b62d27c8b2'

        headers = {
            'Content-type': 'application/json',
            'X-Auth-Token': self.sct_api_key
        }

        status = 200
        content = {'status': 'Aguardando migração'}

        mock = Mock()
        mock.json = content
        mock.status_code = status
        mock_request.return_value = mock

        response = self.client.transfer_status(project_id)
        mock_request.assert_called_once_with(
            '{}/v1/transfer/status/{}'.format(self.sct_host, project_id),
            headers=headers
        )
        self.assertEqual(response.status_code, status)
        self.assertEqual(response.json, content)

    @patch('swift_cloud_tools.client.requests.get')
    def test_transfer_status_progress(self, mock_request):
        project_id = '64b10d56454c4b1eb91b46b62d27c8b2'

        headers = {
            'Content-type': 'application/json',
            'X-Auth-Token': self.sct_api_key
        }

        status = 200
        content = {'status': 'Migrando', 'progress': 93}

        mock = Mock()
        mock.json = content
        mock.status_code = status
        mock_request.return_value = mock

        response = self.client.transfer_status(project_id)
        mock_request.assert_called_once_with(
            '{}/v1/transfer/status/{}'.format(self.sct_host, project_id),
            headers=headers
        )
        self.assertEqual(response.status_code, status)
        self.assertEqual(response.json, content)

    @patch('swift_cloud_tools.client.requests.get')
    def test_transfer_status_all(self, mock_request):
        project_id = '64b10d56454c4b1eb91b46b62d27c8b2'
        project_name = 'alan'
        environment = 'dev'
        page = 1
        per_page = 50

        headers = {
            'Content-type': 'application/json',
            'X-Auth-Token': self.sct_api_key
        }

        status = 200
        content = {
            "page": page,
            "per_page": per_page,
            "pages": 0,
            "total": 0,
            "items": [
                {
                    'id': 22,
                    'project_id': project_id,
                    'project_name': project_name,
                    'environment': environment,
                    'container_count_swift': 0,
                    'object_count_swift': 0,
                    'bytes_used_swift': 0,
                    'last_object': '',
                    'count_error': 0,
                    'container_count_gcp': 0,
                    'object_count_gcp': 0,
                    'bytes_used_gcp': 0,
                    'initial_date': '2021-10-07 11:05:00',
                    'final_date': '2021-10-07 11:29:00'
                }
            ]
        }

        mock = Mock()
        mock.json = content
        mock.status_code = status
        mock_request.return_value = mock

        response = self.client.transfer_status_all(page, per_page)
        mock_request.assert_called_once_with(
            '{}/v1/transfer/status?page={}&per_page={}'.format(self.sct_host, page, per_page),
            headers=headers
        )
        self.assertEqual(response.status_code, status)
        self.assertEqual(response.json, content)

    @patch('swift_cloud_tools.client.requests.post')
    def test_transfer_status_by_projects(self, mock_request):
        project_id = '64b10d56454c4b1eb91b46b62d27c8b2'
        project_name = 'alan'
        environment = 'dev'

        headers = {
            'Content-type': 'application/json',
            'X-Auth-Token': self.sct_api_key
        }

        status = 200
        content = [
            {
                'id': 22,
                'project_id': project_id,
                'project_name': project_name,
                'environment': environment,
                'container_count_swift': 0,
                'object_count_swift': 0,
                'bytes_used_swift': 0,
                'last_object': '',
                'count_error': 0,
                'container_count_gcp': 0,
                'object_count_gcp': 0,
                'bytes_used_gcp': 0,
                'initial_date': '2021-10-07 11:05:00',
                'final_date': '2021-10-07 11:29:00'
            }
        ]

        mock = Mock()
        mock.json = content
        mock.status_code = status
        mock_request.return_value = mock
        project_ids = [project_id]

        response = self.client.transfer_status_by_projects(project_ids)
        mock_request.assert_called_once_with(
            '{}/v1/transfer/status'.format(self.sct_host),
            data=json.dumps(project_ids),
            headers=headers
        )
        self.assertEqual(response.status_code, status)
        self.assertEqual(response.json, content)
