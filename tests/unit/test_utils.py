# tests/unit/test_utils.py - Versão corrigida
from http import HTTPStatus

from src.controllers.utils import requires_role


def test_requires_role_success(mocker):
    """Testa o decorator requires_role com role correta."""
    # Given
    mock_role = mocker.Mock()
    mock_role.name = "admin"  # CORREÇÃO: 'name' em vez de 'username'

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
    """Testa o decorator requires_role com role incorreta."""
    # Given
    mock_role = mocker.Mock()
    mock_role.name = "normal"  # CORREÇÃO: 'name' em vez de 'username'

    mock_user = mocker.Mock()
    mock_user.role = mock_role

    mocker.patch("src.controllers.utils.get_jwt_identity", return_value=1)
    mocker.patch("src.controllers.utils.db.get_or_404", return_value=mock_user)

    # When
    decorated_function = requires_role("admin")(lambda: "success")
    result = decorated_function()

    # Then
    assert result == ({"msg": "Access forbidden"}, HTTPStatus.FORBIDDEN)
