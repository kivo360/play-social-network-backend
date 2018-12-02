import re

def validate_password(password):
    if len(password) < 8:
        return "Make sure your password is at lest 8 letters", 400
    elif re.search('[0-9]',password) is None:
        return "Make sure your password has a number in it", 400
    elif re.search('[A-Z]',password) is None: 
        return "Make sure your password has a capital letter in it", 400
    else:
        return "Your password seems fine", 200
    

def validate_pin(pin):
    if len(str(pin)) < 6:
        return "Make sure your pin has at least 6 digits", 400   
    else:
        return "You pin is fine", 200