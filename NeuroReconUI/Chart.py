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
                "data": [456723, 587611, 129990]
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
                "data": [242345, 198768, 128769]
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
                "data": [128767, 342233, 665543]
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
                "data": [342345, 123231, 453421]
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
                "data": [124345, 342321, 453212]
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
                "data": [223454, 432123, 542132]
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
                "data": [453212, 543212, 124562]
            }
        ]
    }
    return JsonResponse(data)