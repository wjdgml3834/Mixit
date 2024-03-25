import requests
import cache
from datetime import timedelta
from datetime import datetime,timedelta

def _Create_apointment(firstname,lastname,emailaddress,starttime,duration,postalcode,housenr,streetname,typeapoint,bedprod,AddMessagecheck,specialMessage,AddDoctorcheck,Doctorid):   
    
    #generalvar
    url = "https://graph.microsoft.com/v1.0/me/events"
    test = ["Calendars.ReadWrite"]
    token = cache._get_token_from_cache(test)

    #data handeling
    fullname= firstname +" " + lastname
    location = postalcode +" " + housenr +" " + streetname
    parsed_date = datetime.strptime(starttime, "%Y-%m-%dT%H:%M")

    #datetime add duration and calculate time
    if duration == "15":
        Updated_date = parsed_date+ timedelta(minutes=15)
    elif duration == "30":
        Updated_date = parsed_date+ timedelta(minutes=30)
    elif duration == "45":
        Updated_date = parsed_date+ timedelta(minutes=45)
    elif duration == "1":
        Updated_date = parsed_date+ timedelta(hours=1)
    elif duration == "2":
        Updated_date = parsed_date+ timedelta(hours=1)

    #convert back to ISO format
    enddate = Updated_date.isoformat()
    
    if AddDoctorcheck == "true":
        if Doctorid == "1":
            doctorname = "Dr.Smith@mixit.com"
            doctoremail = "Dr. Smith"
        elif Doctorid == "2":
            doctorname = "Dr.Patel@mixit.com"
            doctoremail = "Dr. Patel"
        elif Doctorid == "3":
            doctorname = "Dr.Nguyen@mixit.com"
            doctoremail = "Dr. Nguyen"
        elif Doctorid == "4":
            doctorname = "Dr.García@mixit.com"
            doctoremail = "Dr. García"
        elif Doctorid == "5":
            doctorname = "Dr.Müller@mixit.com"
            doctoremail = "Dr. Müller"
        elif Doctorid == "6":
            doctorname = "Dr.Kim@mixit.com"
            doctoremail = "Dr. Kim"
    
    if bedprod == "true":
        typeapoint = typeapoint + " en bed verschonen"  
          
    if AddMessagecheck == "true":
        jsonmassage =  "Dear " + firstname + ",<br> We hope this message finds you well.<br> This email is to confirm your upcoming healthcare appointment scheduled for " + starttime + " with Mixit. <br> Should you need to make any changes to this appointment or have any inquiries, please don't hesitate to contact us <br> We look forward to seeing you and providing the necessary care for your well-being.<br>" + "With the aditional request of: " + specialMessage + "<br>Best Regards,"

    else:
        jsonmassage =  "Dear " + firstname + ",<br> We hope this message finds you well.<br> This email is to confirm your upcoming healthcare appointment scheduled for " + starttime + " with Mixit. <br> Should you need to make any changes to this appointment or have any inquiries, please don't hesitate to contact us <br> We look forward to seeing you and providing the necessary care for your well-being.<br> Best Regards,"
    
    #json handeling
    if AddDoctorcheck == "true":
        sampleDict = {
        "subject": ""+typeapoint+"",
        "body": {
            "contentType": "HTML",
            "content": ""+jsonmassage+""
        },
        "start": {
            "dateTime": ""+starttime+"",
            "timeZone": "Europe/Berlin"
        },
        "end": {
            "dateTime": ""+enddate+"",
            "timeZone": "Europe/Berlin"
        },
        "location": {
            "displayName": ""+location+""
        },
        "attendees": [
            {
                "emailAddress": {
                    "address": ""+emailaddress+"",
                    "name": ""+fullname+""
                },
                "type": "required"
            },
            {
                "emailAddress": {
                    "address": ""+doctoremail+"",
                    "name": ""+doctorname+""
                },
                "type": "required"
            }
        ],
        "allowNewTimeProposals": "true" 
        }
    else: 
        sampleDict = {
        "subject": ""+typeapoint+"",
        "body": {
            "contentType": "HTML",
            "content": ""+jsonmassage+""
        },
        "start": {
            "dateTime": ""+starttime+"",
            "timeZone": "Europe/Berlin"
        },
        "end": {
            "dateTime": ""+enddate+"",
            "timeZone": "Europe/Berlin"
        },
        "location": {
            "displayName": ""+location+""
        },
        "attendees": [
            {
                "emailAddress": {
                    "address": ""+emailaddress+"",
                    "name": ""+fullname+""
                },
                "type": "required"
            }
        ],
        "allowNewTimeProposals": "true" 
        }

    jsonData = sampleDict
    print(jsonData)
    
    create_apointment = requests.post(  
        url,
        headers={'Authorization': 'Bearer ' + token['access_token']},
        json=jsonData
    ).json()
    
    return  create_apointment

