from src.services.auth import auth_service


def test_decode_and_encode_access_token():
    data = {"user_id": 1}
    jwt_token = auth_service.create_access_token(data)

    assert jwt_token
    assert isinstance(jwt_token, str)

    payload = auth_service.decode_jwt(jwt_token)
    assert payload
    assert payload["user_id"] == data["user_id"]
