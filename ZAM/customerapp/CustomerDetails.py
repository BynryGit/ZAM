__author__ = 'vikas kumawat'

from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from zamapp.captcha_form import CaptchaForm
from customerapp.models import *
from django.db import transaction
from django.shortcuts import render
from django.shortcuts import render_to_response
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseRedirect
import pdb
import json
from datetime import date, timedelta, datetime
from zamapp.models import *
import datetime
import calendar
import time
from django.db.models import Q
from django.db.models import F

def open_customer_details(request):
    if request.user.is_authenticated():
        try:
            check_obj = UserProfile.objects.get(user_id=request.session['customer_id'])
            user_title = check_obj.user_title
            first_name = check_obj.user_first_name
            last_name = check_obj.user_last_name
            customer_obj = CustomerPersonalInfo.objects.get(user = check_obj)
            user_title = customer_obj.user_title
            if customer_obj.dob:
                dob = customer_obj.dob.strftime('%d/%m/%Y')
            else:
                dob = ''
            if customer_obj.spouse_dob:
                spouse_dob = customer_obj.spouse_dob.strftime('%d/%m/%Y')
            else:
                spouse_dob = ''
            if customer_obj.registration_date:
                dor = customer_obj.registration_date.strftime('%d/%m/%Y')
            else:
                dor = ''
            child_obj = []
            variable_list = ''
            variable_lists = []

            if customer_obj:
                "Edit customer"
                if customer_obj.no_of_child > 0:
                    child_objs = CustomerChildrenInfo.objects.filter(customer_id = customer_obj)
                    i = 0
                    for child in child_objs:
                        i = i + 1
                        child_data = {
                            'child_count':i,
                            'child_name': child.child_name,
                            'child_age': child.age,
                            'child_dob': child.child_dob.strftime('%d/%m/%Y'),
                            'child_gender': child.child_gender,
                        }
                        child_obj.append(child_data)
                    # print child_objs
                    # print child_obj
                else:
                    child_obj = ''
                variable_obj = Variable.objects.filter(variableType_id =2,row_status = 'Active')
                cust_var_obj = CustomerVariable.objects.filter(customer_id = customer_obj, row_status = 'Active')

                for variables in cust_var_obj:
                    delete_btn = '<a id="'+str(variables.CustomerVariable_id)+'" name="'+variables.variable.variable+'"' \
                                                                              ' onclick=delete_variable(this.id,this.name)  class="infont"> ' + '<i class="fa fa-trash-o"></i></i>  </a>'
                    variables_data = {
                        'variable': variables.variable.variable,
                        'amount': variables.amount,
                        'variable_id': variables.CustomerVariable_id,
                    }
                    variable_lists.append(variables_data)

                for variables in cust_var_obj:
                    variable_list = variable_list + ',' + str(variables.variable.variable_id)
                data = {'variable_obj':variable_obj,'dob':dob,'spouse_dob':spouse_dob,'customer_obj':customer_obj,'dor':dor,
                        'child_obj':child_obj, 'variable_list': variable_list,
                        'variable_lists':variable_lists, 'user_title':user_title}
                return render(request,'edit_customer_details.html',data)

        except CustomerPersonalInfo.DoesNotExist, e:
            "Add customer"
            variable_obj = Variable.objects.filter(variableType_id =2,row_status = 'Active')
            data = {'variable_obj':variable_obj,'user_title':user_title,'first_name':first_name,'last_name':last_name}
            return render(request,'add_customer_details.html',data)
    else:
        form = CaptchaForm()
        return render_to_response('login.html', dict(
            form=form
        ), context_instance=RequestContext(request))

