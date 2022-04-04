"""AMS URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from . import views

urlpatterns = [
    path('', views.manufacturerHome, name="manufacturerHome"),
    path('blueprint/', views.createBlueprint),
    path('blueprint_operation/', views.blueprint_operation),
    path('blueprint-<int:id>/', views.editBlueprint),
    path('initiate_order/', views.initiateOrder),
    path('order_created/', views.order_created),
    path('balance/', views.addBalance),
    path('add_balance/', views.add_balance),
    path('wholesale_deal-<int:id>/', views.deal),
    path('wholesale_accept/', views.process_deal),
]