from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.db.models.signals import post_save, post_delete, pre_delete
from django.dispatch import receiver
from brewery import util
from decimal import Decimal
from brewery.tasks import send_alert_notification

# Create your models here.
    
class Equipment(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=100) #Required
    tun_volume = models.DecimalField(decimal_places=4, max_digits=10) #Required
    tun_weight = models.DecimalField(decimal_places=4, max_digits=10) #Required
    tun_specific_heat = models.DecimalField(decimal_places=4, max_digits=10) #Required
    trub_chiller_loss = models.DecimalField(decimal_places=4, max_digits=10) #Required
    evap_rate = models.DecimalField(decimal_places=4, max_digits=10) #Required
    lauter_deadspace = models.DecimalField(decimal_places=4, max_digits=10) #Required
    hop_utilization = models.DecimalField(decimal_places=4, max_digits=10) #Required
    notes = models.TextField(blank=True)
    default_top_up_kettle = models.DecimalField(decimal_places=4, max_digits=10) #Required
    default_top_up_water = models.DecimalField(decimal_places=4, max_digits=10) #Required
    default_boil_size = models.DecimalField(decimal_places=4, max_digits=10) #Required
    default_batch_size = models.DecimalField(decimal_places=4, max_digits=10) #Required
    default_boil_size = models.DecimalField(decimal_places=4, max_digits=10) #Required
    default_mash_efficiency = models.DecimalField(decimal_places=4, max_digits=10, default=0.80) #Required
    default_efficiency = models.DecimalField(decimal_places=4, max_digits=10, default=0.72)

class Style(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=100) #Required
    category = models.CharField(max_length=100) #Required
    category_number = models.IntegerField() #Required
    style_letter = models.CharField(max_length=100) #Required
    style_guide = models.CharField(max_length=100) #Required
    type = models.CharField(max_length=100) #Required
    og_min = models.DecimalField(decimal_places=4, max_digits=10) #Required
    og_max = models.DecimalField(decimal_places=4, max_digits=10) #Required
    fg_min = models.DecimalField(decimal_places=4, max_digits=10) #Required
    fg_max = models.DecimalField(decimal_places=4, max_digits=10) #Required
    ibu_min = models.DecimalField(decimal_places=4, max_digits=10) #Required
    ibu_max = models.DecimalField(decimal_places=4, max_digits=10) #Required
    color_min = models.DecimalField(decimal_places=4, max_digits=10) #Required
    color_max = models.DecimalField(decimal_places=4, max_digits=10) #Required
    carb_min = models.DecimalField(decimal_places=4, max_digits=10, null=True) 
    carb_max = models.DecimalField(decimal_places=4, max_digits=10, null=True) 
    abv_min = models.DecimalField(decimal_places=4, max_digits=10, null=True) 
    abv_max = models.DecimalField(decimal_places=4, max_digits=10, null=True) 
    notes = models.TextField(blank=True)
    profile = models.TextField(blank=True)
    ingredients = models.TextField(blank=True)
    examples = models.TextField(blank=True)

class Fermentation_profile(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=100) #Required
    notes = models.TextField(blank=True)
    
class Fermentation_step(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=100) #Required
    order = models.IntegerField()
    start_temp = models.DecimalField(decimal_places=2, max_digits=10) #Required
    end_temp = models.DecimalField(decimal_places=2, max_digits=10) #Required
    length = models.IntegerField()
    fermentation_profile = models.ForeignKey(Fermentation_profile, related_name='fermentation_steps', on_delete=models.CASCADE) #Required
    
    class Meta:
        unique_together = ('fermentation_profile', 'order')  
        
class Mash_profile(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=100) #Required
    sparge_temp = models.DecimalField(decimal_places=2, max_digits=10, null=True) 
    ph = models.DecimalField(decimal_places=2, max_digits=10, null=True)
    notes = models.TextField(blank=True) 
    
class Mash_profile_usage(models.Model):    
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    grain_temp = models.DecimalField(decimal_places=2, max_digits=10, null=True) 
    tun_temp = models.DecimalField(decimal_places=2, max_digits=10, null=True)
    equip_adjust = models.BooleanField(default=False) #Default False
    mash_profile = models.ForeignKey(Mash_profile, on_delete=models.CASCADE)#Required
    sparge_volume = models.DecimalField(decimal_places=6, max_digits=10, null=True)
    #recipe = models.ForeignKey(Recipe, related_name='mash_profile', on_delete=models.CASCADE)#Required
    
