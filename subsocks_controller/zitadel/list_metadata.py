import http.client
import json

from env import domain, token, userid

conn = http.client.HTTPSConnection(f"{domain}")
payload = json.dumps({
    "pagination": {
        "offset": 0,
        "limit": 10,
        "asc": False
    },
    # "filters": [
    #     {
    #         "keyFilter": {
    #             "key": "key",
    #             "method": "TEXT_FILTER_METHOD_EQUALS"
    #         }
    #     }
    # ]
})
headers = {
    'Content-Type': 'application/json',
    'Accept': 'application/json',
    'Authorization': f'Bearer {token}'
}
conn.request("POST", f"/v2/users/{userid}/metadata/search", payload, headers)
res = conn.getresponse()
data = res.read()
print(data.decode("utf-8"))