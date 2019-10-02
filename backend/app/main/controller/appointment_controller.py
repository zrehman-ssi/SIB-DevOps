import json,os,datetime

from flask import request
from flask_restplus import Resource
from flask_jwt_extended import jwt_required

from ..util.enums import OrganizationType
from ..util.constants import Messages,GlobalSettings

from ..util.dto import ResponseDto,AppointmentDto #Dto's

from ..util.dto import Appointment,MakeAppointment,AppointmentType #Api Model
 
from ..service.appointment_service import getAllAppointments,getAllAppointmentsDetails,makeAppointment,saveAppointmentType,cancelAppointment,getPendingAppointmentsByPatientId,getPendingAppointmentsByDoctorId,getAppointmentById,doneAppointment



api = AppointmentDto.api
_appointment_dto = AppointmentDto.appointment
_make_appointment_dto = AppointmentDto.makeAppointment
_appointment_type_dto = AppointmentDto.appointmentType
_pending_appointment_dto = AppointmentDto.pendingAppointment
_appointmentDetails_dto = AppointmentDto.appointmentDetails

_GlobalSettings = GlobalSettings

@api.route('/getAppointments')
class Appointments(Resource):
    @api.doc('list_of_available_appointments_details')
    @api.marshal_list_with(_appointment_dto, envelope='data')
    #@jwt_required
    def get(self):
        """List of all available appointments details"""
        return getAllAppointmentsDetails()

@api.route('/getAppointment/<appointment_id>')
class GetAppointment(Resource):
    @api.doc('appointment details')
    @api.marshal_list_with(_appointmentDetails_dto, envelope='data')
    #@jwt_required
    def get(self,appointment_id):
        """appointment details"""
        return getAppointmentById(appointment_id)


@api.route('/makeAppointment')
class MakeAppointment(Resource):

    @api.doc('make appointment')
    @api.expect(_make_appointment_dto, validate=True)
    #@jwt_required
    def post(self):
        """Make Appointment"""        
         
        data = request.json
        if(data is not None):
            makeAppointment_dto = MakeAppointment()
            makeAppointment_dto.appointment_date =datetime.datetime.strptime(data['appointment_date'], _GlobalSettings.DEFAULT_DATE_TIME_FORMAT) 
            makeAppointment_dto.created_by = data['created_by'] 
            makeAppointment_dto.doctor_id = data['doctor_id']
            makeAppointment_dto.patient_id = data['patient_id'] 
            makeAppointment_dto.appointment_type = data['appointment_type'] 
            
            makeAppointment(makeAppointment_dto)
            return ''


@api.route('/doneAppointment')
class DoneAppointment(Resource):

    @api.doc('done appointment')
    @api.expect(_appointment_dto, validate=True)
    #@jwt_required
    def post(self):
        """Done Appointment"""        
         
        data = request.json
        if(data is not None):
            doneAppointment_dto = Appointment()            
            doneAppointment_dto.appointment_id = data['appointment_id'] 
            doneAppointment(doneAppointment_dto) 
            return ''


@api.route('/cancelAppointment')
class CancelAppointment(Resource):

    @api.doc('cancel appointment')
    @api.expect(_appointment_dto, validate=True)
    #@jwt_required
    def post(self):
        """Cancel Appointment"""        
         
        data = request.json
        if(data is not None):
            cancelAppointment_dto = Appointment()            
            cancelAppointment_dto.appointment_id = data['appointment_id']             
            
            cancelAppointment(cancelAppointment_dto)
            return ''


@api.route('/getPendingAppointmentsByPatientId/<patient_id>')
class PendingPatientAppointments(Resource):
    @api.doc('list_of_pending_patients_appointments')
    @api.marshal_list_with(_pending_appointment_dto, envelope='data')
    #@jwt_required
    def get(self,patient_id):
        """List of all pending patients appointments"""
        return getPendingAppointmentsByPatientId(patient_id)


@api.route('/getPendingAppointmentsByDoctorId/<doctor_id>')
class PendingDoctorAppointments(Resource):
    @api.doc('list_of_pending_doctors_appointments')
    @api.marshal_list_with(_pending_appointment_dto, envelope='data')
    #@jwt_required
    def get(self,doctor_id):
        """List of all pending doctors appointments"""
        return getPendingAppointmentsByDoctorId(doctor_id)


@api.route('/saveAppointmentType')
class AppointmentType(Resource):

    @api.doc('save appointment type')
    @api.expect(_appointment_type_dto, validate=True)
    #@jwt_required
    def post(self):
        """Save appointment type"""        
         
        data = request.json
        if(data is not None):
            appointmentType_dto = AppointmentType()
            appointmentType_dto.name = data['name']
            appointmentType_dto.description = data['description']
            appointmentType_dto.created_by = data['created_by']
            appointmentType_dto.tags = data['tags']
            appointmentType_dto.user_id = data['user_id']
            saveAppointmentType(appointmentType_dto)
            
            return ''            