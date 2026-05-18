import pytest
from httpx import AsyncClient

pytestmark = pytest.mark.asyncio


async def test_create_project(client: AsyncClient):
    response = await client.post(
        "/projects/",
        json={
            "name": "Trip to Chicago",
            "description": "Art tour",
            "start_date": "2026-06-01",
        },
    )
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Trip to Chicago"
    assert data["description"] == "Art tour"
    assert data["start_date"] == "2026-06-01"
    assert data["places"] == []


async def test_create_project_with_places(client: AsyncClient):
    response = await client.post(
        "/projects/", json={"name": "Trip with Places", "places": ["123", "456"]}
    )
    assert response.status_code == 201
    data = response.json()
    assert len(data["places"]) == 2
    assert data["places"][0]["external_place_id"] == "123"


async def test_create_project_invalid_place(client: AsyncClient):
    response = await client.post(
        "/projects/", json={"name": "Trip with invalid place", "places": ["invalid_id"]}
    )
    assert response.status_code == 400
    assert "not found" in response.json()["detail"]


async def test_get_projects(client: AsyncClient):
    await client.post("/projects/", json={"name": "Project 1"})
    await client.post("/projects/", json={"name": "Project 2"})

    response = await client.get("/projects/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 2


async def test_get_project_by_id(client: AsyncClient):
    create_resp = await client.post("/projects/", json={"name": "Project 1"})
    project_id = create_resp.json()["id"]

    response = await client.get(f"/projects/{project_id}")
    assert response.status_code == 200
    assert response.json()["name"] == "Project 1"


async def test_update_project(client: AsyncClient):
    create_resp = await client.post("/projects/", json={"name": "Project 1"})
    project_id = create_resp.json()["id"]

    response = await client.put(
        f"/projects/{project_id}",
        json={"name": "Updated Project", "description": "New description"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Updated Project"
    assert data["description"] == "New description"


async def test_delete_project(client: AsyncClient):
    create_resp = await client.post("/projects/", json={"name": "Project to delete"})
    project_id = create_resp.json()["id"]

    del_resp = await client.delete(f"/projects/{project_id}")
    assert del_resp.status_code == 204

    get_resp = await client.get(f"/projects/{project_id}")
    assert get_resp.status_code == 404


async def test_cannot_delete_project_with_visited_places(client: AsyncClient):
    create_resp = await client.post(
        "/projects/", json={"name": "Project", "places": ["123"]}
    )
    project_id = create_resp.json()["id"]
    place_id = create_resp.json()["places"][0]["id"]

    await client.patch(
        f"/projects/{project_id}/places/{place_id}", json={"is_visited": True}
    )

    del_resp = await client.delete(f"/projects/{project_id}")
    assert del_resp.status_code == 400
    assert "visited places" in del_resp.json()["detail"]
