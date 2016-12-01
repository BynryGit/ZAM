import MySQLdb
import pdb
import datetime
import random
import smtplib
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render
from django.shortcuts import render_to_response
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_exempt
from ZAM.config import *
from captcha_form import CaptchaForm
from django.template import RequestContext
from django.contrib.auth import authenticate, login, logout
from zamapp.models import UserProfile
import json
from zamapp.models import *

YOUR_OTP = 0

def retrive_user(request):
    try:
        # pdb.set_trace()
        '=====================Retrive User==============================='
        user_id = UserProfile.objects.get(user_id=request.GET.get('user_id'))
        user_id.row_status = 'Active'
        user_id.save()
        data = {'success': 'success'}
    except Exception, e:
        print 'Index.py|retrive_user| Error :', e
        data = {'success': 'false'}
    return HttpResponse(json.dumps(data), content_type='application/json')

def login_open(request):
    if request.user.is_authenticated():
        return redirect('/index/')
    else:
        form = CaptchaForm()
        return render_to_response('login.html', dict(
            form=form
        ), context_instance=RequestContext(request))


@csrf_exempt
# def loging_in(request):
#     if request.POST:
#         form = CaptchaForm(request.POST)
#         print 'logs: login request with: ', request.POST
#         username = request.POST['username']
#         password = request.POST['password']
#         # pdb.set_trace()
#         print 'valid form form----->',form.is_valid()
#         if form.is_valid():
#             try:
#                 user = authenticate(username=username, password=password)
#                 print 'valid form befor----->'
#                 if user is not None:
#                     if user.is_active:
#                         print 'valid form after----->'
#                         user_profile_obj = UserProfile.objects.get(user_email_id=username)
#                         if user_profile_obj.row_status == 'Inactive':
#                             data = 'Invalid Username or Password'
#                             return render_to_response('login.html', dict(
#                                 form=form, message=data
#                             ), context_instance=RequestContext(request))
#
#                         if user_profile_obj.user_emailId_verified == 'No':
#                             msg = 'First verify your email id(user name)'
#                             form = CaptchaForm()
#                             return render_to_response('login.html', dict(
#                                 form=form, message=msg
#                             ), context_instance=RequestContext(request))
#
#                         request.session['login_user'] = user.username
#                         request.session['full_name'] = user.first_name + " " + user.last_name
#                         request.session['user_role'] = UserProfile.objects.get(user_email_id=user.username).role_id.role
#                         request.session['login_status'] = True
#                         request.session["user_id"] = user_profile_obj.user_id
#                         login(request, user)
#                         print '------end session and redicrect to deashboard------'
#                         #return redirect('/open-dashboard/')
#                         return redirect('/crm-index/')
#                         # YOUR_OTP=send_otp_to_user(UserProfile.objects.get(user_email_id=user.username))
#                         # print 'YOUR_OTP',YOUR_OTP
#                         # if YOUR_OTP!=0:
#                         #     return redirect('/open-otp/')
#                         # else:
#                         #     data = {'success': 'false', 'message': 'Server Error!'}
#                     else:
#                         print 'User is not Active'
#                         data = {'success': 'false', 'message': 'User Is Not Active'}
#                 else:
#                     print 'Logs:------Invalid Username or Password---------'
#                     data = 'Invalid Username or Password'
#                     return render_to_response('login.html', dict(
#                         form=form, message=data
#                     ), context_instance=RequestContext(request))
#             except User.DoesNotExist:
#                 print 'login error logs:- user does not exist'
#                 data = 'User Not Exit'
#             except MySQLdb.OperationalError, e:
#                 print 'login error logs db:-', e
#                 data = 'Internal Server Error '
#             except Exception, e:
#                 print 'login error logs e:-', e
#                 data = 'Internal Server Error'
#                 form = CaptchaForm()
#                 return render_to_response('login.html', dict(
#                     form=form, message=data
#                 ), context_instance=RequestContext(request))
#         else:
#             form = CaptchaForm()
#         return render_to_response('login.html', dict(
#             form=form, message='Invalid Captcha', username=username
#         ), context_instance=RequestContext(request))



