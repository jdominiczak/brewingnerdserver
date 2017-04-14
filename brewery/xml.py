from brewery import models
from rest_framework.response import Response
from brewery import util
import re
from decimal import *
from rest_framework.reverse import reverse
from brewery import views


try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET

def stripChar(stringChar):
    return re.sub(r'[^\d.]+', '', stringChar)
    
def getValue(element, key, stripChars=False, noneValue=""):
    if stripChars:
        return stripChar(element.find(key).text) if ((element.find(key) is not None) and (element.find(key).text is not None)) else noneValue
    else:
        retString = element.find(key).text if ((element.find(key) is not None) and (element.find(key).text is not None)) else noneValue
        if retString == "-":
            return None
        if retString == "" and noneValue is None:
            return None
        else:
            return retString
    
            
def toBool(boolString, default=False):
    if boolString.lower() == "false":
        return False
    elif boolString.lower() == "true":
        return True
    else:
        return default
        
def recipe_data_from_element(element):
    recipeDict = {}
    recipeDict["name"] = getValue(element, "NAME")
    recipeDict["type"] = getValue(element, "TYPE")
    recipeDict["brewer"] = getValue(element, "BREWER") 
    recipeDict["asst_brewer"] = getValue(element, "ASST_BREWER")
    recipeDict["batch_size"] = getValue(element, "BATCH_SIZE" )
    recipeDict["est_boil_size"] = getValue(element, "BOIL_SIZE")
    recipeDict["boil_time"] = getValue(element, "BOIL_TIME")
    recipeDict["est_efficiency"] = getValue(element, "EFFICIENCY")
    recipeDict["notes"] = getValue(element, "NOTES") 
    recipeDict["taste_notes"] = getValue(element, "TASTE_NOTES") 
    recipeDict["taste_rating"] = getValue(element, "TASTE_RATING") 
    recipeDict["measured_og"] = getValue(element, "OG", True) 
    recipeDict["measured_fg"] = getValue(element, "FG", True) 
    recipeDict["age"] = getValue(element, "AGE") 
    recipeDict["age_temp"] = getValue(element, "AGE_TEMP") 
    recipeDict["carbonation"] = getValue(element, "CARBONATION") 
    recipeDict["forced_carbonation"] = toBool(getValue(element, "FORCED_CARBONATION"))
    recipeDict["priming_sugar_name"] = getValue(element, "PRIMING_SUGAR_NAME")
    recipeDict["carbonation_temp"] = getValue(element, "CARBONATION_TEMP", noneValue=None)
    recipeDict["priming_sugar_equiv"] = getValue(element, "PRIMING_SUGAR_EQUIV", noneValue=None) 
    recipeDict["keg_priming_factor"] = getValue(element, "KEG_PRIMING_FACTOR", noneValue=None) 
    recipeDict["est_og"] = getValue(element, "EST_OG", True) 
    recipeDict["est_fg"] = getValue(element, "EST_FG", True) 
    recipeDict["est_ibu"] = getValue(element, "IBU", True) 
    recipeDict["est_ibu_method"] = getValue(element, "IBU_METHOD") 
    recipeDict["est_abv"] = getValue(element, "EST_ABV", True) 
    recipeDict["measured_abv"] = getValue(element, "ABV", True) 
    recipeDict["measured_efficiency"] = getValue(element, "ACTUAL_EFFICIENCY", True)
    recipeDict["est_color"] = getValue(element, "EST_COLOR", True)

    #print(recipeDict)
    recipe = models.Recipe(**recipeDict)
    
    ### Make the fermentation Steps
    ferm_stages = int(getValue(element, "FERMENTATION_STAGES")) 
    if ferm_stages == 2:
        ferm_prof_name = "Two Stage Fermentation"
    if ferm_stages == 3:
        ferm_prof_name = "Three Stage Fermentation"
    else:
        ferm_prof_name = "Single Stage Fermentation"
    ferm_profile = models.Fermentation_profile(name=ferm_prof_name)
    ferm_profile.save()
    if ferm_stages > 0:
        prim_age = getValue(element, "PRIMARY_AGE", noneValue = "14")
        prim_age = int(round(float(prim_age)))
        prim_temp = getValue(element, "PRIMARY_TEMP", noneValue = "18.89") 
        ferm_step1 = models.Fermentation_step(name="Primary Fermentation", order=1, start_temp=prim_temp, end_temp=prim_temp, length=prim_age, fermentation_profile=ferm_profile)
        ferm_step1.save()
    if ferm_stages > 1:
        sec_age = getValue(element, "SECONDARY_AGE", noneValue = "14") 
        sec_age = int(round(float(prim_age)))
        sec_temp = getValue(element, "SECONDARY_TEMP", noneValue = "18.89") 
        ferm_step2 = models.Fermentation_step(name="Secondary Fermentation", order=2, start_temp=sec_temp, end_temp=sec_temp, length=sec_age, fermentation_profile=ferm_profile)   
        ferm_step2.save()
    if ferm_stages > 2:
        ter_age = getValue(element, "TERTIARY_AGE", noneValue = "14") 
        ter_age = int(round(float(prim_age)))
        ter_temp = getValue(element, "TERTIARY_TEMP", noneValue = "18.89") 
        ferm_step3 = models.Fermentation_step(name="Tertiary Fermentation", order=3, start_temp=ter_temp, end_temp=ter_temp, length=ter_age, fermentation_profile=ferm_profile)   
        ferm_step3.save()    
    
    recipe.fermentation_profile = ferm_profile
    recipe._meta._ignore_update = True
    recipe.save()
    return recipe


