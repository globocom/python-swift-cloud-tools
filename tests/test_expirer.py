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


class TestExpirer(TestCase):

    def setUp(self):
        self.sct_host = 'http://swift-cloud-tools-dev.gcloud.dev.globoi.com'
        self.sct_api_key = 'd003d7dc6e2a48e99aed5082160de1fa'

        self.client = SCTClient(
            self.sct_host,
            self.sct_api_key
        )

    @patch('swift_cloud_tools.client.requests.post')
    def test_expirer_create(self, mock_request):
        account = 'auth_792079638c6441bca02071501f4eb273'
        container = 'container'
        obj = 'object.jpeg'
        date = '2021-10-06 12:15:00'

        headers = {
            'Content-type': 'application/json',
            'X-Auth-Token': self.sct_api_key
        }

        data = {
            "account": account,
            "container": container,
            "object": obj,
            "date": date
        }

        status = 201
        content = "Expired object '{}/{}/{}' created".format(account, container, obj)

        mock = Mock()
        mock.content = content
        mock.status_code = status
        mock_request.return_value = mock

        response = self.client.expirer_create(account, container, obj, date)
        mock_request.assert_called_once_with(
            '{}/v1/expirer/'.format(self.sct_host),
            data=json.dumps(data),
            headers=headers
        )
        self.assertEqual(response.status_code, status)
        self.assertEqual(response.content, content)

    @patch('swift_cloud_tools.client.requests.post')
    def test_expirer_create_unauthenticated(self, mock_request):
        account = 'auth_792079638c6441bca02071501f4eb273'
        container = 'container'
        obj = 'object.jpeg'
        date = '2021-10-06 12:15:00'

        headers = {
            'Content-type': 'application/json',
            'X-Auth-Token': '123456789'
        }

        data = {
            "account": account,
            "container": container,
            "object": obj,
            "date": date
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

        response = client.expirer_create(account, container, obj, date)
        mock_request.assert_called_once_with(
            '{}/v1/expirer/'.format(self.sct_host),
            data=json.dumps(data),
            headers=headers
        )
        self.assertEqual(response.status_code, status)
        self.assertEqual(response.content, content)

    @patch('swift_cloud_tools.client.requests.post')
    def test_expirer_create_incorrect_parameters(self, mock_request):
        account = 'auth_792079638c6441bca02071501f4eb273'
        container = 'container'
        obj = 'object.jpeg'
        date = ''

        headers = {
            'Content-type': 'application/json',
            'X-Auth-Token': self.sct_api_key
        }

        data = {
            "account": account,
            "container": container,
            "object": obj,
            "date": ''
        }

        status = 422
        content = 'incorrect parameters'

        mock = Mock()
        mock.content = content
        mock.status_code = status
        mock_request.return_value = mock

        response = self.client.expirer_create(account, container, obj, date)
        mock_request.assert_called_once_with(
            '{}/v1/expirer/'.format(self.sct_host),
            data=json.dumps(data),
            headers=headers
        )
        self.assertEqual(response.status_code, status)
        self.assertEqual(response.content, content)

    @patch('swift_cloud_tools.client.requests.post')
    def test_expirer_create_invalid_date_format(self, mock_request):
        account = 'auth_792079638c6441bca02071501f4eb273'
        container = 'container'
        obj = 'object.jpeg'
        date = '2021-10-06'

        headers = {
            'Content-type': 'application/json',
            'X-Auth-Token': self.sct_api_key
        }

        data = {
            "account": account,
            "container": container,
            "object": obj,
            "date": '2021-10-06'
        }

        status = 422
        content = 'invalid date format: YYYY-MM-DD HH:MM:SS'

        mock = Mock()
        mock.content = content
        mock.status_code = status
        mock_request.return_value = mock

        response = self.client.expirer_create(account, container, obj, date)
        mock_request.assert_called_once_with(
            '{}/v1/expirer/'.format(self.sct_host),
            data=json.dumps(data),
            headers=headers
        )
        self.assertEqual(response.status_code, status)
        self.assertEqual(response.content, content)

    @patch('swift_cloud_tools.client.requests.delete')
    def test_expirer_delete(self, mock_request):
        account = 'auth_792079638c6441bca02071501f4eb273'
        container = 'container'
        obj = 'object.jpeg'

        headers = {
            'Content-type': 'application/json',
            'X-Auth-Token': self.sct_api_key
        }

        data = {
            "account": account,
            "container": container,
            "object": obj
        }

        status = 200
        content = "Expired object '{}/{}/{}' deleted".format(account, container, obj)

        mock = Mock()
        mock.content = content
        mock.status_code = status
        mock_request.return_value = mock

        response = self.client.expirer_delete(account, container, obj)
        mock_request.assert_called_once_with(
            '{}/v1/expirer/'.format(self.sct_host),
            data=json.dumps(data),
            headers=headers
        )
        self.assertEqual(response.status_code, status)
        self.assertEqual(response.content, content)

    @patch('swift_cloud_tools.client.requests.delete')
    def test_expirer_delete_incorrect_parameters(self, mock_request):
        account = 'auth_792079638c6441bca02071501f4eb273'
        container = 'container'
        obj = ''

        headers = {
            'Content-type': 'application/json',
            'X-Auth-Token': self.sct_api_key
        }

        data = {
            "account": account,
            "container": container,
            "object": obj
        }

        status = 422
        content = 'incorrect parameters'

        mock = Mock()
        mock.content = content
        mock.status_code = status
        mock_request.return_value = mock

        response = self.client.expirer_delete(account, container, obj)
        mock_request.assert_called_once_with(
            '{}/v1/expirer/'.format(self.sct_host),
            data=json.dumps(data),
            headers=headers
        )
        self.assertEqual(response.status_code, status)
        self.assertEqual(response.content, content)

    @patch('swift_cloud_tools.client.requests.delete')
    def test_expirer_delete_not_found(self, mock_request):
        account = 'auth_792079638c6441bca02071501f4eb273'
        container = 'container'
        obj = 'object.jpeg'

        headers = {
            'Content-type': 'application/json',
            'X-Auth-Token': self.sct_api_key
        }

        data = {
            "account": account,
            "container": container,
            "object": obj
        }

        status = 404
        content = 'not found'

        mock = Mock()
        mock.content = content
        mock.status_code = status
        mock_request.return_value = mock

        response = self.client.expirer_delete(account, container, obj)
        mock_request.assert_called_once_with(
            '{}/v1/expirer/'.format(self.sct_host),
            data=json.dumps(data),
            headers=headers
        )
        self.assertEqual(response.status_code, status)
        self.assertEqual(response.content, content)
