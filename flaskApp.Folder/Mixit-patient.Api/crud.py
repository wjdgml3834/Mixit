from models import Base, Patient, Policy, Address, Employee, Appointment, PolicyHasPolicyOption, PolicyOption
from sqlalchemy.orm import Session


def get_patient_by_id(db: Session, id: int):
    return db.query(Patient).filter(Patient.id == id).first()

def get_patient(db: Session, hashed_bsn: str):
    return db.query(Patient).filter(Patient.hashedbsn == hashed_bsn).first()

def get_address(db: Session, hashed_bsn: str):
    return db.query(Address).join(Patient).filter(Patient.hashedbsn == hashed_bsn).first()

def get_policy(db: Session, hashed_bsn: str):
    return db.query(PolicyOption).join(PolicyHasPolicyOption).join(Policy).join(Patient).filter(Patient.hashedbsn == hashed_bsn).all()

def get_appointment(db: Session, email: str):
    return db.query(Appointment).join(Employee).filter(Employee.email == email).all()

def get_appointment_id(db: Session, graphql_id: str):
    return db.query(Appointment).filter(Appointment.graphql_id == graphql_id).first()

def get_patients(db: Session):
    return db.query(Patient).all()

def get_appointments(db: Session):
    return db.query(Appointment).all()


def create_patient(db: Session, patient_info: dict, address_info: dict):
    address = Address(province= address_info["province"], city= address_info["city"], country= address_info["country"], postcode= address_info["country"], housenumber= address_info["housenumber"], streetname= address_info["streetname"])
    db.add(address)
    db.flush()
    patient = Patient(firstname= patient_info["firstname"], lastname= patient_info["lastname"], birthdate= patient_info["birthdate"], comment= patient_info["comment"], hashedbsn= patient_info["hashedbsn"], address_id= address.id)
    db.add(patient)
    db.commit()

def create_appointment():
    pass

def get_hashedbsn(db: Session, graphql_id: str):

    return db.query(Patient.hashedbsn).join(Appointment).filter(Appointment.graphql_id == graphql_id).first()
