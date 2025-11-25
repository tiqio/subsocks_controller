import http.client
import json

# 从环境变量导入必要的配置
from env import domain, token, userid

# 创建 HTTPS 连接
conn = http.client.HTTPSConnection(domain)

# 定义请求的有效负载和头部
payload = json.dumps({})
headers = {
    'Content-Type': 'application/json',
    'Accept': 'application/json',
    'Authorization': f'Bearer {token}'  # 使用从环境导入的 token
}

# 发送 POST 请求
conn.request("POST", f"/v2/users/{userid}/secret", payload, headers)

# 获取响应
res = conn.getresponse()
data = res.read()

# 打印响应数据
print(data.decode("utf-8"))
