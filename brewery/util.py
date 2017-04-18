
from brewery import models
import decimal
from decimal import Decimal
from math import exp

SHRINKAGE_PERCENT = Decimal(0.04)
DEFAULT_EVAP_RATE = Decimal(14.8)
DEFAULT_LAUTER_DEADSPACE = Decimal(0.0)
DEFAULT_GRAIN_ABSORB = Decimal(1) #1Liter per kg absorbtion 
DEFAULT_P_KG_L = Decimal(383.888737) #points per kg per liter
DEFAULT_PELLET_ADJUST = Decimal(0.10)
DEFAULT_PLUG_ADJUST = Decimal(0.02)
DEFAULT_YEAST_ATTENUATION = Decimal(0.75)


def updateRecipe(recipe):
    #see if this recipe is being imported and don't update it until it's finished
    if hasattr(recipe._meta, '_ignore_update') and recipe._meta._ignore_update==True:
        print("Ignoring Update")
        # Don't update this recipe as an import is in process
        return
    print("Updating Recipe ID:" + str(recipe.id) + " Name:" + recipe.name)
    ### Update the estimates based on the recipe values or default values if the recipe does not contain it
    
    
    chillerLoss = Decimal(0.0)
    evap_rate = DEFAULT_EVAP_RATE
    lauter_deadspace = DEFAULT_LAUTER_DEADSPACE
    if recipe.equipment is not None:
        chillerLoss = Decimal(recipe.equipment.trub_chiller_loss)
        evap_rate = recipe.equipment.evap_rate
        lauter_deadspace = recipe.equipment.lauter_deadspace

        
    postboilColdVol = Decimal(recipe.batch_size) + chillerLoss
    postboilHotVol = (postboilColdVol/(1-SHRINKAGE_PERCENT)) #postboilColdVol + shrinkage
    evap_amount = (Decimal(postboilHotVol) / (1- (Decimal(evap_rate))/100 )) - Decimal(postboilHotVol)
    preboilVol = postboilHotVol + evap_amount
    
    grain_weight = getGrainWeight(recipe)
    grain_absorption = DEFAULT_GRAIN_ABSORB * grain_weight
    premashVol = preboilVol + lauter_deadspace + grain_absorption 
    
    gravity_points_potential = getGravityPointsPotential(recipe)
    
    if recipe.est_by_mash_efficiency == True:
        # Estimate by Mash Efficiency
        mash_efficiency = Decimal(recipe.est_mash_efficiency) / Decimal(100)
        preboil_points = gravity_points_potential * mash_efficiency
        preboil_og = ((preboil_points/preboilVol)/1000) + 1
        chiller_loss_points = (preboil_points / postboilColdVol) * chillerLoss
        fermenter_points = preboil_points - chiller_loss_points
        fermenter_og = ((fermenter_points/Decimal(recipe.batch_size))/1000) + 1
        try:
            recipe.est_efficiency = fermenter_points / gravity_points_potential * 100
        except decimal.InvalidOperation:
            recipe.est_efficiency = Decimal(0)
        
        recipe.est_boil_size = preboilVol
        recipe.est_og = fermenter_og
        recipe.est_pre_boil_og = preboil_og
        recipe.est_pre_boil_vol = preboilVol
        recipe.est_total_water_vol = premashVol
        
    else:
        # Estimate by Brewhouse efficiency
        bh_efficiency = Decimal(recipe.est_efficiency)/Decimal(100)
        fermenter_points = gravity_points_potential * bh_efficiency
        fermenter_og = ((fermenter_points/Decimal(recipe.batch_size))/1000) + 1
        chiller_loss_points = fermenter_points * chillerLoss / Decimal(recipe.batch_size)
        preboil_points = fermenter_points + chiller_loss_points
        preboil_og = ((preboil_points/preboilVol)/1000) + 1
        recipe.est_boil_size = preboilVol
        recipe.est_og = fermenter_og
        recipe.est_pre_boil_og = preboil_og
        recipe.est_pre_boil_vol = preboilVol
        try:
            recipe.est_mash_efficiency = preboil_points / gravity_points_potential * 100
        except decimal.InvalidOperation:
            recipe.est_mash_efficiency = Decimal(0)        
        recipe.est_total_water_vol = premashVol

    ## Calculate IBU
    recipe.est_ibu = getIBU(recipe)
    recipe.est_ibu_method = "Tinseth"
    ## TODO: This only does Tinseth
    
    ## Calculate est FG for yeast
    attenuation = DEFAULT_YEAST_ATTENUATION
    if recipe.yeast_usages.first() is not None:
        attenuation = getMaxYeastAttenuation(recipe)
    recipe.est_fg = ((recipe.est_og - Decimal(1)) * Decimal(1000)) * (Decimal(1) - (attenuation)/Decimal(100)) / Decimal(1000) + Decimal(1)
    recipe.est_attenuation = attenuation
    
    ## Calculate ABV estimate
    recipe.est_abv = getABV(recipe.est_og,recipe.est_fg)
    
    # Calculate Color SRM
    recipe.est_color = getSRMColor(recipe)
    
    # Calculate Calories Estimated
    recipe.est_calories = getCalories(recipe.est_og, recipe.est_fg)
    
    # Calculate Mash Profile Usages
    updateMashProfile(recipe)
    
    ######################
    #
    #  Calculate actual values 
    #
    ######################
    
    #Calculate measured mash efficiency
    if recipe.measured_pre_boil_og is not None and recipe.measured_pre_boil_vol is not None:
        try:
            measured_points = (recipe.measured_pre_boil_og - Decimal(1))* Decimal(1000)  * recipe.measured_pre_boil_vol
            #print(measured_points)
            recipe.measured_mash_efficiency = measured_points / gravity_points_potential * 100
        except decimal.InvalidOperation:
            recipe.measured_mash_efficiency = Decimal(0)
    else:
        recipe.measured_mash_efficiency = None
    
    #Calculate Brewhouse Efficiency    
    if recipe.measured_og is not None and recipe.measured_batch_size is not None:
        try:
            measured_points = (recipe.measured_og - Decimal(1))* Decimal(1000)  * recipe.measured_batch_size
            #print(measured_points)
            recipe.measured_efficiency = measured_points / gravity_points_potential * 100
        except decimal.InvalidOperation:
            recipe.measured_efficiency = Decimal(0)        
    else:
        recipe.measured_efficiency = None    
    
    #Calculate Measured Attenuation
    if recipe.measured_og is not None and recipe.measured_fg is not None:
        measured_points = (Decimal(recipe.measured_fg) - Decimal(1) )* Decimal(1000)
        og_points = (Decimal(recipe.measured_og) - Decimal(1))* Decimal(1000)
        #print("Measured:" + str(measured_points) + " OG:" + str(og_points))
        recipe.measured_attenuation = (Decimal(1) -(measured_points / og_points)) * Decimal(100)
        recipe.measured_abv = getABV(recipe.est_og,recipe.est_fg)
    else:
        recipe.measured_attenuation = None    
        recipe.measured_abv = None
    
    recipe.measured_calories = getCalories(recipe.measured_og, recipe.measured_fg)
        
    recipe.save()
    