def hop_data_from_element(element, recipe):
    
    hopDict = {}
    usageDict = {}
    hopDict["name"] = getValue(element, "NAME") #element.find("NAME").text
    hopDict["default_alpha"] = getValue(element, "ALPHA") #element.find("ALPHA").text if element.find("ALPHA") is not None else None
    usageDict["alpha"] = getValue(element, "ALPHA") 
    usageDict["amount"] = getValue(element, "AMOUNT") #element.find("AMOUNT").text if element.find("AMOUNT") is not None else None
    usageDict["use"] = getValue(element, "USE") #element.find("USE").text if element.find("USE") is not None else None
    usageDict["time"] = getValue(element, "TIME") #element.find("TIME").text if element.find("TIME") is not None else None
    hopDict["notes"] = getValue(element, "NOTES") #element.find("NOTES").text if element.find("NOTES") is not None else None
    hopDict["type"] = getValue(element, "TYPE") #element.find("TYPE").text if element.find("TYPE") is not None else None
    usageDict["form"] = getValue(element, "FORM") #element.find("FORM").text if element.find("FORM") is not None else None
    usageDict["beta"] = getValue(element, "BETA", noneValue = None) #element.find("BETA").text if element.find("BETA") is not None else None
    hopDict["default_beta"] = getValue(element, "BETA", noneValue = None)
    hopDict["hsi"] = getValue(element, "HSI", noneValue = None) #element.find("HSI").text if element.find("HSI") is not None else None
    hopDict["origin"] = getValue(element, "ORIGIN") #element.find("ORIGIN").text if element.find("ORIGIN") is not None else None
    hopDict["substitutes"] = getValue(element, "SUBSTITUTES") #element.find("SUBSTITUTES").text if element.find("SUBSTITUTES") is not None else None
    hopDict["default_humulene"] = getValue(element, "HUMULENE", noneValue = None) #element.find("HUMULENE").text if element.find("HUMULENE") is not None else None
    hopDict["default_caryophyllene"] = getValue(element, "CARYOPHYLLENE", noneValue = None) #element.find("CARYOPHYLLENE").text if element.find("CARYOPHYLLENE") is not None else None
    hopDict["default_cohumulone"] = getValue(element, "COHUMULONE", noneValue = None) #element.find("COHUMULONE").text if element.find("COHUMULONE") is not None else None
    hopDict["default_myrcene"] = getValue(element, "MYRCENE", noneValue = None) #element.find("MYRCENE").text if element.find("MYRCENE") is not None else None
    usageDict["humulene"] = getValue(element, "HUMULENE", noneValue = None) #element.find("HUMULENE").text if element.find("HUMULENE") is not None else None
    usageDict["caryophyllene"] = getValue(element, "CARYOPHYLLENE", noneValue = None) #element.find("CARYOPHYLLENE").text if element.find("CARYOPHYLLENE") is not None else None
    usageDict["cohumulone"] = getValue(element, "COHUMULONE", noneValue = None) #element.find("COHUMULONE").text if element.find("COHUMULONE") is not None else None
    usageDict["myrcene"] = getValue(element, "MYRCENE", noneValue = None) #element.find("MYRCENE").text if element.find("MYRCENE") is not None else None
    #print("Hop Dict")
    #print(hopDict)
    #print("Usage Dict")
    #print(usageDict)
    # Try to find a hop that matches name(ie Cascade)
    try:
        hop = models.Hop.objects.get(name__iexact=hopDict["name"])
    except models.Hop.DoesNotExist:
        hop = models.Hop(**hopDict)
        hop.save()
        
    usage = models.Hop_usage(**usageDict)
    usage.recipe=recipe
    usage.hop=hop   
    usage.save()  



