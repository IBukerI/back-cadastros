from app import db
from app.models import User  

def find_password_by_user(email):
    try:        
        user = User.query.filter_by(email=email, ativo=1).first()        
        if user:
            return user.senha_hash
        return None
    except Exception as e:   
        return(f"An error occurred: {e}")
        
