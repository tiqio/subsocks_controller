import http.client
import json

from env import domain, token, userid

conn = http.client.HTTPSConnection(f"{domain}")
payload = json.dumps({
    "metadata": [
        {
            "key": "test1",
            "value": "VGhpcyBpcyBteSBmaXJzdCB2YWx1ZQ=="
        },
        {
            "key": "test2",
            "value": "VGhpcyBpcyBteSBzZWNvbmQgdmFsdWU="
        }
    ]
})
headers = {
    'Content-Type': 'application/json',
    'Accept': 'application/json',
    'Authorization': f'Bearer {token}'
}
conn.request("POST", f"/v2/users/{userid}/metadata", payload, headers)
res = conn.getresponse()
data = res.read()
print(data.decode("utf-8"))