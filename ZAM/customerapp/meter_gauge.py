__author__ = 'vikas kmt'

import calendar
import datetime
import datetime
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


def open_implementation(request):
    if request.user.is_authenticated():
        try:
            meter_reading, meter_list = meter_gauge_calculations(request)
            data = {'meter_reading': meter_reading, 'meter_list': meter_list}
            #print data
        except Exception, e:
            print "Exception:",e
            data = []
        return render(request, 'Implementation.html', data)
    else:
        form = CaptchaForm()
        return render_to_response('login.html', dict(
            form=form
        ), context_instance=RequestContext(request))


def meter_gauge_calculations(request):
    try:
        pre_date = datetime.now()
        pre_year = pre_date.year
        meter_reading = []
        cash_flow_list, total_data = get_goals_details(request)
        salary_data, expence_list, new_balance_data, year_list, temp_desc, end_saving = view_asset_analysis(request)
        goal_cat_obj = Goal_Category.objects.all()
        meter_data = []
        index = 0
        for category in goal_cat_obj:
            check_obj=UserProfile.objects.get(user_id=request.session['customer_id'])
            goal_obj = Goal.objects.filter(goal_cat_id=category,user_id=check_obj,row_status='Active')
            for goals in goal_obj:
                if goals:

                    index = index + 1
                    list1 = []
                    goal_year = goals.goal_target_year
                    goal_name = goals.goal_name
                    target_year = int(goal_year) - int(pre_year)
                    saving_year = int(goal_year)
                    for i in range(target_year + 1):
                        xyz = pre_year + i
                        list1.append(total_data[xyz])

                    total_outflow_npv = numpy.npv(0.1, list1) * -1
                    saving_npv = npv_blnc(0.1, end_saving[saving_year], target_year)
                    GAP = total_outflow_npv + saving_npv
                    final_gap = (GAP / saving_npv) * 100

                    # print "\n========================================================"
                    # print 'goal_name', goal_name
                    # print 'target_year', target_year
                    # print "list", list1
                    # print "outflow", total_outflow_npv
                    # print "saving",end_saving[saving_year]
                    # print "saving outflow",saving_npv
                    # print "final_gap",final_gap
                    # print "========================================================\n"

                    if final_gap < 0:
                        final_gaps = 0
                    if final_gap > 0 and final_gap <=10:
                        final_gaps = 40 + (final_gap * 2)
                    if final_gap > 10:
                        final_gaps = 60 + ((final_gap-10) / 2)
                    if final_gap >= 100:
                        final_gaps = 100
                    if final_gaps >= 100:
                        final_gaps = 100
                    if final_gaps < 20:
                        goals.goal_status = "Not Met"
                        goals.save()
                    if final_gaps >= 20 and final_gaps <= 80:
                        goals.goal_status = "May Be"
                        goals.save()
                    if final_gaps > 80:
                        goals.goal_status = "Met"
                        goals.save()
                    meter_reading.append(final_gaps)
                    meter_list = {'index':index,'goal_cat_name':goal_name, 'goal_year':goal_year, 'goal_amounts':goals.amount}

                meter_data.append(meter_list)

            data = []
    except Exception, e:
        print e
        data = []
    return meter_reading, meter_data


def npv(rate, cashflows):
    total = 0.0
    for i, cashflow in enumerate(cashflows):
        total += cashflow / (1 + rate) ** i
    return total * -1


def npv_blnc(rate, cashflows, year):
    total = 0.0
    total += cashflows / (1 + rate) ** year
    return total


def cal_percentage(amount, percentage):
    try:
        return round(amount * ((1 + percentage) ** 10) * (-1), 2)
    except Exception, e:
        print 'Exception==>', e
