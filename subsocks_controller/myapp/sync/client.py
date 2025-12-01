import json
import http.client
import urllib


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
        self.keys = ["metadata", "endpoints", "accessinfo", "testkey"]

    def get_user(self, filters):
        """
       根据筛选条件查询用户
       :param filters: 筛选条件，格式为字典，例如：
           {
               "userName": "gigi-giraffe",
               "firstName": "Gigi",
               "lastName": "Giraffe",
               "email": "gigi@zitadel.com",
               "loginName": "gigi@zitadel.cloud"
           }
       :return: 返回响应数据
       """
        conn = http.client.HTTPSConnection(self.domain)

        # 构建查询条件
        queries = []
        for key, value in filters.items():
            if key == "userName":
                queries.append({
                    "userNameQuery": {
                        "userName": value,
                        "method": "TEXT_QUERY_METHOD_EQUALS"
                    }
                })
            elif key == "firstName":
                queries.append({
                    "firstNameQuery": {
                        "firstName": value,
                        "method": "TEXT_QUERY_METHOD_EQUALS"
                    }
                })
            elif key == "lastName":
                queries.append({
                    "lastNameQuery": {
                        "lastName": value,
                        "method": "TEXT_QUERY_METHOD_EQUALS"
                    }
                })
            elif key == "email":
                queries.append({
                    "emailQuery": {
                        "emailAddress": value,
                        "method": "TEXT_QUERY_METHOD_EQUALS"
                    }
                })
            elif key == "loginName":
                queries.append({
                    "loginNameQuery": {
                        "loginName": value,
                        "method": "TEXT_QUERY_METHOD_EQUALS"
                    }
                })

        # 构建请求体
        payload = json.dumps({
            "query": {
                "offset": 0,
                "limit": 100,
                "asc": True
            },
            "sortingColumn": "USER_FIELD_NAME_UNSPECIFIED",
            "queries": queries
        })

        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'Authorization': f'Bearer {self.token}'
        }

        # 发送 POST 请求
        conn.request("POST", "/v2/users", payload, headers)
        res = conn.getresponse()
        data = res.read()

        # 返回响应数据
        user = data.decode("utf-8")
        return user

    def is_result_valid(self, data):
        """
        检查 JSON 数据是否存在 'result' 且长度为 1
        :param data: JSON 格式的字符串
        :return: True 如果 'result' 存在且长度为 1，否则 False
        """
        try:
            # 将字符串解析为字典
            parsed_data = json.loads(data)

            # 检查是否存在 'result' 且其长度为 1
            if 'result' in parsed_data and isinstance(parsed_data['result'], list) and len(parsed_data['result']) == 1:
                self.userid = parsed_data['result'][0].get('userId', None)
                print("set userid to => ", self.userid)
                return True
            return False
        except json.JSONDecodeError:
            # 如果解析失败，返回 False
            return False

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
        user_dict = json.loads(user)
        print("user_dict", user_dict)
        self.userid = user_dict["id"]
        print("set userid to => ", self.userid)
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

    def del_metadata(self):
        """
        遍历 keys 列表，为每个键分别发起 DELETE 请求
        :param keys: 要删除的元数据键列表，例如 ["metadata", "endpoints", "accessinfo", "testkey"]
        :return: 返回每次请求的响应数据列表
        """
        if not self.userid:
            raise ValueError("User ID is not set. Cannot delete metadata.")
        if not self.keys or not isinstance(self.keys, list):
            raise ValueError("Keys must be a non-empty list of metadata keys to delete.")

        conn = http.client.HTTPSConnection(self.domain)

        headers = {
            'Accept': 'application/json',
            'Authorization': f'Bearer {self.token}'
        }

        responses = []

        # 遍历 keys 列表，分别发起 DELETE 请求
        for key in self.keys:
            # 将单个键作为查询参数
            query_params = urllib.parse.urlencode({"keys": key})

            # 发起 DELETE 请求
            conn.request("DELETE", f"/v2/users/{self.userid}/metadata?{query_params}", headers=headers)
            res = conn.getresponse()
            response_data = res.read()

            # 打印每次请求的响应数据
            print(f"Response for key '{key}' => ", response_data)

            # 将响应结果解码并添加到响应列表
            responses.append({
                "key": key,
                "status": res.status,  # HTTP 状态码
                "response": response_data.decode("utf-8")
            })

        # 返回所有响应结果
        return responses

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
        secret_dict = json.loads(secret)
        self.secret =  secret_dict["clientSecret"]
        print("set secret to => ", self.secret)
        return secret

# 使用示例
'''
    get_user(N) ——> add_user——|
                        set_metadata ——> add_secret
get_user(Y) ——> del_metadata——|
'''
if __name__ == "__main__":
    # 从环境变量导入配置
    from env import domain, token, orgid

    # 初始化 Client
    client = Client(domain=domain, token=token, orgid=orgid)

    resp = client.get_user({
        "userName": "minnie-mouse",
    })
    print("is get_user.valid:", client.is_result_valid(resp))

    # 当存在用户时不去额外添加，此时is_result_valid会记录这个数据的userid
    if not client.is_result_valid(resp):
        # 添加用户，如果已经存在该user就会报错
        # {"code":6, "message":"User already exists (V3-DKcYh)", "details":[{"@type":"type.googleapis.com/zitadel.v1.ErrorDetail", "id":"V3-DKcYh", "message":"User already exists"}]}
        add_user_response = client.add_user(
            username="minnie-mouse",
            machine_name="minnie",
            machine_description="this is one test user"
        )
        print("Add User Response:", add_user_response)
    else:
        resp = client.del_metadata()

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
