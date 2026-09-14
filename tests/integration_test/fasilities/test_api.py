# тест апи на получение fasilities
async def test_get_fasilities(ac):
    response = await ac.get(
        "/fasilities",
    )
    print(f"{response.json()=}")

    assert response.status_code == 200


# тест апи на создание fasilitie
async def test_post_fasilities(ac):
    response = await ac.post(url="/fasilities", json={"title": "Хороший туалет"})
    assert response.status_code == 200
