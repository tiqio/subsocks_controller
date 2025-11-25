from django.http import JsonResponse
from django.shortcuts import render
from django.shortcuts import get_object_or_404

from .models import ServiceTable, AccessTable


# Create your views here.

def item_list(request):
    items = [{'name': 'Item 1'}, {'name': 'Item 2'}]

    return JsonResponse(items, safe=False)

def info_service(request, name):
    """根据服务别名返回服务信息"""
    service = get_object_or_404(ServiceTable, name=name)
    service_data = {
        'id': service.id,
        'name': service.name,
        'addr': service.addr,
        'protocol': service.protocol,
        'timestamp': service.timestamp,
    }
    return JsonResponse(service_data)

def info_access(request, name):
    """根据接入点别名返回接入点信息"""
    access_point = get_object_or_404(AccessTable, name=name)
    access_data = {
        'id': access_point.id,
        'name': access_point.name,
        'addr': access_point.addr,
        'ca_info_id': access_point.ca_info.id if access_point.ca_info else None,
        'timestamp': access_point.timestamp,
    }
    return JsonResponse(access_data)