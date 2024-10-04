import bcrypt

#hashing the password
def hash_password(plain_password:str):
    #Generate a salt and hash the password
    salt=bcrypt.gensalt()
    hashed_password=bcrypt.hashpw(plain_password.encode('utf-8'),salt)
    return hashed_password.decode('utf-8')


#verifying the password
def verify_password(plain_password:str,hashed_password:str):
    #Checking
    return bcrypt.checkpw(plain_password.encode('utf-8'),hashed_password.encode('utf-8'))