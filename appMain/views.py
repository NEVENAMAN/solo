from django.shortcuts import render,redirect
from django.contrib import messages
from .models import *

def form_page(request):
    therapists = get_all_therapist(request)
    for i in therapists :
        print(i.first_name)
    context = {
        "therapists" : therapists,
    }
    return render(request,'index.html',context)

# welcome page after visitor send a request
def welcome_page(request):
    visitor = request.session['full_name']
    context = {
        "visitor" : visitor,
    }
    return render(request,'welcome_page.html',context)
# register method
def register(request):
    print("***** 1 ")
    error = User.objects.basic_validator(request.POST)
    if len(error) > 0:
        print("***** 2 ")
        for key, value in error.items():
            messages.error(request, value, extra_tags=key)
        return redirect('/register_page')
    else:
        if request.method == "POST":
            print("***** 3 ")
            Register(request)
            print("***** 4 ")
        return redirect('/')

# login method
def login(request):
    error = User.objects.sigin_validator(request.POST)
    if len(error) > 0:
        print("***** 2 ")
        for key, value in error.items():
            messages.error(request, value, extra_tags=key)
        return redirect('/login_page')
    else:
        userId =  Login(request)
        print(userId)
        if userId != None :
            print("333")
            request.session['userid'] = userId
            user = User.objects.get(id =request.session['userid'] )
            if user.user_level == 'admin' :
                print("444")
                return redirect('/dashboard_page')
            else:
                return redirect('/therapist_dashboard/'+ str( user.id))
        else:
            print("4444")
        return redirect('/')  

# send user request
def send_user_request(request,id):
    therapist = User.objects.get(id=id)
    therapists = get_all_therapist(request)
    context = {
        "therapist" : therapist,
        "therapists" : therapists,
    }
    return render(request,'send_request.html',context)

# send visitor request
def send_visitor_request(request):
    request.session['full_name'] = request.POST['full_name']
    therapist_id= request.POST['therapist_id']
    therapist = User.objects.get(id=therapist_id)
    error = Order.objects.request_validator(request.POST)
    if len(error) > 0:
        print("***** 2 ")
        for key, value in error.items():
            messages.error(request, value, extra_tags=key)
        return redirect('/send_user_request/'+str(therapist.id))
    else:
        request.session['full_name'] = request.POST['full_name']
        full_name = request.POST['full_name']
        print(full_name)
        age = request.POST['age']
        identity_number = request.POST['identity_number']
        phone_number = request.POST['phone_number']
        telphone_number = request.POST['telphone_number']
        email = request.POST['email']
        state = request.POST['state']
        street = request.POST['street']
        service_desc = request.POST['service_desc']
        therapist_Select = request.POST['therapist']
        therapist = User.objects.filter(treatment_field = therapist_Select)
        add_request_to_therapist(full_name,age,identity_number,phone_number,telphone_number,email,state,street,service_desc,therapist[0])
        return redirect('/welcome_page')

# add member page
def add_member_page(request):
    if 'userid' in request.session:
        admin = User.objects.get(id=request.session['userid'])
        context = {
            "admin":admin,
        }
        return render(request,'add_member.html',context)
    else:
        return redirect('/login_page')

# register page
def register_page(request):
    return render(request,'register.html')

# login page
def login_page(request):
    return render(request,'login.html')

# dashboard page
def dashboard_page(request):
    if 'userid' in request.session:
        admin = User.objects.get(id=request.session['userid'])
        context = {
            "admin":admin,
        }
        return render(request,'dashboard.html',context)
    else:
        return redirect('/login_page')

# edit_profile_by_admin page
def edit_by_admin_page(request,id):
    if 'userid' in request.session:
        user = User.objects.get(id=id)
        admin = User.objects.get(id=request.session['userid'])
        print("id : ",admin.id)
        print("id : ",user.id)
        context = {
            "admin" :admin,
            "user" :user,
        }
        return render(request,'edit_profile.html',context)
    else:
        return redirect('/login_page')

# edit by admin method
def edit_method_by_admin(request,id):
    print("000")
    first_name = request.POST['first_name']
    last_name = request.POST['last_name']
    email = request.POST['email']
    identity_number = request.POST['identity_number']
    treatment_field = request.POST['treatment_field']
    years_of_experience = request.POST['years_of_experience']
    desc = request.POST['desc']
    certificate = request.POST['certificate']
    photograph = request.POST['photograph']
    user_level = request.POST['user_level']
    print(user_level)
    print("111")
    edit_by_admin(id,first_name,last_name,email,identity_number,treatment_field,years_of_experience,desc,certificate,photograph,user_level)
    return redirect('/members_page')