def fermentable_data_from_element(element, recipe):
    fermentableDict = {}
    usageDict = {}
    fermentableDict["name"] = getValue(element, "NAME") #element.find("NAME").text
    fermentableDict["type"] = getValue(element, "TYPE") #element.find("TYPE").text if element.find("TYPE") is not None else None
    fermentableDict["raw_yield"] = getValue(element, "YIELD", noneValue=None) #element.find("YIELD").text if element.find("YIELD") is not None else None
    fermentableDict["color"] = getValue(element, "COLOR", noneValue=None) #element.find("COLOR").text if element.find("COLOR") is not None else None
    fermentableDict["origin"] = getValue(element, "ORIGIN") #element.find("ORIGIN").text if element.find("ORIGIN") is not None else None
    fermentableDict["supplier"] = getValue(element, "SUPPLIER") #element.find("SUPPLIER").text if element.find("SUPPLIER") is not None else None
    fermentableDict["notes"] = getValue(element, "NOTES") #element.find("NOTES").text if element.find("NOTES") is not None else None
    fermentableDict["coarse_fine_diff"] = getValue(element, "COARSE_FINE_DIFF", noneValue=None) #element.find("COARSE_FINE_DIFF").text if element.find("COARSE_FINE_DIFF") is not None else None
    fermentableDict["moisture"] = getValue(element, "MOISTURE", noneValue=None) #element.find("MOISTURE").text if element.find("MOISTURE") is not None else None
    fermentableDict["diastatic_power"] = getValue(element, "DIASTATIC_POWER", noneValue=None) #element.find("DIASTATIC_POWER").text if element.find("DIASTATIC_POWER") is not None else None
    fermentableDict["protein"] = getValue(element, "PROTEIN", noneValue=None) #element.find("PROTEIN").text if element.find("PROTEIN") is not None else None
    fermentableDict["max_in_batch"] = getValue(element, "MAX_IN_BATCH", noneValue=None) #element.find("MAX_IN_BATCH").text if element.find("MAX_IN_BATCH") is not None else None
    fermentableDict["recommend_mash"] = toBool(getValue(element, "RECOMMEND_MASH")) #element.find("RECOMMEND_MASH").text if element.find("RECOMMEND_MASH") is not None else None
    fermentableDict["ibu_gal_per_lb"] = getValue(element, "IBU_GAL_PER_LB", noneValue=None) #element.find("IBU_GAL_PER_LB").text if element.find("IBU_GAL_PER_LB") is not None else None
    fermentableDict["potential"] = getValue(element, "POTENTIAL", noneValue=None) #element.find("POTENTIAL").text if element.find("PTOENTIAL") is not None else None
    
    usageDict["amount"] = getValue(element, "AMOUNT") #element.find("AMOUNT").text if element.find("AMOUNT") is not None else None
    usageDict["add_after_boil"] = toBool(getValue(element, "ADD_AFTER_BOIL")) #element.find("ADD_AFTER_BOIL").text if element.find("ADD_AFTER_BOIL") is not None else None
    
    #print("Ferm Dict")
    #print(fermentableDict)
    #print("Usage Dict")
    #print(usageDict)
    try:
        ferm = models.Fermentable.objects.get(name__iexact=fermentableDict["name"], type__iexact=fermentableDict["type"])
    except models.Fermentable.DoesNotExist:
        ferm = models.Fermentable(**fermentableDict)
        ferm.save()
    usage = models.Fermentable_usage(**usageDict)
    usage.recipe=recipe
    usage.fermentable=ferm
    usage.save()