def loging_in(request):
    #pdb.set_trace()
    if request.POST:
        form = CaptchaForm(request.POST)
        print 'logs: login request with: ', request.POST
        username = request.POST['username']
        password = request.POST['password']
        # pdb.set_trace()
        print 'valid form form----->',form.is_valid()
        if form.is_valid():
            try:
                user = authenticate(username=username, password=password)
                print 'valid form befor----->'
                if user is not None:
                    if user.is_active:
                        print 'valid form after----->'
                        user_profile_obj = UserProfile.objects.get(user_email_id=username)
                        if user_profile_obj.row_status == 'Inactive':
                            data = 'Invalid Username or Password'
                            return render_to_response('login.html', dict(
                                form=form, message=data
                            ), context_instance=RequestContext(request))

                        if user_profile_obj.user_emailId_verified == 'No':
                            msg = 'First verify your email id(user name)'
                            form = CaptchaForm()
                            return render_to_response('login.html', dict(
                                form=form, message=msg
                            ), context_instance=RequestContext(request))

                        request.session['login_user'] = user.username
                        request.session['full_name'] = user.first_name + " " + user.last_name
                        request.session['user_role'] = UserProfile.objects.get(user_email_id=user.username).role_id.role
                        request.session['login_status'] = True
                        request.session["user_id"] = user_profile_obj.user_id


                        if request.session['user_role']=="Customer":
                            request.session["customer_id"] = user_profile_obj.user_id
                            request.session['customer_full_name'] = user.first_name + " " + user.last_name
                            request.session['customer_user_role'] = UserProfile.objects.get(
                                user_email_id=user.username).role_id.role
                            login(request,user)
                            return redirect('/customer/')
                        else:
                            YOUR_OTP = send_otp_to_user(UserProfile.objects.get(user_email_id=user.username))
                            print 'YOUR_OTP',YOUR_OTP
                            if YOUR_OTP!=0:
                                request.session["OTP"]=YOUR_OTP
                                return redirect('/open-otp/')
                            else:
                                data = {'success': 'false', 'message': 'OTP Server Error'}
                    else:
                        print 'User is not Active'
                        data = {'success': 'false', 'message': 'User Is Not Active'}
                else:
                    print 'Logs:------Invalid Username or Password---------'
                    data = 'Invalid Username or Password'
                    return render_to_response('login.html', dict(
                        form=form, message=data
                    ), context_instance=RequestContext(request))
            except User.DoesNotExist:
                print 'login error logs:- user does not exist'
                data = 'User Not Exit'
            except MySQLdb.OperationalError, e:
                print 'login error logs db:-', e
                data = 'Internal Server Error '
            except Exception, e:
                print 'login error logs e:-', e
                data = 'Internal Server Error'
                form = CaptchaForm()
                return render_to_response('login.html', dict(
                    form=form, message=data
                ), context_instance=RequestContext(request))
        else:
            form = CaptchaForm()
            return render_to_response('login.html', dict(
            form=form, message='Invalid Captcha', username=username
        ), context_instance=RequestContext(request))

@csrf_exempt
def check_otp(request):
    #pdb.set_trace()
    try:
        opt=request.POST.get('opt_txt')
        user=request.session['login_user']
        session_otp=request.session['OTP']
        user_obj=User.objects.get(username=user)
        if opt==session_otp:
            user_obj.backend = 'django.contrib.auth.backends.ModelBackend'
            login(request,user_obj)
            if request.session['user_role']=="Super Admin" or request.session['user_role']=="Admin" or request.session['user_role']=='Portfolio Manager' or request.session['user_role']=='Marketing Manager':
                return redirect('/crm-index/')
            elif request.session['user_role']=="Analyst":
                return redirect('/open-research-page/')
        else:
            data={'message':'Check Your OTP'}
    except Exception, e:
        print 'index.py|check_otp|error',e
        data={'message':'Check Your OTP'}
    return render(request,'otp.html',data)

def signing_out(request):
    logout(request)
    form = CaptchaForm()
    return render_to_response('login.html', dict(
        form=form, message_logout='You have successfully logged out.'
    ), context_instance=RequestContext(request))


def delete_user(request):
    try:
        # pdb.set_trace()
        '=====================Delete User==============================='
        user_id = UserProfile.objects.get(user_id=request.GET.get('user_id'))
        user_id.row_status = 'Inactive'
        #user_id.user_updated_by = request.session['login_user']
        #user_id.user_updated_date = datetime.datetime.now()
        user_id.save()
        data = {'success': 'success'}
    except Exception, e:
        print 'Index.py|delete user| Error :', e
        data = {'success': 'false'}
    return HttpResponse(json.dumps(data), content_type='application/json')


def do_active_user(request):
    try:
        # pdb.set_trace()
        user_obj = UserProfile.objects.get(user_id=request.GET.get('user_id'))
        user_obj.user_emailId_verified = 'Yes'
        user_obj.save()
        message = 'You have verified your email Id successfully Please login.'
    except Exception, e:
        print 'index.py|do_active_user| Exception ', e
        message = 'Server Error'
    form = CaptchaForm()
    return render_to_response('login.html', dict(
        form=form, message_logout=message
    ), context_instance=RequestContext(request))


