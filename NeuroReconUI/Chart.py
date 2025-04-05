from django.urls import path
from . import views
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import HttpResponse, JsonResponse

@api_view(['GET'])
def chart1(request):
    data = {
        "labels": ["Product", "Party", "Account"],
        "datasets": [
            {
                "data": [650000, 590000, 800000]
            }
        ]
    }
    return JsonResponse(data)

@api_view(['GET'])
def chart2(request):
    data = {
       "labels": ["Product", "Party", "Account"],
        "datasets": [
            {
                "data": [1200000, 800000, 950000]
            }
        ]
    }
    return JsonResponse(data)

@api_view(['GET'])
def chart3(request):
    data = {
        "labels": ["SMCP", "ACTI", "PARTYI"],
        "datasets": [
            {
                "data": [1500000, 500000, 1000000]
            }
        ]
    }
    return JsonResponse(data)

@api_view(['GET'])
def chart4(request):
    data = {
        "labels": ["SMCP", "ACTI", "PARTYI"],
        "datasets": [
            {
                "data": [500000, 700000, 900000]
            }
        ]
    }
    return JsonResponse(data)

@api_view(['GET'])
def chart5(request):
    data = {
         "labels": ["Product", "Party", "Account"],
        "datasets": [
            {
                "data": [100000, 200000, 300000]
            }
        ]
    }
    return JsonResponse(data)

@api_view(['GET'])
def chart6(request):
    data = {
         "labels": ["Product", "Party", "Account"],
        "datasets": [
            {
                "data": [450000, 600000, 750000]
            }
        ]
    }
    return JsonResponse(data)

@api_view(['GET'])
def chart7(request):
    data = {
       "labels": ["SMCP", "ACTI", "PARTYI"],
        "datasets": [
            {
                "data": [450000, 600000, 750000]
            }
        ]
    }
    return JsonResponse(data)

@api_view(['GET'])
def chart8(request):
    data = {
        "labels": ["SMCP", "ACTI", "PARTYI"],
        "datasets": [
            {
                "data": [450000, 600000, 750000]
            }
        ]
    }
    return JsonResponse(data)