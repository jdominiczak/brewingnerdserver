from django.shortcuts import render
from rest_framework import viewsets, views, status
from rest_framework.parsers import FileUploadParser, MultiPartParser, FormParser
from rest_framework.reverse import reverse
from brewery import serializers
from django.contrib.auth.models import User
from rest_framework.response import Response
from brewery import models, util
from brewery.xml import DeserializeRecipeXML
from django.forms.utils import flatatt
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import list_route
from datetime import datetime
from django.db.models import DateTimeField
import json



#class UploadRecipeViewSet(viewsets.ViewSet):
#    """
#    This viewset allows for the uploading of a BeerXML 1.0 Standard recipe http://beerxml.com.  Supports `form-data` and `x-www-form-urlencoded` in a post.  Will return the hyperlink to the recipes created.
#    """
#    #parser_classes = (FileUploadParser,)
#    parser_classes = (FormParser,MultiPartParser,)
#    #base_name = "UploadRecipe"
#    def create(self, request):
#        file_obj = request.data['file'] #.data['file']
#        print("Got to Create")
#        return DeserializeRecipeXML(file_obj, request)

#class UploadDataViewSet(viewsets.ViewSet):
#    """
#    This viewset allows for importing data points from an IOT device
#    """
#    def create(self, request):
#        print(request.data["key"])
#        return Response("urls", status=400)

class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """
    This viewset automatically provides `list` and `detail` actions.
    """
    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer
    
class RecipeViewSet(viewsets.ModelViewSet):
    """
    This viewset creates the actions for the Recipe Model.
    Query Parameters: type (filter by type), search (search by recipe name)
    """
    #queryset = models.Recipe.objects.all()
    serializer_class = serializers.RecipeSerializer


    #### Handle XML Upload
    parser_classes = (FormParser,MultiPartParser,)
    @list_route(methods=['post'])
    def uploadxml(self, request):
        file_obj = request.data['file'] #.data['file']
        print("Got to Create")
        return DeserializeRecipeXML(file_obj, request)

    def get_queryset(self):
        queryset = models.Recipe.objects.all().order_by('-created_at')
        type = self.request.query_params.get('type')
        search = self.request.query_params.get('search')
        if type:
            queryset = queryset.filter(type=type)
        if search:
            queryset = queryset.filter(name__icontains=search)
        return queryset
    
    def list(self, request):
        serializer = serializers.RecipeListSerializer(self.get_queryset(), many=True, context={'request':request})
        return Response(serializer.data)
        
    
    
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
    
class RecipeAssignmentViewSet(viewsets.ModelViewSet):
    """
    This viewset provides the actions for the Yeast items 
    """
    #queryset = models.RecipeAssignment.objects.all()
    serializer_class = serializers.RecipeAssignmentSerializer
    
    def get_queryset(self):
        queryset = models.RecipeAssignment.objects.all()
        active = self.request.query_params.get('active')
        #search = self.request.query_params.get('search')
        if active is not None:
            activeBool = util.toBool(active)
            if activeBool:
                # Filter for those with end as null
                queryset = queryset.filter(end_datetime__isnull=True)
            else:
                queryset = queryset.filter(end_datetime__isnull=False)
        return queryset
    
class AlertViewSet(viewsets.ModelViewSet):
    """
    This viewset provides the actions for alerts
    """
    queryset = models.Alert.objects.all()
    serializer_class = serializers.AlertSerializer

class DataViewSet(viewsets.ModelViewSet):
    """
    This viewset provides the actions for data handles filter by `sensor_id`.  `datetime_start` and `datetime_end` are used to get a subset of the datapoints. 
    
    Time fields should be of type 2017-04-12T15:25:30Z
    
    */data/upload/* should be a post json of type {'device_serial':'device_serial','datapoints':[ {'unit':'unitval', 'serial':'sensor_serial_here', 'data':'datapoint_val', 'timestamp':'2017-04-12T15:25:30Z'}, ... ]}
    """
    #queryset = models.Data.objects.all()
    serializer_class = serializers.DataSerializer
    
    def get_queryset(self):
        queryset = models.Data.objects.all()
        sensor_id = self.request.query_params.get("sensor_id")
        sensor_serial = self.request.query_params.get("sensor_serial")
        datetime_start = self.request.query_params.get("datetime_start")
        datetime_end = self.request.query_params.get("datetime_end")
        if sensor_id:
            queryset=queryset.filter(sensor=sensor_id)
        if datetime_start:
            queryset = queryset.filter(timestamp__gte=datetime_start)
        if datetime_end:
            print(datetime_end)
            if datetime_end.lower() is not "now":
                queryset = queryset.filter(timestamp__lte=datetime_end)
        return queryset
        
    @list_route(methods=['post'])
    def upload(self, request):
        # handle the upload from a device
        json_data = json.loads(request.body.decode('utf-8'))
        try:
            #Find the device with this serial number
            device_serial = json_data['device_serial']
            device, device_created = models.Device.objects.get_or_create(serial=device_serial)
            if device_created:
                ### TODO: Kick off Celery task to create new alert
                alert = serializers.AlertSerializer(data={'title':'New Device found on network', 'description': 'New Device with serial "' + device_serial + '" was first seen on ' + datetime.now().strftime("%B %d, %Y"), 'target': reverse('device-detail', args=[device.id], request=request) })
                if alert.is_valid():
                    alert.save()
                else:
                    print(str(alert.errors))
                
            print("Device Created:" + str(device_created))
            #data_array = json_data['datapoints']
            for datapoint in json_data['datapoints']:
                print("Unit:" + datapoint["unit"] + " Serial:" + datapoint["serial"] + " Data:" + datapoint["data"] + " Timestamp:" + datapoint["timestamp"])
                sensor, sensor_created = models.Sensor.objects.get_or_create(serial=datapoint['serial'], device=device, unit=datapoint['unit'])
                if sensor_created:
                    alert = serializers.AlertSerializer(data={'title':'New Sensor found on network', \
                        'description': 'New Sensor with serial "' + datapoint['serial'] + '" was first seen on ' + datetime.now().strftime("%B %d, %Y"), \
                        'target': reverse('sensor-detail', args=[sensor.id], request=request) })
                    if alert.is_valid():
                        alert.save()
                    else:
                        print(str(alert.errors))
                print("Sensor Created:" + str(sensor_created))    
                datapoint.pop('serial')
                datapoint['sensor'] = reverse('sensor-detail', args=[sensor.id], request=request)
                
                point = serializers.DataSerializer(data=datapoint)
                if point.is_valid():
                    point.save()
                else:
                    print("Bad Serialization: " + str(point.errors) + " Request:" + str(request.body.decode('utf-8')))
                    return Response(data=point.errors, status=status.HTTP_400_BAD_REQUEST)
                
        except KeyError:
            #malformed datapost!
            print("Malformed Request - Request:" + request.body.decode('utf-8'))
            return Response(data={'Error':'Malformed Request'}, status=status.HTTP_400_BAD_REQUEST)
            
        return Response(status=status.HTTP_201_CREATED)