def yeast_data_from_element(element, recipe):
    yeastDict = {}
    usageDict = {}
    yeastDict["name"] = getValue(element, "NAME") #element.find("NAME").text
    yeastDict["type"] = getValue(element, "TYPE") #element.find("TYPE").text if element.find("TYPE") is not None else None
    yeastDict["form"] = getValue(element, "FORM") #element.find("FORM").text if element.find("FORM") is not None else None
    usageDict["amount"] = getValue(element, "AMOUNT") #element.find("AMOUNT").text if element.find("AMOUNT") is not None else None
    usageDict["amount_is_weight"] = toBool(getValue(element, "AMOUNT_IS_WEIGHT")) #element.find("AMOUNT_IS_WEIGHT").text if element.find("AMOUNT_IS_WEIGHT") is not None else None
    yeastDict["laboratory"] = getValue(element, "LABORATORY") #element.find("LABORATORY").text if element.find("LABORATORY") is not None else None
    yeastDict["product_id"] = getValue(element, "PRODUCT_ID") #element.find("PRODUCT_ID").text if element.find("PRODUCT_ID") is not None else None
    yeastDict["min_temperature"] = getValue(element, "MIN_TEMPERATURE") #element.find("MIN_TEMPERATURE").text if element.find("MIN_TEMPERATURE") is not None else None
    yeastDict["max_temperature"] = getValue(element, "MAX_TEMPERATURE") #element.find("MAX_TEMPERATURE").text if element.find("MAX_TEMPERATURE") is not None else None
    yeastDict["flocculation"] = getValue(element, "FLOCCULATION") #element.find("FLOCCULATION").text if element.find("FLOCCULATION") is not None else None
    yeastDict["attenuation"] = getValue(element, "ATTENUATION") #element.find("ATTENUATION").text if element.find("ATTENUATION") is not None else None
    yeastDict["notes"] = getValue(element, "NOTES") #element.find("NOTES").text if element.find("NOTES") is not None else None
    yeastDict["best_for"] = getValue(element, "BEST_FOR") #element.find("BEST_FOR").text if element.find("BEST_FOR") is not None else None
    usageDict["times_cultured"] = getValue(element, "TIMES_CULTURED") #element.find("TIMES_CULTURED").text if element.find("TIMES_CULTURED") is not None else None
    yeastDict["max_reuse"] = getValue(element, "MAX_REUSE") #element.find("MAX_REUSE").text if element.find("MAX_REUSE") is not None else None
    usageDict["add_to_secondary"] = toBool(getValue(element, "ADD_TO_SECONDARY")) #element.find("ADD_TO_SECONDARY").text if element.find("ADD_TO_SECONDARY") is not None else None
    #yeastDict["inventory"] = getValue(element, "") #element.find("INVENTORY").text if element.find("INVENTORY") is not None else None
    #yeastDict["culture_date"] = getValue(element, "CULTURE_DATE") #element.find("CULTURE_DATE").text if element.find("CULTURE_DATE") is not None else None
    #return yeastDict
    try:
        yeast = models.Yeast.objects.get(name__iexact=yeastDict["name"], form__iexact=yeastDict["form"], laboratory__iexact=yeastDict["laboratory"], product_id__iexact=yeastDict["product_id"])
    except models.Yeast.DoesNotExist:
        yeast = models.Yeast(**yeastDict)
        yeast.save()
    usage = models.Yeast_usage(**usageDict)
    usage.yeast=yeast
    usage.recipe=recipe
    usage.save()
    


def misc_data_from_element(element, recipe):
    miscDict = {}
    usageDict = {}
    miscDict["name"] = getValue(element, "NAME") #element.find("NAME").text
    #miscDict["recipe_id"] = recipe_id
    #miscDict["version"] = element.find("VERSION").text if element.find("VERSION") is not None else None
    miscDict["type"] = getValue(element, "TYPE") #element.find("TYPE").text if element.find("TYPE") is not None else None
    usageDict["use"] = getValue(element, "USE") #element.find("USE").text if element.find("USE") is not None else None
    usageDict["time"] = getValue(element, "TIME") #element.find("TIME").text if element.find("TIME") is not None else None
    usageDict["amount"] = getValue(element, "AMOUNT") #element.find("AMOUNT").text if element.find("AMOUNT") is not None else None
    usageDict["amount_is_weight"] = toBool(getValue(element, "AMOUNT_IS_WEIGHT")) #element.find("AMOUNT_IS_WEIGHT").text if element.find("AMOUNT_IS_WEIGHT") is not None else None
    miscDict["use_for"] = getValue(element, "USE_FOR") #element.find("USE_FOR").text if element.find("USE_FOR") is not None else None
    miscDict["notes"] = getValue(element, "NOTES") #element.find("NOTES").text if element.find("NOTES") is not None else None
    #miscDict["inventory"] = element.find("INVENTORY").text if element.find("INVENTORY") is not None else None
    #return miscDict

    try:
        misc = models.Misc.objects.get(name__iexact=miscDict["name"], type__iexact=miscDict["type"])
    except models.Misc.DoesNotExist:
        misc = models.Misc(**miscDict)
        misc.save()
    usage = models.Misc_usage(**usageDict)
    usage.misc=misc
    usage.recipe=recipe
    usage.save()



