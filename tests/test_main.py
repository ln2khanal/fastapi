import pytest
from pathlib import Path
from app.main import app
from dotenv import load_dotenv
from httpx import ASGITransport, AsyncClient


def pytest_configure():
    load_dotenv()


client = AsyncClient(
    transport=ASGITransport(app=app), base_url="http://webserver/api/v1"
)


@pytest.mark.asyncio
async def test_read_root():
    response = await client.get("/")

    assert response.status_code == 200
    assert type(response.content) == bytes


@pytest.mark.asyncio
async def test_post_request_to_sales():

    response = await client.post("/crud/sales")

    assert response.status_code == 405


@pytest.mark.asyncio
async def test_non_existing_sales():

    response = await client.get("/crud/sales")

    assert response.status_code == 200
    response_json = response.json()
    assert response_json["data"] == [None]


@pytest.mark.asyncio
async def test_existing_sales():

    response = await client.get("/crud/sales")

    assert response.status_code == 200
    response_json = response.json()
    assert response_json["data"] == [None]


@pytest.mark.asyncio
async def test_unsuccessful_file_upload():

    file_name = "non_xlsx_file.txt"

    with open(file_name, "w") as f:
        f.write("I am not a xlsx/csv contet for sure.")

    with open(file_name, "rb") as file:
        response = await client.post(
            "/datasource/add",
            files={"datafile": (file_name, file, "text/plain")},
        )

    assert response.status_code == 400
    response_json = response.json()
    assert response_json["error"] == "Please upload a valid .xlsx file."


@pytest.mark.asyncio
async def test_successful_file_upload():
    file_path = Path(__file__).parent.parent
    file_name = "sampledata.xlsx"
    full_path = file_path / file_name
    with open(full_path, "rb") as file:
        response = await client.post(
            "/datasource/add",
            files={
                "datafile": (
                    file_name,
                    file,
                    "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                )
            },
        )

    assert response.status_code == 200
    response_json = response.json()

    assert response_json.get("context") == "File uploaded successfully"


# This test must have been passed. But following the errors, the timeout is causing errors.
# Using swagger apis, it's all good. Need to investigete it further.


@pytest.mark.asyncio
async def test_existing_sales():

    response = await client.get("/crud/sales")

    assert response.status_code == 200
    response_json = response.json()
    assert response_json["data"] == [153738]
