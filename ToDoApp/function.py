import re


def validate_pass(password):
    
    if password is None:
        return False
    elif re.match("^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$#%])[A-Za-z\d@$#%]{6,20}$", password):
        return True
    else :
        return False
     
     
def validate_username(username):
    if username is None:
        return False
    elif re.match("^[a-z]+$", username):
        return True
    else:
        return False

def validate_email(email):
    if email is None:
        return False
    
    elif re.match("[^@\s]+@[^@\s]+\.[^@\s]+", email):
        return True
    return False

def firstAndLastName(name):
    if name is None:
        return False
    elif re.match("^[A-Za-z]+$", name):
        return True
    else:
        return False
    
    
def LastName(name):
    if name is None:
        return True
    if re.match("^$|^[A-Za-z]+$", name):
        return True
    else:
        return False

