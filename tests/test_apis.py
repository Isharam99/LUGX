import requests
import pytest

# --- Test Configuration ---
# You will need to find the correct NodePort for your game-service
# Run 'kubectl get service game-service' to find it
GAME_SERVICE_URL = "http://localhost:5001"  # Replace XXXXX with the game-service NodePort

# --- Tests for the Enhanced Game Service ---

def test_get_all_games():
    """Tests if the /games endpoint returns a list of games."""
    response = requests.get(f"{GAME_SERVICE_URL}/games")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_single_game():
    """Tests if getting a single game by ID works."""
    response = requests.get(f"{GAME_SERVICE_URL}/games/1")
    assert response.status_code == 200
    game = response.json()
    assert game['id'] == 1
    assert game['name'] == 'Cyberpunk 2077'

def test_get_nonexistent_game():
    """Tests that asking for a game that doesn't exist returns a 404 error."""
    response = requests.get(f"{GAME_SERVICE_URL}/games/9999")
    assert response.status_code == 404

def test_create_update_and_delete_game():
    """Tests the full lifecycle: Create, Update, and Delete a game."""
    # 1. CREATE a new game
    new_game_data = {
        "name": "Test Game",
        "category": "Test Category",
        "price": 99.99,
        "release_date": "2025-01-01",
        "description": "A game for testing."
    }
    create_response = requests.post(f"{GAME_SERVICE_URL}/games", json=new_game_data)
    assert create_response.status_code == 201
    created_game = create_response.json()
    game_id = created_game['id']

    # 2. UPDATE the game
    updated_game_data = {
        "name": "Updated Test Game",
        "category": "Updated Category",
        "price": 109.99,
        "release_date": "2025-02-02",
        "description": "An updated game for testing."
    }
    update_response = requests.put(f"{GAME_SERVICE_URL}/games/{game_id}", json=updated_game_data)
    assert update_response.status_code == 200

    # 3. DELETE the game
    delete_response = requests.delete(f"{GAME_SERVICE_URL}/games/{game_id}")
    assert delete_response.status_code == 200

    # 4. Verify the game is gone
    verify_response = requests.get(f"{GAME_SERVICE_URL}/games/{game_id}")
    assert verify_response.status_code == 404