def water_data_from_element(element, recipe):
    waterDict = {}
    usageDict = {}
    waterDict["name"] = getValue(element, "NAME") #element.find("NAME").text
    #waterDict["version"] = element.find("VERSION").text if element.find("VERSION") is not None else None
    usageDict["amount"] = getValue(element, "AMOUNT") #element.find("AMOUNT").text if element.find("AMOUNT") is not None else None
    waterDict["calcium"] = getValue(element, "CALCIUM") #element.find("CALCIUM").text if element.find("CALCIUM") is not None else None
    waterDict["bicarbonate"] = getValue(element, "BICARBONATE") #element.find("BICARBONATE").text if element.find("BICARBONATE") is not None else None
    waterDict["sulfate"] = getValue(element, "SULFATE") #element.find("SULFATE").text if element.find("SULFATE") is not None else None
    waterDict["chloride"] = getValue(element, "CHLORIDE") #element.find("CHLORIDE").text if element.find("CHLORIDE") is not None else None
    waterDict["sodium"] = getValue(element, "SODIUM") #element.find("SODIUM").text if element.find("SODIUM") is not None else None
    waterDict["magnesium"] = getValue(element, "MAGNESIUM") #element.find("MAGNESIUM").text if element.find("MAGNESIUM") is not None else None
    waterDict["ph"] = getValue(element, "PH") #element.find("PH").text if element.find("PH") is not None else None
    waterDict["notes"] = getValue(element, "NOTES") #element.find("NOTES").text if element.find("NOTES") is not None else None
    
    try:
        water = models.Water.objects.get(name__iexact=waterDict["name"])
    except models.Water.DoesNotExist:
        water = models.Water(**waterDict)
        water.save()
    usage = models.Water_usage(**usageDict)
    usage.water=water
    usage.recipe=recipe
    usage.save()
    
    


def style_data_from_element(element, recipe):
    styleDict = {}
    styleDict["name"] = getValue(element, "NAME") #element.find("NAME").text
    styleDict["category"] = getValue(element, "CATEGORY") #element.find("CATEGORY").text if element.find("CATEGORY") is not None else None
    #styleDict["version"] = element.find("VERSION").text if element.find("VERSION") is not None else None
    styleDict["category_number"] = getValue(element, "CATEGORY_NUMBER") #element.find("CATEGORY_NUMBER").text if element.find("CATEGORY_NUMBER") is not None else None
    styleDict["style_letter"] = getValue(element, "STYLE_LETTER") #element.find("STYLE_LETTER").text if element.find("STYLE_LETTER") is not None else None
    styleDict["style_guide"] = getValue(element, "STYLE_GUIDE") #element.find("STYLE_GUIDE").text if element.find("STYLE_GUIDE") is not None else None
    styleDict["type"] = getValue(element, "TYPE") #element.find("TYPE").text if element.find("TYPE") is not None else None
    styleDict["og_min"] = getValue(element, "OG_MIN") #element.find("OG_MIN").text if element.find("OG_MIN") is not None else None
    styleDict["og_max"] = getValue(element, "OG_MAX") #element.find("OG_MAX").text if element.find("OG_MAX") is not None else None
    styleDict["fg_min"] = getValue(element, "FG_MIN") #element.find("FG_MIN").text if element.find("FG_MIN") is not None else None
    styleDict["fg_max"] = getValue(element, "FG_MAX") #element.find("FG_MAX").text if element.find("FG_MAX") is not None else None
    styleDict["ibu_min"] = getValue(element, "IBU_MIN") #element.find("IBU_MIN").text if element.find("IBU_MIN") is not None else None
    styleDict["ibu_max"] = getValue(element, "IBU_MAX") #element.find("IBU_MAX").text if element.find("IBU_MAX") is not None else None
    styleDict["color_min"] = getValue(element, "COLOR_MIN") #element.find("COLOR_MIN").text if element.find("COLOR_MIN") is not None else None
    styleDict["color_max"] = getValue(element, "COLOR_MAX") #element.find("COLOR_MAX").text if element.find("COLOR_MAX") is not None else None
    styleDict["carb_min"] = getValue(element, "CARB_MIN") #element.find("CARB_MIN").text if element.find("CARB_MIN") is not None else None
    styleDict["carb_max"] = getValue(element, "CARB_MAX", stripChars=True) #element.find("CARB_MAX").text if element.find("CARB_MAX") is not None else None
    styleDict["abv_min"] = getValue(element, "ABV_MIN") #element.find("ABV_MIN").text if element.find("ABV_MIN") is not None else None
    styleDict["abv_max"] = getValue(element, "ABV_MAX") #element.find("ABV_MAX").text if element.find("ABV_MAX") is not None else None
    styleDict["notes"] = getValue(element, "NOTES") #element.find("NOTES").text if element.find("NOTES") is not None else None
    styleDict["profile"] = getValue(element, "PROFILE") #element.find("PROFILE").text if element.find("PROFILE") is not None else None
    styleDict["ingredients"] = getValue(element, "INGREDIENTS") #element.find("INGREDIENTS").text if element.find("INGREDIENTS") is not None else None
    styleDict["examples"] = getValue(element, "EXAMPLES") #element.find("EXAMPLES").text if element.find("EXAMPLES") is not None else None
    #styleDict["display_og_min"] = getValue(element, "") #element.find("DISPLAY_OG_MIN").text if element.find("DISPLAY_OG_MIN") is not None else None
    #styleDict["display_og_max"] = getValue(element, "") #element.find("DISPLAY_OG_MAX").text if element.find("DISPLAY_OG_MAX") is not None else None
    #styleDict["display_fg_min"] = getValue(element, "") #element.find("DISPLAY_FG_MIN").text if element.find("DISPLAY_FG_MIN") is not None else None
    #styleDict["display_fg_max"] = getValue(element, "") #element.find("DISPLAY_FG_MAX").text if element.find("DISPLAY_FG_MAX") is not None else None
    #styleDict["display_color_min"] = getValue(element, "") #element.find("DISPLAY_COLOR_MIN").text if element.find("DISPLAY_COLOR_MIN") is not None else None
    #styleDict["display_color_max"] = getValue(element, "") #element.find("DISPLAY_COLOR_MAX").text if element.find("DISPLAY_COLOR_MAX") is not None else None
    #styleDict["og_range"] = getValue(element, "") #element.find("OG_RANGE").text if element.find("OG_RANGE") is not None else None
    #styleDict["fg_range"] = getValue(element, "") #element.find("FG_RANGE").text if element.find("FG_RANGE") is not None else None
    #styleDict["ibu_range"] = getValue(element, "") #element.find("IBU_RANGE").text if element.find("IBU_RANGE") is not None else None
    #styleDict["carb_range"] = getValue(element, "") #element.find("CARB_RANGE").text if element.find("CARB_RANGE") is not None else None
    #styleDict["color_range"] = getValue(element, "") #element.find("COLOR_RANGE").text if element.find("COLOR_RANGE") is not None else None
    #styleDict["abv_range"] = getValue(element, "") #element.find("ABV_RANGE").text if element.find("ABV_RANGE") is not None else None
    
    try:
        style = models.Style.objects.get(name__iexact=styleDict["name"], category_number__iexact=styleDict["category_number"], style_letter__iexact=styleDict['style_letter'], style_guide__iexact=styleDict['style_guide'])
    except models.Style.DoesNotExist:
        style = models.Style(**styleDict)
        style.save()
    recipe.style=style
    recipe.save()
    #return styleDict


