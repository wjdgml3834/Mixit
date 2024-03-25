from models import Base, prescription_has_medicine, prescription_has_patient, Medicine, Patient, Prescriber, Prescription
from sqlalchemy.orm import Session
from sqlalchemy import select

def get_medicine(db: Session, medicine_id: int):
    return db.execute(select(Medicine).where(Medicine.id == medicine_id)).first()

def get_patient(db: Session, hashed_bsn: str):
    return db.execute(select(Patient).where(Patient.hashedbsn == hashed_bsn)).first()

def get_prescriber(db: Session, prescriber_id: int):
    return db.execute(select(Prescriber).where(Prescriber.id == prescriber_id)).first()

def get_prescription(db: Session, prescription_id: int):
    return db.execute(select(Prescription).where(Prescription.id == prescription_id)).first()

def get_prescription_by_prescriber(db: Session, prescriber_id: int):
    return db.execute(select(Prescription).where(Prescription.prescriber_id == prescriber_id)).first()

# def get_address(db: Session, hashed_bsn: str):
#     return db.query(Address).join(Patient).filter(Patient.hashedbsn == hashed_bsn).first()

# def get_policy(db: Session, hashed_bsn: str):
#     return db.query(PolicyOption).join(PolicyHasPolicyOption).join(Policy).join(Patient).filter(Patient.hashedbsn == hashed_bsn).all()

# def get_appointment(db: Session, email: str):
#     return db.query(Appointment).join(Employee).filter(Employee.email == email).all()

# def get_patients(db: Session):
#     return db.query(Patient).all()

# def get_appointments(db: Session):
#     return db.query(Appointment).all()


# def create_patient(db: Session, patient_info: dict, address_info: dict):
#     address = Address(province= address_info["province"], city= address_info["city"], country= address_info["country"], postcode= address_info["country"], housenumber= address_info["housenumber"], streetname= address_info["streetname"])
#     db.add(address)
#     db.flush()
#     patient = Patient(firstname= patient_info["firstname"], lastname= patient_info["lastname"], birthdate= patient_info["birthdate"], comment= patient_info["comment"], hashedbsn= patient_info["hashedbsn"], address_id= address.id)
#     db.add(patient)
#     db.commit()

# def create_appointment():
#     pass

