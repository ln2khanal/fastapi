import pytest
from pathlib import Path
from app.main import app
from dotenv import load_dotenv
from fastapi.testclient import TestClient


def pytest_configure():
    load_dotenv()


client = TestClient(app)


def test_read_root():
    response = client.get("/")

    assert response.status_code == 200
    assert type(response.content) == bytes


def test_post_request_to_sales():

    response = client.post("/sales")

    assert response.status_code == 405


def test_non_existing_sales():

    response = client.get("/sales")

    assert response.status_code == 200
    response_json = response.json()
    assert response_json["data"] == [None]


def test_existing_sales():

    response = client.get("/sales")

    assert response.status_code == 200
    response_json = response.json()
    assert response_json["data"] == [None]


def test_unsuccessful_file_upload():

    file_name = "non_xlsx_file.txt"

    with open(file_name, "w") as f:
        f.write("I am not a xlsx/csv contet for sure.")

    with open(file_name, "rb") as file:
        response = client.post(
            "/api/v1/datasource/add",
            files={"datafile": (file_name, file, "text/plain")},
        )

    assert response.status_code == 400
    response_json = response.json()
    assert response_json["error"] == "Please upload a valid .xlsx file."


# To the best of my knowledge, the xlsx file reading and attaching it causing some issues
# Using swagger apis, it's all good. I will investigete it further.
def test_successful_file_upload():
    file_path = Path(__file__)

    file_name = "sampledata.xlsx"
    with open(f"{file_path.parent.parent}/{file_name}", "rb") as file:
        response = client.post(
            "/api/v1/datasource/add",
            files={"datafile": (file_name, file, "text/plain")},
        )

    assert response.status_code == 200
    response_json = response.json()

    assert response_json["context"] == "File uploaded successfully"


# This test must have been passed. But following the errors, the timeout is causing errors.
# Using swagger apis, it's all good. Need to investigete it further.
def test_existing_sales():

    response = client.get("/sales")

    assert response.status_code == 200
    response_json = response.json()
    assert response_json["data"] == [153738]
