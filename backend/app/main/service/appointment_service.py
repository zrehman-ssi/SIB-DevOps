import uuid
import datetime

from ..util.enums import UserType,OrganizationType,AppointmentStatus

from app.main import db # Database
 
from ..util.dto import AppointmentDto #Dto's

from app.main.model.appointment import Appointment #Database Model
from app.main.model.appointment_details import AppointmentDetails #Database Model
from app.main.model.appointment_type import AppointmentType #Database Model

from ..service.user_service import isAdminUser
from ..service.user_service import isDoctor,isPatient,isAdminUser

def getAllAppointments():
    return Appointment.query.all()    

def getAllAppointmentsDetails():
    return AppointmentDetails.query.all()
        

def getAppointmentById(appointment_id):
    return Appointment.query.filter_by(id=appointment_id).first()

def getAppointmentDetailsByAppointmentId(appointment_id):
    return AppointmentDetails.query.filter_by(appointment_id=appointment_id).first()

def getPendingAppointmentsByPatientId(patient_id):
    appointments = Appointment.query.filter_by(patient_id=patient_id).all()
    pending_appointments = []
    if(appointments is not None):
        for appointment in appointments:
            appointmentDetail = AppointmentDetails.query.filter_by(appointment_id=appointment.id).first()
            expireAppointment(appointmentDetail)
            if(appointmentDetail is not None and appointmentDetail.appointment_status == AppointmentStatus.PENDING.value):
                pending_appointments.append(appointmentDetail)

        return pending_appointments
    return pending_appointments            

def getPendingAppointmentsByDoctorId(doctor_id):
    appointments = Appointment.query.filter_by(doctor_id=doctor_id).all()
    pending_appointments = []
    if(appointments is not None):
        for appointment in appointments:
            appointmentDetail = AppointmentDetails.query.filter_by(appointment_id=appointment.id).first()
            #expireAppointment(appointmentDetail)
            if(appointmentDetail is not None and appointmentDetail.appointment_status == AppointmentStatus.PENDING.value):
                pending_appointments.append(appointmentDetail)

        return pending_appointments
    return pending_appointments      

def makeAppointment(appointment):
    if(appointment is not None):
        if(isPatient(appointment.patient_id)== True and isDoctor(appointment.doctor_id)==True and isAppointmentTypeExists(appointment.appointment_type) == True):
            appointmentModel =   Appointment(
                doctor_id = appointment.doctor_id,
                patient_id = appointment.patient_id
            )

            data = saveChanges(appointmentModel)
            if(data is not None):
                appointment_detailsModel = AppointmentDetails(
                    appointment_date = appointment.appointment_date,  
                    created_by = appointment.created_by,
                    created_on = datetime.datetime.utcnow(),
                    appointment_id = data.id,
                    appointment_status = AppointmentStatus.PENDING.value,
                    appointment_type = appointment.appointment_type
                )
                saveChanges(appointment_detailsModel)

def cancelAppointment(cancelAppointment):
    if(cancelAppointment is not None):
        appointment = getAppointmentById(cancelAppointment.appointment_id)
        if(appointment is not None):
            appointmentDetails = getAppointmentDetailsByAppointmentId(cancelAppointment.appointment_id)
            if(appointmentDetails is not None):
                
                appointmentDetails.appointment_status = AppointmentStatus.CANCELLED.value  

                db.session.commit()

def doneAppointment(doneAppointment):
    if(doneAppointment is not None):
        appointment = getAppointmentById(doneAppointment.appointment_id)
        if(appointment is not None):
            appointmentDetails = getAppointmentDetailsByAppointmentId(doneAppointment.appointment_id)
            if(appointmentDetails is not None):
                
                appointmentDetails.appointment_status = AppointmentStatus.DONE.value 
                db.session.commit()

def expireAppointmentById(appointment_id):
    try:
        appointmentDetails = AppointmentDetails.query.filter_by(appointment_id=appointment_id).first()
        if(appointmentDetails is not None):
            dateNow = datetime.datetime.utcnow()
            appoinmentDate= appointmentDetails.appointment_date
            result = appoinmentDate < dateNow
            
            if(result==True):
                appointmentDetails.appointment_status = AppointmentStatus.EXPIRED.value
                db.session.commit()
    except Exception as e:
        print(e)


def expireAppointment(appointmentDetails):
    try:
        if(appointmentDetails is not None):
            dateNow = datetime.datetime.utcnow()
            appoinmentDate= appointmentDetails.appointment_date
            result = appoinmentDate < dateNow
            
            if(result==True):
                appointmentDetails.appointment_status = AppointmentStatus.EXPIRED.value
                db.session.commit()
    except Exception as e:
        print(e)

def saveAppointmentType(appointment_type):
    if(appointment_type is not None):
        if(isAdminUser(appointment_type.user_id) == True):
            existingAppointmentType = AppointmentType.query.filter_by(name=appointment_type.name).first()
            if(existingAppointmentType is None):
                appointmentTypeModel = AppointmentType(
                    name =  appointment_type.name,
                    description =  appointment_type.description,
                    tags =   appointment_type.tags  ,
                    created_by = appointment_type.created_by , 
                    created_on = datetime.datetime.utcnow(),
                    is_deleted =  False
                )
                data = saveChanges(appointmentTypeModel)
                if(data is not None):
                    return True
             
    return False

    
def isAppointmentTypeExists(appointment_type):
    
    try:
        appointment_typeModel = AppointmentType.query.filter_by(id=appointment_type).first()
        if(appointment_typeModel is not None):
            return True
        else:
            return False 
    except Exception as e :
        return False    
    
    

def saveChanges(data):
    db.session.add(data)
    db.session.commit()
    return data      