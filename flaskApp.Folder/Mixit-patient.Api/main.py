from fastapi import FastAPI, HTTPException
from database import session, get_creds
from crud import get_patient, get_policy, get_appointment, get_address, get_patients, get_appointments, create_patient, get_appointment_id, get_hashedbsn
from fastapi.middleware.cors import CORSMiddleware
import json
import os

app = FastAPI(debug=True)

origins = [
    "http://localhost:8080",
    "http://localhost:5000",
    "http://localhost:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

creds   = get_creds("cred.json")

if "PatientApiDatabaseName" in os.environ: 
    Session = session(os.environ.get('PatientApiDatabaseUsername'), os.environ.get('PatientApiDatabasePassword'), os.environ.get('PatientApiDatabaseName'))
else:
    Session = session(creds['mixit-patient']['username'], creds['mixit-patient']['password'], creds['mixit-patient']['database_name'])


@app.get("/get_address_by_patient_id/{id}")
def read_patient(id: int):
    patient = get_patient_by_id(Session, id)
    if patient is None:
        raise HTTPException(status_code=404, detail="Patient not found")
    print(patient.hashedbsn)
    adress = get_address(Session, patient.hashedbsn)
    if adress is None: 
        raise HTTPException(status_code=404, detail="Adress not found")
    return adress

@app.get("/get_patient_by_id/{id}")
def read_patient(id: int):
    patient = get_patient_by_id(Session, id)
    if patient is None:
        raise HTTPException(status_code=404, detail="Patient not found")
    return patient

@app.get("/get_patient/{hashed_bsn}")
def read_patient(hashed_bsn: str):
    patient = get_patient(Session, hashed_bsn)
    if patient is None:
        raise HTTPException(status_code=404, detail="Patient not found")
    filtered_patient_data = {
        'firstname': patient.firstname, 
        'lastname': patient.lastname,
        'birthdate': patient.birthdate
        }
    return filtered_patient_data 

@app.get("/get_address/{hashed_bsn}")
def read_address(hashed_bsn: str):
    address = get_address(Session, hashed_bsn)
    if address is None:
        raise HTTPException(status_code=404, detail="Address not found")
    filtered_address_data = {
        'straatnaam': address.streetname,
        'huisnummer': address.housenumber,
        'postcode': address.postcode,
        'stad': address.city
    }
    return filtered_address_data

@app.get("/get_policy/{hashed_bsn}")
def read_policy(hashed_bsn: str):
    policy = get_policy(Session, hashed_bsn)
    if not policy:
        raise HTTPException(status_code=404, detail="Policy not found")
    return policy

@app.get("/get_appointment/{email}")
def read_appointment(email: str):
    appointment = get_appointment(Session, email)
    if not appointment:
        raise HTTPException(status_code=404, detail="Appointment not found")
    return appointment

 
    
@app.get("/get_appointment_id/{graphql_id}")
def read_appointment(graphql_id: str):
    appointment = get_appointment_id(Session, graphql_id)
    if not appointment:
        raise HTTPException(status_code=404, detail="Appointment not found")
    filtered_appointment_data = {
        'datum': appointment.date,
        'samenvatting': appointment.summary,
        'notitie': appointment.note,
        'medewerker': appointment.employee_id
    }
    return filtered_appointment_data

@app.get("/get_patients")
def read_patients():
    patients = get_patients(Session)
    return patients

@app.get("/get_appointments")
def read_appointments():
    appointments = get_appointments(Session)
    return appointments

#Please use these formats when creating a new patient:
# patient info: {"firstname": "", "lastname": "", "birthdate": "", "comment": "", "hashedbsn": ""}
# address info: {"province": "", "city": "", "country": "", "postcode": "", "housenumber": , "streetname": ""}
@app.get("/create_patient/{patient_info}/{address_info}")
def make_patient(patient_info, address_info):
    try:
        patient_info = json.loads(patient_info)
        address_info = json.loads(address_info)
        patient = create_patient(Session, patient_info, address_info)
        return "Patient created succesfully"
    except:
        raise HTTPException(status_code=500, detail="Please make sure that you are using the right format for inserting information. See docs for more information")

@app.get("/get_hashedbsn/{graphql_id}")
def read_hashedbsn(graphql_id: str):
    bsn = get_hashedbsn(Session, graphql_id)
    if bsn is None:
        raise HTTPException(status_code=404, detail="Hashedbsn not found")
    return {"hashedbsn": bsn[0]}
