from rest_framework import serializers
from .models import Table

class TableSerializer(serializers.ModelSerializer):
    qr_code = serializers.ImageField(read_only=True)

    class Meta:
        model = Table
        fields = ('id', 'qr_code')
