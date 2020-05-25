
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
from pyspark.sql import SparkSession
from pyspark.sql import functions as f
from pyspark.sql.window import Window
from pyspark.ml.feature import Tokenizer, RegexTokenizer
from pyspark.ml.feature import StopWordsRemover
from pyspark.ml.feature import HashingTF, IDF
from pyspark.ml.feature import IDFModel
from pyspark.ml import PipelineModel
@api_view(['GET', 'POST'])
def new_evento(request):
    if request.method == 'GET':
        nombre_data= request.GET['data']
        print(nombre_data)
        newText=nombre_data
        spark =  SparkSession.builder.appName("Taller").getOrCreate()
        sentenceDataFrame = spark.createDataFrame([
            (0, newText),
        ], ["label", "text"])
        tokenizer = Tokenizer(inputCol="text", outputCol="words")
        regexTokenizer = RegexTokenizer(inputCol="text", outputCol="words", pattern="\\W")
            # alternatively, pattern="\\w+", gaps(False)
        regexTokenized2 = regexTokenizer.transform(sentenceDataFrame)

        remover2 = StopWordsRemover(inputCol="words", outputCol="filtered")
        remover2=remover2.transform(regexTokenized2)

        hashingTF = HashingTF(inputCol="filtered", outputCol="rawFeatures", numFeatures=2**16)
        featurizedData2 = hashingTF.transform(remover2)
        idfModel2=IDFModel.load('/home/jefferson/Big Data/Corte3/idfmodel')

        rescaledData2 = idfModel2.transform(featurizedData2)
        sameModel = PipelineModel.load('/home/jefferson/Big Data/Corte3/sentiments_modelLG')
        predictions2 = sameModel.transform(rescaledData2)
        result_data=predictions2.select("prediction", "indexedLabel").collect()
        prediction=result_data[0][0]
        result_text=''
        if prediction==0.0:
            result_text='positive'
        elif prediction==2.0:
            result_text='negative'
        else:
            result_text='neutral'
        print(result_text)

        return Response({'validate':result_text}, status=status.HTTP_201_CREATED)