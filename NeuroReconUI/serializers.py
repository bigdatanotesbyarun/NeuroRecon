from rest_framework import serializers
from .models import ReconVO
from .models import GemfireCountTable1,SKReconTable,GZTable,Jobs

class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model=ReconVO
        fields='__all__'


class GemfireItemSerializer(serializers.ModelSerializer):
    class Meta:
        model=GemfireCountTable1
        fields='__all__'

class SKReconItemSerializer(serializers.ModelSerializer):
    class Meta:
        model=SKReconTable
        fields='__all__'
        
class GreenZoneItemSerializer(serializers.ModelSerializer):
    class Meta:
        model=GZTable
        fields='__all__'

class JobsItemSerializer(serializers.ModelSerializer):
    class Meta:
        model=Jobs
        fields='__all__'

        