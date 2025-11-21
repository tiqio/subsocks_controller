from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.

def item_list(request):
    items = [{'name': 'Item 1'}, {'name': 'Item 2'}]
    return JsonResponse(items, safe=False)