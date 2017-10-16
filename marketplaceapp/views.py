# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render

def home(request):
    return render(request, 'home.html', {})

def gig_details(request, id):
    return render(request, 'gig_details.html', {})
