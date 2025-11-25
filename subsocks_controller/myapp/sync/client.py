import json
import http.client

class Client:
    def __init__(self, domain, token, orgid):
        """
        初始化 Client 类
        :param domain: API 的域名
        :param token: API 的认证 token
        :param orgid: 组织 ID，可选
        """
        self.secret = None
        self.userid = None
        self.domain = domain
        self.token = token
        self.orgid = orgid

    def add_user(self, username, machine_name, machine_description):
        """
        添加用户
        :param username: 用户名
        :param machine_name: 机器名称
        :param machine_description: 机器描述
        :return: 返回响应数据
        """
        conn = http.client.HTTPSConnection(self.domain)
        payload = json.dumps({
            "organizationId": f"{self.orgid}",
            # "userId": f"{userid}",
            "username": username,
            "machine": {
                "name": machine_name,
                "description": machine_description
            }
        })
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'Authorization': f'Bearer {self.token}'
        }
        conn.request("POST", "/v2/users/new", payload, headers)
        res = conn.getresponse()
        data = res.read()
        user = data.decode("utf-8")
        self.userid = user.id
        return user

    def set_metadata(self, metadata):
        """
        设置用户的元数据
        :param metadata: 元数据列表，格式为 [{"key": "key1", "value": "value1"}, ...]
        :return: 返回响应数据
        """
        conn = http.client.HTTPSConnection(self.domain)

        # 将元数据转换为 JSON 格式
        payload = json.dumps({
            "metadata": metadata
        })

        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'Authorization': f'Bearer {self.token}'
        }

        # 发送 POST 请求
        conn.request("POST", f"/v2/users/{self.userid}/metadata", payload, headers)
        res = conn.getresponse()
        metadata = res.read()

        # 返回响应结果
        return metadata.decode("utf-8")

    def add_secret(self):
        """
        添加用户密钥
        :return: 返回响应数据
        """
        conn = http.client.HTTPSConnection(self.domain)
        payload = json.dumps({})
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'Authorization': f'Bearer {self.token}'
        }
        conn.request("POST", f"/v2/users/{self.userid}/secret", payload, headers)
        res = conn.getresponse()
        data = res.read()
        secret = data.decode("utf-8")
        self.secret = secret.clientSecret
        return secret

# 使用示例
if __name__ == "__main__":
    # 从环境变量导入配置
    from env import domain, token, orgid, userid

    # 初始化 Client
    client = Client(domain=domain, token=token, orgid=orgid)

    # 添加用户，如果已经存在该user就会报错
    # {"code":6, "message":"User already exists (V3-DKcYh)", "details":[{"@type":"type.googleapis.com/zitadel.v1.ErrorDetail", "id":"V3-DKcYh", "message":"User already exists"}]}
    add_user_response = client.add_user(
        username="minnie-mouse",
        machine_name="minnie",
        machine_description="this is one test user"
    )
    print("Add User Response:", add_user_response)

    # 设置元数据
    metadata = [
        {
            "key": "test1",
            "value": "VGhpcyBpcyBteSBmaXJzdCB2YWx1ZQ=="
        },
        {
            "key": "test2",
            "value": "VGhpcyBpcyBteSBzZWNvbmQgdmFsdWU="
        }
    ]
    metadata_response = client.set_metadata(
        metadata
    )
    print("Set Metadata Response:", metadata_response)

    # 添加密钥
    add_secret_response = client.add_secret()
    print("Add Secret Response:", add_secret_response)
