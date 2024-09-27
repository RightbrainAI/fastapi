from datetime import datetime
from fastapi import FastAPI, Request
from fastapi.testclient import TestClient

app = FastAPI()


@app.get("/{first}/{second}/{third}")
def route1(request: Request, third: datetime):
    return {}


@app.get("/{fourth:int}/{fifth:str}/{sixth:str}")
def route2(request: Request, sixth: datetime):
    return {}


def test_openapi_schema_with_dynamic_path_parameters():
    client = TestClient(app)
    response = client.get("/openapi.json")
    schema = response.json()
    route1 = schema["paths"]["/{first}/{second}/{third}"]["get"]
    assert "parameters" in route1
    route1_params = route1["parameters"]
    assert len(route1_params) == 3
    route1_first = next(p for p in route1_params if p["name"] == "first")
    route1_second = next(p for p in route1_params if p["name"] == "second")
    route1_third = next(p for p in route1_params if p["name"] == "third")
    assert route1_first["schema"]["type"] == "string"
    assert route1_first["in"] == "path"
    assert route1_first["required"]
    assert route1_second["schema"]["type"] == "string"
    assert route1_second["in"] == "path"
    assert route1_second["required"]
    assert route1_third["schema"]["type"] == "string"
    assert route1_third["schema"]["format"] == "date-time"
    assert route1_third["in"] == "path"
    assert route1_third["required"]
    route2 = schema["paths"]["/{fourth}/{fifth}/{sixth}"]["get"]
    assert "parameters" in route1
    route2_params = route2["parameters"]
    assert len(route2_params) == 3
    route2_fourth = next(p for p in route2_params if p["name"] == "fourth")
    route2_fifth = next(p for p in route2_params if p["name"] == "fifth")
    route2_sixth = next(p for p in route2_params if p["name"] == "sixth")
    assert route2_fourth["schema"]["type"] == "integer"
    assert route2_fourth["in"] == "path"
    assert route2_fourth["required"]
    assert route2_fifth["schema"]["type"] == "string"
    assert route2_fifth["in"] == "path"
    assert route2_fifth["required"]
    assert route2_sixth["schema"]["type"] == "string"
    assert route2_sixth["schema"]["format"] == "date-time"
    assert route2_sixth["in"] == "path"
    assert route2_sixth["required"]