def updateMashProfile(recipe):
    SPECIFIC_HEAT_GRAIN = Decimal(0.3822)
    
    
    if recipe.mash_profile_usage is not None:
        infuse_amount = 0
        for step_usage in recipe.mash_profile_usage.mash_steps.all():
            if step_usage.mash_step.type == "Infusion":
                step_usage.infuse_amount = step_usage.mash_step.water_grain_ratio * Decimal(2.08635) * getGrainWeight(recipe) 
                print(step_usage.infuse_amount)
                infuse_amount += step_usage.infuse_amount
                step_usage.save()
        print(infuse_amount)
        if infuse_amount == 0:
            recipe.mash_profile_usage.sparge_volume = None
        else:
            recipe.mash_profile_usage.sparge_volume = recipe.est_total_water_vol - infuse_amount
        recipe.mash_profile_usage.save()
        
        ## Mash Temperatures for infusions
        
        for step_usage in recipe.mash_profile_usage.mash_steps.all():
            if step_usage.mash_step.type == "Infusion":
                # calculate infusion temperature
                if step_usage.mash_step.mash_order == 0:
                    step_usage.infuse_temp = getGrainWeight(recipe) * Decimal(1000) * SPECIFIC_HEAT_GRAIN * (Decimal(step_usage.mash_step.step_temp) - Decimal(recipe.mash_profile_usage.grain_temp)) / (Decimal(step_usage.infuse_amount) * Decimal(1000)) + Decimal(step_usage.mash_step.step_temp)
                    step_usage.save()    
                    
            
    