class Mash_step(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=100) #Required
    type = models.CharField(max_length=100) #Required
    step_temp = models.DecimalField(decimal_places=2, max_digits=10) #Required
    step_time = models.DecimalField(decimal_places=2, max_digits=10) #Required
    ramp_time = models.DecimalField(decimal_places=2, max_digits=10, default=0.0)
    end_temp = models.DecimalField(decimal_places=2, max_digits=10, null=True)
    water_grain_ratio = models.DecimalField(decimal_places=2, max_digits=10)
    mash_order = models.IntegerField() #required
    mash_profile = models.ForeignKey(Mash_profile, related_name='mash_steps', on_delete=models.CASCADE) #Required
    
    class Meta:
        order_with_respect_to = 'mash_order'
        unique_together = ('mash_order', 'mash_profile')
    
class Mash_step_usage(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    infuse_amount = models.DecimalField(decimal_places=4, max_digits=10, null=True) #required
    infuse_temp = models.DecimalField(decimal_places=2, max_digits=10, null=True)
    mash_step = models.ForeignKey(Mash_step, on_delete=models.CASCADE)#Required
    mash_profile_usage = models.ForeignKey(Mash_profile_usage, related_name='mash_steps', on_delete=models.CASCADE)#Required

class Recipe(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=100, blank=True) 
    type = models.CharField(max_length=100) # Required
    brewer = models.CharField(max_length=100, blank=True)
    asst_brewer = models.CharField(max_length=100, blank=True)
    batch_size = models.DecimalField(decimal_places=4, max_digits=10) # Required
    boil_time = models.DecimalField(decimal_places=4, max_digits=10) # Required
    
    notes = models.TextField(blank=True)
    taste_notes = models.TextField(blank=True)
    taste_rating = models.DecimalField(decimal_places=4, max_digits=10, null=True)
    
    age = models.DecimalField(decimal_places=4, max_digits=10, null=True)
    age_temp = models.DecimalField(decimal_places=4, max_digits=10, null=True)
    date = models.DateTimeField(null=True)
    carbonation = models.DecimalField(decimal_places=4, max_digits=10, null=True)
    forced_carbonation = models.BooleanField(default=True)
    priming_sugar_name = models.CharField(max_length=100, blank=True)
    carbonation_temp = models.DecimalField(decimal_places=4, max_digits=10, null=True, blank=True)
    priming_sugar_equiv = models.DecimalField(decimal_places=4, max_digits=10, null=True, blank=True)
    keg_priming_factor = models.DecimalField(decimal_places=4, max_digits=10, null=True, blank=True)
    
    ### These were in Equipment_usage that used to exist
    top_up_kettle = models.DecimalField(decimal_places=4, max_digits=10, null=True)
    top_up_water = models.DecimalField(decimal_places=4, max_digits=10, null=True)
    
    
    est_total_water_vol = models.DecimalField(decimal_places=4, max_digits=10, null=True)
    est_og = models.DecimalField(decimal_places=4, max_digits=10, null=True)
    est_fg = models.DecimalField(decimal_places=4, max_digits=10, null=True)
    est_ibu = models.DecimalField(decimal_places=4, max_digits=10, null=True)
    est_ibu_method = models.CharField(max_length=100, blank=True)  #multi choice field
    est_color = models.DecimalField(decimal_places=4, max_digits=10, null=True)
    est_abv = models.DecimalField(decimal_places=4, max_digits=10, null=True)
    est_pre_boil_og = models.DecimalField(decimal_places=4, max_digits=10, null=True)
    est_pre_boil_vol = models.DecimalField(decimal_places=4, max_digits=10, null=True)
    est_calories = models.DecimalField(decimal_places=4, max_digits=10, null=True)
    est_boil_size = models.DecimalField(decimal_places=4, max_digits=10, null=True) 
    est_efficiency = models.DecimalField(decimal_places=4, max_digits=10, default=Decimal(72))
    est_mash_efficiency = models.DecimalField(decimal_places=4, max_digits=10, null=True)
    est_by_mash_efficiency = models.BooleanField(default=False)
    est_attenuation = models.DecimalField(decimal_places=4, max_digits=10, null=True)
    
    
    
    measured_abv = models.DecimalField(decimal_places=4, max_digits=10, null=True)
    measured_calories = models.DecimalField(decimal_places=4, max_digits=10, null=True)
    measured_og = models.DecimalField(decimal_places=4, max_digits=10, null=True)
    measured_fg = models.DecimalField(decimal_places=4, max_digits=10, null=True)
    measured_batch_size = models.DecimalField(decimal_places=4, max_digits=10, null=True)
    measured_pre_boil_og = models.DecimalField(decimal_places=4, max_digits=10, null=True)
    measured_pre_boil_vol = models.DecimalField(decimal_places=4, max_digits=10, null=True)
    measured_efficiency = models.DecimalField(decimal_places=4, max_digits=10, null=True)
    measured_mash_efficiency = models.DecimalField(decimal_places=4, max_digits=10, null=True)
    measured_attenuation = models.DecimalField(decimal_places=4, max_digits=10, null=True)
    
    ## Foreign Keys
    equipment = models.ForeignKey(Equipment, on_delete=models.SET_NULL, null=True)
    style = models.ForeignKey(Style, on_delete=models.SET_NULL, null=True)
    fermentation_profile = models.ForeignKey(Fermentation_profile, on_delete=models.SET_NULL, null=True)
    mash_profile_usage = models.ForeignKey(Mash_profile_usage, on_delete=models.CASCADE, null=True)

class Misc(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=100) # Required
    type = models.CharField(max_length=100) # Required
    use_for = models.TextField(blank=True)
    notes = models.TextField(blank=True)    
    
class Misc_usage(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    time = models.DecimalField(decimal_places=4, max_digits=10) # Required
    amount = models.DecimalField(decimal_places=4, max_digits=10) # Required
    amount_is_weight = models.BooleanField(default=False)
    use = models.CharField(max_length=100) #required
    misc = models.ForeignKey(Misc, on_delete=models.PROTECT) # Required
    recipe = models.ForeignKey(Recipe, related_name='misc_usages', on_delete=models.CASCADE) # Required

class Hop(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=100)  # Required
    default_alpha = models.DecimalField(decimal_places=4, max_digits=10) # Required
    notes = models.TextField(blank=True)
    type = models.CharField(max_length=100, blank=True) 
    
    default_beta = models.DecimalField(decimal_places=4, max_digits=10, null=True)
    hsi = models.DecimalField(decimal_places=4, max_digits=10, null=True)
    origin = models.TextField(blank=True)
    substitutes = models.TextField(blank=True)
    default_humulene = models.DecimalField(decimal_places=4, max_digits=10, null=True)
    default_caryophyllene = models.DecimalField(decimal_places=4, max_digits=10, null=True)
    default_cohumulone = models.DecimalField(decimal_places=4, max_digits=10, null=True)
    default_myrcene = models.DecimalField(decimal_places=4, max_digits=10, null=True)

class Hop_usage(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    alpha = models.DecimalField(decimal_places=4, max_digits=10, null=True)
    amount = models.DecimalField(decimal_places=4, max_digits=10, null=True) 
    use = models.CharField(max_length=100) # Required
    time = models.DecimalField(decimal_places=4, max_digits=10) # Required
    form = models.CharField(max_length=100) # Required
    beta = models.DecimalField(decimal_places=4, max_digits=10, null=True) 
    humulene = models.DecimalField(decimal_places=4, max_digits=10, null=True) 
    caryophyllene = models.DecimalField(decimal_places=4, max_digits=10, null=True) 
    cohumulone = models.DecimalField(decimal_places=4, max_digits=10, null=True) 
    myrcene = models.DecimalField(decimal_places=4, max_digits=10, null=True) 
    hop = models.ForeignKey(Hop, on_delete=models.PROTECT) # Required
    recipe = models.ForeignKey(Recipe, related_name='hop_usages', on_delete=models.CASCADE) # Required


    
class Yeast(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=100) # Required
    type = models.CharField(max_length=100) # Required
    form = models.CharField(max_length=100) # Required
    laboratory = models.CharField(max_length=100, blank=True)
    product_id = models.CharField(max_length=100, blank=True)
    min_temperature = models.DecimalField(decimal_places=4, max_digits=10, null=True) 
    max_temperature = models.DecimalField(decimal_places=4, max_digits=10, null=True) 
    flocculation = models.CharField(max_length=100, blank=True)
    attenuation = models.DecimalField(decimal_places=4, max_digits=10, null=True) 
    notes = models.TextField(blank=True)
    best_for = models.TextField(blank=True)
    max_reuse = models.IntegerField(null=True)
    
class Yeast_usage(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    amount = models.DecimalField(decimal_places=4, max_digits=10, null=True)  # Required
    amount_is_weight = models.BooleanField(default=False)
    times_cultured = models.IntegerField(null=True)
    add_to_secondary = models.BooleanField(default=False)
    yeast = models.ForeignKey(Yeast, on_delete=models.PROTECT) # Required
    recipe = models.ForeignKey(Recipe, related_name='yeast_usages', on_delete=models.CASCADE) # Required
    
class Fermentable(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=100) # Required
    type = models.CharField(max_length=100) # Required
    raw_yield = models.DecimalField(decimal_places=4, max_digits=10, null=True) # Required
    color = models.DecimalField(decimal_places=4, max_digits=10, null=True) # Required
    origin = models.TextField(blank=True)
    supplier = models.CharField(max_length=100, blank=True)
    notes = models.TextField(blank=True)
    coarse_fine_diff = models.DecimalField(decimal_places=4, max_digits=10, null=True)
    moisture = models.DecimalField(decimal_places=4, max_digits=10, null=True)
    diastatic_power = models.DecimalField(decimal_places=4, max_digits=10, null=True)
    protein = models.DecimalField(decimal_places=4, max_digits=10, null=True)
    max_in_batch = models.DecimalField(decimal_places=4, max_digits=10, null=True)
    recommend_mash = models.BooleanField(default=True)
    ibu_gal_per_lb = models.DecimalField(decimal_places=4, max_digits=10, null=True)
    potential = models.DecimalField(decimal_places=4, max_digits=10, null=True)

class Fermentable_usage(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    amount = models.DecimalField(decimal_places=4, max_digits=10) #Required
    add_after_boil = models.BooleanField(default=False)#Required
    fermentable = models.ForeignKey(Fermentable, on_delete=models.PROTECT) #Required
    recipe = models.ForeignKey(Recipe, related_name='fermentable_usages', on_delete=models.CASCADE) #Required
        
class Water(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=100) #Required
    calcium = models.DecimalField(decimal_places=4, max_digits=10) #Required
    bicarbonate = models.DecimalField(decimal_places=4, max_digits=10) #Required
    sulfate = models.DecimalField(decimal_places=4, max_digits=10) #Required
    chloride = models.DecimalField(decimal_places=4, max_digits=10) #Required
    sodium = models.DecimalField(decimal_places=4, max_digits=10) #Required
    magnesium = models.DecimalField(decimal_places=4, max_digits=10) #Required
    ph = models.DecimalField(decimal_places=4, max_digits=10, null=True) 
    notes = models.TextField(blank=True)
        
class Water_usage(models.Model):    
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    amount = models.DecimalField(decimal_places=4, max_digits=10)
    water = models.ForeignKey(Water, on_delete=models.PROTECT) #REQUIRED
    recipe = models.ForeignKey(Recipe, related_name='water_usages', on_delete=models.CASCADE) #Required
    

  
class Fermenter(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=100)
    chamber = models.ForeignKey('Chamber', related_name='fermenter', on_delete=models.CASCADE) #required
    
class Chamber(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=100)
    manual_temp = models.DecimalField(decimal_places=2, max_digits=10, null=True)
    manual_heat_diff = models.DecimalField(decimal_places=2, max_digits=10, null=True)
    manual_cool_diff = models.DecimalField(decimal_places=2, max_digits=10, null=True)
    operation_type = models.CharField(max_length=100, default="Off")
    active_fermenter = models.ForeignKey(Fermenter, on_delete=models.SET_NULL, null=True, related_name='active_fermenter')    
    
class Tap(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=100)
    kegerator = models.ForeignKey('Kegerator', related_name='Taps', on_delete=models.CASCADE) #required
    
class Kegerator(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=100)
    manual_temp = models.DecimalField(decimal_places=2, max_digits=10, null=True)
    manual_heat_diff = models.DecimalField(decimal_places=2, max_digits=10, null=True)
    manual_cool_diff = models.DecimalField(decimal_places=2, max_digits=10, null=True)
    operation_type = models.CharField(max_length=100, default="Off")
    active_tap = models.ForeignKey(Tap, on_delete=models.SET_NULL, null=True, related_name='active_tap')  
    
    
class Device(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    serial = models.CharField(max_length=100)  
    name = models.CharField(max_length=100, null=True)
    
class Sensor(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    type = models.CharField(max_length=100) 
    serial = models.CharField(max_length=100) 
    device = models.ForeignKey(Device, on_delete=models.SET_NULL, null=True, related_name='sensors')   
    unit = models.CharField(max_length=100) 
    name = models.CharField(max_length=100, null=True)
    enabled = models.BooleanField(default=True)
    checkin_interval = models.IntegerField(default=5)
    
class RecipeAssignment(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    start_datetime = models.DateTimeField(null=True)
    end_datetime = models.DateTimeField(null=True)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name="assignments")
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    assignment = GenericForeignKey('content_type', 'object_id')
    
    
class SensorAssignment(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    start_datetime = models.DateTimeField(null=True)
    end_datetime = models.DateTimeField(null=True)
    sensor = models.ForeignKey(Sensor, on_delete=models.CASCADE, related_name="sensor_assignment")
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    assignment = GenericForeignKey('content_type', 'object_id')
    
    
class Alert(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    title = models.CharField(max_length=200) 
    description = models.TextField()
    acknowledged = models.BooleanField(default=False)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    target = GenericForeignKey('content_type', 'object_id')    
    #priority = models.CharField(max_length=20, default="Low")
    resolved_timestamp = models.DateTimeField(default=None, null=True)
    type = models.CharField(max_length=100, default="Other")
    notification_timestamp = models.DateTimeField(default=None, null=True)
    
class Data(models.Model):
    created_at = models.DateTimeField()
    data = models.CharField(max_length=200)
    unit = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    timestamp = models.DateTimeField(null=True)
    sensor = models.ForeignKey(Sensor, on_delete=models.CASCADE, related_name="data")
    
    
    
    
################################
#
# Signals to tell the updateRecipe function to run or to ignore
#
################################

@receiver(post_save, sender=Hop_usage)
@receiver(post_delete, sender=Hop_usage)
@receiver(post_save, sender=Fermentable_usage)
@receiver(post_delete, sender=Fermentable_usage)
@receiver(post_save, sender=Yeast_usage)
@receiver(post_delete, sender=Yeast_usage)
def usage_update_handler(sender, instance, **kwargs):
    # Update the parent Recipe
    util.updateRecipe(instance.recipe)

@receiver(pre_delete, sender=Recipe)
def recipe_delete_handler(sender, instance, **kwargs):
    instance._meta._ignore_update = True
    
@receiver(post_delete, sender=Recipe)
def recipe_delete_post_handler(sender, instance, **kwargs):
    instance._meta._ignore_update = False
    del instance._meta._ignore_update
     
@receiver(post_save, sender=Recipe)
def recipe_update_handler(sender, instance, **kwargs):
    # Extra code here is to not recursively update the recipe since the update recipe saves on 
    if hasattr(instance, '_save_in_progress'):
        del instance._save_in_progress
        return
    instance._save_in_progress = True
    util.updateRecipe(instance)
    
## Update all recipes that use this Yeast
@receiver(post_save, sender=Yeast)
@receiver(post_delete, sender=Yeast)
def yeast_update_handler(sender, instance, **kwargs):
    usages = Yeast_usage.objects.filter(yeast=instance)
    for usage in usages:
        if usage.recipe is not None:
            usage.recipe._save_in_progress = True
            util.updateRecipe(usage.recipe)

## Update all recipes that use this Fermentable
@receiver(post_save, sender=Fermentable)
@receiver(post_delete, sender=Fermentable)
def fermentable_update_handler(sender, instance, **kwargs):
    usages = Fermentable_usage.objects.filter(fermentable=instance)
    for usage in usages:
        if usage.recipe is not None:
            usage.recipe._save_in_progress = True
            util.updateRecipe(usage.recipe)

## Update all recipes that use this Equip Profile
@receiver(post_save, sender=Equipment)
@receiver(post_delete, sender=Equipment)
def equipment_update_handler(sender, instance, **kwargs):
    usages = Recipe.objects.filter(equipment=instance)
    for recipes in usages:
            recipe._save_in_progress = True
            util.updateRecipe(recipe)

@receiver(post_save, sender=Alert)
def alert_create_handler(sender, instance, created, **kwargs):
    if created:
        ### Fire off a notification celery task that a new alert has been created
        send_alert_notification.delay(instance.title, instance.description, "") #instance.target.url)
        print("******* New Alert Created **********")
