import MySQLdb
import pdb
import smtplib
from django.contrib.auth import authenticate
from django.http import HttpResponse
from django.shortcuts import render_to_response, render
from ZAM.config import *
from models import *
from django.views.decorators.csrf import csrf_exempt
import json
from django.shortcuts import redirect
from customerapp.models import *

#SERVER_URL='http://192.168.0.123:9632/'
SERVER_URL='http://ec2-54-179-153-165.ap-southeast-1.compute.amazonaws.com'

def open_user_index(request):
     if request.user.is_authenticated():
        return render(request,'users_index.html')
        form = CaptchaForm()
        return render_to_response('login.html', dict(
            form=form
        ), context_instance=RequestContext(request))


def open_add_user_page(request):
     if request.user.is_authenticated():
        user_roles=UserRole.objects.filter(role_status='Active')
        data={"success":"ture",'user_role_list':user_roles}
        return render(request,'user_add.html',data)
        form = CaptchaForm()
        return render_to_response('login.html', dict(
            form=form
        ), context_instance=RequestContext(request))


def open_rename_password(request):
     if request.user.is_authenticated():
        return render(request, 'change_password.html')
        form = CaptchaForm()
        return render_to_response('login.html', dict(
            form=form
        ), context_instance=RequestContext(request))



@csrf_exempt
def change_password(request):
    try:
        password = request.POST['old_password']
        new_password = request.POST['password']
        user_name=request.session['login_user']
        user = authenticate(username=user_name, password=password)
        if user is not None:
            user.set_password(new_password)
            user.save()
            data= {'success':'true','error_msg':'Your password has been changed successfully! Please Login again'}
        else:
            data= {'success':'false','error_msg':'Current Password does not match!'}
        print '--------------------------------------------------'
    except Exception, e:
        print '----------Exception---------------'
        print e
        data={'success':'flase','error_msg':'Server Exception!'}
    return HttpResponse(json.dumps(data), content_type='application/json')


def get_user_list(request):
    try:
        #userobj_list = UserProfile.objects.filter(record_status='Active')
        userobj_list = UserProfile.objects.all().exclude(role_id=UserRole.objects.get(role_id='6'))
        user_list = []
        for user in userobj_list:
            retrive = ''
            if user.row_status == 'Active':
                view   =   '<a href=/view-user-details/?user_id='+ str(user.user_id)  +' class="infont"> ''<i class="fa fa-eye"></i></i></a>'
                if request.session['user_role'] == "Super Admin":
                    delete = '<a onclick=delete_user(' + str(
                        user.user_id) + ') class="infont"> ''<i class="fa fa-trash-o"></i></i></a>'
                else:
                    if user.role_id.role == "Admin":
                        delete = ''
                    else:
                        delete = '<a onclick=delete_user('+ str(user.user_id)  +') class="infont"> ''<i class="fa fa-trash-o"></i></i></a>'
            else:
                retrive = '<a onclick=retrive_user_pop('+ str(user.user_id)  +') class="infont"> ''<i class="fa fa-history" style="margin-left: -58px;"></i></i></a>'
                view = ''
                delete=''
            user_obj = {
                'first_name': user.user_first_name,
                'last_name': user.user_last_name,
                'contact_no': user.user_contact_number,
                'user_name': user.user_email_id,
                'user_role': user.role_id.role,
                'verified': user.user_emailId_verified,
                'created_date':user.user_created_date.strftime('%d/%m/%Y'),
                'view': view,
                'delete':delete,
                'retrive': retrive,
            }
            user_list.append(user_obj)
        data = {'data': user_list}
    except Exception, e:
        print 'Exception at user list: ', e
        data = {'data': 'none'}
    return HttpResponse(json.dumps(data), content_type='application/json')

