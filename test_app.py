import pytest
from src.app import app
from src.process_query import process_query


def test_knows_about_dinosaurs():
    expected = "Dinosaurs ruled the Earth 200 million years ago"
    assert process_query("dinosaurs") == expected


def test_does_not_know_about_asteroids():
    assert process_query("asteroids") == "Unknown"


def test_what_is_your_name():
    assert process_query("What is your name?") == "SiCi"


@pytest.fixture
def client():
    with app.test_client() as client:
        yield client


def test_hello_world(client):
    response = client.get("/")
    assert response.status_code == 200


def test_submit_happy(client):
    response = client.post("/submit", data={
        "name": "Alice",
        "age": "30",
        "gender": "female",
        "happy": "5"
    })
    assert response.status_code == 200
    assert b"Hello Alice" in response.data


def test_submit_sad(client):
    response = client.post("/submit", data={
        "name": "Bob",
        "age": "25",
        "gender": "male",
        "happy": "-1"
    })
    assert response.status_code == 200
    assert b"Hello Bob" in response.data


def test_query(client):
    response = client.get("/query", query_string={"q": "dinosaurs"})
    assert response.status_code == 200
    assert b"Dinosaurs ruled the Earth 200 million years ago" in response.data


def test_query_unknown(client):
    response = client.get("/query", query_string={"q": "asteroid"})
    assert response.status_code == 200
    assert b"Unknown" in response.data
