import pytest
from requests import get, head, options, post, delete, put, patch
import re
import datetime

ENDPOINT_URL = "https://api.chucknorris.io/jokes/categories"
EXPECTED_RESPONSE_BODY = ["animal","career","celebrity","dev","explicit","fashion","food","history","money","movie",
                             "music","political","religion","science","sport","travel"]


def test_response_headers():
    response = get(ENDPOINT_URL)
    expected_date_time = datetime.datetime.utcnow().strftime("%a, %d %b %Y %H:%M")

    if response.headers['Content-Type'] != 'application/json;charset=UTF-8':
        pytest.fail("Wrong Content-Type", pytrace=True)
    elif response.headers['Connection'] != 'keep-alive':
        pytest.fail("Wrong Connection", pytrace=True)
    elif not re.match(f"{expected_date_time}:[0-5][0-9] GMT", response.headers['Date']):
        pytest.fail("Wrong Date", pytrace=True)
    else:
        assert True


def test_response_body():
    response = get(ENDPOINT_URL)
    response_body = response.json()
    assert response_body == EXPECTED_RESPONSE_BODY


def test_http_redirect():
    http_url = re.sub('https://', 'http://', ENDPOINT_URL)
    response = get(http_url)
    redirect_from_http = response.history[0]
    assert response.status_code == 200 and redirect_from_http.status_code == 301


def test_404():
    nonexistent_url = ENDPOINT_URL + '/0'
    response = get(nonexistent_url)
    assert response.status_code == 404


def test_supported_get():
    response = get(ENDPOINT_URL)
    assert response.status_code == 200


def test_supported_head():
    response = head(ENDPOINT_URL)
    assert response.status_code == 200


def test_supported_options():
    response = options(ENDPOINT_URL)
    assert response.status_code == 200


def test_unsupported_post():
    response = post(ENDPOINT_URL)
    assert response.status_code == 405


def test_unsupported_put():
    response = put(ENDPOINT_URL)
    assert response.status_code == 405


def test_unsupported_patch():
    response = patch(ENDPOINT_URL)
    assert response.status_code == 405


def test_unsupported_delete():
    response = delete(ENDPOINT_URL)
    assert response.status_code == 405