def get_customer_list(request):
    try:
        #userobj_list = UserProfile.objects.filter(record_status='Active')
        user_role = UserRole.objects.get(role = "Customer")
        userobj_list = UserProfile.objects.filter(role_id=user_role)

        user_list = []
        for user in userobj_list:
            try:
                check_obj = UserProfile.objects.get(user_id=user.user_id)
                if check_obj.welcome_mail == 'No':
                    email = '<a onclick=send_mail(' + str(
                        check_obj.user_id) + ') class="infont"> ''<i class="fa fa-envelope-o"></i></i></a>'
                else:
                    email = ''
                customer_obj = CustomerPersonalInfo.objects.get(user=check_obj)
                if customer_obj.report_description:
                    comment = ''
                else:
                    comment = '<a onclick=add_description(' + str(
                        customer_obj.user_id) + ') class="infont"> ''<i class="fa fa-comment-o"></i></i></a>'

            except CustomerPersonalInfo.DoesNotExist:
                comment = ''

            retrive=''
            if user.row_status == 'Active':
                view   =   '<a href=/view-customer-details/?customer_id='+ str(user.user_id)  +' class="infont"> ''<i class="fa fa-eye"></i></i></a>'
                if user.role_id.role == "Admin":
                    delete = ''
                else:
                    delete = '<a onclick=delete_user('+ str(user.user_id)  +') class="infont"> ''<i class="fa fa-trash-o"></i></i></a>'
            else:
                retrive = '<a onclick=retrive_user_pop('+ str(user.user_id)  +') class="infont"> ''<i class="fa fa-history" style="margin-left: -70px;"></i></i></a>'
                view = ''
                delete=''
            user_obj = {
                'first_name': user.user_first_name,
                'last_name': user.user_last_name,
                'contact_no': user.user_contact_number,
                'user_name': user.user_email_id,
                'user_role': user.role_id.role,
                'verified': user.user_emailId_verified,
                'created_date':user.user_created_date.strftime('%d/%m/%Y'),
                'comment': comment,
                'email': email,
                'view': view,
                'delete':delete,
                'retrive':retrive,
            }
            user_list.append(user_obj)
        data = {'data': user_list}
    except Exception, e:
        print 'Exception at user list: ', e
        data = {'data': 'none'}
    return HttpResponse(json.dumps(data), content_type='application/json')

@csrf_exempt
def save_customer_description(request):
    print request.POST
    if request.method == "POST":
        try:
            cust_id = request.POST.get('cust_id')
            check_obj = UserProfile.objects.get(user_id=cust_id)
            customer_obj = CustomerPersonalInfo.objects.get(user=check_obj)
            customer_obj.report_description = request.POST.get('txt_description')
            customer_obj.save()
            data = {'success': 'true'}
        except CustomerPersonalInfo.DoesNotExist, e:
            print 'CustomerPersonalInfo.DoesNotExist :', e
            data = {'success': 'false'}
        except Exception, e:
            print 'Exception :', e
            data = {'success': 'false', 'error_msg': 'Internal Server Error'}
        return HttpResponse(json.dumps(data), content_type='application/json')

def view_user_details(request):
    try:
        user_id=request.GET.get('user_id')
        user_obj=UserProfile.objects.get(user_id=user_id)

        if user_obj.role_id.role=='Admin':
            user_roles=UserRole.objects.filter(role_status='Active')
        else:
            user_roles=UserRole.objects.filter(role_status='Active')
        if user_obj.user_title:
            user_title = user_obj.user_title
        else:
            user_title = ''
        data = {
                'success':'true',
                'user_role_list':user_roles,
                'user_id':user_obj.user_id,
                'user_title': user_title ,
                'first_name': user_obj.user_first_name,
                'last_name': user_obj.user_last_name,
                'contact_no': user_obj.user_contact_number,
                'user_name': user_obj.user_email_id,
                'user_role': user_obj.role_id,
                'role': user_obj.role_id.role,
                'created_date':user_obj.user_created_date.strftime('%d/%m/%Y'),
                'updated_date':user_obj.user_created_date.strftime('%d/%m/%Y'),
                'created_by':user_obj.user_created_by,
                'updated_by':user_obj.user_updated_by,
            }
        print data
    except Exception,e:
        print 'Exception at user view: ',e
        data={'success':'false'}
    return render(request,'user_view.html',data)

def view_customer_details(request):
    try:
        customer_id=request.GET.get('customer_id')
        user_profile_obj = UserProfile.objects.get(user_id=customer_id)
        request.session['customer_full_name'] = user_profile_obj.first_name + " " + user_profile_obj.last_name
        request.session['customer_user_role'] = user_profile_obj.role_id.role
        request.session["customer_id"] = customer_id
        print request.session['customer_full_name'],request.session['customer_user_role'],request.session['customer_id']
    except Exception,e:
        print 'Exception at user view: ',e
        data={'success':'false'}
    return redirect('/customer/')
    #return render(request,'user_view.html',data)

def open_signup_page(request):
    try:
        user_roles=UserRole.objects.filter(role_status='Active')
        data={"success":"ture",'user_role_list':user_roles}
    except Exception,e:
        print 'Exception ',e
        data={"success":"false"}
    return render(request,'register.html',data)