@csrf_exempt
def add_customer_details(request):
    try:
        print "adding customer details"
        #print request.POST
        check_obj=UserProfile.objects.get(user_id=request.session['customer_id'])

        customer_obj = CustomerPersonalInfo(
            user  =  check_obj,
            user_title = request.POST.get('title'),
            first_name = request.POST.get('txt_name'),
            last_name = request.POST.get('txt_last_name'),
            age = request.POST.get('txt_age'),
            gender = request.POST.get('gender'),
            marital_status = request.POST.get('txt_marital_status'),
            dob=datetime.datetime.strptime(request.POST.get('txt_dob'),"%d/%m/%Y").date(),#=request.POST.get('txt_dob'),
            registration_date=datetime.datetime.strptime(request.POST.get('txt_dor'),"%d/%m/%Y").date(),#=request.POST.get('txt_dob'),
            occupation=request.POST.get('txt_occupation'),
            monthly_salary=float(request.POST.get('txt_monthly_salary')),
            govt_benefit=request.POST.get('txt_gov_benefits'),
            profile_updated = 'YES',
            report_description = '',
            row_status = 'Active',
            created_by = request.session['login_user'],
            created_date = datetime.datetime.now()
        )
        customer_obj.save()

        if request.POST.get('txt_child_no'):
            customer_obj.no_of_child = request.POST.get('txt_child_no')



        if request.POST.get('txt_marital_status') == "Married":
            customer_obj.spouse_first_name = request.POST.get('txt_spouse_first_name')
            customer_obj.spouse_dob = datetime.datetime.strptime(request.POST.get('txt_spouse_dob'),"%d/%m/%Y").date()
            customer_obj.spouse_last_name = request.POST.get('txt_spouse_last_name')
            customer_obj.spouse_age = request.POST.get('txt_spouse_age')
            customer_obj.spouse_gender = request.POST.get('spouse_gender')
            if request.POST.get('txt_spouse_occupation'):
                customer_obj.spouse_occupation = request.POST.get('txt_spouse_occupation')
            if request.POST.get('txt_spouse_monthly_salary'):
                customer_obj.spouse_monthly_salary = float(request.POST.get('txt_spouse_monthly_salary'))
            if request.POST.get('txt_spouse_gov_benefits'):
                customer_obj.spouse_govt_benefit = request.POST.get('txt_spouse_gov_benefits')

        if request.POST.get('txt_score'):
            customer_obj.cibil_score = float(request.POST.get('txt_score'))
        if request.POST.get('txt_salary'):
            customer_obj.total_salary = float(request.POST.get('txt_salary'))
        if request.POST.get('txt_saving'):
            customer_obj.start_saving = float(request.POST.get('txt_saving'))
        if request.POST.get('txt_mortgage'):
            customer_obj.mortgage = float(request.POST.get('txt_mortgage'))
        if request.POST.get('txt_credit'):
            customer_obj.credit_card_deb = float(request.POST.get('txt_credit'))
        if request.POST.get('txt_loans'):
            customer_obj.other_loans = float(request.POST.get('txt_loans'))

        customer_obj.save()
        print "adding childs"

        if request.POST.get('txt_child_no'):
            if request.POST.get('txt_child_no') > 0:
                child_gender = request.POST.getlist('child_gender')
                child_age = request.POST.getlist('txt_child_age')
                child_name = request.POST.getlist('txt_child_name')
                child_dob = request.POST.getlist('txt_child_dob')
                for i in range(len(child_name)):
                    child_obj = CustomerChildrenInfo(
                            customer_id = customer_obj,
                            child_name= child_name[i],
                            child_gender = child_gender[i],
                            age = child_age[i],
                            child_dob = datetime.datetime.strptime(child_dob[i],"%d/%m/%Y").date(),
                            row_status = 'Active',
                            created_by = request.session['login_user'],
                            created_date = datetime.datetime.now()
                        )
                    child_obj.save()

        print "adding variables"

        table_data = request.POST.get('totalData')
        tables_data = json.loads(table_data)

        for data in tables_data:
            cat_name = data.get('Category Name')
            var_obj = Variable.objects.get(variable = cat_name)
            amount = float(data.get('Amount'))
            cust_var_obj = CustomerVariable(
                    variable = var_obj,
                    customer_id = customer_obj,
                    amount = amount,
                    row_status = 'Active',
                    created_by = request.session['login_user'],
                    created_date = datetime.datetime.now()
                )
            cust_var_obj.save()
        data = {'success': 'true'}
    except Exception, e:
        print e
        data = {'success': 'false'}
    return HttpResponse(json.dumps(data), content_type='application/json')

def customer_variable_details(request):
    try:
        check_obj = UserProfile.objects.get(user_id=request.session['customer_id'])
        customer_obj = CustomerPersonalInfo.objects.get(user = check_obj)
        cust_var_obj = CustomerVariable.objects.filter(customer_id = customer_obj, row_status = 'Active')
        variable_list = []
        for variables in cust_var_obj:
            delete_btn = '<a id="'+str(variables.CustomerVariable_id)+'" name="'+variables.variable.variable+'"' \
                                                                      ' onclick=delete_variable(this.id,this.name)  class="infont"> ' + '<i class="fa fa-trash-o"></i></i>  </a>'
            variables_data = {
                'variable': variables.variable.variable,
                'amount': variables.amount,
                'delete_btn': delete_btn,
            }
            variable_list.append(variables_data)
        #print variable_list
        data = {'data': variable_list}
    except Exception, e:
        print e
        data = {'success': 'false'}
    return HttpResponse(json.dumps(data), content_type='application/json')

@csrf_exempt
def delete_variable(request):
    try:
        cust_var_obj = CustomerVariable.objects.get(CustomerVariable_id = request.POST.get('variable_id'))
        #print cust_var_obj
        cust_var_obj.row_status = 'Inactive'
        cust_var_obj.save()
        data = {'success': 'true'}
    except Exception, e:
        print e
        data = {'success': 'false'}
    return HttpResponse(json.dumps(data), content_type='application/json')

