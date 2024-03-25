import requests
from flask import Flask, render_template, session, request, redirect, url_for, Response, stream_with_context
from flask_session import Session  # https://pythonhosted.org/Flask-Session
import msal
import app_config
import create_apointment
import json
import cache
import build
import time
import os
from azure.servicebus import ServiceBusClient, ServiceBusMessage
from datetime import datetime, timezone, timedelta
from apscheduler.schedulers.background import BackgroundScheduler
import polling 
from datetime_helpers import format_start_date, format_end_time, format_start_time
from flask import jsonify

app = Flask(__name__)
app.config.from_object(app_config)
app.config['session_cookie_name'] = 'my_session_cookie'
app.debug = True
Session(app)
app.jinja_env.filters['format_start_date'] = format_start_date
app.jinja_env.filters['format_end_time'] = format_end_time
app.jinja_env.filters['format_start_time'] = format_start_time

# This section is needed for url_for("foo", _external=True) to automatically
# generate http scheme when this sample is running on localhost,
# and to generate https scheme when it is deployed behind reversed proxy.
# See also https://flask.palletsprojects.com/en/1.0.x/deploying/wsgi-standalone/#proxy-setups
from werkzeug.middleware.proxy_fix import ProxyFix
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

@app.context_processor
def inject_apiurl():
    return dict(ApotheekApiUrl=os.environ.get("ApotheekApiUrl"), PatientApiUrl=os.environ.get("PatientApiUrl"))

def datetimeformat(value=None, format='%Y-%m-%d'):
    if value is None or value == 'now':
        return datetime.now().strftime(format)
    else:
        datetime_obj = datetime.strptime(value.rsplit('.', 1)[0], '%Y-%m-%dT%H:%M:%S')
        return datetime_obj.strftime('%Y-%m-%d %H:%M')

# Add filter to Jinja2 environment
app.jinja_env.filters['datetimeformat'] = datetimeformat

@app.route("/")
def index():
    if not session.get("user"):
        return redirect(url_for("login"))

    token = cache._get_token_from_cache(app_config.SCOPE)
    if not token:
        return redirect(url_for("login"))

    graph_data = requests.get(
        app_config.ENDPOINT,
        headers={'Authorization': 'Bearer ' + token['access_token']},
    ).json()
    # Pass the current date to the template
    today = datetime.now().strftime('%Y-%m-%d')

# filter the Graph api results for appointments happening today
    appointmentsToday = []
    for appointment in graph_data['value']:
        thedate = appointment['start']['dateTime']
        if thedate[0:10] == today: appointmentsToday.append(appointment)
    
    print(appointmentsToday)
       
    # TodayAppointmentsFiltered
    return render_template('index.html', user=session["user"], version=msal.__version__, appointments_today=appointmentsToday, result=graph_data['value'], active_page='Landingspagina', today=today)

@app.route(app_config.REDIRECT_PATH)  # Its absolute URL must match your app's redirect_uri set in AADtoday=datetime.now().strftime('%Y-%m-%d')
def authorized():
    try:
        thecache = cache._load_cache()
        result = build._build_msal_app(cache=thecache).acquire_token_by_auth_code_flow(
            session.get("flow", {}), request.args)
        if "error" in result:
            return render_template("auth_error.html", result=result)
        session["user"] = result.get("id_token_claims")
        cache._save_cache(thecache)
    except ValueError:  # Usually caused by CSRF
        pass  # Simply ignore them
    return redirect(url_for("index"))

@app.route("/graphcall")
def graphcall():
    token = cache._get_token_from_cache(app_config.SCOPE)
    if not token:
        return redirect(url_for("login"))
    graph_data = requests.get(  # Use token to call downstream service
        app_config.ENDPOINT,
        headers={'Authorization': 'Bearer ' + token['access_token']},
        ).json()
    return render_template('display.html', result=graph_data['value'], active_page='Agenda')


#scheduler = BackgroundScheduler()
#polling.start_polling(scheduler)
#scheduler.start()

@app.route("/updated_events")
def show_updated_events():
    updated_events = polling.get_updated_events()
    if updated_events is None:
        return redirect(url_for("login"))
    return render_template('events_table.html', events=updated_events)

