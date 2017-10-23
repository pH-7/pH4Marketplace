from django.forms import ModelForm
from marketplaceapp.models import Gig

class GigForm(ModelForm):
    class Meta:
        model = Gig
        fields = ['title', 'category', 'price', 'photo', 'status']
