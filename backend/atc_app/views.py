from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.template import loader
from .models import *
from .serializers import *
from rest_framework import generics
from rest_framework import viewsets
from req_handler.models import *
import json




# general error message 
error_msg = {'team_id':'wbPGjYCpmLa92Pjwc25fCvRk6fTPffub',
                            'obj_type':'',
                            'id':'',
                            'error':''}

def gateRequest(request):
    package = request.body.decode('utf-8')
    
    new_request = Request(package, 'gate')
        
    # check for conflicts and insert new data
    if new_request.duplicate_gate():
      error_msg['obj_type'] = 'GATE'
      error_msg['id'] = json.loads(package)['gate']
      error_msg['error'] = 'DUPLICATE_GATE'
      return HttpResponse(json.dumps(error_msg), request)
    
    elif new_request.gate_is_too_small():
      error_msg['obj_type'] = 'GATE'
      error_msg['id'] = json.loads(package)['gate']
      error_msg['error'] = 'TOO_SMALL_GATE'
      return HttpResponse(json.dumps(error_msg), request)
    
    elif new_request.duplicate_runway():
      error_msg['obj_type'] = 'RUNWAY'
      error_msg['id'] = json.loads(package)['runway']
      error_msg['error'] = 'DUPLICATE_RUNWAY'
      return HttpResponse(json.dumps(error_msg), request)
    
    elif new_request.runway_is_too_small():
      error_msg['obj_type'] = 'RUNWAY'
      error_msg['id'] = json.loads(package)['runway']
      error_msg['error'] = 'TOO_SMALL_RUNWAY'
      return HttpResponse(json.dumps(error_msg), request)
    else: 
      # success / no conflicts
      new_request.insert_new_gate_data()
      
      
def passengerRequest(request):
    package = request.body.decode('utf-8')
    new_request = Request(package, 'pass_count')
    
    if new_request.too_many_passengers():
      error_msg['obj_type'] = 'PLANE'
      error_msg['id'] = json.loads(package)['plane']
      error_msg['error'] = 'TOO_MANY_PASSENGERS'
      return HttpResponse(json.dumps(error_msg), request) 
    else:
      # success
      new_request.insert_new_passenger_data()
      
      
def takeOffRequest(request):
    package = request.body.decode('utf-8')
    new_request = Request(package, 'plane')
    
    if new_request.collision_imminent():
      error_msg['obj_type'] = 'PLANE'
      error_msg['id'] = json.loads(package)['plane']
      error_msg['error'] = 'COLLISION_IMMINENT'
      return HttpResponse(json.dumps(error_msg), request)
    else:
      # success
      new_request.insert_new_plane_data()




def home(request):
    airports = Airport.objects.all()
    return render(request, 'home.html', {'airports': airports})

def addAirport(request):
  template = loader.get_template('addAirport.html')
  return HttpResponse(template.render({}, request))

def addrecord(request):
  name = request.POST['airportname']
  xcoord = request.POST['xcoord']
  ycoord = request.POST['ycoord']
  
  airport = Airport(name=name, x=xcoord, y=ycoord)
  airport.save()
  return HttpResponseRedirect(reverse('home'))
def deleteAirport(request, id):
  airport = Airport.objects.get(id=id)
  airport.delete()
  return HttpResponseRedirect(reverse('home'))

def updateAirport(request, id):
  airport = Airport.objects.get(id=id)
  template = loader.get_template('updateAirport.html')
  context = {
    'airport': airport,
  }
  return HttpResponse(template.render(context, request))
def updaterecord(request, id):
  name = request.POST['airportname']
  xcoord = request.POST['xcoord']
  ycoord = request.POST['ycoord']
  airport = Airport.objects.get(id=id)
  airport.name = name
  airport.x = xcoord
  airport.y = ycoord
  airport.save()
  return HttpResponseRedirect(reverse('home'))
class AirportViewSet(viewsets.ModelViewSet):
    queryset = Airport.objects.all().order_by('name')
    serializer_class = Airport


class AirportCreate(generics.CreateAPIView):
    # API endpoint that allows creation of a new Airport
    queryset = Airport.objects.all(),
    serializer_class = AirportSerializer
class AirportList(generics.ListAPIView):
    # API endpoint that allows Airports to be viewed.
    queryset = Airport.objects.all()
    serializer_class = AirportSerializer
class AirportDetail(generics.RetrieveAPIView):
    # API endpoint that returns a single Airport by pk.
    queryset = Airport.objects.all()
    serializer_class = AirportSerializer

class AirportUpdate(generics.RetrieveUpdateAPIView):
    # API endpoint that allows a Airport record to be updated.
    queryset = Airport.objects.all()
    serializer_class = AirportSerializer

class AirportDelete(generics.RetrieveUpdateAPIView):
    # API endpoint that allows a Airport record to be updated.
    queryset = Airport.objects.all()
    serializer_class = AirportSerializer



