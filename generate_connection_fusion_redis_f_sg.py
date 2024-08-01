from generate_connection_fusion import generate_connection

import redis, json

r = redis.Redis(host="localhost", port=6379, db=0)

result = generate_connection(
    json.loads(r.hget("session_id0802", "first_story")),
    json.loads(r.hget("session_id0802", "second_story")),
)

print(result)
print(type(result))