# edit_login_page
def edit_login_page(request,id):
    if 'userid' in request.session:
        admin = User.objects.get(id=request.session['userid'])
        user = User.objects.get(id=id)
        context = {
            "admin" : admin,
            "user" : user,
        }
        return render(request,'edit_login_info.html',context)
    else:
        return redirect('/login_page')

# edit login information
def edit_login_info(request,id):
    user_id = User.objects.get(id=id)
    error = User.objects.edit_login_validator(request.POST)
    if len(error) > 0:
        print("***** 2 ")
        for key, value in error.items():
            messages.error(request, value, extra_tags=key)
        return redirect('/edit_login_page/'+str(user_id.id))
    else:
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        edit_Login_data(id,email,password,confirm_password)
        return redirect('/dashboard_page')

# run members page
def members_page(request):
    if 'userid' in request.session:
        admin = User.objects.get(id=request.session['userid'])
        members = get_all_user(request)
        context = {
            "admin" : admin,
            "members" : members,
        }
        return render(request,'members.html',context)
    else:
        return redirect('/login_page')

# add member method from admin
def add_member_by_admin(request):
    error = User.objects.basic_validator(request.POST)
    if len(error) > 0:
        print("***** 2 ")
        for key, value in error.items():
            messages.error(request, value, extra_tags=key)
        return redirect('/add_member_page')
    else:
        if request.method == "POST":
            print("***** 3 ")
            Register(request)
            print("***** 4 ")
        return redirect('/members_page')

# edit member page
def edit_member_page(request,id):
    if 'userid' in request.session:
        admin = User.objects.get(id=request.session['userid'])
        user = User.objects.get(id=id)
        context = {
            "admin" : admin,
            "member" : user,
        }
        return render(request,'edit_member_control.html',context)
    else:
        return redirect('/login_page')

# delete user from database
def del_member(request,id):
    delete_user(id)
    return redirect('/members_page')


# view dashboard therpist
def dash_therpist(request):
    if 'userid' in request.session:
        return render(request,'dash_therpist.html')
    else:
        return redirect('/login_page')
# add request page
def add_request_page(request):
    admin = User.objects.get(id=request.session['userid'])
    therapists = get_all_therapist(request)
    context = {
        "admin":admin,
        "therapists" : therapists,
    }
    return render(request,'add_request.html',context)

# add request by admin
def add_request(request):
    error = Order.objects.request_validator(request.POST)
    if len(error) > 0:
        print("***** 2 ")
        for key, value in error.items():
            messages.error(request, value, extra_tags=key)
        return redirect('/add_request_page')
    else:
        full_name = request.POST['full_name']
        age = request.POST['age']
        identity_number = request.POST['identity_number']
        phone_number = request.POST['phone_number']
        telphone_number = request.POST['telphone_number']
        email = request.POST['email']
        state = request.POST['state']
        street = request.POST['street']
        service_desc = request.POST['service_desc']
        therapist_Select = request.POST['therapist']
        therapist = User.objects.filter(treatment_field = therapist_Select)
        add_request_to_therapist(full_name,age,identity_number,phone_number,telphone_number,email,state,street,service_desc,therapist[0])
        return redirect('/requests_page')

# view all requests
def requests_page(request):
    if 'userid' in request.session:
        admin = User.objects.get(id=request.session['userid'])
        requests = get_all_requests(request)
        context = {
            "admin":admin,
            "requests" : requests,
        }
        return render(request,'requests.html',context)
    else:
        return redirect('/login_page')

# send message page
def send_message_page(request):
    if 'userid' in request.session:
        admin = User.objects.get(id=request.session['userid'])
        users = get_all_user(request)
        context = {
            "admin":admin,
            "users" : users,
        }
        return render(request,'send_message.html',context)
    else:
        return redirect('/login_page')
# send message method
def send_message_method(request):
    error = Order.objects.message_validator(request.POST)
    if len(error) > 0:
        print("***** 2 ")
        for key, value in error.items():
            messages.error(request, value, extra_tags=key)
        return redirect('/send_message_page')
    else:
        sender = User.objects.filter( first_name = request.POST['send_from'])
        print(sender[0].first_name)
        message_context = request.POST['message_context']
        send_from = sender[0]
        reciver = User.objects.filter(first_name = request.POST['send_to'])
        send_to = reciver[0]
        send_message(message_context,send_from,send_to)
        if send_from.user_level == "admin":
            return redirect('/messages_page/' + str(send_from.id))
        else:
            return redirect('/therapist_messages/'+ str(send_from.id))

