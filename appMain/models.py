import re
from django.db import models 
import bcrypt

class UserManager(models.Manager):
    def basic_validator(self, postData):
        error = {}
        email_regex = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        password_regex =re.compile(r'^[a-zA-Z0-9.+_-]')
        special_symbols = ['$','@','#','%','^','&']
        if len(postData['first_name']) < 3 :
            error['first_name'] = "first name should be at least 3 characters"
        if len(postData['last_name']) < 3 :
            error['last_name'] = "last name should be at least 3 characters"
        if len(postData['identity_number']) < 9 :
            error['identity_number'] = "Phone number should be at least 3 characters"
        if len(postData['treatment_field']) < 3 :
            error['treatment_field'] = "treatment field should be at least 3 characters"
        if len(postData['years_of_experience']) < 1 :
            error['years_of_experience'] = "years of experience should be at least 3 characters"
        if len(postData['desc']) < 3 :
            error['desc'] = "description should be at least 3 characters"
        if not email_regex.match(postData['email']) :
            error['email'] = "invaild email"
        if len(postData['password']) < 6:
            error['password_less_than'] = "Password must have atleast 6 characters"
        if len(postData['password']) > 20 :
            error['password_grather_than'] = "'Password cannot have more than 20 characters"
        if not any(characters.isupper() for characters in postData['password']):
            error['password_notInclude_upper'] = "Password must have at least one uppercase character"
        if not any(characters.islower() for characters in postData['password']):
            error['password_notInclude_lower'] = "Password must have at least one lowercase character"
        if not any(characters.isdigit() for characters in postData['password']):
            error['password_notInclude_number'] = "Password must have at least one numeric character."
        if not any(characters in special_symbols for characters in postData['password']):
            error['password_symbol'] = "Password should have at least one of the symbols $@#%^&"
        if postData['password'] != postData['confirm_password']:
            error['not_the_same'] = "please insert password similer as above"
        return error
    
    def edit_login_validator(self, postData):
        error = {}
        email_regex = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        special_symbols = ['$','@','#','%','^','&']
        if not email_regex.match(postData['email']) :
            error['email'] = "invaild email"
        if len(postData['password']) < 6:
            error['password_less_than'] = "Password must have atleast 6 characters"
        if len(postData['password']) > 20 :
            error['password_grather_than'] = "'Password cannot have more than 20 characters"
        if not any(characters.isupper() for characters in postData['password']):
            error['password_notInclude_upper'] = "Password must have at least one uppercase character"
        if not any(characters.islower() for characters in postData['password']):
            error['password_notInclude_lower'] = "Password must have at least one lowercase character"
        if not any(characters.isdigit() for characters in postData['password']):
            error['password_notInclude_number'] = "Password must have at least one numeric character."
        if not any(characters in special_symbols for characters in postData['password']):
            error['password_symbol'] = "Password should have at least one of the symbols $@#%^&"
        if postData['password'] != postData['confirm_password']:
            error['not_the_same'] = "please insert password similer as above"
        return error
        
    def sigin_validator(self, postData):
        error = {}
        userid = User.objects.filter(email = postData['email'])
        print(postData['email'])
        if len(userid) == 0 :
            error['user_not_found'] = "user not exisit"
            return error
        user = userid[0]
        if (bcrypt.checkpw(postData['password'].encode(), user.password.encode()) != True):
            error['incorrect_password'] = "you insert password error"
        return error

    def request_validator(self, postData):
        error = {}
        email_regex = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if len(postData['full_name']) < 3 :
            error['full_name'] = "full name should be at least 3 characters"
        if len(postData['age']) < 2 :
            error['age'] = " age should be at least 2 characters"
        if len(postData['identity_number']) < 8 :
            error['identity_number'] = " identity number should be 10 characters"
        if len(postData['phone_number']) < 10 :
            error['phone_number'] = "phone number should be at least 10 characters "
        if len(postData['telphone_number']) < 6 :
            error['telphone_number'] = " telphone number should be at least 6 characters"
        if not email_regex.match(postData['email']) :
            error['email'] = "invaild email "
        if len(postData['state']) < 3 :
            error['state'] = "state should be at least 3 characters "
        if len(postData['street']) < 3 :
            error['street'] = " street name should be at least  c3haracters"
        if len(postData['service_desc']) < 10 :
            error['service_desc'] = " service description should be at least 10 characters"
        if len(postData['therapist']) < 1 :
            error['therapist'] = "you should choice therapist "
        return error

    def message_validator(self, postData):
        error = {}
        if len(postData['send_from']) < 3 :
            error['send_from'] = "sender should be at least 3 characters "
        if len(postData['message_context']) < 1 :
            error['message_context'] = "message should be at least 1 characters "
        if len(postData['send_to']) < 3 :
            error['send_to'] = " should select reciever "
        return error


