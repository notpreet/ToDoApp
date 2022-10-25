from django.contrib.auth import authenticate
from django.shortcuts import render, redirect

from django.contrib.auth import logout, login
from django.contrib.auth.models import User, auth
from .models import UserData, Tasks



# Create your views here.