@csrf_exempt
def update_userdetails_up(request):
    #pdb.set_trace()
    print request.POST
    if request.method == "POST":
        try:
            user_id = request.POST['user_id']
            check_obj = UserProfile.objects.get(user_id=user_id);

            user_title = request.POST['title']
            first_name = request.POST['first_name']
            last_name = request.POST['last_name']
            new_username = request.POST['username']
            password = request.POST['password']
            contactno=request.POST['contact_no']
            change_password=request.POST['password_change']

            if check_obj.role_id.role!='Admin':
                role = request.POST['selectuserrole']
                check_obj.role_id=UserRole.objects.get(role_id=role)

            old_username=check_obj.username
            check_obj.user_title=user_title
            check_obj.first_name=first_name
            check_obj.user_first_name=first_name
            check_obj.last_name=last_name
            check_obj.user_last_name=last_name
            check_obj.user_contact_number=contactno
            check_obj.user_updated_date=datetime.now()
            check_obj.user_updated_by=request.session['login_user']
            if change_password=="1":
                check_obj.set_password(password)

            print old_username
            print new_username

            print old_username!=new_username

            if old_username!=new_username:
                new_obj = UserProfile.objects.get(username=new_username);
                if new_obj:
                    data={'success':'exist','error_msg': 'User Already Exist!'}
                    return HttpResponse(json.dumps(data), content_type='application/json')
            else:
                check_obj.save()
                data={'success':'true'}

        except User.DoesNotExist:
            check_obj.username=new_username
            check_obj.user_email_id=new_username
            check_obj.save()
            data={'success':'true'}
        except Exception, e:
            print 'BIG :', e
            data={'success':'false','error_msg': 'Internal Server Error'}
        return HttpResponse(json.dumps(data), content_type='application/json')


@csrf_exempt
def signing_up(request):
    print '==============================================='
    #pdb.set_trace()
    if request.method == "POST":
        try:
            user_title = request.POST['title']
            first_name = request.POST['first_name']
            last_name = request.POST['last_name']
            username = request.POST['username']
            password = request.POST['password']
            role = request.POST['selectuserrole']
            contactno=request.POST['contact_no']
            cpassword = request.POST['confirm_password']
            check_obj = UserProfile.objects.get(username=username);
            if check_obj:
                data={'success':'exist','error_msg': 'User Already Exist!'}
                return HttpResponse(json.dumps(data), content_type='application/json')

        except User.DoesNotExist:
            user_obj = UserProfile(
                    username=username,
                    password=password,
                    first_name=first_name,
                    last_name=last_name,
                    user_title=user_title,
                    user_first_name=first_name,
                    user_last_name=last_name,
                    user_email_id=username,
                    user_contact_number=contactno,
                    role_id=UserRole.objects.get(role_id=role),
                    user_created_date=datetime.now().date(),
                    user_updated_date=datetime.now().date(),
                    user_created_by=request.session['login_user'],
                    user_updated_by=request.session['login_user'],
                )
            user_obj.is_staff = True
            user_obj.set_password(password)
            user_obj.save()
            if role == '5':
                user_obj.user_emailId_verified = 'Yes'
                user_obj.save()
            else:
                send_admin_notification(user_obj,password)
            data={'success':'true','error_msg': 'User Created Successfully!'}
            return HttpResponse(json.dumps(data), content_type='application/json')
            #else:
            #    data={'success':'false','error_msg': 'Passwords do not match!'}
        except MySQLdb.OperationalError,e:
            print 'DB :', e
            data={'success':'false','error_msg': 'Internal Server Error'}
            return HttpResponse(json.dumps(data), content_type='application/json')
        except Exception, e:
            print 'BIG :', e
            data={'success':'false','error_msg': 'Internal Server Error'}
            return HttpResponse(json.dumps(data), content_type='application/json')


def send_admin_notification(user_obj,password):
    gmail_user = EMAIL_ID
    gmail_pwd = EMAIL_PASSWORD
    FROM = 'ZAM'
    user_profile_obj=UserProfile.objects.get(user_email_id=(str(user_obj.username)))
    TO = [(str(user_obj.username))]
    try:
        TO.append(user_obj.username)
        #TEXT="Hi "+(str(user_profile_obj.user_first_name))+' '+(str(user_profile_obj.user_last_name))+',\n\n'+SERVER_URL+'do_active_user//'+'?user_id='+(str(user_profile_obj.user_id))
        TEXT="Hi "+(str(user_profile_obj.user_first_name))+' '+(str(user_profile_obj.user_last_name))+',\n\n'\
                +'You have Successfully Register in ZAM with Following Details\n\n=> User Name: '+user_obj.username+'\n'+'=> Password: '+password +'\n'+'=> User Type '+user_profile_obj.role_id.role+'\nPlease verify your email id by clicking on following link and login\n'\
                +SERVER_URL+'/do-active-user/'+'?user_id='+(str(user_profile_obj.user_id))
        SUBJECT = "ZAM User Verification"
        server = smtplib.SMTP("smtp.gmail.com", 587) #or port 465 doesn't seem to work!
        server.ehlo()
        server.starttls()
        server.login(gmail_user, gmail_pwd)
        message = """From: %s\nTo: %s\nSubject: %s\n\n%s """ % (FROM, ", ".join(TO), SUBJECT, TEXT)
        server.sendmail(FROM, TO, message)
        server.close()
        data = {'success': 'true', 'message' : "Forgot Password Send Successfully" }

    except UserProfile.DoesNotExist, e:
        data = {'success': 'false', 'message':"Forgot Password Failed"}
        print "failed to send mail", e
    except Exception, e:
        print e
        data = {'success': 'false', 'message':"Server Error, Please try again!"}
    return HttpResponse(json.dumps(data), content_type='application/json')

