import os

from flask import Flask, Response
from flask_restful import Api
from dotenv import load_dotenv

from src.api import SendMsgAPI, DummyAPI


load_dotenv()


def create_app(test_config=None):
    app = Flask(__name__)
    app.config['DEBUG'] = os.environ.get('DEBUG')

    api = Api(app)
    api.add_resource(SendMsgAPI, '/send_message', endpoint='send')

    for i, endpoint in enumerate(os.environ.get('ENDPOINTS').split(' ')):
        api.add_resource(DummyAPI, f'/{endpoint}', endpoint=f'dummy_{i}')

    return app
