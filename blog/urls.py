from django.conf.urls import url
from django.contrib import admin
from . import views

urlpatterns = [
    url(r'^$', views.Predict, name='blog-home'),
    # path('tem/', views.demo_linechart, name='blog-blog'),

    # path('about/', views.about, name='blog-about'),
    url(r'^model/$',views.data_Predict,name="model")
]