def equipment_data_from_element(element, recipe):
    equipmentDict = {}
    
    equipmentDict["name"] = getValue(element, "NAME") #element.find("NAME").text
    #equipmentDict["version"] = element.find("VERSION").text if element.find("VERSION") is not None else None
    equipmentDict["default_boil_size"] = getValue(element, "BOIL_SIZE") #element.find("BOIL_SIZE").text if element.find("BOIL_SIZE") is not None else None
    equipmentDict["default_batch_size"] = getValue(element, "BATCH_SIZE") #element.find("BATCH_SIZE").text if element.find("BATCH_SIZE") is not None else None
    equipmentDict["tun_volume"] = getValue(element, "TUN_VOLUME") #element.find("TUN_VOLUME").text if element.find("TUN_VOLUME") is not None else None
    equipmentDict["tun_weight"] = getValue(element, "TUN_WEIGHT") #element.find("TUN_WEIGHT").text if element.find("TUN_WEIGHT") is not None else None
    equipmentDict["tun_specific_heat"] = getValue(element, "TUN_SPECIFIC_HEAT") #element.find("TUN_SPECIFIC_HEAT").text if element.find("TUN_SPECIFIC_HEAT") is not None else None
    equipmentDict["default_top_up_water"] = getValue(element, "TOP_UP_WATER") #element.find("TOP_UP_WATER").text if element.find("TOP_UP_WATER") is not None else None
    equipmentDict["trub_chiller_loss"] = getValue(element, "TRUB_CHILLER_LOSS") #element.find("TRUB_CHILLER_LOSS").text if element.find("TRUB_CHILLER_LOSS") is not None else None
    equipmentDict["evap_rate"] = getValue(element, "EVAP_RATE") #element.find("EVAP_RATE").text if element.find("EVAP_RATE") is not None else None
    #equipmentDict["boil_time"] = element.find("BOIL_TIME").text if element.find("BOIL_TIME") is not None else None
    #equipmentDict["calc_boil_volume"] = element.find("CALC_BOIL_VOLUME").text if element.find("CALC_BOIL_VOLUME") is not None else None
    equipmentDict["lauter_deadspace"] = getValue(element, "LAUTER_DEADSPACE") #element.find("LAUTER_DEADSPACE").text if element.find("LAUTER_DEADSPACE") is not None else None
    equipmentDict["default_top_up_kettle"] = getValue(element, "TOP_UP_KETTLE") #element.find("TOP_UP_KETTLE").text if element.find("TOP_UP_KETTLE") is not None else None
    equipmentDict["hop_utilization"] = getValue(element, "HOP_UTILIZATION") #element.find("HOP_UTILIZATION").text if element.find("HOP_UTILIZATION") is not None else None
    equipmentDict["notes"] = getValue(element, "NOTES") #element.find("NOTES").text if element.find("NOTES") is not None else None

    try:
        equipment = models.Equipment.objects.get(name__iexact=equipmentDict["name"])
    except models.Equipment.DoesNotExist:
        equipment = models.Equipment(**equipmentDict)
        equipment.save()
    recipe.equipment=equipment
    recipe.top_up_kettle = getValue(element, "TOP_UP_KETTLE")
    recipe.top_up_water = getValue(element, "TOP_UP_WATER")
    recipe.save()


