import uuid
import datetime

from ..util.enums import UserType,OrganizationType

from app.main import db # Database
 
from ..util.dto import DiseaseDto #Dto's

from app.main.model.disease import Disease #Database Model

from ..service.user_service import isAdminUser

def saveDisease(disease):
    try:
        if(disease is not None):
            if(isAdminUser(disease.user_id)==True):
                existingDisease = Disease.query.filter_by(name=disease.name).first()
                if(existingDisease is None):
                    diseaseModel = Disease(
                        name =  disease.name,
                        description =  disease.description,
                        tags =   disease.tags  ,
                        created_by = disease.created_by , 
                        created_on = datetime.datetime.utcnow(),
                        is_deleted =  False,
                        user_id = disease.user_id   
                    )
                    data = saveChanges(diseaseModel)
                    return data

    except Exception as e:
        print(e)
        return None    
    return None

def getDiseaseById(disease_id):
    return Disease.query.filter_by(id=disease_id).first()    

def getDiseaseByName(disease_name):
    return Disease.query.filter_by(name=disease_name).first()

def getAllDiseases():
    return Disease.query.all()    


def saveChanges(data):
    db.session.add(data)
    db.session.commit()
    return data    