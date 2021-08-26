import time
import asyncio
import logging
import requests
from requests import Response
from functools import wraps, partial
from http.client import OK, IM_USED, INTERNAL_SERVER_ERROR
from typing import Callable
from requests.exceptions import RequestException


logger = logging.getLogger(__name__)


def background(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        loop = asyncio.get_event_loop()
        return loop.run_in_executor(None, partial(func, *args, **kwargs))
    return wrapper


def retry_with_backoff_strategy(
    url: str,
    data: str,
    times: int = 3,
    backoff: int = 60) -> Response:
    '''
    Функция для выполнения POST запроса с опцией для перезапроса
    при определенных статусах ответа и ограниченным кол-вом попыток
    '''
    response = None
    while times > 0:
        try:
            response = requests.post(url=url, json=data)

            if OK <= response.status_code <= IM_USED:
                return response
        except RequestException as ex:
            logger.exception(ex)

        times -= 1
        time.sleep(backoff)
    else:
        if response:
            return response

        response = Response()
        response.status_code = INTERNAL_SERVER_ERROR
        return response


@background
def request_gateway_host(url: str, payload: dict, request_startegy: Callable = retry_with_backoff_strategy):
    response = request_startegy(url, data=payload)

    return response