def mashprofile_data_from_element(element, recipe):
    mashDict = {}
    mashUsageDict={}
    mashDict["name"] = getValue(element, "NAME") #element.find("NAME").text
    #mashDict["version"] = element.find("VERSION").text if element.find("VERSION") is not None else None
    mashDict["notes"] = getValue(element, "NOTES") #element.find("NOTES").text if element.find("NOTES") is not None else None
    mashDict["sparge_temp"] = getValue(element, "SPARGE_TEMP") #element.find("SPARGE_TEMP").text if element.find("SPARGE_TEMP") is not None else None
    mashDict["ph"] = getValue(element, "PH") #element.find("PH").text if element.find("PH") is not None else None
    
    mashUsageDict["grain_temp"] = getValue(element, "GRAIN_TEMP")
    mashUsageDict["tun_temp"] = getValue(element, "TUN_TEMP")
    mashUsageDict["equip_adjust"] = toBool(getValue(element, "EQUIP_ADJUST"))

    stepOrder = 0
    stepArray = []
    for step in element.find("MASH_STEPS").findall("MASH_STEP"):
        stepArray.append(mashstep_data_from_element(step, stepOrder))
        stepOrder += 1
        
        
    ## See if this mash profile exists already 
    found_profile = None
    try:
        query = models.Mash_profile.objects.filter(name__iexact=mashDict["name"])
        profiles = list(query)
        #print(profiles)
        for profile in profiles:
            # get a list of steps
            if found_profile == None:
                try:
                    steps = list(models.Mash_step.objects.filter(mash_profile=profile))
                    #print("****STEPS*****")
                    #print(steps)
                    # match number of steps
                    if len(steps) == len(stepArray):
                        the_same=True
                        # match step info
                        for i, step in enumerate(steps):
                            inputtedStep = stepArray[i][0]
                            if inputtedStep["name"] == step.name and \
                                inputtedStep["type"] == step.type \
                                and abs(Decimal(inputtedStep["step_temp"]) - step.step_temp) < 0.1 \
                                and abs(Decimal(inputtedStep["step_time"]) - step.step_time) < 0.1 \
                                and abs(Decimal(inputtedStep["ramp_time"]) - step.ramp_time) < 0.1 \
                                and abs(Decimal(inputtedStep["end_temp"]) - step.end_temp) < 0.1\
                                and abs(Decimal(inputtedStep["water_grain_ratio"]) - step.water_grain_ratio) < 0.1:
                                pass;
                            else:
                                the_same = False
                        if the_same == True:
                            found_profile = profile
                except models.Mash_step.DoesNotExist:
                    pass
    except models.Mash_profile.DoesNotExist:
        pass
    
    if found_profile == None:
        mash_profile = models.Mash_profile(**mashDict)
        mash_profile.save()
    else:
        mash_profile = found_profile
        
    mash_usage = models.Mash_profile_usage(**mashUsageDict)
    mash_usage.mash_profile=mash_profile
    mash_usage.save()
    recipe.mash_profile_usage = mash_usage
    recipe.save()
    
    for step in stepArray:
        if found_profile == None:    
            mash_step = models.Mash_step(**step[0])
            mash_step.mash_profile = mash_profile
            mash_step.save()
        else:
            # Find the step that matches this
            mash_step = models.Mash_step.objects.get(mash_profile=mash_profile, mash_order=step[0]["mash_order"])
            
        step_usage = models.Mash_step_usage(**step[1])
        step_usage.mash_step = mash_step
        step_usage.mash_profile_usage = mash_usage
        step_usage.save()



