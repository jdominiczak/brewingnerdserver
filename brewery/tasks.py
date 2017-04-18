from __future__ import absolute_import, unicode_literals
from brewingnerd.celery import app
from brewery import models, util
import requests
from datetime import datetime, timezone
from django.contrib.contenttypes.models import ContentType

NOTIFICATION_RESEND_TIME = 28800 #8 hours  #43200 #12 hours

@app.task
def send_alert_notification(alertTitle, alertDescription, alertUrl):
    send_pushbullet_message(alertTitle, alertDescription, alertUrl)
    return True
    
@app.task
def recurring_watchdog():
    print("Watchdog Process Running")
    for sensor in models.Sensor.objects.all().filter(enabled=True):
        data = util.getLastDatapoint(sensor)
        now_time = datetime.now(timezone.utc)
        if data is not None:
            diff = now_time - data.timestamp
        else:
            diff = now_time - sensor.created_at
        allowed_diff = 3*sensor.checkin_interval*60
        print("Diff:" + str(diff.total_seconds()) + " Allowed:" + str(allowed_diff))
        if allowed_diff < diff.total_seconds():
            create_inactivity_alert(sensor)
        else:
            #see if there is an alert for this and resolve it
            ctype = ContentType.objects.get_for_model(models.Sensor)
            alerts = models.Alert.objects.filter(content_type=ctype, object_id=sensor.id, type="inactivity", resolved_timestamp__isnull=True).order_by("-created_at")
            if len(alerts) > 0:
                for alert in alerts:
                    #If there are multiple alerts still open for this sensor, close them all
                    alert.resolved_timestamp = datetime.now(timezone.utc)
                    if sensor.name is not None:
                        title = "Sensor: " + sensor.name + " is now active."
                        description = "Sensor: " + sensor.name + " (Serial: " + sensor.serial + ") is now active after a period of inactivity."
                    else:
                        title = "Sensor: " + sensor.serial + " is now active."
                        description = "Sensor: " + sensor.serial + " is now active after a period of inactivity."
                    send_pushbullet_message(title, description, "")
                    alert.notification_timestamp = datetime.now(timezone.utc)
                    alert.save()
                    

    return True
    
def create_inactivity_alert(sensor):
    #get list of alerts by sensor provided
    ctype = ContentType.objects.get_for_model(models.Sensor)
    alerts = models.Alert.objects.filter(content_type=ctype, object_id=sensor.id, type="inactivity", resolved_timestamp__isnull=True).order_by("-created_at")
    
    # If there is an alert already, check the notification time to see if we need to resend the alert
    if len(alerts) > 0:
        alert = alerts[0]
        #check notification time
        if alert.notification_timestamp is None or (datetime.now(timezone.utc) - alert.notification_timestamp).total_seconds() > NOTIFICATION_RESEND_TIME:
            #haven't sent out notification - do it now
            send_pushbullet_message(alert.title, alert.description, "")
            alert.notification_timestamp = datetime.now(timezone.utc)
            alert.save()
    else:
        # We need to create a new alert as there is not one already
        if sensor.name is not None:
            title = "Sensor: " + sensor.name + " is inactive."
            description = "Sensor: " + sensor.name + " (Serial: " + sensor.serial + ") is inactive after missing 3 check-in periods."
        else:
            title = "Sensor: " + sensor.serial + " is inactive."
            description = "Sensor: " + sensor.serial + " is inactive after missing 3 check-in periods."
     
        alert = models.Alert(**{"title":title, "description":description, "type":"inactivity", "target":sensor})
        alert.save()
    
    
    
def send_pushbullet_message(title, body, url):
    pburl = "https://api.pushbullet.com/v2/pushes"
    headers = {"Access-Token":"o.kjUIVVWp4RNzTlvdpAVMap2RKpZnkA5y","Content-Type":"application/json"}
    payload = {"type":"note", "title": title, "body":body, "url": url}
    r = requests.post(pburl, json=payload, headers=headers)
    

