import pytest


@pytest.mark.parametrize("email, password, status_code", [
    ("coto@mail.com", "1234", 200),
])
async def test_auth_flow(email: str, password: str, status_code, ac):

    # /register
    register_resp = await ac.post(
        url="/users/register",
        json={
            "email": email, 
            "password": password
        },
    )
    assert register_resp.status_code == status_code
    if status_code != 200:
        return
    

    # /login
    login_resp = await ac.post(
        url="/users/login",
        json={
            "email": email, 
            "password": password
        },
    )
    assert ac.cookies["access_token"]
    assert login_resp.status_code == status_code


    # /get_me
    me_resp = await ac.get(url="/users/get_me")
    assert me_resp.status_code == 200
    user = me_resp.json()
    assert user["email"] == email
    assert "password" not in user
    assert "hashed_password" not in user


    #/logout
    delete_resp = await ac.delete(url="/users/logout")
    assert delete_resp.status_code == status_code
    assert "access_token" not in ac.cookies