@app.route('/Add_Client', methods=['POST'] )
def background_process_test():
    
    #get data post request 
    firstname = request.form['firstname']
    lastname = request.form['lastname']
    emailaddress = request.form['emailaddress']
    starttime = request.form['start-time']
    duration = request.form['duration']
    postalcode = request.form['postalcode']
    housenr = request.form['housenr']
    streetname = request.form['streetname']
    typeapoint = request.form['typeapoint']
    bedprod = request.form['bedprod']          
    AddMessagecheck = request.form['AddMessagecheck']       
    specialMessage = request.form['specialMessage']    
    AddDoctorcheck = request.form['AddDoctorcheck']       
    Doctorid = request.form['Doctorid']       
   
    #call function 
    api_call = create_apointment. _Create_apointment(firstname,lastname,emailaddress,starttime,duration,postalcode,housenr,streetname,typeapoint,bedprod,AddMessagecheck,specialMessage,AddDoctorcheck,Doctorid)
    
    return api_call

@app.route("/login")
def login():
    # Technically we could use empty list [] as scopes to do just sign in,
    # here we choose to also collect end user consent upfront
    session["flow"] = build._build_auth_code_flow(scopes=app_config.SCOPE)
    return render_template("login.html", auth_url=session["flow"]["auth_uri"], version=msal.__version__)

@app.route("/logout")
def logout():
    session.clear()  # Wipe out user and its token cache from session
    return redirect(  # Also logout from your tenant's web session
        app_config.AUTHORITY + "/oauth2/v2.0/logout" +
        "?post_logout_redirect_uri=" + url_for("index", _external=True))

def sendsmstoqueue(nullsixnumber, smstext):

    with open('deployment_output.json') as json_file:
        output_data = json.load(json_file)

    connection_string = output_data['connectionString']['value']    
    queue_name = 'inputsms'

    try:
        # Create a Service Bus client
        with ServiceBusClient.from_connection_string(connection_string) as client:
            # Create a sender for the queue
            with client.get_queue_sender(queue_name) as sender:
                # Concatenate the nullsixnumber and smstext
                message_body = f'{nullsixnumber};{smstext}'
                message = ServiceBusMessage(message_body)
                
                # Send the message
                sender.send_messages(message)

        print('Message sent successfully.')

    except Exception as e:
        print(f'An error occurred: {str(e)}')

def get_event_stream():
    def stream():
        while True:
            updated_events = polling.get_updated_events()
            if updated_events:
                json_data = json.dumps(updated_events)
                yield f"data: {json_data}\n\n"
            time.sleep(2)  

    return Response(stream_with_context(stream()), content_type='text/event-stream')


@app.route('/events')
def stream_events():
    return get_event_stream()

@app.route("/apointmentdetails/<id>", methods=['GET'])
def apointmentdetailspage(id):
    
    hash_url = 'http://127.0.0.1:8000/get_hashedbsn/' + id
    get_hashedbsn = requests.get(
        hash_url
    ).json()   
    patient_url = 'http://127.0.0.1:8000/get_patient/' + get_hashedbsn['hashedbsn']
    patient = requests.get(  
        patient_url
    ).json()
    print(patient)
    
    appointment_url = 'http://127.0.0.1:8000/get_appointment_id/' + id
    appointment = requests.get(  
        appointment_url
    ).json()
    print(appointment)
    address_url = 'http://127.0.0.1:8000/get_address/' + get_hashedbsn['hashedbsn']
    address = requests.get(  
        address_url
    ).json()
    print(address)

    patient_url = 'http://127.0.0.1:4000/get_patient/' + get_hashedbsn['hashedbsn']
    Madicine_patient_id = requests.get(  
        patient_url
    ).json()

    patientid= str(Madicine_patient_id['Patient']['id'])
    print(patientid)

    get_prescription_url = 'http://127.0.0.1:4000/get_prescription/' + patientid
    prescription = requests.get(  
        get_prescription_url
    ).json()
    print(prescription)
    prescriptiondata= str(prescription['Prescription']['name'])


    get_prescriber_url = 'http://127.0.0.1:4000/get_prescriber/' + patientid
    prescriber = requests.get(  
        get_prescriber_url
    ).json()

    madisineid = str(prescriber['Prescriber']['id'])
    get_medicine_url = 'http://127.0.0.1:4000/get_medicine/' + madisineid
    Medicine = requests.get(  
        get_medicine_url
    ).json()
    print(Medicine['Medicine'])

    return render_template('patient_page.html', apointmentsId=id, patient=patient, address=address, appointment=appointment, prescriptiondata=prescription['Prescription'],prescriberdata = prescriber['Prescriber'], medicine=Medicine['Medicine'])

if __name__ == "__main__":
    app.run()