def mashstep_data_from_element(element, order):
    #print("step:" + str(order))
    stepDict = {}
    usageDict = {}
    stepDict["name"] = getValue(element, "NAME") #element.find("NAME").text
    #mashDict["mash_profile_id"] = mash_id
    #mashDict["version"] = element.find("VERSION").text if element.find("VERSION") is not None else None
    stepDict["type"] = getValue(element, "TYPE") #element.find("TYPE").text if element.find("TYPE") is not None else None
    usageDict["infuse_amount"] = getValue(element, "INFUSE_AMOUNT") #element.find("INFUSE_AMOUNT").text if element.find("INFUSE_AMOUNT") is not None else None
    stepDict["step_time"] = getValue(element, "STEP_TIME") #element.find("STEP_TIME").text if element.find("STEP_TIME") is not None else None
    stepDict["step_temp"] = getValue(element, "STEP_TEMP") #element.find("STEP_TEMP").text if element.find("STEP_TEMP") is not None else None
    stepDict["ramp_time"] = getValue(element, "RAMP_TIME") #element.find("RAMP_TIME").text if element.find("RAMP_TIME") is not None else None
    stepDict["end_temp"] = getValue(element, "END_TEMP") #element.find("END_TEMP").text if element.find("END_TEMP") is not None else None
    #stepDict["description"] = getValue(element, "DESCRIPTION") #element.find("DESCRIPTION").text if element.find("DESCRIPTION") is not None else None
    stepDict["water_grain_ratio"] = stripChar(getValue(element, "WATER_GRAIN_RATIO")) #element.find("WATER_GRAIN_RATIO").text if element.find("WATER_GRAIN_RATIO") is not None else None
    #stepDict["decoction_amt"] = getValue(element, "DECOCTION_AMT") #element.find("DECOCTION_AMT").text if element.find("DECOCTION_AMT") is not None else None
    #usageDict["infuse_temp"] = stripChargetValue(element, "INFUSE_TEM") #element.find("INFUSE_TEMP").text if element.find("INFUSE_TEMP") is not None else None
    stepDict["mash_order"] = order
    return [stepDict, usageDict]


def ProcessRecipe(rec, request):
    if rec.tag == "RECIPE":
        recipe = recipe_data_from_element(rec)
    
        ## Insert Hops
        hops = rec.find("HOPS")
        if hops is not None:
            for hop in hops.findall("HOP"):
                hop_data_from_element(hop, recipe)
            
        ferms = rec.find("FERMENTABLES")
        if ferms is not None:
            for fermentable in ferms.findall("FERMENTABLE"):
                fermentable_data_from_element(fermentable, recipe)
            
        yeasts = rec.find("YEASTS")
        if yeasts is not None:
            for yeastElement in yeasts.findall("YEAST"):
                yeast_data_from_element(yeastElement, recipe)
            
        miscs = rec.find("MISCS")
        if miscs is not None:
            for miscElement in miscs.findall("MISC"):
                misc_data_from_element(miscElement, recipe)
            
        waters = rec.find("WATERS")
        if waters is not None:
            for waterElement in waters.findall("WATER"):
                water_data_from_element(waterElement, recipe)
            
        styles = rec.find("STYLES")
        if styles is not None:
            for styleElement in styles.findall("STYLE"):
                style_data_from_element(styleElement, recipe)
        else:
            styleElement = rec.find("STYLE")
            if styleElement is not None:
                style_data_from_element(styleElement, recipe)
            
        equipmentElement = rec.find("EQUIPMENT")
        if equipmentElement is not None:
            equipment_data_from_element(equipmentElement, recipe)
            
        mashElement = rec.find("MASH")
        if mashElement is not None:
            mashprofile_data_from_element(mashElement, recipe)
            
    recipe._meta._ignore_update = False
    del recipe._meta._ignore_update
      
    ## Recipe is finalized, update it (which also saves it)
    util.updateRecipe(recipe)
    
    ### Return the link to this recipe    
    return True, {"url" : reverse("recipe-detail", args=[recipe.id], request=request)}


def DeserializeRecipeXML(file, request):
    xml_file = file.read().decode("utf-8")
    #print(xml_file)
    #for line in file:
    #    print(line)
    urls = []
    tree = ET.fromstring(xml_file)
    created = True
    for recipe in tree:
        created, val = ProcessRecipe(recipe, request)
        if created:
            urls.append(val)
        else: 
            created = False
    if created:
        return Response(urls, status=201)
    else:
        return Response(urls, status=400)