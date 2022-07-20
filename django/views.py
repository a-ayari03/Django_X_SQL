from django.shortcuts import render,redirect
from .models import indicator_room

# Create your views here.

def show(request):
    indicator_rooms = indicator_room.objects.all()
    return render(request,"show.html",{'indicator_room':indicator_rooms})