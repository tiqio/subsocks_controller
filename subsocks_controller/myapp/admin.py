from django.contrib import admin
from .models import CertTable, AccessTable, ClientTable, ServiceTable

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
    list_display = ('id', 'name', 'addr', 'display_access_point', 'formatted_timestamp')
    ordering = ('timestamp',)

    def display_access_point(self, obj):
        return ', '.join([point.name for point in obj.access_point.all()])

    def formatted_timestamp(self, obj):
        return obj.timestamp.strftime('%Y年%m月%d日-%H时%M分')

    display_access_point.short_description = '接入点组名称'
    formatted_timestamp.short_description = '创建时间'

@admin.register(ServiceTable)
class ServiceTableAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'addr', 'protocol', 'formatted_timestamp')
    ordering = ('timestamp',)

    def formatted_timestamp(self, obj):
        return obj.timestamp.strftime('%Y年%m月%d日-%H时%M分')

    formatted_timestamp.short_description = '创建时间'
