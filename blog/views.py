from django.shortcuts import render
from django.contrib.auth import get_user_model
from keras import backend
from keras.models import load_model
import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets
from rest_framework.decorators import api_view
from django.conf import settings
from django.views.generic import View
from keras import backend as K 

User = get_user_model()

   
def fill_missing(past_data):
        for row in range(past_data.shape[0]):
            for col in range(past_data.shape[1]):
                if np.isnan(past_data[row, col]):
                    i = 1
                    missing_next = past_data[row + i, col]
                    while(np.isnan(missing_next)):
                        i += 1
                        missing_next = past_data[row + i, col]
                    past_data[row, col] = past_data[row - 1, col] + ((missing_next - past_data[row - 1, col]) / (i+1))
                    
def data_Predict(request,*args,**kwargs):
        # if request.method==POST:
        past_data = pd.read_csv('PoultryData.csv')
        regressor = load_model('lstm-chicken.h5')
        date=past_data['Date'].iloc[-150:]
        date=pd.to_datetime(date).tolist()
        date2=past_data["Date"].iloc[-1]
        date2=pd.Series(pd.date_range(date2, periods=53, freq='7D'))
        date2=date2[1:].tolist()    
        past_data.set_index(['Date'], inplace= True)
        fill_missing(past_data.values)
        past_data = past_data.round(2)
        past_price = past_data.loc[:]['Harga Ladang'].round(2)
        date=date + date2
        date = list(map(str, date))
        for i in range (0, len(date)):
            date[i] = date[i].split(' ')[0]
        feedin_price = []
        feedin_price.append(past_price[(len(past_price)-52):])
        feedin_price = np.array(feedin_price)

        sc = MinMaxScaler(feature_range = (0, 1))
        feedin_price_scaled = sc.fit_transform(feedin_price.reshape(-1, 1))
        feedin_price_scaled = feedin_price_scaled.reshape(1, feedin_price_scaled.shape[0], 1)
        
        future_price = regressor.predict(feedin_price_scaled)
        future_price = sc.inverse_transform(future_price)
        future_price = future_price.reshape(-1 ,1)
        future_price=future_price.round(2).tolist()
        past_price= past_price.tolist() + future_price #so I get total_price and date(complete)
        
        past_price = list(map(str, past_price))

        for i in range (1, len(past_price)):
            past_price[i] = past_price[i].replace('[', '').replace(']', '')


        data={
            'labels':','.join(date),
            'default': ','.join(past_price)
        }
        K.clear_session()
        return JsonResponse(data)
    

class Predict(View):
    def get(self,request, *args, **kwargs):
            return render(request,'blog/base.html')
    