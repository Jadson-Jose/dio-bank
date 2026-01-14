from http import HTTPStatus
from typing import Dict, cast

from src.controllers.utils import requires_role


def test_requires_role_success(mocker):
    # Given
    mock_role = mocker.Mock()
    mock_role.username = "admin"

    mock_user = mocker.Mock()
    mock_user.role = mock_role

    mocker.patch("src.controllers.utils.get_jwt_identity", return_value=1)
    mocker.patch("src.controllers.utils.db.get_or_404", return_value=mock_user)

    # When
    decorated_function = requires_role("admin")(lambda: "success")
    result = decorated_function()

    # Then
    assert result == "success"


def test_requires_role_fail(mocker):
    # Given
    mock_role = mocker.Mock()
    mock_role.username = "normal"

    mock_user = mocker.Mock()
    mock_user.role = mock_role

    mocker.patch("src.controllers.utils.get_jwt_identity", return_value=1)
    mocker.patch("src.controllers.utils.db.get_or_404", return_value=mock_user)

    # When
    decorated_function = requires_role("admin")(lambda: "success")
    result = decorated_function()

    body, status = result
    body = cast(Dict[str, str], body)

    # then
    assert body["message"] == "User do not have access."
    assert status == HTTPStatus.FORBIDDEN


# def test_eleva_quadrado_sucesso():
#     resultado = elevar_quadrado(2)
#     assert resultado == 2
