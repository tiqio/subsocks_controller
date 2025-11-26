import base64
import json

class Metadata:
    def __init__(self, client_type, client_id):
        self.type = client_type
        self.id = client_id

    def __repr__(self):
        return f"Metadata(type={self.type}, id={self.id})"


class Endpoint:
    def __init__(self, endpoint_name):
        self.name = endpoint_name

    def __repr__(self):
        return f"Endpoint(name={self.name})"


class ServiceInfo:
    def __init__(self, service_id, delay=None):
        self.service_id = service_id
        self.delay = delay

    def __repr__(self):
        return f"ServiceInfo(service_id={self.service_id}, delay={self.delay})"


class AccessInfo:
    def __init__(self, access_id, services):
        self.access_id = access_id
        self.services = services  # services should be a list of ServiceInfo instances

    def __repr__(self):
        return f"AccessInfo(access_id={self.access_id}, services={self.services})"


class ClientMeta:
    def __init__(self, metadata, endpoints, accessinfo):
        self.metadata = metadata  # Metadata instance
        self.endpoints = endpoints  # List of Endpoint instances
        self.accessinfo = accessinfo  # List of AccessInfo instances

    def __repr__(self):
        return (f"ClientMeta(metadata={self.metadata}, "
                f"endpoints={self.endpoints}, "
                f"accessinfo={self.accessinfo})")

    def print_structure(self):
        print("ClientMeta Structure:")
        print(f"  Metadata: {self.metadata}")
        print("  Endpoints:")
        for endpoint in self.endpoints:
            print(f"    - {endpoint}")
        print("  Access Info:")
        for access in self.accessinfo:
            print(f"    - Access ID: {access.access_id}")
            print("      Services:")
            for service in access.services:
                print(f"        - {service.service_id} (Delay: {service.delay})")


    def merge(self, other):
        """合并两个 ClientMeta 实例"""
        if self.metadata.id != other.metadata.id:
            raise ValueError("Cannot merge ClientMeta instances with different IDs.")

        # 合并 endpoints
        existing_endpoints = {endpoint.name for endpoint in self.endpoints}
        for endpoint in other.endpoints:
            if endpoint.name not in existing_endpoints:
                self.endpoints.append(endpoint)
                existing_endpoints.add(endpoint.name)

        # 合并 accessinfo
        existing_access_ids = {access.access_id for access in self.accessinfo}
        for access in other.accessinfo:
            if access.access_id not in existing_access_ids:
                self.accessinfo.append(access)
                existing_access_ids.add(access.access_id)
            else:
                # 如果 Access ID 已存在，合并服务
                for service in access.services:
                    if service not in [s.service_id for s in self.accessinfo[existing_access_ids.index(access.access_id)].services]:
                        self.accessinfo[existing_access_ids.index(access.access_id)].services.append(service)

    def convert_client_meta_to_dict(self):
        """
        将 ClientMeta 实例转换为指定的 JSON 格式。
        :return: 包含 metadata、endpoints 和 accessinfo 的字典
        """
        # 转换 metadata
        metadata_dict = {
            "type": self.metadata.type,
            "id": self.metadata.id
        }
        metadata_bytes = json.dumps(metadata_dict).encode("utf-8")  # 转换为字节类型
        metadata_base64 = base64.b64encode(metadata_bytes).decode("utf-8")  # 转换为 Base64 编码字符串

        # 转换 endpoints
        endpoints_list = [endpoint.name for endpoint in self.endpoints]
        endpoints_bytes = json.dumps(endpoints_list).encode("utf-8")  # 转换为字节类型
        endpoints_base64 = base64.b64encode(endpoints_bytes).decode("utf-8")  # 转换为 Base64 编码字符串\

        # 转换 accessinfo
        accessinfo_list = []
        for access in self.accessinfo:
            services_list = [
                {
                    "service_id": service.service_id,
                    "delay": service.delay
                }
                for service in access.services
            ]
            accessinfo_list.append({
                "access_id": access.access_id,
                "services": services_list
            })
        accessinfo_bytes = json.dumps(accessinfo_list).encode("utf-8")  # 转换为字节类型
        accessinfo_base64 = base64.b64encode(accessinfo_bytes).decode("utf-8")  # 转换为 Base64 编码字符串

        # 构造最终的字典
        result = {
            "metadata": metadata_base64,
            "endpoints": endpoints_base64,
            "accessinfo": accessinfo_base64
        }

        return result

if __name__ == '__main__':
    # 示例使用
    metadata1 = Metadata(client_type="client", client_id="Windows11")
    endpoints1 = [Endpoint("IPSB"), Endpoint("YouTube")]
    services1 = [ServiceInfo(service_id="IPSB", delay=100), ServiceInfo(service_id="YouTube", delay=100)]
    accessinfo1 = [AccessInfo(access_id="Ubuntu25", services=services1)]

    client_meta1 = ClientMeta(metadata1, endpoints1, accessinfo1)

    metadata2 = Metadata(client_type="client", client_id="Windows11")
    endpoints2 = [Endpoint("YouTube")]  # 重复的端点
    services2 = [ServiceInfo(service_id="YouTube", delay=100)]
    accessinfo2 = [AccessInfo(access_id="Ubuntu22", services=services2)]

    client_meta2 = ClientMeta(metadata2, endpoints2, accessinfo2)

    # 合并两个 ClientMeta 实例
    client_meta1.merge(client_meta2)

    # 打印合并后的结果
    client_meta1.print_structure()

    # 转换为字典格式
    result = client_meta1.convert_client_meta_to_dict()

    # 打印json结果（metadata）
    print(json.dumps(result, indent=4))