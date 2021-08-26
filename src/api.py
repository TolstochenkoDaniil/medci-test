from http.client import OK
import os

from flask import request, Response
from flask_restful import Resource, reqparse

from src.utils import request_gateway_host


class SendMsgAPI(Resource):
    def __init__(self) -> None:
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('message', type = str, location = 'json', required=True)
        self.reqparse.add_argument('gateway', type = str, location = 'json', required=True)

        super().__init__()

    def post(self) -> Response:
        request.get_json(force=True)
        payload = self.reqparse.parse_args()
        url=''.join((os.environ.get('GATEWAY_URL'), payload.get('gateway')))

        request_gateway_host(url, dict(message=payload.get('message')))

        return Response(status=OK)


class DummyAPI(Resource):
    def __init__(self) -> None:
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('msg', type = str, location = 'json', required=True)

        super().__init__()

    def post(self) -> Response:
        return Response(status=OK)
