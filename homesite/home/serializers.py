from rest_framework import serializers
from .models import Homes
from .models import Bricks

class home_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Homes
        fields = '__all__'
