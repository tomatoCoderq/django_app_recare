from calendar import c


from django.forms import ModelForm   
from .models import RobotsCode

class CodeInput(ModelForm):
    class Meta:
        model = RobotsCode
        fields = ['code']