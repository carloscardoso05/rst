import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def get_all_filenames():
    response = client.get("/files/")
    assert response.status_code == 200
    filenames = response.json()
    assert isinstance(filenames, list)
    assert len(filenames) > 0
    return filenames

def test_get_all_files():
    filenames = get_all_filenames()
    assert len(filenames) > 0

@pytest.mark.parametrize("filename", get_all_filenames())
def test_file(filename):
    print(f"Testing file: {filename}")
    response = client.get(f"/files/{filename}")
    assert response.status_code == 200, f"Failed to get file: {filename}"
    
    # Check if the response has the expected structure
    data = response.json()
    assert "file_path" in data, f"Missing file_path in response for {filename}"
    assert "intra_sentential_relations" in data, f"Missing intra_sentential_relations in response for {filename}"
    
    # Check if intra_sentential_relations is a list
    assert isinstance(data["intra_sentential_relations"], list), f"intra_sentential_relations should be a list for {filename}"
    
    # If there are relations, check their structure
    for relation in data["intra_sentential_relations"]:
        assert "id" in relation, f"Missing id in relation for {filename}"
        assert "parent_id" in relation, f"Missing parent_id in relation for {filename}"
        assert "relname" in relation, f"Missing relname in relation for {filename}"
        assert "text" in relation, f"Missing text in relation for {filename}" 