# messages page
def messages_page(request,id):
    if 'userid' in request.session:
        admin = User.objects.get(id=request.session['userid'])
        user = User.objects.get(id = id)
        messages_recieve =user.messages_recieve.all()
        message_send = user.message_send.all()
        context = {
            "admin" : admin,
            "user" : user,
            "messages_recieve" : messages_recieve,
            "message_send" : message_send, 
        }
        return render(request,'view_messages.html',context)
    else:
        return redirect('/login_page')

# view message data
def view_message_data(request,id):
    if 'userid' in request.session:
        admin = User.objects.get(id=request.session['userid'])
        message = Message.objects.get(id=id)
        context = {
            "admin" :admin,
            "message" : message,
        }
        return render(request,'view_message_data.html',context)
    else:
        return redirect('/login_page')
# delete message 
def delete_message(request,id):
    message = Message.objects.get(id=id)
    del_message(message)
    return redirect('/messages_page/' + str(id))



# therapist dashbpard methos-----------------------------------------------------------------------

# view therapist dashboard
def therpist_dash(request,id):
    if 'userid' in request.session:
        therapist = User.objects.get(id=id)
        context = {
            "therapist" : therapist,
        }
        return render(request,'dash_therapist.html',context)
    else:
        return redirect('/login_page')

# view all therapist requests
def therpist_requests(request,id):
    if 'userid' in request.session:
        therapist = User.objects.get(id=id)
        therapist_requests = User.objects.get(id=id)
        requests = therapist_requests.orders.all()
        context = {
            "therapist" : therapist,
            "requests" : requests,
        }
        return render(request,'therapist_requests.html',context)
    else:
        return redirect('/login_page')

# delete request
def del_request(request,id):
    delete_request(id)
    return redirect('/requests_page')

# delete therpist request
def del_therapist_request(request,id):
    therapist = User.objects.get(id = request.session['userid'])
    delete_request(id)
    return redirect('/therapist_request/'+str(therapist.id))

# view request data
def view_request(request,id):
    therapist = User.objects.get(id=id)
    requeste = get_request(id)
    print(requeste.full_name)
    context = {
        "therapist" : therapist,
        "request" :requeste,
    }
    return render(request,'view_request.html',context)


# view therapist data
def view_therapist(request,id):
    if 'userid' in request.session:
        admin = User.objects.get(id=request.session['userid'])
        therapist = User.objects.get(id=id)
        context = {
            "therapist" : therapist,
            "admin" : admin,
        }
        return render(request,'view_therapist.html',context)
    else:
        return redirect('/login_page')

# therapist profile
def therapist_profile(request,id):
    if 'userid' in request.session:
        therapist = User.objects.get(id=id)
        context = {
            "therapist" : therapist,
        }
        return render(request,'therapist_profile.html',context)
    else:
        return redirect('/login_page')

# edit therapist his login data
def therapist_login_data(request,id):
    if 'userid' in request.session:
        therapist = User.objects.get(id=id)
        context = {
            "therapist" : therapist,
        }
        return render(request,'therapist_login_data.html',context)
    else:
        return redirect('/login_page')

# therapist messages page
def therapist_messages(request,id):
    if 'userid' in request.session:
        therapist = User.objects.get(id=id)
        messages_recieve =therapist.messages_recieve.all()
        message_send = therapist.message_send.all()
        context = {
            "therapist" : therapist,
            "messages_recieve" : messages_recieve,
            "message_send" : message_send,
        }
        return render(request,'therapist_messages.html',context)
    else:
        return redirect('/login_page')

# therapist send message page
def therapist_send_message(request,id):
    if 'userid' in request.session:
        therapist = User.objects.get(id=id)
        users = get_all_user(request)
        context = {
            "therapist" : therapist,
            "users" : users,
        }
        return render(request,'therapist_send_message.html',context)
    else:
        return redirect('/login_page')

# therapist message data
def therapist_message_data(request,id):
    if 'userid' in request.session:
        therapist = User.objects.get(id=request.session['userid'])
        message = Message.objects.get(id=id)
        context = {
            "therapist" : therapist,
            "message" : message,
        }
        return render(request,'therapist_message_data.html',context)
    else:
        return redirect('/login_page')

# delete message
def delete_message_therapist(request,id):
    therapist = User.objects.get(id=request.session['userid'])
    message = Message.objects.get(id=id)
    del_message(message)
    return redirect('/therapist_messages/'+str(therapist.id))

# view data of therapist requests
def therapist_request_data(request,id):
    therapist = User.objects.get(id=request.session['userid'])
    print(therapist.id)
    requeste = Order.objects.get(id=id)
    print(requeste.id)
    context = {
        "therapist" : therapist,
        "request" : requeste,
    }

    return render(request,'therapist_request_data.html',context)

# logout method
def logout(request):
    request.session.flush()
    return redirect('/login_page')