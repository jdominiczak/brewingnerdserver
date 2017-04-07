from django.contrib.auth.models import User
from rest_framework import serializers
from brewery import models 
from brewery import signals
from generic_relations.relations import GenericRelatedField

class AssignmentRelatedField(serializers.RelatedField):
    """
    A custom field to use for the `tagged_object` generic relationship.
    """
    def to_native(self, value):
            """
            Serialize bookmark instances using a bookmark serializer,
            and note instances using a note serializer.
            """
            if isinstance(value, Fermenter):
                serializer = FermenterSerializer(value)
            elif isinstance(value, Chamber):
                serializer = ChamberSerializer(value)
            else:
                raise Exception('Unexpected type of tagged object')

            return serializer.data


class UserSerializer(serializers.HyperlinkedModelSerializer): 
    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'first_name', 'last_name')
        #fields = '__all__'
        
class RecipeSerializer(serializers.HyperlinkedModelSerializer):
    type = serializers.ChoiceField(choices=['All Grain', 'Partial Mash', 'Extract'])
    miscs = serializers.HyperlinkedRelatedField(many=True, read_only=True, view_name='misc_usage-detail')
    hops = serializers.HyperlinkedRelatedField(many=True, read_only=True, view_name='hop_usage-detail')
    yeasts = serializers.HyperlinkedRelatedField(many=True, read_only=True, view_name='yeast_usage-detail')
    fermentables = serializers.HyperlinkedRelatedField(many=True, read_only=True, view_name='fermentable_usage-detail')
    waters = serializers.HyperlinkedRelatedField(many=True, read_only=True, view_name='water_usage-detail')
    mash_profile = serializers.HyperlinkedRelatedField(many=True, read_only=True, view_name='mash_profile_usage-detail')
    est_ibu_method = serializers.ChoiceField(choices=['Rager', 'Tinseth', 'Garetz'])
    
    #fermentation_profile = serializers.HyperlinkedRelatedField(many=True, read_only=True, view_name='fermentation_profile-detail')
    class Meta:
        model = models.Recipe
        fields = '__all__'   
            
class MiscSerializer(serializers.HyperlinkedModelSerializer):
    type = serializers.ChoiceField(choices=['Spice', 'Fining', 'Water Agent', 'Herb', 'Flavor', 'Other'])
    
    class Meta:
        model = models.Misc
        fields = '__all__'
        
class Misc_usageSerializer(serializers.HyperlinkedModelSerializer):
    use = serializers.ChoiceField(choices=['Boil', 'Mash', 'Primary', 'Secondary', 'Bottling'])
    class Meta:
        model = models.Misc_usage
        fields = '__all__'
        
class HopSerializer(serializers.HyperlinkedModelSerializer):
    type = serializers.ChoiceField(choices=['Bittering', 'Aroma', 'Both'])
    
    class Meta:
        model = models.Hop
        fields = '__all__'
        
class Hop_usageSerializer(serializers.HyperlinkedModelSerializer):
    use = serializers.ChoiceField(choices=['Boil', 'Dry Hop', 'Mash', 'First Wort', 'Aroma'])
    form = serializers.ChoiceField(choices=['Pellet', 'Plug', 'Leaf', 'Hash'])
    class Meta:
        model = models.Hop_usage
        fields = '__all__'
        
class YeastSerializer(serializers.HyperlinkedModelSerializer):
    type = serializers.ChoiceField(choices=['Ale', 'Lager', 'Wheat', 'Wine', 'Champagne'])
    form = serializers.ChoiceField(choices=['Liquid', 'Dry', 'Slant', 'Culture'])
    flocculation = serializers.ChoiceField(choices=['Low', 'Medium', 'High', 'Very High'])
    class Meta:
        model = models.Yeast
        fields = '__all__'
        
class Yeast_usageSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Yeast_usage
        fields = '__all__'
        
class FermentableSerializer(serializers.HyperlinkedModelSerializer):
    type = serializers.ChoiceField(choices=['Grain', 'Sugar', 'Extract', 'Dry Extract', 'Adjunct'])
    class Meta:
        model = models.Fermentable
        fields = '__all__'
        
class Fermentable_usageSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Fermentable_usage
        fields = '__all__'
        
class WaterSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Water
        fields = '__all__'
        
class Water_usageSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Water_usage
        fields = '__all__'
        
class EquipmentSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Equipment
        fields = '__all__'
        
class StyleSerializer(serializers.HyperlinkedModelSerializer):
    type = serializers.ChoiceField(choices=['Lager', 'Ale', 'Mead', 'Wheat', 'Mixed', 'Cider'])
    class Meta:
        model = models.Style
        fields = '__all__'
        
        
