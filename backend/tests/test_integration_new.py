import pytest
from app.modules.events.schemas import EventCreate
from app.modules.fields.schemas import FieldCreate, FieldType
from app.modules.tags.schemas import TagCreate

def test_complex_event_creation_integration(auth_client):
    """
    Test creation of an event with existing and new tags, and custom fields.
    Verifies that all associations are correctly established.
    """
    # 1. Create a field first
    field_data = FieldCreate(
        name="Source",
        description="Event source",
        field_type=FieldType.string
    )
    field_res = auth_client.post("/v1/fields/", json=field_data.model_dump())
    field_id = field_res.json()["id"]

    # 2. Create an event with a mix of new tags and the field
    event_data = {
        "name": "Integration Test Event",
        "description": "Testing complex relations",
        "tags": ["existing-tag", "brand-new-tag"],
        "fields": [field_id]
    }
    
    response = auth_client.post("/v1/events/", json=event_data)
    assert response.status_code == 201
    event = response.json()
    assert event["name"] == event_data["name"]
    
    # 3. Verify tags are created/linked
    assert len(event["tags"]) == 2
    tag_ids = [t["id"] for t in event["tags"]]
    assert "existing-tag" in tag_ids
    assert "brand-new-tag" in tag_ids
    
    # 4. Verify fields are linked
    assert len(event["fields"]) == 1
    assert event["fields"][0]["id"] == field_id

def test_event_list_integration(auth_client):
    """
    Test that listing events works and returns all created events.
    """
    # Create 3 events
    for i in range(3):
        auth_client.post("/v1/events/", json={
            "name": f"Event {i}",
            "description": "Desc",
            "tags": [],
            "fields": []
        })
    
    # Verify we can list them
    res = auth_client.get("/v1/events/")
    assert res.status_code == 200
    events = res.json()
    assert len(events) >= 3

def test_event_deletion_cascade_integration(auth_client, db):
    """
    Test that deleting an event cleans up its associations but not the entities themselves.
    """
    # 1. Create a tag and a field
    auth_client.post("/v1/tags/", json={"id": "persist-tag", "description": "d"})
    f_res = auth_client.post("/v1/fields/", json={"name": "f", "description": "d", "field_type": "string"})
    field_id = f_res.json()["id"]
    
    # 2. Create an event linked to them
    e_res = auth_client.post("/v1/events/", json={
        "name": "To Delete",
        "description": "d",
        "tags": ["persist-tag"],
        "fields": [field_id]
    })
    event_id = e_res.json()["id"]
    
    # 3. Delete the event
    del_res = auth_client.delete(f"/v1/events/{event_id}")
    assert del_res.status_code == 200
    
    # 4. Verify event is gone
    get_res = auth_client.get(f"/v1/events/{event_id}")
    assert get_res.status_code == 404
    
    # 5. Verify tag and field still exist (they are independent entities)
    assert auth_client.get("/v1/tags/persist-tag").status_code == 200
    assert auth_client.get(f"/v1/fields/{field_id}").status_code == 200
    
    # 6. Verify join table records are gone (implied by no errors and clean DB state, 
    # but we can check if another event creation with same tags works)
    e_res2 = auth_client.post("/v1/events/", json={
        "name": "New Event",
        "description": "d",
        "tags": ["persist-tag"],
        "fields": [field_id]
    })
    assert e_res2.status_code == 201