@csrf_exempt
def send_welcome_email(request):
    gmail_user = EMAIL_ID
    gmail_pwd = EMAIL_PASSWORD
    FROM = 'ZAM'
    user_profile_obj=UserProfile.objects.get(user_id= request.POST.get('user_id'))
    TO = [str(user_profile_obj.username)]
    try:
        TEXT="Hi "+(str(user_profile_obj.user_first_name))+' '+(str(user_profile_obj.user_last_name))+',\n\n'\
                +'You have Successfully Register in ZAM with Following Details\n\n=> User Name: '+user_profile_obj.username+'\n'+'=> Password: \n'+'=> User Type '+user_profile_obj.role_id.role+'\nPlease verify your email id by clicking on following link and login\n'\
                +SERVER_URL+'/do-active-user/'+'?user_id='+(str(user_profile_obj.user_id))
        SUBJECT = "ZAM User Verification"
        server = smtplib.SMTP("smtp.gmail.com", 587) #or port 465 doesn't seem to work!
        server.ehlo()
        server.starttls()
        server.login(gmail_user, gmail_pwd)
        message = """From: %s\nTo: %s\nSubject: %s\n\n%s """ % (FROM, ", ".join(TO), SUBJECT, TEXT)
        server.sendmail(FROM, TO, message)
        server.close()
        user_profile_obj.welcome_mail = 'Yes'
        user_profile_obj.save()
        data = {'success': 'true', 'message' : "Forgot Password Send Successfully" }

    except UserProfile.DoesNotExist, e:
        data = {'success': 'false', 'message':"Forgot Password Failed"}
        print "failed to send mail", e
    except Exception, e:
        print e
        data = {'success': 'false', 'message':"Server Error, Please try again!"}
    return HttpResponse(json.dumps(data), content_type='application/json')

##
##def send_admin_notification(user_obj):
##    # print "in the send_password_reset_mail"
##    #pdb.set_trace()
##    gmail_user = "training.tungsten@gmail.com"
##    gmail_pwd = "BynryTungsten2015"
##    FROM = 'ZAM'
##    TO = ['sagar.suryawanshi@tungstenbigdata.com']
##
##
##    try:
##        TO.append(user_obj.username)
##        TEXT="""User Name: %s 
##           """%(str(user_obj.username))
##        SUBJECT = "Notification For Customer Registration"
##        server = smtplib.SMTP("smtp.gmail.com", 587) #or port 465 doesn't seem to work!
##        server.ehlo()
##        server.starttls()
##        server.login(gmail_user, gmail_pwd)
##        message = """From: %s\nTo: %s\nSubject: %s\n\n%s """ % (FROM, ", ".join(TO), SUBJECT, TEXT)
##        server.sendmail(FROM, TO, message)
##        server.close()          
##        data = {'success': 'true', 'message' : "Forgot Password Send Successfully" }
##
##    except UserProfile.DoesNotExist, e:
##        data = {'success': 'false', 'message':"Forgot Password Failed"}
##        print "failed to send mail", e
##    except Exception, e:
##        print e
##        data = {'success': 'false', 'message':"Server Error, Please try again!"}
##    return HttpResponse(json.dumps(data), content_type='application/json')


#             return render_to_response('register.html',{'error_msg':'User Created Successfully!'})
#     else:
#             return render_to_response('register.html',{'error_msg':'Passwords do not match!'})
# except MySQLdb.OperationalError, e:
#     print 'DB :',e
#     return render_to_response('register.html',{'error_msg':'Internal Server Error!'})
# except Exception, e:
#     print 'BIG :',e
#     return render_to_response('register.html',{'error_msg':'Internal Server Error!'})