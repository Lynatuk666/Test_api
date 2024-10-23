import pytest
from fastapi.testclient import TestClient
from app import app
from database_scripts import insert_data, create_db

client = TestClient(app)

testdata_1 = [(1, 200), (2, 200), (500, 400), ("333", 400), ("one", 400), (-1, 400)]
testdata_2 = [(1, "DEPOSIT", 1000, 200),
              (1, "WITHDRAW", 1000, 200),
              (1, "WITHDRAW", 100000, 103),
              (55, "DEPOSIT", 1, 400),
              (-1, "DEPOSIT", 1, 400),
              ("one", "DEPOSIT", 1, 400),
              ("55", "DEPOSIT", 1, 400)]


@pytest.mark.parametrize("uid, expected", testdata_1)
def test_get(uid, expected):
    response = client.get(f"/api/v1/wallets/{uid}")
    assert response.status_code == 200
    assert response.json()[1] == expected


@pytest.mark.parametrize("uid, operation_type, amount, expected", testdata_2)
def test_post(uid, operation_type, amount, expected):
    response = client.post(f"/api/v1/wallets/{uid}/operation",
                           json={"operationType": operation_type,
                                 "amount": amount})
    assert response.status_code == 200
    assert response.json()[1] == expected


some_data = [
    (1, 100),
    (2,),
    (378787, 800000)
]


if __name__ == '__main__':
    create_db()
    insert_data(some_data)
    test_get()
    test_post()