@csrf_exempt
def update_customer_details(request):
    try:
        print "adding customer details"
        #print request.POST
        check_obj=UserProfile.objects.get(user_id=request.session['customer_id'])
        customer_obj = CustomerPersonalInfo.objects.get(user = check_obj)
        customer_obj.user_title = request.POST.get('title')
        customer_obj.first_name = request.POST.get('txt_name')
        customer_obj.last_name = request.POST.get('txt_last_name')
        customer_obj.age = request.POST.get('txt_age')
        customer_obj.gender = request.POST.get('gender')
        customer_obj.marital_status = request.POST.get('txt_marital_status')
        customer_obj.updated_by = request.session['login_user']
        customer_obj.updated_date = datetime.datetime.now()
        customer_obj.dob = datetime.datetime.strptime(request.POST.get('txt_dob'),"%d/%m/%Y").date()
        customer_obj.registration_date = datetime.datetime.strptime(request.POST.get('txt_dor'),"%d/%m/%Y").date()
        customer_obj.occupation = request.POST.get('txt_occupation')
        customer_obj.monthly_salary = request.POST.get('txt_monthly_salary')
        customer_obj.govt_benefit = request.POST.get('txt_gov_benefits')
        customer_obj.profile_updated = 'YES'
        customer_obj.report_description = ''

        customer_obj.save()
        print "===========user_title=============",customer_obj.user_title
        if request.POST.get('txt_child_no'):
            customer_obj.no_of_child = request.POST.get('txt_child_no')

        if request.POST.get('txt_marital_status') == "Married":
            customer_obj.spouse_first_name = request.POST.get('txt_spouse_first_name')
            customer_obj.spouse_last_name = request.POST.get('txt_spouse_last_name')
            customer_obj.spouse_dob = datetime.datetime.strptime(request.POST.get('txt_spouse_dob'), "%d/%m/%Y").date()
            customer_obj.spouse_age = request.POST.get('txt_spouse_age')
            customer_obj.spouse_gender = request.POST.get('spouse_gender')
            if request.POST.get('txt_spouse_occupation'):
                customer_obj.spouse_occupation = request.POST.get('txt_spouse_occupation')
            if request.POST.get('txt_spouse_monthly_salary'):
                customer_obj.spouse_monthly_salary = float(request.POST.get('txt_spouse_monthly_salary'))
            if request.POST.get('txt_spouse_gov_benefits'):
                customer_obj.spouse_govt_benefit = request.POST.get('txt_spouse_gov_benefits')

        if request.POST.get('txt_score'):
            customer_obj.cibil_score = float(request.POST.get('txt_score'))
        else:
            customer_obj.cibil_score = 0
        if request.POST.get('txt_salary'):
            customer_obj.total_salary = float(request.POST.get('txt_salary'))
        else:
            customer_obj.total_salary = 0
        if request.POST.get('txt_saving'):
            customer_obj.start_saving = float(request.POST.get('txt_saving'))
        else:
            customer_obj.start_saving = 0
        if request.POST.get('txt_mortgage'):
            customer_obj.mortgage = float(request.POST.get('txt_mortgage'))
        else:
            customer_obj.mortgage = 0
        if request.POST.get('txt_credit'):
            customer_obj.credit_card_deb = float(request.POST.get('txt_credit'))
        else:
            customer_obj.credit_card_deb = 0
        if request.POST.get('txt_loans'):
            customer_obj.other_loans = float(request.POST.get('txt_loans'))
        else:
            customer_obj.other_loans = 0

        customer_obj.save()
        print "adding childs"

        if request.POST.get('txt_child_no'):
            if request.POST.get('txt_child_no') > 0:
                CustomerChildrenInfo.objects.filter(customer_id=customer_obj).delete()
                child_gender = request.POST.getlist('child_gender')
                child_age = request.POST.getlist('txt_child_age')
                child_name = request.POST.getlist('txt_child_name')
                child_dob = request.POST.getlist('txt_child_dob')
                for i in range(len(child_name)):
                    child_obj = CustomerChildrenInfo(
                        customer_id=customer_obj,
                        child_name=child_name[i],
                        child_gender=child_gender[i],
                        age=child_age[i],
                        child_dob=datetime.datetime.strptime(child_dob[i], "%d/%m/%Y").date(),
                        row_status='Active',
                        created_by=request.session['login_user'],
                        created_date=datetime.datetime.now()
                    )
                    child_obj.save()

        print "adding variables"

        table_data = request.POST.get('totalData')
        tables_data = json.loads(table_data)
        #print tables_data
        CustomerVariable.objects.filter(customer_id = customer_obj).delete()
        for data in tables_data:
            cat_name = data.get('Category Name')
            var_obj = Variable.objects.get(variable = cat_name)
            amount = float(data.get('Amount'))
            cust_var_obj = CustomerVariable(
                    variable = var_obj,
                    customer_id = customer_obj,
                    amount = amount,
                    row_status = 'Active',
                    created_by = request.session['login_user'],
                    created_date = datetime.datetime.now()
                )
            cust_var_obj.save()
        data = {'success': 'true'}
    except Exception, e:
        print e
        data = {'success': 'false'}
    return HttpResponse(json.dumps(data), content_type='application/json')