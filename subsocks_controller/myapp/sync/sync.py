"""
1. 使用client参数作为ServiceUser的名称
2，使用meta参数（元数据键值对）同步元数据到指定的ServiceUser
3. 如果指定的用户不存在就添加用户；如果用户已存在就删除旧的元数据并设置新的元数据
4. 添加密钥已生成clientSecret
"""

from .client import Client
from .env import domain, token, orgid  # 从配置文件导入环境变量
from ..models import ZitadelTable
from .metadata import Metadata, Endpoint, ClientMeta

def sync_client_to_zitadel(client_name, meta):
    """
    在 Zitadel 平台同步 ServiceUser 的数据。
    :param client_name: ServiceUser 的名称
    :param meta: 元数据键值对，格式为 [{"key": "key1", "value": "value1"}, ...]
    """
    # 初始化 Client
    client = Client(domain=domain, token=token, orgid=orgid)

    # 1. 检查用户是否存在
    resp = client.get_user({
        "userName": client_name
    })
    print("is get_user.valid:", client.is_result_valid(resp))

    # 2. 如果用户不存在，创建用户
    if not client.is_result_valid(resp):
        print(f"User '{client_name}' does not exist. Creating new user...")
        try:
            add_user_response = client.add_user(
                username=client_name,
                machine_name=client_name,
                machine_description=f"Service user for {client_name}"
            )
            print("Add User Response:", add_user_response)
        except Exception as e:
            print(f"Failed to add user '{client_name}': {e}")
            return
    else:
        print(f"User '{client_name}' already exists. User ID: {client.userid}")
        # 3. 如果用户已存在，删除旧的元数据，仅涉及到metadata，endpoints，accessinfo和testkey
        try:
            del_metadata_response = client.del_metadata()
            print("Delete Metadata Response:", del_metadata_response)
        except Exception as e:
            print(f"Failed to delete metadata for user '{client_name}': {e}")
            return

    # 4. 设置新的元数据
    try:
        # 转换meta为指定的键值对格式
        metadata = [
            {"key": key, "value": value}
            for key, value in meta.items()
        ]
        metadata_response = client.set_metadata(metadata)
        print("Set Metadata Response:", metadata_response)
    except Exception as e:
        print(f"Failed to set metadata for user '{client_name}': {e}")
        return

    # 5. 添加密钥
    try:
        add_secret_response = client.add_secret()
        print("Add Secret Response:", add_secret_response)

        # 6. 所有操作成功后，更新或创建 ZitadelTable 数据
        ZitadelTable.objects.update_or_create(
            user_id=client.userid,
            defaults={
                "type": 'Client',
                "client_id" : client_name,
                "client_secret" : client.secret,
            }
        )
    except Exception as e:
        print(f"Failed to add secret for user '{client_name}': {e}")
        return

    print(f"Sync completed for user '{client_name}'.")

def sync_access_to_zitadel(access_name, meta):
    """
    在 Zitadel 平台同步 ServiceUser 的数据。
    :param client_name: ServiceUser 的名称
    :param meta: 集合类型，格式为 {'YouTube', 'IPSB}
    """
    # 初始化 Client
    client = Client(domain=domain, token=token, orgid=orgid)

    # 1. 检查用户是否存在
    resp = client.get_user({
        "userName": access_name
    })
    print("is get_user.valid:", client.is_result_valid(resp))

    # 2. 如果用户不存在，创建用户
    if not client.is_result_valid(resp):
        print(f"User '{access_name}' does not exist. Creating new user...")
        try:
            add_user_response = client.add_user(
                username=access_name,
                machine_name=access_name,
                machine_description=f"Service user for {access_name}"
            )
            print("Add User Response:", add_user_response)
        except Exception as e:
            print(f"Failed to add user '{access_name}': {e}")
            return
    else:
        print(f"User '{access_name}' already exists. User ID: {client.userid}")
        # 3. 如果用户已存在，删除旧的元数据，仅涉及到metadata，endpoints，accessinfo和testkey
        try:
            del_metadata_response = client.del_metadata()
            print("Delete Metadata Response:", del_metadata_response)
        except Exception as e:
            print(f"Failed to delete metadata for user '{access_name}': {e}")
            return

    # 4. 设置新的元数据
    try:
        # 转换meta为指定的键值对格式
        metadata = Metadata(client_type="access", client_id=access_name)
        endpoints = [Endpoint(name) for name in meta]
        accessinfo = []

        client_meta = ClientMeta(metadata, endpoints, accessinfo)


        metadata = [
            {"key": key, "value": value}
            for key, value in client_meta.convert_client_meta_to_dict().items()
        ]

        metadata_response = client.set_metadata(metadata)
        print("Set Metadata Response:", metadata_response)
    except Exception as e:
        print(f"Failed to set metadata for user '{access_name}': {e}")
        return

    # 5. 添加密钥
    try:
        add_secret_response = client.add_secret()
        print("Add Secret Response:", add_secret_response)

        # 6. 所有操作成功后，更新或创建 ZitadelTable 数据
        ZitadelTable.objects.update_or_create(
            user_id=client.userid,
            defaults={
                "type": 'Access',
                "client_id" : access_name,
                "client_secret" : client.secret,
            }
        )
    except Exception as e:
        print(f"Failed to add secret for user '{access_name}': {e}")
        return

    print(f"Sync completed for user '{access_name}'.")