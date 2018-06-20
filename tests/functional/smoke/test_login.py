from typing import Dict
import pytest
from server.api.requests import Request
from server.api.responses import Response

_zero: int = 0


@pytest.mark.smoke
def test_login_page_url(login_url_response: Response, success: int) -> None:
    assert login_url_response.status_code() == success


@pytest.mark.smoke
def test_login_page_content(login_url_response: Response) -> None:
    assert len(login_url_response.content()) > _zero


@pytest.mark.smoke
def test_login_user(login_user_request: Request, success: int) -> None:
    data: Dict[str, str] = {"email": "admin@blog.com",
                            "password": "password",
                            "submit": "Login"}

    assert login_user_request.response(data=data).status_code() == success
