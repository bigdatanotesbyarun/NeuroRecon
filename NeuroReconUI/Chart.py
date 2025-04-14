from django.urls import path
from . import views
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import HttpResponse, JsonResponse

@api_view(['GET'])
def chart1(request):
    data = {
        "labels": ["Table1", "Table2", "Table3"],
        "datasets": [
            {
                "data": [657689, 590978, 846789]
            }
        ]
    }
    return JsonResponse(data)

@api_view(['GET'])
def chart2(request):
    data = {
       "labels": ["Table1", "Table2", "Table3"],
        "datasets": [
            {
                "data": [657689, 590978, 846789]
            }
        ]
    }
    return JsonResponse(data)

@api_view(['GET'])
def chart3(request):
    data = {
        "labels": ["Region1", "Region2", "Region3"],
        "datasets": [
            {
                "data": [657689, 590978, 846789]
            }
        ]
    }
    return JsonResponse(data)

@api_view(['GET'])
def chart4(request):
    data = {
        "labels": ["Region1", "Region2", "Region3"],
        "datasets": [
            {
                "data": [657689, 590978, 846789]
            }
        ]
    }
    return JsonResponse(data)

@api_view(['GET'])
def chart5(request):
    data = {
         "labels": ["Table1", "Table2", "Table3"],
        "datasets": [
            {
                "data": [657689, 590978, 846789]
            }
        ]
    }
    return JsonResponse(data)

@api_view(['GET'])
def chart6(request):
    data = {
         "labels": ["Table1", "Table2", "Table3"],
        "datasets": [
            {
                "data":[657689, 590978, 846789]
            }
        ]
    }
    return JsonResponse(data)

@api_view(['GET'])
def chart7(request):
    data = {
       "labels": ["Region1", "Region2", "Region3"],
        "datasets": [
            {
                "data": [657689, 590978, 846789]
            }
        ]
    }
    return JsonResponse(data)

@api_view(['GET'])
def chart8(request):
    data = {
        "labels": ["Region1", "Region2", "Region3"],
        "datasets": [
            {
                "data": [657689, 590978, 846789]
            }
        ]
    }
    return JsonResponse(data)