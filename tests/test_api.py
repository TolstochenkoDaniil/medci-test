import pytest

from http.client import OK, BAD_REQUEST

import json


def test_index_api(client):
    response = client.get('/')

    assert response.status_code == OK


def test_send_message_api(client):
    response = client.post('/send_message', data=json.dumps(dict(message='foobar', gateway='gateway_1')))

    assert response.status_code == OK


def test_send_message_api_bad_request(client):
    response = client.post('/send_message', data=json.dumps(dict(gateway='gateway_1')))

    assert response.status_code == BAD_REQUEST
