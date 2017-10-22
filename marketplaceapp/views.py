# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, redirect

from marketplace.settings import MEDIA_URL
from marketplaceapp.models import Gig

def home(request):
    gigs = Gig.objects.filter(status=True)
    return render(request, 'home.html', {'gigs': gigs, 'media_url': MEDIA_URL})

def gig_details(request, id):
    try:
        gig = Gig.objects.get(id=id)
    except Gig.DoesNotExist:
        return redirect('/')

    return render(request, 'gig_details.html', {'gig': gig, 'media_url': MEDIA_URL})
