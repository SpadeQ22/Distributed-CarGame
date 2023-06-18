import json
import redis

# Connect to Redis server
redis_client = redis.Redis(host="redis-12791.c44.us-east-1-2.ec2.cloud.redislabs.com", port=12791, db=0, password='bg17VYxIffU1IyzMvsiaZ1xLY5xxbpeU')

# Save game state to Redis
def save_game_state(session_id, game_state):
    key = f"game:{session_id}"
    value = json.dumps(game_state)
    result = redis_client.set(key, value)
    if result:
        pass
        # print(f"Saved game state for session {session_id}")
    else:
        pass
        # print(f"Error saving game state for session {session_id}")

# Retrieve game state from Redis
def get_game_state(session_id):
    key = f"game:{session_id}"
    value = redis_client.get(key)
    if value:
        game_state = json.loads(value)
        return game_state
    else:
        pass
        # print(f"No game state found for session {session_id}")
        return None

def delete_game_state(session_id):
    key = f"game:{session_id}"
    value = redis_client.get(key)
    if value:
        redis_client.delete(key)
        return True
    else:
        # print(f"No game state found for session {session_id}")
        return False



