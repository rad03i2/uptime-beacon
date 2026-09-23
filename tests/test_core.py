import io
import urllib.error
from unittest.mock import patch
import pytest
from uptime_beacon.core import check_url, validate_url

class Response:
    status = 204
    def __enter__(self): return self
    def __exit__(self, *args): return False

def test_validate_url():
    assert validate_url("https://example.com/a") == "https://example.com/a"

@pytest.mark.parametrize("url", ["example.com", "ftp://example.com", "https://u:p@example.com"])
def test_rejects_unsafe_or_invalid_urls(url):
    with pytest.raises(ValueError): validate_url(url)

def test_success_result():
    with patch("urllib.request.urlopen", return_value=Response()):
        result = check_url("https://example.com", slow_ms=999999)
    assert result.ok and result.status == 204 and not result.slow

def test_http_error_is_down():
    err = urllib.error.HTTPError("https://example.com", 503, "Unavailable", {}, io.BytesIO())
    with patch("urllib.request.urlopen", side_effect=err):
        result = check_url("https://example.com")
    assert not result.ok and result.status == 503 and result.error == "HTTP 503"

def test_network_error_is_down():
    with patch("urllib.request.urlopen", side_effect=urllib.error.URLError("offline")):
        result = check_url("https://example.com")
    assert not result.ok and result.status is None and "offline" in result.error

def test_options_validation():
    with pytest.raises(ValueError): check_url("https://example.com", timeout=0)
    with pytest.raises(ValueError): check_url("https://example.com", method="POST")
