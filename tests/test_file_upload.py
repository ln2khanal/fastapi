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