def home(request):
    if request.user.is_authenticated():
        return render(request, 'index.html')
        form = CaptchaForm()
    return render_to_response('login.html', dict(
        form=form
    ), context_instance=RequestContext(request))


#def open_dashboard(request):
#    return render(request, 'index.html')
    #if request.user.is_authenticated():
    #    if request.session['user_role']=="Admin" or request.session['user_role']=='Portfolio Manager' or request.session['user_role']=='Marketing Manager':
    #            return redirect('/crm-index/')
    #    elif request.session['user_role']=="Analysit":
    #            return redirect('/open-security-page/')
    #            #return render(request, 'index.html')
    #form = CaptchaForm()
    #return render_to_response('login.html', dict(
    #    form=form
    #), context_instance=RequestContext(request))

def open_index01(request):
    if request.user.is_authenticated():
        if request.session['user_role']=="Super Admin" or request.session['user_role']=='Portfolio Manager' or request.session['user_role']=='Marketing Manager':
                return redirect('/crm-index/')
        elif request.session['user_role']=="Analyst":
                return redirect('/open-security-page/')
                #return render(request, 'index.html')
    form = CaptchaForm()
    return render_to_response('login.html', dict(
        form=form
    ), context_instance=RequestContext(request))



def open_index(request):
    try:
        if request.user.is_authenticated():
            if request.session['user_role']=="Super Admin" or request.session['user_role']=='Portfolio Manager' or request.session['user_role']=='Marketing Manager':
                    return redirect('/crm-index/')
            elif request.session['user_role']=="Analyst":
                    return redirect('/open-security-page/')
            elif request.session['user_role']=="Customer":
                    return redirect('/customer/')
            elif request.session['user_role']=="Admin":
                    return redirect('/open-discussion-forum/')
        else:
            form = CaptchaForm()
            return render_to_response('login.html', dict(
                form=form
            ), context_instance=RequestContext(request))
    except Exception,e:
        if request.user.is_authenticated():
            logout(request)
        form = CaptchaForm()
        return render_to_response('login.html', dict(
            form=form
        ), context_instance=RequestContext(request))



def open_dashboard(request):
    if request.user.is_authenticated():
        question_obj = Question.objects.filter(read_status = "Unread")
        question_count = question_obj.count()
        response_obj = Response.objects.filter(read_status = "Unread")
        response_count = response_obj.count()
        responseto_obj = Responseto.objects.filter(read_status = "Unread")
        responseto_count = responseto_obj.count()
        total_count = question_count + response_count + responseto_count
        data = { 'question_count' : question_count, 'response_count' : response_count, 'responseto_count' : responseto_count, 'total_count' : total_count }  
        return render(request, 'index.html',data)
    form = CaptchaForm()
    return render_to_response('login.html', dict(
        form=form
    ), context_instance=RequestContext(request))


# def open_dashboard(request):
#     if request.user.is_authenticated():
#         return render(request, 'index.html')
#     form = CaptchaForm()
#     return render_to_response('login.html', dict(
#         form=form
#     ), context_instance=RequestContext(request))


def open_otp(request):
    return render(request, 'otp.html')

def random_challenge():
    ret = u''
    ret = ''.join(random.choice('0123456789ABCDEF') for i in range(5))
    print ret
    return ret


def send_otp_to_user(user_obj):
    opt_number = random_challenge()
    try:
        gmail_user = EMAIL_ID
        gmail_pwd = EMAIL_PASSWORD
        print gmail_user
        print gmail_pwd
        FROM = 'ZAM'
        user_profile_obj = UserProfile.objects.get(user_email_id=(str(user_obj.username)))
        TO = [(str(user_obj.username))]
        TO.append(user_obj.username)
        TEXT = "Hi " + (str(user_profile_obj.user_first_name)) + ' ' + (str(user_profile_obj.user_last_name)) + ',\n\n' \
               + 'Your OTP for ZAM User login is: ' + opt_number +'\n\nRegards,\nZeus Asset Management'
        SUBJECT = "OTP"
        server = smtplib.SMTP("smtp.gmail.com", 587)  # or port 465 doesn't seem to work!
        server.ehlo()
        server.starttls()
        server.login(gmail_user, gmail_pwd)
        message = """From: %s\nTo: %s\nSubject: %s\n\n%s """ % (FROM, ", ".join(TO), SUBJECT, TEXT)
        server.sendmail(FROM, TO, message)
        server.close()
    except Exception, e:
        print 'index.py|send_otp_to_user|error', e
        opt_number = 0
    return opt_number
