import pytest
import pytest_asyncio
from httpx import AsyncClient

pytestmark = pytest.mark.asyncio


@pytest_asyncio.fixture
async def project_id(client: AsyncClient):
    response = await client.post("/projects/", json={"name": "Test Project"})
    return response.json()["id"]


async def test_create_place(client: AsyncClient, project_id: int):
    response = await client.post(
        f"/projects/{project_id}/places/",
        json={"external_place_id": "789", "notes": "Must see"},
    )
    assert response.status_code == 201
    data = response.json()
    assert data["external_place_id"] == "789"
    assert data["notes"] == "Must see"
    assert data["is_visited"] is False


async def test_create_place_invalid_id(client: AsyncClient, project_id: int):
    response = await client.post(
        f"/projects/{project_id}/places/", json={"external_place_id": "invalid_id"}
    )
    assert response.status_code == 400
    assert "not found" in response.json()["detail"]


async def test_create_duplicate_place(client: AsyncClient, project_id: int):
    await client.post(
        f"/projects/{project_id}/places/", json={"external_place_id": "789"}
    )
    response = await client.post(
        f"/projects/{project_id}/places/", json={"external_place_id": "789"}
    )
    assert response.status_code == 400
    assert "already exists" in response.json()["detail"]


async def test_get_places(client: AsyncClient, project_id: int):
    await client.post(
        f"/projects/{project_id}/places/", json={"external_place_id": "111"}
    )
    await client.post(
        f"/projects/{project_id}/places/", json={"external_place_id": "222"}
    )

    response = await client.get(f"/projects/{project_id}/places/")
    assert response.status_code == 200
    assert len(response.json()) == 2


async def test_update_place(client: AsyncClient, project_id: int):
    create_resp = await client.post(
        f"/projects/{project_id}/places/", json={"external_place_id": "333"}
    )
    place_id = create_resp.json()["id"]

    response = await client.patch(
        f"/projects/{project_id}/places/{place_id}",
        json={"notes": "Updated note", "is_visited": True},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["notes"] == "Updated note"
    assert data["is_visited"] is True
