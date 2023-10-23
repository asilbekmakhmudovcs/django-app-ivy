from django.forms import ModelForm
from .models import Room

class RoomForm(ModelForm):
    class Meta:
        model = Room  #create a form based on this class
        fields = '__all__' # in the form it asks for 'all' attributes of this model (name, topic, description etc)
                                 # you can get specific attributes like only room name and description, in that case you use
                                #  ['name', 'description'...] sometimes you dont neeedd to ask for username in forms for ex.
        exclude = ['host', 'participants']