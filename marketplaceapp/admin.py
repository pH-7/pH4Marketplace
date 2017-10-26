# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from marketplaceapp.models import Profile, Gig, Purchase, Review
from django.contrib import admin

admin.site.register(Profile)
admin.site.register(Gig)
admin.site.register(Purchase)
admin.site.register(Review)
