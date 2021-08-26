import json
import pytest

import time
from http.client import OK

from src.utils import retry_with_backoff_strategy, request_gateway_host


@pytest.mark.parametrize(
    'times, backoff', [
        (3, 3)
    ]
)
def test_retry_strategy_with_bad_gateway(times, backoff):
    start_time = time.time()
    response = retry_with_backoff_strategy(
        'http://127.0.0.1/bad_gateway',
        {'message': 'bar'},
        times=times,
        backoff=backoff
    )
    end_time = time.time()

    assert (times-1)*backoff < end_time - start_time


@pytest.mark.asyncio
async def test_request_gateway_host(client):
    response = request_gateway_host('/gateway_1', json.dumps({"message":"test"}), request_startegy=client.post)

    await response

    assert response.done() == True
    assert response.result().status_code == OK
