import pytest
from app.redis_client import r
from app.rate_limit import limit_requests

URLS = [
    ("/applications/getall", None),
    ("/applications/company", {"company_name": "Acme"}),
]  # both routes to test

def cache_keys():
    return list(r.scan_iter("applications:user:*"))  # everything cached

@pytest.mark.parametrize("url, params", URLS)  # runs once per URL
def test_read_fills_cache(authorized_client, application_id, url, params):
    assert cache_keys() == []  # cache starts empty
    authorized_client.get(url, params=params)
    assert len(cache_keys()) == 1  # one read, one cached entry

@pytest.mark.parametrize("url, params", URLS)
def test_update_clears_cache(authorized_client, application_id, url, params):
    authorized_client.get(url, params=params)  # fills the cache
    assert len(cache_keys()) == 1
    response= authorized_client.patch(f"/applications/{application_id}/status", json={"status": "Interviewing"})  #my update payload
    response.status_code == 200, response.text 
    assert cache_keys() == []  # cache cleared


def test_get_all_applications(authorized_client, application_id):
    response = authorized_client.get("/applications/getall")
    assert response.status_code == 200, (response.status_code, response.text)
    applications = response.json()
    assert isinstance(applications, list)
    assert len(applications) >= 1
    
def test_create_application(authorized_client,test_user):
    response= authorized_client.post("/applications/create", json={"job_title": "Backend Developer", "company": "Acme Ltd"})
    assert response.status_code == 201
    data = response.json()
    assert data["job_title"] == "Backend Developer"
    assert data["company"] == "Acme Ltd"
    assert data["status"] == "Applied"

def test_get_application_by_company(authorized_client,test_user):
    # First, create an application
    create_response = authorized_client.post("/applications/create", json={"job_title": "Backend Developer", "company": "Acme Ltd"})
    assert create_response.status_code == 201
    application_id = create_response.json()["id"]
    # Now, retrieve the application by company
    response = authorized_client.get(
    "/applications/company", params={"company_name": "Acme Ltd"}
)
    assert response.status_code == 200
    applications = response.json()
    assert len(applications) == 1
    assert applications[0]["id"] == application_id
    assert applications[0]["job_title"] == "Backend Developer"

def test_update_application(authorized_client,test_user):
    create_response = authorized_client.post(
        "/applications/create",
        json={
            "job_title": "Backend Developer", 
            "company": "Acme Ltd"
        },
    )
    assert create_response.status_code == 201
    application_id = create_response.json()["id"]
    response= authorized_client.patch(f"/applications/{application_id}/status", json={"status": "Interviewing"})
    assert response.status_code == 200
    assert response.json()["status"] == "Interviewing"


def test_delete_application(authorized_client,test_user):
    # First, create a application to delete
    create_response = authorized_client.post("/applications/create", json={"job_title": "Backend Developer", "company": "Acme Ltd"})
    assert create_response.status_code == 201
    application_id = create_response.json()["id"]
    # Now, delete the application
    response = authorized_client.delete(f"/applications/{application_id}")
    assert response.status_code == 204
    # Verify that the application no longer exists
    get_response = authorized_client.get(f"/applications/get/{application_id}")
    assert get_response.status_code == 404

@pytest.mark.parametrize("method, endpoint", [
    ("GET", "/applications/getall"),
    ("GET", "/applications/company"),
    ("POST", "/applications/create"),
    ("PATCH", "/applications/1/status"),
])
def test_unauthorized_access(client, method, endpoint):
    # client.request() lets me pass the method dynamically as a string
    response = client.request(method, endpoint)
    assert response.status_code == 401
    assert response.json()["detail"] == "Not authenticated"

@pytest.mark.parametrize("url, params", [
    ("/applications/getall", None),
    ("/applications/company", {"company_name": "Acme Ltd"}),
])
def test_get_routes_rate_limiting(authorized_client, application_id, url, params):
    for i in range(5):
        response = authorized_client.get(url, params=params)
        assert response.status_code == 200, (response.status_code, response.text)
    