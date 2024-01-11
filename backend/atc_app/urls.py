from django.urls import path, include
from atc_app import views
from django.views.generic.base import TemplateView
from .views import *
from rest_framework import routers
router = routers.DefaultRouter()
router.register('Airports', views.AirportViewSet)



urlpatterns = [
    
    # path("", TemplateView.as_view(template_name="home.html"), name="home"),  # Home page
    path("", views.home, name="home"),
    # path("login/", views.login, name="login"),
    path('Airports/create/', AirportCreate.as_view(), name='create-airport'),
    path('Airports/', AirportList.as_view()),
    path('Airports/<int:pk>/', AirportDetail.as_view(), name='retrieve-airport'),
    path('Airports/update/<int:pk>/', AirportUpdate.as_view(), name='update-airport'),
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('addAirport/', views.addAirport, name='addAirports'),
    path('addAirport/addrecord/', views.addrecord, name='addrecord'),
    path('deleteAirport/<int:id>', views.deleteAirport, name='delete-airport'),
    path('updateAirport/<int:id>', views.updateAirport, name='update-airport'),
    path('updateAirport/updaterecord/<int:id>', views.updaterecord, name='updaterecord'),
    # path('delete/<int:pk>/', AirportDelete.as_view(), name='delete-airport')
    
    
    path('atc_app/gate/req/', views.gateRequest, name='gate-request'),
    path('atc_app/passenger/req', views.passengerRequest, name='pass-request'),
    path('atc_app/takeoff/req', views.takeOffRequest, name='takeoff-request'),


]