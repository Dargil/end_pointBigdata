
from rest_framework import viewsets
from .models import *
from .serializer import *
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
import json
import boto3

from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from rest_framework.parsers import JSONParser

@api_view(['GET', 'POST'])
def new_evento(request):
    if request.method == 'GET':
        nombre_data= request.GET['data']
        return Response({'validate':True}, status=status.HTTP_201_CREATED)