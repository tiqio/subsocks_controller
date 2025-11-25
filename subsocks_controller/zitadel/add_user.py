import http.client
import json

from env import domain, token, userid, orgid

conn = http.client.HTTPSConnection(f"{domain}")
payload = json.dumps({
    "organizationId": f"{orgid}",
    "userId": f"{userid}",
    "username": "minnie-mouse",
    "machine": {
        "name": "minnie",
        "description": "this is one test user"
    }
})
headers = {
    'Content-Type': 'application/json',
    'Accept': 'application/json',
    'Authorization': f'Bearer {token}'
}
conn.request("POST", "/v2/users/new", payload, headers)
res = conn.getresponse()
data = res.read()
print(data.decode("utf-8"))