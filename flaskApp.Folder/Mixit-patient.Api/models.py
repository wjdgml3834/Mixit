from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()

class Address(Base):
    __tablename__ = 'address'

    id = Column(Integer, primary_key=True, autoincrement=True)
    streetname = Column(String(45), nullable=False)
    province = Column(String(45), nullable=False)
    city = Column(String(45), nullable=False)
    country = Column(String(45), nullable=False)
    postcode = Column(String(45), nullable=False)
    housenumber = Column(Integer, nullable=False)
    streetname = Column(String(45), nullable=False)

class Patient(Base):
    __tablename__ = 'patient'

    id = Column(Integer, primary_key=True, autoincrement=True)
    firstname = Column(String(45), nullable=False)
    lastname = Column(String(45), nullable=False)
    birthdate = Column(DateTime, nullable=False)
    comment = Column(Text(255), nullable=True)
    hashedbsn = Column(String(255), nullable=False)

    address_id = Column(Integer, ForeignKey('address.id'), nullable=False)
    address = relationship('Address', backref='patients')

    __table_args__ = (UniqueConstraint('id', 'hashedbsn', name='_id_hashedbsn_uc'),)

class Employee(Base):
    __tablename__ = 'employee'

    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String(45), nullable=False)

class Appointment(Base):
    __tablename__ = 'appointment'

    id = Column(Integer, primary_key=True)
    graphql_id = Column(String(255), unique=True, nullable=False)
    date = Column(DateTime, nullable=False)
    summary = Column(Text(1000), nullable=True)
    note = Column(Text(1000), nullable=True)
    patient_id = Column(Integer, ForeignKey('patient.id'), nullable=False)
    employee_id = Column(Integer, ForeignKey('employee.id'), nullable=False)
    completed = Column(Integer, nullable=False, default=0)

    patient = relationship('Patient', backref='appointments')
    employee = relationship('Employee', backref='appointments')

class Policy(Base):
    __tablename__ = 'policy'

    id = Column(Integer, primary_key=True)
    patient_id = Column(Integer, ForeignKey('patient.id'), nullable=False)

    patient = relationship('Patient', backref='policies')

class PolicyOption(Base):
    __tablename__ = 'policy_option'

    id = Column(Integer, primary_key=True)
    name = Column(String(45), nullable=True)

class PolicyHasPolicyOption(Base):
    __tablename__ = 'policy_has_policy_option'

    policy_id = Column(Integer, ForeignKey('policy.id'), primary_key=True, nullable=False)
    policy_option_id = Column(Integer, ForeignKey('policy_option.id'), primary_key=True, nullable=False)

    policy = relationship('Policy', backref='policy_options')
    policy_option = relationship('PolicyOption', backref='policies')
