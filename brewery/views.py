from django.shortcuts import render
from rest_framework import viewsets, views
from rest_framework.parsers import FileUploadParser, MultiPartParser, FormParser
from brewery import serializers
from django.contrib.auth.models import User
from rest_framework.response import Response
from brewery import models
from brewery.xml import DeserializeRecipeXML


class UploadRecipeViewSet(viewsets.ViewSet):
    """
    This viewset allows for the uploading of a BeerXML 1.0 Standard recipe http://beerxml.com.  Supports `form-data` and `x-www-form-urlencoded` in a post.  Will return the hyperlink to the recipes created.
    """
    #parser_classes = (FileUploadParser,)
    parser_classes = (FormParser,MultiPartParser,)
    #base_name = "UploadRecipe"
    def create(self, request):
        file_obj = request.data['file'] #.data['file']
        print("Got to Create")
        return DeserializeRecipeXML(file_obj)


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """
    This viewset automatically provides `list` and `detail` actions.
    """
    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer
    
class RecipeViewSet(viewsets.ModelViewSet):
    """
    This viewset creates the actions for the Recipe Model
    """
    queryset = models.Recipe.objects.all()
    serializer_class = serializers.RecipeSerializer
    
class MiscViewSet(viewsets.ModelViewSet):
    """
    This viewset provides the actions for the Misc items 
    """
    queryset = models.Misc.objects.all()
    serializer_class = serializers.MiscSerializer
    
class Misc_usageViewSet(viewsets.ModelViewSet):
    """
    This viewset provides the actions for the Misc_usage items 
    """
    queryset = models.Misc_usage.objects.all()
    serializer_class = serializers.Misc_usageSerializer
    
class HopViewSet(viewsets.ModelViewSet):
    """
    This viewset provides the actions for the Hop items 
    """
    queryset = models.Hop.objects.all()
    serializer_class = serializers.HopSerializer
    
class Hop_usageViewSet(viewsets.ModelViewSet):
    """
    This viewset provides the actions for the Hop_usage items 
    """
    queryset = models.Hop_usage.objects.all()
    serializer_class = serializers.Hop_usageSerializer
    
class YeastViewSet(viewsets.ModelViewSet):
    """
    This viewset provides the actions for the Yeast items 
    """
    queryset = models.Yeast.objects.all()
    serializer_class = serializers.YeastSerializer
    
class Yeast_usageViewSet(viewsets.ModelViewSet):
    """
    This viewset provides the actions for the Yeast_usage items 
    """
    queryset = models.Yeast_usage.objects.all()
    serializer_class = serializers.Yeast_usageSerializer
    
class FermentableViewSet(viewsets.ModelViewSet):
    """
    This viewset provides the actions for the Yeast items 
    """
    queryset = models.Fermentable.objects.all()
    serializer_class = serializers.FermentableSerializer
    
class Fermentable_usageViewSet(viewsets.ModelViewSet):
    """
    This viewset provides the actions for the Yeast_usage items 
    """
    queryset = models.Fermentable_usage.objects.all()
    serializer_class = serializers.Fermentable_usageSerializer
    
class WaterViewSet(viewsets.ModelViewSet):
    """
    This viewset provides the actions for the Yeast items 
    """
    queryset = models.Water.objects.all()
    serializer_class = serializers.WaterSerializer
    
class Water_usageViewSet(viewsets.ModelViewSet):
    """
    This viewset provides the actions for the Yeast_usage items 
    """
    queryset = models.Water_usage.objects.all()
    serializer_class = serializers.Water_usageSerializer
    
class EquipmentViewSet(viewsets.ModelViewSet):
    """
    This viewset provides the actions for the Yeast items 
    """
    queryset = models.Equipment.objects.all()
    serializer_class = serializers.EquipmentSerializer
    
class StyleViewSet(viewsets.ModelViewSet):
    """
    This viewset provides the actions for the Yeast items 
    """
    queryset = models.Style.objects.all()
    serializer_class = serializers.StyleSerializer

class Mash_profileViewSet(viewsets.ModelViewSet):
    """
    This viewset provides the actions for the Yeast items 
    """
    queryset = models.Mash_profile.objects.all()
    serializer_class = serializers.Mash_profileSerializer
    
class Mash_profile_usageViewSet(viewsets.ModelViewSet):
    """
    This viewset provides the actions for the Yeast items 
    """
    queryset = models.Mash_profile_usage.objects.all()
    serializer_class = serializers.Mash_profile_usageSerializer
    
class Mash_stepViewSet(viewsets.ModelViewSet):
    """
    This viewset provides the actions for the Yeast items 
    """
    queryset = models.Mash_step.objects.all()
    serializer_class = serializers.Mash_stepSerializer
    
class Mash_step_usageViewSet(viewsets.ModelViewSet):
    """
    This viewset provides the actions for the Yeast items 
    """
    queryset = models.Mash_step_usage.objects.all()
    serializer_class = serializers.Mash_step_usageSerializer
    
class Fermentation_profileViewSet(viewsets.ModelViewSet):
    """
    This viewset provides the actions for the Yeast items 
    """
    queryset = models.Fermentation_profile.objects.all()
    serializer_class = serializers.Fermentation_profileSerializer

class Fermentation_stepViewSet(viewsets.ModelViewSet):
    """
    This viewset provides the actions for the Yeast items 
    """
    queryset = models.Fermentation_step.objects.all()
    serializer_class = serializers.Fermentation_stepSerializer
    
class FermenterViewSet(viewsets.ModelViewSet):
    """
    This viewset provides the actions for the Yeast items 
    """
    queryset = models.Fermenter.objects.all()
    serializer_class = serializers.FermenterSerializer
    
class ChamberViewSet(viewsets.ModelViewSet):
    """
    This viewset provides the actions for the Yeast items 
    """
    queryset = models.Chamber.objects.all()
    serializer_class = serializers.ChamberSerializer
    
class TapViewSet(viewsets.ModelViewSet):
    """
    This viewset provides the actions for the Yeast items 
    """
    queryset = models.Tap.objects.all()
    serializer_class = serializers.TapSerializer
    
class KegeratorViewSet(viewsets.ModelViewSet):
    """
    This viewset provides the actions for the Yeast items 
    """
    queryset = models.Kegerator.objects.all()
    serializer_class = serializers.KegeratorSerializer
    
class DeviceViewSet(viewsets.ModelViewSet):
    """
    This viewset provides the actions for the Yeast items 
    """
    queryset = models.Device.objects.all()
    serializer_class = serializers.DeviceSerializer
    
class SensorViewSet(viewsets.ModelViewSet):
    """
    This viewset provides the actions for the Yeast items 
    """
    queryset = models.Sensor.objects.all()
    serializer_class = serializers.SensorSerializer
    
class SensorAssignmentViewSet(viewsets.ModelViewSet):
    """
    This viewset provides the actions for the Yeast items 
    """
    queryset = models.SensorAssignment.objects.all()
    serializer_class = serializers.SensorAssignmentSerializer
    
class AlertViewSet(viewsets.ModelViewSet):
    """
    This viewset provides the actions for alerts
    """
    queryset = models.Alert.objects.all()
    serializer_class = serializers.AlertSerializer