def getCalories(og, fg):
    if og is not None and fg is not None:
        og = Decimal(og)
        fg = Decimal(fg)
        cal_alc = Decimal(1881.22) * fg * (og-fg)/(Decimal(1.775) - og)
        cal_carb = Decimal(Decimal(3550.0)) * fg * ((Decimal(0.1808) * og) + (Decimal(0.8192) * fg) - Decimal(1.0004))    
        return cal_alc + cal_carb
    else:
        return Decimal(0)
        
def getABV(og, fg):
    if og is not None and fg is not None:
        og = Decimal(og)
        fg = Decimal(fg)
        return ((og - fg ) * Decimal(131.25)) * Decimal(100)
    else:
        return Decimal(0)

def getIBU(recipe):
    ibu_total = Decimal(0)
    bigness_factor = Decimal(1.65)*(Decimal(.000125)**(recipe.est_og-Decimal(1)))
    for hop in recipe.hop_usages.all():
        boiltime_factor = (Decimal(1) - Decimal(exp(Decimal(-0.04)*hop.time)))/Decimal(4.15)
        utilization_percent = bigness_factor * boiltime_factor
        hop_alpha_percent = hop.alpha/Decimal(100)
        ibu = Decimal(utilization_percent) * Decimal(hop_alpha_percent) * Decimal(hop.amount) * Decimal(1000000)/Decimal(recipe.batch_size)
        if hop.form == "Pellet":
            ibu = ibu + ibu * DEFAULT_PELLET_ADJUST
        elif hop.form == "Plug":
            ibu = ibu + ibu * DEFAULT_PLUG_ADJUST
        ibu_total += ibu

    return ibu_total


def getGrainWeight(recipe):
    grainWeight = 0
    
    for fermentable_usage in recipe.fermentable_usages.all():
        if fermentable_usage.fermentable.type == "Grain" and fermentable_usage.add_after_boil == False:
            grainWeight += fermentable_usage.amount
    return grainWeight
    
def getGravityPointsPotential(recipe):
    points = 0
    for fermentable_usage in recipe.fermentable_usages.all():
        if fermentable_usage.add_after_boil == False:
            points += fermentable_usage.amount * (fermentable_usage.fermentable.raw_yield/Decimal(100)) * DEFAULT_P_KG_L
            #print(fermentable.fermentable.name + "Added Points:" + str(fermentable.amount * (fermentable.fermentable.raw_yield/Decimal(100)) * DEFAULT_P_KG_L ) + " Total Points:" + str(points))
    #return (points/Decimal(100))
    return points
    
def getSRMColor(recipe):
    #MCU = (grain_color * grain_weight_lbs)/volume_gal
    #SRM = 1.4922 * (mcu ^ 0.6859)
    total_mcu = 0
    for fermentable_usage in recipe.fermentable_usages.all():
        mcu = (fermentable_usage.fermentable.color * kgToPounds(fermentable_usage.amount))/litersToGallons(recipe.batch_size)
        total_mcu += mcu
    srm = Decimal(1.4922) * total_mcu**Decimal(0.6859)
    return srm
    
def getMaxYeastAttenuation(recipe):
    max_attenuation = 0
    for yeast_usage in recipe.yeast_usages.all():
        if yeast_usage.yeast.attenuation > max_attenuation:
            max_attenuation = yeast_usage.yeast.attenuation
    return max_attenuation
    
def getLastDatapoint(sensor):
    try:
        return models.Data.objects.order_by("-timestamp").filter(sensor=sensor)[0:1].get()  
    except models.Data.DoesNotExist:
        return None  
    
    

def gallonsToLiters(gallons):
    return Decimal(gallons) * Decimal(3.785411784)
    
def litersToGallons(liters):
    return Decimal(liters) * Decimal(0.26417205235815)

def kgToPounds(kg):
    return Decimal(kg) / Decimal(0.45359242)
    
def poundsToKg(pounds):
    return Decimal(pounds) / Decimal(2.2046224)
    
def gramsToOz(grams):
    return Decimal(grams) * Decimal(0.035274)
    
def ozToGrams(oz):
    return Decimal(oz) * Decimal(28.3495)
    
def toBool(string):
    return string.lower() in ("yes", "true", "t", "1")
