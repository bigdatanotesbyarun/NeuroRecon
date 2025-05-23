from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import requests
import json

@api_view(['POST'])
def get_kafka_data(request):
    if request.method == "POST":
        try:
            incoming_data = json.loads(request.body)
            
            # Hardcoded JSON data for the response
            response_data = {
               "OrderId": 111,
                "OrderName": "AC",
                "OrderPrice": 10000,
                "OrderDate": "2025-04-10T14:30:00.123",
                "OrderType": "Electronic",
                "AddressLine1": "UP",
                "PinCode": 210120,
                "State": "UP",
                "District": "Pune",
                "PhoneNumber": 0000000000
            }
            # Return the hardcoded JSON data as a response
            return JsonResponse(response_data, status=200)
        
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON format"}, status=400)
           


@api_view(['POST'])
def get_gemfire_data(request):
    if request.method == "POST":
        try:
            # incoming_data = json.loads(request.body)
            # external_api_url = "http://localhost:8000/get_skrecon_data/"
            # headers = {"Content-Type": "application/json"}
            # response = requests.post(external_api_url, json=incoming_data, headers=headers)
            # return JsonResponse(response.json(), status=response.status_code)
            response_data = {
                 "OrderId": 111,
                "OrderName": "AC",
                "OrderPrice": 10000,
                "OrderDate": "2025-04-10T14:30:00.123",
                "OrderType": "Electronic",
                "AddressLine1": "UP",
                "PinCode": 210120,
                "State": "UP",
                "District": "Pune",
                "PhoneNumber": 0000000000
            }
            # Return the hardcoded JSON data as a response
            return JsonResponse(response_data, status=200)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON format"}, status=400)


@api_view(['POST'])
def get_cloud_data(request):
    if request.method == "POST":
        try:
            # incoming_data = json.loads(request.body)
            # external_api_url = "http://localhost:8000/get_skrecon_data/"
            # headers = {"Content-Type": "application/json"}
            # response = requests.post(external_api_url, json=incoming_data, headers=headers)
            # return JsonResponse(response.json(), status=response.status_code)
            response_data = {
                "OrderId": 111,
                "OrderName": "AC",
                "OrderPrice": 10000,
                "OrderDate": "2025-04-10T14:30:00.123",
                "OrderType": "Electronic",
                "AddressLine1": "UP",
                "PinCode": 210120,
                "State": "UP",
                "District": "Pune",
                "PhoneNumber": 0000000000
            }
            # Return the hardcoded JSON data as a response
            return JsonResponse(response_data, status=200)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON format"}, status=400)


@api_view(['POST'])
def get_impala_data(request):
    if request.method == "POST":
        try:
            # incoming_data = json.loads(request.body)
            # external_api_url = "http://localhost:8000/get_skrecon_data/"
            # headers = {"Content-Type": "application/json"}
            # response = requests.post(external_api_url, json=incoming_data, headers=headers)
            # return JsonResponse(response.json(), status=response.status_code)
            response_data =  {
                "OrderId": 111,
                "OrderName": "AC",
                "OrderPrice": 10000,
                "OrderDate": "2025-04-10T14:30:00.123",
                "OrderType": "Electronic",
                "AddressLine1": "UP",
                "PinCode": 210120,
                "State": "UP",
                "District": "Pune",
                "PhoneNumber": 0000000000
            }
            # Return the hardcoded JSON data as a response
            return JsonResponse(response_data, status=200)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON format"}, status=400)

