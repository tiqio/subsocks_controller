from django.contrib import admin

from .models import CertTable, AccessTable, ClientTable, ServiceTable, BindTable, DialTable
from .sync.metadata import Metadata, Endpoint, AccessInfo, ServiceInfo, ClientMeta

# Register your models here.

admin.site.site_header = 'Subsocks控制器'
admin.site.site_title = 'Subsocks控制器'
admin.site.index_title = 'Subsocks控制器'

@admin.register(CertTable)
class CertTableAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'ca_cert', 'ca_secret', 'formatted_timestamp')
    ordering = ('timestamp',)

    def formatted_timestamp(self, obj):
        return obj.timestamp.strftime('%Y年%m月%d日-%H时%M分')

    formatted_timestamp.short_description = '创建时间'

@admin.register(AccessTable)
class AccessTableAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'addr', 'ca_info', 'formatted_timestamp')
    ordering = ('timestamp',)

    def formatted_timestamp(self, obj):
        return obj.timestamp.strftime('%Y年%m月%d日-%H时%M分')

    formatted_timestamp.short_description = '创建时间'

@admin.register(ClientTable)
class ClientTableAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'display_service', 'display_access_point', 'formatted_timestamp')
    ordering = ('timestamp',)

    actions = ['sync_clients']

    def display_service(self, obj):
        return ', '.join([point.name for point in obj.service.all()])

    def display_access_point(self, obj):
        return ', '.join([point.name for point in obj.access_point.all()])

    def formatted_timestamp(self, obj):
        return obj.timestamp.strftime('%Y年%m月%d日-%H时%M分')

    def sync_clients(self, request, queryset):
        client_meta_map = {}

        for client in queryset:
            services = client.service.all()  # 获取所有相关的 service 对象
            access_points = client.access_point.all()  # 获取所有相关的 access_point 对象

            service_names = [service.name for service in services]
            access_names = [access_point.name for access_point in access_points]

            print(f"客户端 {client.name} 的服务: {service_names}")
            print(f"客户端 {client.name} 的接入点: {[access_names]}")

            # 创建ClientMeta实例
            metadata = Metadata(client_type="client", client_id=client.name)
            endpoints = [Endpoint(name) for name in service_names]
            accessinfo = [
                AccessInfo(access_id=access_point.name,
                           services=[ServiceInfo(service_id=service.name, delay=100) for service in services])
                for access_point in access_points
            ]

            client_meta = ClientMeta(metadata, endpoints, accessinfo)

            # 检查是否存在相同的ClientMeta
            if client.name in client_meta_map:
                # 如果已存在就合并
                existing_meta = client_meta_map[client.name]
                existing_meta.merge(client_meta)
            else:
                # 如果不存在就直接添加
                client_meta_map[client.name] = client_meta

        # 遍历并打印所有 ClientMeta 实例
        print("\n所有合并后的 ClientMeta 实例:")
        for client, meta in client_meta_map.items():
            print(f"\n客户端: {client}")
            meta.print_structure()

        self.message_user(request, "同步成功！")
        return

    sync_clients.short_description = '同步到Zitadel'

    display_service.short_description = '可访问服务名称'
    display_access_point.short_description = '接入点组名称'
    formatted_timestamp.short_description = '创建时间'

@admin.register(ServiceTable)
class ServiceTableAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'addr', 'protocol', 'formatted_timestamp')
    ordering = ('timestamp',)

    def formatted_timestamp(self, obj):
        return obj.timestamp.strftime('%Y年%m月%d日-%H时%M分')

    formatted_timestamp.short_description = '创建时间'

@admin.register(BindTable)
class BindTableAdmin(admin.ModelAdmin):
    list_display = ('id', 'access_point', 'display_service', 'formatted_timestamp')
    ordering = ('timestamp',)

    def display_service(self, obj):
        return ', '.join([srv.name for srv in obj.service.all()])

    def formatted_timestamp(self, obj):
        return obj.timestamp.strftime('%Y年%m月%d日-%H时%M分')

    display_service.short_description = '服务列表'
    formatted_timestamp.short_description = '创建时间'

@admin.register(DialTable)
class DialTableAdmin(admin.ModelAdmin):
    list_display = ('id', 'client', 'display_service', 'formatted_timestamp')
    ordering = ('timestamp',)

    def display_service(self, obj):
        return ', '.join([srv.name for srv in obj.service.all()])

    def formatted_timestamp(self, obj):
        return obj.timestamp.strftime('%Y年%m月%d日-%H时%M分')

    formatted_timestamp.short_description = '创建时间'
    display_service.short_description = '服务列表'

