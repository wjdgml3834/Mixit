from sqlalchemy import Column, Integer, String, DateTime, Text, Date, ForeignKey, UniqueConstraint, Table
from sqlalchemy.orm import relationship, DeclarativeBase

class Base(DeclarativeBase):
    pass

prescription_has_medicine = Table(
    "prescription_has_medicine",
    Base.metadata,
    Column("prescription_id", ForeignKey("prescription.id"), primary_key=True, nullable=False),
    Column("medicine_id", ForeignKey("medicine.id"), primary_key=True, nullable=False),
)

prescription_has_patient = Table(
    "prescription_has_patient",
    Base.metadata,
    Column("prescription_id", ForeignKey("prescription.id"), primary_key=True, nullable=False),
    Column("patient_id", ForeignKey("patient.id"), primary_key=True, nullable=False),
)

class Medicine(Base):
    __tablename__ = 'medicine'

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    name = Column(String(255), nullable=False)
    amount = Column(String(45), nullable=False)
    strength = Column(String(45), nullable=False)
    usage = Column(String(45), nullable=False)

class Patient(Base):
    __tablename__ = 'patient'

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False, unique=True)
    hashedbsn = Column(String(255), nullable=True, unique=True)

class Prescriber(Base):
    __tablename__ = 'prescriber'

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False, unique=True)
    firstname = Column(String(45), nullable=False)
    lastname = Column(String(45), nullable=False)

class Prescription(Base):
    __tablename__ = 'prescription'

    id = Column(Integer, primary_key=True)
    name = Column(DateTime, nullable=False)
    prescriber_id = Column(Integer, ForeignKey('prescriber.id'), nullable=False)