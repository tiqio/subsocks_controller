import http.client

from env import domain, token, userid

conn = http.client.HTTPSConnection(f"{domain}")
payload = ''
headers = {
    'Accept': 'application/json',
    'Authorization': f'Bearer {token}'
}
conn.request("GET", f"/v2/users/{userid}", payload, headers)
res = conn.getresponse()
data = res.read()
print(data.decode("utf-8"))