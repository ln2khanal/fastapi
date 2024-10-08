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
async def test_post_any_sales_should_return_method_not_allowed():

    response = await client.post("/crud/sales")

    assert response.status_code == 405


@pytest.mark.asyncio
async def test_get_sales_should_return_null_value():

    response = await client.get("/crud/sales")

    assert response.status_code == 200
    response_json = response.json()
    assert response_json["data"] == [None]


@pytest.mark.asyncio
async def test_get_sales_after_file_upload_should_return_valid_sales_value():
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

    response = await client.get("/crud/sales")

    assert response.status_code == 200
    response_json = response.json()
    assert response_json["data"][0] > 0
