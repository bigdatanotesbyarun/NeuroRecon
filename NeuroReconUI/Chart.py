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
                "data": [657689, 590978, 846789]
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
                "data": [657689, 590978, 846789]
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
                "data": [657689, 590978, 846789]
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
                "data": [657689, 590978, 846789]
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
                "data": [657689, 590978, 846789]
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
                "data":[657689, 590978, 846789]
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
                "data": [657689, 590978, 846789]
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
                "data": [657689, 590978, 846789]
            }
        ]
    }
    return JsonResponse(data)