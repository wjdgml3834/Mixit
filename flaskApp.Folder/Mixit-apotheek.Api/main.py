from fastapi import FastAPI, HTTPException
from database import session, get_creds
from crud import *
from fastapi.middleware.cors import CORSMiddleware
import os

import json

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

if "ApotheekApiDatabaseName" in os.environ: 
    Session = session(os.environ.get('ApotheekApiDatabaseUsername'), os.environ.get('ApotheekApiDatabasePassword'), os.environ.get('ApotheekApiDatabaseName'))
else:
    Session = session(creds['mixit-apotheek']['username'], creds['mixit-apotheek']['password'], creds['mixit-apotheek']['database_name'])


@app.get("/get_medicine/{medicine_id}")
def read_medicine(medicine_id: int):
    medicine = get_medicine(Session, medicine_id)
    if medicine is None:
        raise HTTPException(status_code=404, detail="Medicine not found")
    #filtered_medicine_data = {
    #    'name': medicine.name,
    #    'amount': medicine.amount,
    #    'strength': medicine.strength,
    #    'usage': medicine.usage
    #}
    return medicine._asdict()


@app.get("/get_patient/{hashed_bsn}")
def read_patient(hashed_bsn: str):
    patient = get_patient(Session, hashed_bsn)
    if patient is None:
        raise HTTPException(status_code=404, detail="Patient not found")
    return patient._asdict()

@app.get("/get_prescriber/{prescriber_id}")
def read_prescriber(prescriber_id: int):
    prescriber = get_prescriber(Session, prescriber_id)
    if prescriber is None:
        raise HTTPException(status_code=404, detail="Prescriber not found")
    return prescriber._asdict()

@app.get("/get_prescription/{prescription_id}")
def read_prescription(prescription_id: int):
    prescription = get_prescription(Session, prescription_id)
    if prescription is None:
        raise HTTPException(status_code=404, detail="Prescription not found")
    return prescription._asdict()

@app.get("/get_prescription_by_prescriber/{prescriber_id}")
def read_prescription_prescriber_id(prescriber_id: int):
    prescription = get_prescription_by_prescriber(Session, prescriber_id)
    if prescription is None:
        raise HTTPException(status_code=404, detail="Prescription not found")
    return prescription._asdict()


# @app.get("/get_patient/{hashed_bsn}")
# def read_patient(hashed_bsn: str):
#     patient = get_patient(Session, hashed_bsn)
#     if patient is None:
#         raise HTTPException(status_code=404, detail="Patient not found")
#     return patient

# @app.get("/get_address/{hashed_bsn}")
# def read_address(hashed_bsn: str):
#     address = get_address(Session, hashed_bsn)
#     if address is None:
#         raise HTTPException(status_code=404, detail="Address not found")
#     return address

# @app.get("/get_policy/{hashed_bsn}")
# def read_policy(hashed_bsn: str):
#     policy = get_policy(Session, hashed_bsn)
#     if not policy:
#         raise HTTPException(status_code=404, detail="Policy not found")
#     return policy

# @app.get("/get_appointment/{email}")
# def read_appointment(email: str):
#     appointment = get_appointment(Session, email)
#     if not appointment:
#         raise HTTPException(status_code=404, detail="Appointment not found")
#     return appointment

# @app.get("/get_patients")
# def read_patients():
#     patients = get_patients(Session)
#     return patients

# @app.get("/get_appointments")
# def read_appointments():
#     appointments = get_appointments(Session)
#     return appointments

# #Please use these formats when creating a new patient
# # patient info: {"firstname": "", "lastname": "", "birthdate": "", "comment": "", "hashedbsn": ""}
# # address info: {"province": "", "city": "", "country": "", "postcode": "", "housenumber": "", "streetname": ""}
# @app.get("/create_patient/{patient_info}/{address_info}")
# def make_patient(patient_info, address_info):
#     try:
#         patient_info = json.loads(patient_info)
#         address_info = json.loads(address_info)
#         patient = create_patient(Session, patient_info, address_info)
#         return "Patient created succesfully"
#     except:
#         raise HTTPException(status_code=500, detail="Please make sure that you are using the right format for inserting information. See docs for more information")