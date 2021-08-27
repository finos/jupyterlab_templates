import json

import requests

def test_server_loaded_notebooks():
    resp = requests.get(
        "http://127.0.0.1:8888/templates/names",
    )
    assert resp.status_code == 200, resp.content
    assert resp.json() == {"demo": [{"name": "Sample.ipynb"}]}


    resp2 = requests.get(
        "http://127.0.0.1:8888/templates/get",
        params={"template": "Sample.ipynb"}
    )
    assert resp2.status_code == 200, resp.content
    data = resp2.json()
    assert data["name"] == "demo/Sample.ipynb"
    assert data["path"] == "demo/Sample.ipynb"
    assert data["dirname"] == "demo"
    assert json.loads(data["content"]) != {}