class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    number = models.CharField(max_length=255,default='')
    treatment_field = models.TextField(default=None)
    years_of_experience = models.CharField(max_length=255,default='')
    desc = models.TextField(default=None)
    certificate = models.FileField(upload_to="certificates/", max_length=250,null=True,default='')
    photograph = models.FileField(upload_to="photographs/", max_length=250,null=True,default='')
    password = models.CharField(max_length=255)
    user_level = models.CharField(max_length = 255, default='proccser')
    address = models.CharField(max_length=255,default='')
    created_at=models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    # orders = list of orders for every therapist
    # messages_recieve = list of recieve messages
    # message_send = list of messages send
    objects = UserManager()

class Order(models.Model):
    full_name = models.CharField(max_length=255)
    age = models.CharField(max_length=255)
    identity_number = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=255)
    telphone_number = models.CharField(max_length=255)
    email =models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    street = models.CharField(max_length=255)
    therapist = models.ForeignKey(User , related_name="orders", on_delete=models.DO_NOTHING)
    service_desc = models.TextField()
    created_at=models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

class Message(models.Model):
    message_context = models.TextField()
    send_to = models.ForeignKey(User, related_name="messages_recieve" , on_delete=models.DO_NOTHING)
    send_from = models.ForeignKey(User , related_name="message_send" , on_delete=models.DO_NOTHING)
    created_at=models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

# register new user
def Register(request):
    first_name = request.POST['first_name']
    last_name = request.POST['last_name']
    email = request.POST['email']
    password = request.POST['password']
    identity_number = request.POST['identity_number']
    treatment_field = request.POST['treatment_field']
    years_of_experience = request.POST['years_of_experience']
    desc = request.POST['desc']
    certificate = request.POST['certificate']
    photograph = request.POST['photograph']
    user_level = request.POST['user_level']
    pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode() 
    if (request.POST['confirm_password'] == password):
        user =  User.objects.create(first_name = first_name , last_name = last_name, email = email , password = pw_hash, number=identity_number ,treatment_field=treatment_field,years_of_experience=years_of_experience,desc=desc,certificate=certificate,photograph=photograph,user_level=user_level,address='office')

    current_user = User.objects.get(id = user.id)
    if current_user.id == 1 :
        current_user.user_level = "admin"
        return current_user.save()
    else:
        current_user.user_level = "proccser"
        return current_user.save()

# login current user
def Login(request):
    user = User.objects.filter(email = request.POST['email'])
    if user:
        loged_user = user[0]
        if bcrypt.checkpw(request.POST['password'].encode(), loged_user.password.encode()):
            # request.session['userid'] = loged_user.id
            return loged_user.id
    else:
        return None

# edit profile by admin
def edit_by_admin(id,first_name,last_name,email,number,treatment_field,years_of_experience,desc,certificate,photograph,user_level):
    user = User.objects.get(id=id)
    user.first_name = first_name
    user.last_name = last_name
    user.email = email
    user.number = number
    user.treatment_field = treatment_field
    user.years_of_experience = years_of_experience
    user.desc = desc
    user.certificate = certificate
    user.photograph = photograph
    user.user_level = user_level
    print("333")
    return user.save()

# get all users
def get_all_user(request):
    return User.objects.all()

# edit login info
def edit_Login_data(id,email,password,confirm_password):
    user = User.objects.get(id=id)
    pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
    if(password == confirm_password):
        user.password = pw_hash
        user.email = email
    return user.save()

# delete user from database
def delete_user(id):
    user = User.objects.get(id=id)
    return user.delete()

# get all therapist
def get_all_therapist(request):
    return User.objects.all()

# add request
def add_request_to_therapist(full_name,age,identity_number,phone_number,telphone_number,email,state,street,service_desc,therapist):
    return Order.objects.create(full_name=full_name,age=age,identity_number=identity_number,phone_number=phone_number,telphone_number=telphone_number,email=email,state=state,street=street,service_desc=service_desc,therapist=therapist)

# get all requests
def get_all_requests(request):
    return Order.objects.all()

#get specific request
def get_request(id):
    return Order.objects.get(id=id)

# delete request
def delete_request(id):
    request = Order.objects.get(id=id)
    return request.delete()

# store message in database
def send_message(message_context,send_from,send_to):
    return Message.objects.create(message_context = message_context , send_from = send_from , send_to = send_to)

# delete message
def del_message(message):
    return message.delete()

def get_therapists(request):
    return User.objects.filter(user_level = "process")