from fastapi.testclient import TestClient

from src.server.main import app

client = TestClient(app)

def test_read_main() -> None:
    response = client.get('/')
    index_html = open("static/index.html", "r").read()
    assert response.status_code == 200
    assert response.text == index_html

def test_read_script() -> None:
    response = client.get('/static/script.js')
    assert response.status_code == 200

def test_read_checker_query() -> None:
    response = client.get(
        '/check/',
        params={"domain": "example.com"},
    )
    assert response.status_code == 200
    assert response.json() == {
        "is_valid": True,
        "data": {
            "subdomain": "",
            "root_domain": "example.com",
            "etld": "com",
            "tld": "com",
        }
    }

def test_read_checker_path() -> None:
    response = client.get(
        '/check/example.com',
    )
    assert response.status_code == 200
    assert response.json() == {
        "is_valid": True,
        "data": {
            "subdomain": "",
            "root_domain": "example.com",
            "etld": "com",
            "tld": "com",
        }
    }

