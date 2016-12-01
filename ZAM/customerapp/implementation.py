__author__ = 'vikas kmt'

import calendar

from datetime import datetime,timedelta
import json
import pdb
import time
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction
from django.db.models import F
from django.db.models import Q
from django.http import HttpResponse
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.shortcuts import render, redirect
from django.shortcuts import render_to_response
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.views.decorators.csrf import csrf_exempt

from customerapp.models import *
from customerapp.myplan import *
from zamapp.captcha_form import CaptchaForm
from zamapp.models import *
import numpy



def open_roadmap(request):
    if request.user.is_authenticated():
        meter_data, index = implementatoin_calculations(request)
        data = {'goal_data': meter_data,'count':index}
        # print data
        return render(request, 'roadmap.html',data)
    else:
        form = CaptchaForm()
        return render_to_response('login.html', dict(
            form=form
        ), context_instance=RequestContext(request))

def calc_year_month(pre_date,target_date):
    date_format = "%m/%d/%Y"
    pre_date = pre_date.strftime("%m/%d/%Y")
    goal_date = target_date.strftime("%m/%d/%Y")
    a = datetime.strptime(pre_date, date_format)
    b = datetime.strptime(goal_date, date_format)
    delta = b - a
    day = int(delta.days) + 1
    month = ((b.year - a.year)) * 12 + (b.month - a.month) + 1
    #print "-------month----------", month
    year = 0.00273790926 * float(day)
    return year,month

def implementatoin_calculations(request):
    try:
        #pre_date = datetime.now()
        goal_cat_obj = Goal_Category.objects.all()
        meter_data = []
        index = 0
        for category in goal_cat_obj:
            check_obj=UserProfile.objects.get(user_id=request.session['customer_id'])
            goal_obj = Goal.objects.filter(goal_cat_id=category,user_id=check_obj,row_status='Active')
            for goals in goal_obj:
                if goals:
                    index = index + 1
                    goal_date = goals.goal_target_date
                    pre_date = datetime.now()
                    year, month = calc_year_month(pre_date,goal_date)
                    goal_date = goal_date.strftime("%d/%m/%Y")
                    goal_name = goals.goal_name
                    final_value = calculate_final_value(goals,year)
                    emi = round(numpy.pmt(0.1/12,month,0,float(final_value)),2)*-1
                    meter_list = {'index':index,'goal_id':goals.goal_id,'goal_cat_name':goal_name,'goal_emi':emi, 'goal_year':goal_date, 'goal_amount':int(goals.amount)}
                meter_data.append(meter_list)

            data = []
    except Exception, e:
        print e
        data = []
    return meter_data,index

def calculate_final_value(goal, i):
    try:
        variable_obj = Goal_Category.objects.get(goal_cat_id=goal.goal_cat_id.goal_cat_id).goal_percentage
        percentage_data = (variable_obj / 100)
        amt = cal_cash_flow(float(goal.amount), percentage_data, i)
        bullet_amount = amt
    except Exception, e:
        print e
    return bullet_amount

def cal_cash_flow(amount, percentage, i):
    try:
        return float(amount * ((1 + percentage) ** i))
    except Exception, e:
        print 'Exception==>', e

@csrf_exempt
def implementation_year_calc(request):
    try:
        goal_year = request.POST.get('year')
        print goal_year
        goal_id = request.POST.get('goal_id')
        goal_obj = Goal.objects.get(goal_id=goal_id)
        goal_date = goal_obj.goal_target_date
        pre_date = datetime.now()
        end_date = pre_date + timedelta(366 * int(goal_year))
        year, month = calc_year_month(end_date,goal_date)
        final_value = calculate_final_value(goal_obj,year)
        emi = round(numpy.pmt(0.1/12,month,0,float(final_value)),2)*-1
        data = {'success':'true','emi':emi}
    except Exception, e:
        print 'Exception==>', e
        data = {'success':'false'}
    return HttpResponse(json.dumps(data), content_type='application/json')

@csrf_exempt
def implementation_debt_equity_calc(request):
    try:
        pre_date = datetime.now()
        pre_year = pre_date.year
        goal_id = request.POST.get('goal_id')
        rate = request.POST.get('rate')

        goal_obj = Goal.objects.get(goal_id=goal_id)
        goal_date = goal_obj.goal_target_date
        year, month = calc_year_month(pre_date, goal_date)
        final_value = calculate_final_value(goal_obj, year)
        emi = round(numpy.pmt(float(rate)/12,month,0,float(final_value)),2)*-1

        # print "final_value:",final_value
        # print "rate:",rate
        # print "target_year:",target_year
        # print "emi:",emi

        data = {'success':'true','emi':emi}
    except Exception, e:
        print 'Exception==>', e
        data = {'success':'false'}
    return HttpResponse(json.dumps(data), content_type='application/json')

# from django import template
#
# register = template.Library()
#
# def lower(value):
#     return value.lower()
#
# register.filter('lower', lower)