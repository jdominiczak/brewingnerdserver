from django.conf.urls import url, include
from brewery import views
from rest_framework.routers import DefaultRouter

# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'recipes', views.RecipeViewSet)
router.register(r'miscs', views.MiscViewSet)
router.register(r'misc_usages', views.Misc_usageViewSet)
router.register(r'hops', views.HopViewSet)
router.register(r'hop_usages', views.Hop_usageViewSet)
router.register(r'yeasts', views.YeastViewSet)
router.register(r'yeast_usages', views.Yeast_usageViewSet)
router.register(r'fermentables', views.FermentableViewSet)
router.register(r'fermentable_usages', views.Fermentable_usageViewSet)
router.register(r'waters', views.WaterViewSet)
router.register(r'water_usages', views.Water_usageViewSet)
router.register(r'equipments', views.EquipmentViewSet)
router.register(r'styles', views.StyleViewSet)
router.register(r'mash_profiles', views.Mash_profileViewSet)
router.register(r'mash_profile_usages', views.Mash_profile_usageViewSet)
router.register(r'mash_steps', views.Mash_stepViewSet)
router.register(r'mash_step_usages', views.Mash_step_usageViewSet)
router.register(r'fermentation_profiles', views.Fermentation_profileViewSet)
router.register(r'fermentation_steps', views.Fermentation_stepViewSet)
router.register(r'fermenters', views.FermenterViewSet)
router.register(r'chambers', views.ChamberViewSet)
router.register(r'taps', views.TapViewSet)
router.register(r'kegerators', views.KegeratorViewSet)
router.register(r'devices', views.DeviceViewSet)
router.register(r'sensors', views.SensorViewSet)
router.register(r'sensor_assignments', views.SensorAssignmentViewSet)
router.register(r'alerts', views.AlertViewSet)
router.register(r'upload_recipe', views.UploadRecipeViewSet, base_name='upload_recipe')

# The API URLs are now determined automatically by the router.
# Additionally, we include the login URLs for the browsable API.

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
