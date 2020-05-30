
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

import re
from joblib import dump, load

def processing_text(texto):
    # Remove all the special characters
    processed_feature = re.sub(r'\W', ' ', str(texto))
    # remove all single characters
    processed_feature= re.sub(r'\s+[a-zA-Z]\s+', ' ', processed_feature)
    # Remove single characters from the start
    processed_feature = re.sub(r'\^[a-zA-Z]\s+', ' ', processed_feature) 
    # Removing prefixed 'b'
    processed_feature = re.sub(r'^b\s+', '', processed_feature)
    # Converting to Lowercase
    return processed_feature

@api_view(['GET', 'POST'])
def new_evento(request):
    if request.method == 'GET':
        text= request.GET['data']
        tfidfquery = load('tfidfquery') 
        text_procesing=processing_text(text).lower()
        features2 = tfidfquery.transform([text_procesing])
        clf= load('semmtiments_analisys.joblib') 
        response=clf.predict(features2)
        return Response({'result':response}, status=status.HTTP_201_CREATED)