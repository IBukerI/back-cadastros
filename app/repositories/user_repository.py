from app import db
from app.models import User 


def find_user_by_email(email):
    try:        
        user = User.query.filter_by(email=email).first()        
        if user:
            return True
        return False
    except Exception as e:   
        return(f"An error occurred: {e}")
    
def find_user_by_cpf(cpf):
    try:
        user = User.query.filter_by(cpf=cpf).first()
        if user:
            return True
        return False
    except Exception as e:   
        return(f"An error occurred: {e}")
    
def find_user_by_email_return_id(email):
    try:
        user = User.query.filter_by(email=email).first()
        if user:
            return user.id
        return False
    except Exception as e:   
        return(f"An error occurred: {e}")
    
def find_user_by_id(id):
    try:
        user = User.query.filter_by(id=id).first()
        if user:
            return user
        return False
    except Exception as e:   
        return(f"An error occurred: {e}")
    
def return_user_list():
    try:
        user_list = User.query.all()
        return [user.to_dict() for user in user_list]
    except Exception as e:
        return(f"An error occurred: {e}")