class Mash_profileSerializer(serializers.HyperlinkedModelSerializer):
    mash_steps = serializers.HyperlinkedRelatedField(many=True, read_only=True, view_name='mash_step-detail')
    class Meta:
        model = models.Mash_profile
        fields = '__all__'
        
class Mash_profile_usageSerializer(serializers.HyperlinkedModelSerializer):
    mash_steps = serializers.HyperlinkedRelatedField(many=True, read_only=True, view_name='mash_step_usage-detail')
    class Meta:
        model = models.Mash_profile_usage
        fields = '__all__'
        
class Mash_stepSerializer(serializers.HyperlinkedModelSerializer):
    type = serializers.ChoiceField(choices=['Infusion', 'Temperature', 'Decoction'])
    class Meta:
        model = models.Mash_step
        fields = '__all__'
        
class Mash_step_usageSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Mash_step_usage
        fields = '__all__'
        
class Fermentation_profileSerializer(serializers.HyperlinkedModelSerializer):
    fermentation_steps = serializers.HyperlinkedRelatedField(many=True, read_only=True, view_name='fermentation_step-detail')
    class Meta:
        model = models.Fermentation_profile
        fields = '__all__'
        
class Fermentation_stepSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Fermentation_step
        fields = '__all__'
        
class FermenterSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Fermenter
        fields = '__all__'
        
class ChamberSerializer(serializers.HyperlinkedModelSerializer):
    operation_type = serializers.ChoiceField(choices=['Off', 'Automatic', 'Manual'])
    class Meta:
        model = models.Chamber
        fields = '__all__'
        
class TapSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Tap
        fields = '__all__'
        
class KegeratorSerializer(serializers.HyperlinkedModelSerializer):
    operation_type = serializers.ChoiceField(choices=['Off', 'Automatic', 'Manual'])
    class Meta:
        model = models.Kegerator
        fields = '__all__'
        
class DeviceSerializer(serializers.HyperlinkedModelSerializer):
    sensors = serializers.HyperlinkedRelatedField(many=True, read_only=True, view_name='sensor-detail')
    class Meta:
        model = models.Device
        fields = '__all__'
        
class SensorSerializer(serializers.HyperlinkedModelSerializer):
    type = serializers.ChoiceField(choices=['Temperature', 'Pressure', 'Flow', 'Gravity', 'Heat_On', 'Cool_On'])
    sensor_assignment = serializers.HyperlinkedRelatedField(many=True, read_only=True, view_name='sensorassignment-detail')
    class Meta:
        model = models.Sensor
        fields = '__all__'
        
class SensorAssignmentSerializer(serializers.HyperlinkedModelSerializer):
    assignment = GenericRelatedField({
            models.Tap: serializers.HyperlinkedRelatedField(
                queryset = models.Tap.objects.all(),
                view_name='tap-detail',
            ),
            models.Kegerator: serializers.HyperlinkedRelatedField(
                queryset = models.Kegerator.objects.all(),
                view_name='kegerator-detail',
            ),
            models.Fermenter: serializers.HyperlinkedRelatedField(
                queryset = models.Fermenter.objects.all(),
                view_name='fermenter-detail',
            ),
            models.Chamber: serializers.HyperlinkedRelatedField(
                queryset = models.Chamber.objects.all(),
                view_name='chamber-detail',
            ),
        })
    class Meta:
        model = models.SensorAssignment
        fields = ('created_at', 'modified_at','start_datetime', 'end_datetime', 'sensor', 'assignment' )
        #fields = '__all__'
        
class AlertSerializer(serializers.HyperlinkedModelSerializer):
    target = GenericRelatedField({
            models.Tap: serializers.HyperlinkedRelatedField(
                queryset = models.Tap.objects.all(),
                view_name='tap-detail',
            ),
            models.Kegerator: serializers.HyperlinkedRelatedField(
                queryset = models.Kegerator.objects.all(),
                view_name='kegerator-detail',
            ),
            models.Fermenter: serializers.HyperlinkedRelatedField(
                queryset = models.Fermenter.objects.all(),
                view_name='fermenter-detail',
            ),
            models.Chamber: serializers.HyperlinkedRelatedField(
                queryset = models.Chamber.objects.all(),
                view_name='chamber-detail',
            ),
        })
    class Meta:
        model = models.SensorAssignment
        fields = ('created_at', 'modified_at','title', 'description', 'acknowledged', 'target' )
        #fields = '__all__'
