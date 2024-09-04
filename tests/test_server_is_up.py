import pytest
from app.main import app
from dotenv import load_dotenv
from httpx import ASGITransport, AsyncClient, HTTPStatusError


def pytest_configure():
    load_dotenv()


client = AsyncClient(transport=ASGITransport(app=app), base_url="http://webserver")


@pytest.mark.asyncio
async def test_read_root():
    try:
        response = await client.get(url="/")

        if response.status_code == 307:
            redirect_url = response.headers.get("Location")
            if redirect_url:
                print(redirect_url)
                response = await client.get(redirect_url)

        assert response.status_code == 200
        assert type(response.content) == bytes

    except HTTPStatusError as e:
        pytest.fail(f"HTTP error occurred: {e}")
    except Exception as e:
        pytest.fail(f"An error occurred: {e}")
