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
async def test_post_family_method_should_not_allow():

    response = await client.post("/crud/family")

    assert (
        response.status_code == 422
    )  # post to /crud/family url requires mandatory parameters


@pytest.mark.asyncio
async def test_get_family_shoul_return_a_valid_dict():

    response = await client.get("/crud/family")

    assert response.status_code == 200
    response_json = response.json()
    assert type(response_json["data"]) is dict


@pytest.mark.asyncio
async def test_get_family_should_upload_file_and_return_valid_product_family():
    file_path = Path(__file__).parent.parent
    file_name = "sampledata.xlsx"
    full_path = file_path / file_name

    with open(full_path, "rb") as file:
        await client.post(
            "/datasource/add",
            files={
                "datafile": (
                    file_name,
                    file,
                    "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                )
            },
        )

    response = await client.get("/crud/family")

    assert response.status_code == 200
    response_json = response.json()
    assert type(response_json["data"]) is dict
