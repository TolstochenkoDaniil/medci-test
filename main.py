import os
from flask import Response

from src import create_app


app = create_app()


@app.route('/')
def index() -> Response:
    return Response(status=200)


if __name__ == '__main__':
    app.run(host=os.environ.get('HOST'), port=os.environ.get('PORT'))