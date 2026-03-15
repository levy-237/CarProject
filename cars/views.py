from rest_framework import generics

from .models import Car
from .serializers import CarSerializer

class CarCreateAndList(generics.ListCreateAPIView):
    queryset = Car.objects.all()
    serializer_class = CarSerializer
    

class CarViewAndUpdate(generics.RetrieveUpdateAPIView):
    queryset = Car.objects.all()
    serializer_class = CarSerializer
    
