import json,os

from flask import request
from flask_restplus import Resource
from flask_jwt_extended import jwt_required

from ..util.enums import OrganizationType,UserType
from ..util.enums import ResponseStatus,FileAccessMode
from ..util.constants import GlobalSettings,Messages

from ..util.dto import ResponseDto, PlanDto #Dto's

from ..util.dto import ProviderPlan #Api Model
from ..util.dto import PatientPlan #Api Model

from ..service.plan_service import providerPlanSignup,patientPlanSignup,getAllPatientPlans,getAllProviderPlans,saveProviderPlans
from ..service.file_service import saveFile,getFile,writeFile
from ..service.disease_service import getDiseaseByName
from ..service.organization_service import isProvider

from ..config import NetworkPath

from ..util import parsers
from ..util.parsers import CsvFileParser

_Global_Settings = GlobalSettings
_Messages = Messages

api = PlanDto.api
_providerPlan_dto = PlanDto.providerPlan
_patientPlan_dto=PlanDto.patientPlan 



@api.route('/allProviderPlans')
class ProviderPlanList(Resource):
    @api.doc('list_of_available_provider_plans')
    @api.marshal_list_with(_providerPlan_dto, envelope='data')
    #@jwt_required
    def get(self):
        """List of all available provider plans"""
        return getAllProviderPlans()


@api.route('/allPatientPlans')
class PatientPlanList(Resource):
    @api.doc('list_of_available__patient_plans')
    @api.marshal_list_with(_patientPlan_dto, envelope='data')
    #@jwt_required
    def get(self):
        """List of all available patient plans"""
        return getAllPatientPlans()


@api.route('/providerPlanSignup')
class ProviderPlanSignup(Resource):

    @api.doc('provider plan signup')
    @api.expect(_providerPlan_dto, validate=True)
    #@jwt_required
    def post(self):
        """Signup Provider Plan"""        
         
        data = request.json
        if(data is not None):
            providerPlanDto=ProviderPlan()
            providerPlanDto.name = data['name']
            providerPlanDto.provider_id=data['provider_id']
            providerPlanDto.created_by=data['created_by']
            providerPlanDto.diseases=data['diseases']
            providerPlanDto.planDetails=data['plan_details']

            providerPlanSignup(providerPlanDto)
            return ''
             

@api.route('/patientPlanSignup')
class PatientPlanSignup(Resource):

    @api.doc('patient plan signup')
    @api.expect(_patientPlan_dto, validate=True)
    #@jwt_required
    def post(self):
        """Signup Patient Plan"""        
         
        data = request.json
        if(data is not None):
            patientPlanDto= PatientPlan()
            patientPlanDto.patient_id=data['patient_id']
            patientPlanDto.plan_id=data['plan_id']
            patientPlanDto.diseases=data['diseases']
            patientPlanSignup(patientPlanDto)
            return ''

@api.route('/savePlansContent')
class SavePlansContent(Resource):
    # Sample Json for data is '{"user_id" : 0 , "provider_id" : 0}'
    @api.doc('save plans content')
    @api.expect(parsers.file_upload, validate=True)
    
    def post(self):
        """Save plans content"""

        if request.files is None or 'file' not in request.files:
            #No file found
            response_object=ResponseDto()
            response_object.data=False,
            response_object.status = ResponseStatus.FAIL.value,
            response_object.message = _Messages.FILE_NOT_FOUND
            response_object.status_code=403      
            return response_object.toJson(),403   
        else:
            args = parsers.file_upload.parse_args()             
            
            file = args['file']
            data = args ['data']
            if((file is not None and data is not None) and file.filename != ''):
                response = saveFile(args)
                response_object=response[0]
                guid = response[1]
                if(response_object is not None and response_object.status_code == 200):
                    fileInfoData = json.loads(args['data'])                    
                    user_id = fileInfoData['user_id']  
                    provider_id = fileInfoData['provider_id']  

                    if(isProvider(provider_id) == False):
                        return ''

                    created_by = ''
                    user_type = UserType.PROVIDER_ADMIN.value

                    fileInfo = getFile(user_id , guid)
                    writeFile(fileInfo,NetworkPath,FileAccessMode.WRITE_ONLY_BINARY_MODE)                     
                    parsedData = CsvFileParser.parse(os.path.join(NetworkPath,file.filename))
                    plans = []
                    if(parsedData is not None):
                        for row in parsedData.rows:  
                            disease_ids = []                   
                            providerPlanDto=ProviderPlan()
                            providerPlanDto.name = row['Name']
                            providerPlanDto.provider_id = provider_id
                            providerPlanDto.created_by = created_by
                            providerPlanDto.planDetails = row['Plan_Details']

                            diseases_name = row['Diseases_Name']
                            names = diseases_name.split(',') #Disaeases name split on ','  
                            for name in names :

                                disease = getDiseaseByName(name)
                                if(disease is not None):
                                    disease_ids.append(disease.id)
                            
                            providerPlanDto.diseases= disease_ids
                            
                            plans.append(providerPlanDto)

                        saveProviderPlans(plans)

                else:
                        #No selected file
                        response_object=ResponseDto()
                        response_object.data=False,
                        response_object.status = ResponseStatus.FAIL.value,
                        response_object.message = _Messages.NO_SELECTED_FILE
                        response_object.status_code=403      
                        return response_object.toJson(),403              