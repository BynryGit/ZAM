__author__ = 'vkm chandel'

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
from zamapp.captcha_form import CaptchaForm
from zamapp.models import *


def open_myplan(request):
    if request.user.is_authenticated():
        try:
            check_obj = UserProfile.objects.get(user_id=request.session['user_id'])
            customer_obj = CustomerPersonalInfo.objects.get(user=check_obj)
            bank_amount = 0
            list1 = []
            list2 = []
            bank_obj = CustomerBankAccountDetails.objects.filter(user=check_obj, row_status='Active')
            if bank_obj:
                i = 1
                for banks in bank_obj:
                    bank_amount = float(bank_amount) + float(banks.amount)
            print bank_amount

            
            info, asset_list = view_asset_details(request)
            var,variables_list=view_variable_details(request)
            product_amount = get_net_worth(request)
            print product_amount
            bank_percentage=round((bank_amount/product_amount)*100,2)
            bank_percentage=int(bank_percentage)
            list1.append('Bank')
            list2.append(bank_percentage)

            print "bank_percentage",bank_percentage
            cust_var_obj = Customer_Product.objects.filter(user_id=check_obj, row_status='Active')
            for variables in asset_list:
                list1.append(str(variables['variable']))
                pro_percentage=round((float(variables['amount'])/product_amount)*100,2)
                print pro_percentage
                list2.append(pro_percentage)

            print list1
            print list2
            
            
            bank_amount = int(bank_amount)
            bank_amount = "{:,d}".format(bank_amount)
            total_sum = int(product_amount - var['sum'])
            formatt= "{:,d}".format(total_sum)
            print "FORMATED",formatt
            product_amount = int(product_amount)
            product_amount = "{:,d}".format(product_amount)
##            total_sum=format(total_sum,",d")
            data = {'success': 'true','produc_name':list1,'product_percentage':list2, 'info': info,'var':var,'bank':'Bank','bank_amount':bank_amount, 'variables_list':variables_list,'asset_list': asset_list, 'product_amount': product_amount, 'total_sum': formatt}
            print "FInAL",data
        except CustomerPersonalInfo.DoesNotExist, e:
            print 'Exception ', e
            list1=[]
            list2=[]
            info = {}
            info['sum'] = 0
            info['customer_age'] = '--'
            total_sum,product_amount = 0,0
            data = {'success': 'true', 'info': info,'produc_name':list1,'product_percentage':list2, 'product_amount': product_amount, 'total_sum': total_sum}
        return render(request, 'myplan.html', data)
    else:
        form = CaptchaForm()
        return render_to_response('login.html', dict(
            form=form
        ), context_instance=RequestContext(request))

def view_variable_details(request):
##    pdb.set_trace()
    print 'Variable List'
    try:
        check_obj = UserProfile.objects.get(user_id=request.session['user_id'])
        var={}
        print check_obj
        customer_obj = CustomerPersonalInfo.objects.get(user = check_obj)
        cust_var_obj = CustomerVariable.objects.filter(customer_id = customer_obj,row_status = 'Active')
        variables_list = []
        sum =0
        for variables in cust_var_obj:
            sum=int(sum + variables.amount)
            variables_data = {

                'variable': variables.variable.variable,
                'amount': int(variables.amount)
            }
            variables_list.append(variables_data)
        var = { 'sum':sum}
        

    except Exception, e:
        print 'Exception ', e
    return var,variables_list

def view_asset_details(request):
    ##    pdb.set_trace()
    print 'Asset List'
    try:
        check_obj = UserProfile.objects.get(user_id=request.session['user_id'])
        info = {}
        customer_obj = CustomerPersonalInfo.objects.get(user=check_obj)
        product_list = Product.objects.all()
        variable_list = []
        for product in product_list:
            sum = 0
            name = ''
            cust_var_obj = Customer_Product.objects.filter(user_id=check_obj,product_id = product.product_id, row_status='Active')
            if cust_var_obj:
                for variables in cust_var_obj:
                    sum = int(sum + float(variables.amount))
                    name = variables.product_id.product
                variables_data = {
                    'variable': name,
                    'amount': sum
                }
                variable_list.append(variables_data)
                print "VARIABLE_LIST",variable_list
        info = { 'sum': sum}

    except Exception, e:
        print 'Exception ', e
    return info, variable_list


def open_new_worth(request):
    if request.user.is_authenticated():
        try:
            bank_amount = 0
            check_obj = UserProfile.objects.get(user_id=request.session['user_id'])
            customer_obj = CustomerPersonalInfo.objects.get(user=check_obj)
            bank_obj = CustomerBankAccountDetails.objects.filter(user=check_obj, row_status='Active')
            if bank_obj:
                i = 1
                for banks in bank_obj:
                    bank_amount = int(bank_amount) + int(banks.amount)
            print bank_amount

            info, asset_list = view_asset_details(request)
            details, analysis_view, balance_data, saving_data = view_asset_analysis(request)
            product_amount = int(get_net_worth(request))
            cash_flow_list, total_overflow = get_goals_detail(request)
            funding_gap_data = get_funding_gap(saving_data,total_overflow)
            total_sum = int(product_amount - info['sum'])
            var,variables_list=view_variable_details(request)

            data = {'success': 'true', 'info': info, 'asset_list': asset_list, 'details': details, 'total_sum': total_sum,
                    'analysis_view': analysis_view, 'balance_data': balance_data, 'product_amount': product_amount, 'variables_list':variables_list,
                    'cash_flow_list': cash_flow_list, 'funding_gap_data':funding_gap_data,'bank':'Bank','bank_amount':bank_amount}
        except CustomerPersonalInfo.DoesNotExist, e:
            print 'Exception ', e
            info = {}
            info['sum'] = 0
            info['customer_age'] = '--'
            total_sum,product_amount = 0,0
            data = {'success': 'true', 'info': info, 'product_amount': int(product_amount), 'total_sum': int(total_sum)}
        return render(request, 'net_worth.html', data)
    else:
        form = CaptchaForm()
        return render_to_response('login.html', dict(
            form=form
        ), context_instance=RequestContext(request))


def view_asset_analysis(request):
    print 'Asset Analysis List'
    try:
        variable_obj = Variable.objects.filter(row_status='Active')
        check_obj = UserProfile.objects.get(user_id=request.session['user_id'])
        customer_obj = CustomerPersonalInfo.objects.get(user=check_obj)
        assets_list1 = []
        salary = customer_obj.total_salary
        saving = customer_obj.start_saving
        i = 1
        percentage = 1 + (Variable.objects.get(variable='Salary (Net)').percentage / 100)
        temp = get_year_calculation(salary, percentage)
        variables_data = {
            'sr_no': i,
            'variable': 'Salary (Net)',
            'amount': int(salary),
            'year1': temp}
        variables_data['year2'] = get_year_calculation(variables_data['year1'], percentage)
        variables_data['year3'] = get_year_calculation(variables_data['year2'], percentage)
        variables_data['year4'] = get_year_calculation(variables_data['year3'], percentage)
        variables_data['year5'] = get_year_calculation(variables_data['year4'], percentage)
        variables_data['year6'] = get_year_calculation(variables_data['year5'], percentage)
        variables_data['year7'] = get_year_calculation(variables_data['year6'], percentage)
        variables_data['year8'] = get_year_calculation(variables_data['year7'], percentage)
        variables_data['year9'] = get_year_calculation(variables_data['year8'], percentage)
        variables_data['year10'] = get_year_calculation(variables_data['year9'], percentage)
        assets_list1.append(variables_data)

        assets_list = []
        sum = 0

        cust_var_obj = CustomerVariable.objects.filter(customer_id=customer_obj, row_status='Active')
        for variables in cust_var_obj:
            sum = sum + variables.amount
            i = i + 1
            percentage = Variable.objects.get(variable_id=variables.variable.variable_id).percentage
            currect_percentage = (1 + percentage / 100)
            temp = get_year_calculation(variables.amount, currect_percentage)
            variables_data = {
                'sr_no': i,
                'variable': variables.variable.variable,
                'amount': int(variables.amount),
                'year1': temp}
            variables_data['year2'] = get_year_calculation(variables_data['year1'], currect_percentage)
            variables_data['year3'] = get_year_calculation(variables_data['year2'], currect_percentage)
            variables_data['year4'] = get_year_calculation(variables_data['year3'], currect_percentage)
            variables_data['year5'] = get_year_calculation(variables_data['year4'], currect_percentage)
            variables_data['year6'] = get_year_calculation(variables_data['year5'], currect_percentage)
            variables_data['year7'] = get_year_calculation(variables_data['year6'], currect_percentage)
            variables_data['year8'] = get_year_calculation(variables_data['year7'], currect_percentage)
            variables_data['year9'] = get_year_calculation(variables_data['year8'], currect_percentage)
            variables_data['year10'] = get_year_calculation(variables_data['year9'], currect_percentage)
            assets_list.append(variables_data)

        temp_desc = {'sr_no': '', 'variable': 'Saving', 'amount': 0, 'year1': 0, 'year2': 0, 'year3': 0, 'year4': 0,
                     'year5': 0, 'year6': 0, 'year7': 0, 'year8': 0, 'year9': 0, 'year10': 0}
        for asset in assets_list:
            temp_desc['amount'] = temp_desc['amount'] + asset['amount']
            temp_desc['year1'] = temp_desc['year1'] + asset['year1']
            temp_desc['year2'] = temp_desc['year2'] + asset['year2']
            temp_desc['year3'] = temp_desc['year3'] + asset['year3']
            temp_desc['year4'] = temp_desc['year4'] + asset['year4']
            temp_desc['year5'] = temp_desc['year5'] + asset['year5']
            temp_desc['year6'] = temp_desc['year6'] + asset['year6']
            temp_desc['year7'] = temp_desc['year7'] + asset['year7']
            temp_desc['year8'] = temp_desc['year8'] + asset['year8']
            temp_desc['year9'] = temp_desc['year9'] + asset['year9']
            temp_desc['year10'] = temp_desc['year10'] + asset['year10']

        for asset in assets_list1:
            temp_desc['amount'] = asset['amount'] - temp_desc['amount']
            temp_desc['year1'] = asset['year1'] - temp_desc['year1']
            temp_desc['year2'] = asset['year2'] - temp_desc['year2']
            temp_desc['year3'] = asset['year3'] - temp_desc['year3']
            temp_desc['year4'] = asset['year4'] - temp_desc['year4']
            temp_desc['year5'] = asset['year5'] - temp_desc['year5']
            temp_desc['year6'] = asset['year6'] - temp_desc['year6']
            temp_desc['year7'] = asset['year7'] - temp_desc['year7']
            temp_desc['year8'] = asset['year8'] - temp_desc['year8']
            temp_desc['year9'] = asset['year9'] - temp_desc['year9']
            temp_desc['year10'] = asset['year10'] - temp_desc['year10']

        assets_list.append(temp_desc)

        percentage = Variable.objects.get(variable='Investment return assumption').percentage
        print percentage
        invest_percentage = (percentage / 100)

        saving_data = {
            'sr_no': 1,
            'balance_sheet': 'Start Saving',
            'year0': int(customer_obj.start_saving)
        }
        new_saving_data = {
            'sr_no': 2,
            'balance_sheet': 'New Saving',
            'year0': int(temp_desc['amount'] * 12)
        }
        investment_data = {
            'sr_no': 3,
            'balance_sheet': 'Investment returns',
            'year0': int(get_year_calculation(saving_data['year0'], invest_percentage))
        }
        end_saving_data = {
            'sr_no': '',
            'balance_sheet': 'End Saving',
            'year0': int(saving_data['year0'] + new_saving_data['year0'] + investment_data['year0'])
        }

        balance_data = []

        saving_data['year1'] = end_saving_data['year0']
        new_saving_data['year1'] = temp_desc['year1'] * 12
        investment_data['year1'] = get_year_calculation(saving_data['year1'], invest_percentage)
        end_saving_data['year1'] = saving_data['year1'] + new_saving_data['year1'] + investment_data['year1']

        saving_data['year2'] = end_saving_data['year1']
        new_saving_data['year2'] = temp_desc['year2'] * 12
        investment_data['year2'] = get_year_calculation(saving_data['year2'], invest_percentage)
        end_saving_data['year2'] = saving_data['year2'] + new_saving_data['year2'] + investment_data['year2']

        saving_data['year3'] = end_saving_data['year2']
        new_saving_data['year3'] = temp_desc['year3'] * 12
        investment_data['year3'] = get_year_calculation(saving_data['year3'], invest_percentage)
        end_saving_data['year3'] = saving_data['year3'] + new_saving_data['year3'] + investment_data['year3']

        saving_data['year4'] = end_saving_data['year3']
        new_saving_data['year4'] = temp_desc['year4'] * 12
        investment_data['year4'] = get_year_calculation(saving_data['year4'], invest_percentage)
        end_saving_data['year4'] = saving_data['year4'] + new_saving_data['year4'] + investment_data['year4']

        saving_data['year5'] = end_saving_data['year4']
        new_saving_data['year5'] = temp_desc['year5'] * 12
        investment_data['year5'] = get_year_calculation(saving_data['year5'], invest_percentage)
        end_saving_data['year5'] = saving_data['year5'] + new_saving_data['year5'] + investment_data['year5']

        saving_data['year6'] = end_saving_data['year5']
        new_saving_data['year6'] = temp_desc['year6'] * 12
        investment_data['year6'] = get_year_calculation(saving_data['year6'], invest_percentage)
        end_saving_data['year6'] = saving_data['year6'] + new_saving_data['year6'] + investment_data['year6']

        saving_data['year7'] = end_saving_data['year6']
        new_saving_data['year7'] = temp_desc['year7'] * 12
        investment_data['year7'] = get_year_calculation(saving_data['year7'], invest_percentage)
        end_saving_data['year7'] = saving_data['year7'] + new_saving_data['year7'] + investment_data['year7']

        saving_data['year8'] = end_saving_data['year7']
        new_saving_data['year8'] = temp_desc['year8'] * 12
        investment_data['year8'] = get_year_calculation(saving_data['year8'], invest_percentage)
        end_saving_data['year8'] = saving_data['year8'] + new_saving_data['year8'] + investment_data['year8']

        saving_data['year9'] = end_saving_data['year8']
        new_saving_data['year9'] = temp_desc['year9'] * 12
        investment_data['year9'] = get_year_calculation(saving_data['year9'], invest_percentage)
        end_saving_data['year9'] = saving_data['year9'] + new_saving_data['year9'] + investment_data['year9']

        saving_data['year10'] = end_saving_data['year9']
        new_saving_data['year10'] = temp_desc['year10'] * 12
        investment_data['year10'] = get_year_calculation(saving_data['year10'], invest_percentage)
        end_saving_data['year10'] = saving_data['year10'] + new_saving_data['year10'] + investment_data['year10']

        balance_data.append(saving_data)
        balance_data.append(new_saving_data)
        balance_data.append(investment_data)
        balance_data.append(end_saving_data)

        details = {'customer_age': customer_obj.age, 'salary_list': assets_list1, 'sum': sum}
        # print "Details====>>>",details

        # print 'assets_list',assets_list
    except Exception, e:
        print 'Exception ', e
    return details, assets_list, balance_data, temp_desc


def get_year_calculation(amount, percentage):
    try:
        return int(amount * percentage)
    except Exception, e:
        print 'Exception==>', e


def cal_bal_sheet(amount, percentage):
    try:
        return int(amount * percentage)
    except Exception, e:
        print 'Exception==>', e


def cal_cash_flow(amount, percentage):
    try:
        return int(amount * ((1 + percentage) ** 10) * (-1))
    except Exception, e:
        print 'Exception==>', e


def get_net_worth(request):
    try:
        check_obj = UserProfile.objects.get(user_id=request.session['user_id'])
        cust_pro_obj = Customer_Product.objects.filter(user_id=check_obj, row_status='Active')
        bank_obj = CustomerBankAccountDetails.objects.filter(user=check_obj, row_status='Active')
        bank_amount = 0
        product_amont = 0
        if bank_obj:
            for banks in bank_obj:
                bank_amount = float(bank_amount) + float(banks.amount)
        for cust_pro in cust_pro_obj:
            product_amont = float(product_amont) + float(cust_pro.amount)
        product_amont = product_amont + bank_amount
        print product_amont
        return product_amont
    except Exception, e:
        print 'Exception==>', e


def get_goals_detail(request):
    try:
        check_obj = UserProfile.objects.get(user_id=request.session['user_id'])
        cash_flow_list = []
        bullet_data = {
            'sr_no': 1, 'cash_flow': 'Bullet Outflow', 'year0': '--', 'year1': '--', 'year2': '--', 'year3': '--',
            'year4': '--', 'year5': '--', 'year6': '--', 'year7': '--', 'year8': '--', 'year9': '--', 'year10': '--'
        }
        annual_data = {
            'sr_no': 2, 'cash_flow': 'Annual Outflow', 'year0': '--', 'year1': '--', 'year2': '--', 'year3': '--',
            'year4': '--', 'year5': '--', 'year6': '--', 'year7': '--', 'year8': '--', 'year9': '--', 'year10': '--'
        }
        unplanned_data = {
            'sr_no': 3, 'cash_flow': 'Unplanned', 'year0': '--', 'year1': '--', 'year2': '--', 'year3': '--',
            'year4': '--', 'year5': '--', 'year6': '--', 'year7': '--', 'year8': '--', 'year9': '--', 'year10': '--'
        }
        total_data = {
            'sr_no': '', 'cash_flow': 'Total Outflow', 'year0': '--', 'year1': '--', 'year2': '--', 'year3': '--',
            'year4': '--', 'year5': '--', 'year6': '--', 'year7': '--', 'year8': '--', 'year9': '--', 'year10': '--'
        }

        
        try:
            goal_cat_obj = Goal_Category.objects.get(goal_cat="Vacation per year")
            print goal_cat_obj
            goal_per_obj = Goal.objects.get(user_id=check_obj, goal_cat_id = goal_cat_obj , row_status='Active')
            print goal_per_obj
            annual_data['year0'] = int(goal_per_obj.amount) * -1
            annual_data['year1'] = int(goal_per_obj.amount) * -1
            annual_data['year2'] = int(goal_per_obj.amount) * -1
            annual_data['year3'] = int(goal_per_obj.amount) * -1
            annual_data['year4'] = int(goal_per_obj.amount) * -1
            annual_data['year5'] = int(goal_per_obj.amount) * -1
            annual_data['year6'] = int(goal_per_obj.amount) * -1
            annual_data['year7'] = int(goal_per_obj.amount) * -1
            annual_data['year8'] = int(goal_per_obj.amount) * -1
            annual_data['year9'] = int(goal_per_obj.amount) * -1
            annual_data['year10'] = int(goal_per_obj.amount) * -1
        except Goal.DoesNotExist, e:
            print "Execption:",e
            annual_data['year0'] = 0
            annual_data['year1'] = 0
            annual_data['year2'] = 0
            annual_data['year3'] = 0
            annual_data['year4'] = 0
            annual_data['year5'] = 0
            annual_data['year6'] = 0
            annual_data['year7'] = 0
            annual_data['year8'] = 0
            annual_data['year9'] = 0
            annual_data['year10'] = 0

        print annual_data

        for i in range(10):
            pre_date = datetime.now()
            pre_year = pre_date.year + i
            goal_target_year_id = Goal_Target_Year.objects.get(goal_target_year=pre_year)
            goal_obj = Goal.objects.filter(user_id=check_obj, row_status='Active',
                                           goal_target_year_id=goal_target_year_id)
            print goal_obj
            goal_obj = goal_obj.exclude(goal_cat_id = goal_cat_obj)
            bullet_amount = 0
            annual_amount = 0
            unplanned_amount = 0

            if goal_obj and i == 0:
                for goal in goal_obj:
                    variable_obj = Goal_Category.objects.get(goal_cat_id=goal.goal_cat_id.goal_cat_id).goal_percentage
                    percentage_data = (variable_obj / 100)
                    amt = cal_cash_flow(float(goal.amount), percentage_data)
                    bullet_amount = bullet_amount + amt
                bullet_data['year0'] = int(bullet_amount)

            if bullet_data['year0'] == '--':
                bullet_data['year0'] = int(0)
            total_data['year0'] = int(float(bullet_data['year0']) + float(annual_data['year0']))

            if goal_obj and i == 1:
                for goal in goal_obj:
                    variable_obj = Goal_Category.objects.get(goal_cat_id=goal.goal_cat_id.goal_cat_id).goal_percentage
                    percentage_data = (variable_obj / 100)
                    amt = cal_cash_flow(float(goal.amount), percentage_data)
                    bullet_amount = bullet_amount + amt
                bullet_data['year1'] = int(bullet_amount)

            if bullet_data['year1'] == '--':
                bullet_data['year1'] = 0
            total_data['year1'] =int(float(bullet_data['year1']) + float(annual_data['year0']))

            if goal_obj and i == 2:
                for goal in goal_obj:
                    variable_obj = Goal_Category.objects.get(goal_cat_id=goal.goal_cat_id.goal_cat_id).goal_percentage
                    percentage_data = (variable_obj / 100)
                    amt = cal_cash_flow(float(goal.amount), percentage_data)
                    bullet_amount = bullet_amount + amt
                bullet_data['year2'] = int(bullet_amount)

            if bullet_data['year2'] == '--':
                bullet_data['year2'] = 0
            final_amount = float(bullet_data['year2']) + float(annual_data['year0'])
            total_data['year2'] = int(final_amount)

            if goal_obj and i == 3:
                for goal in goal_obj:
                    variable_obj = Goal_Category.objects.get(goal_cat_id=goal.goal_cat_id.goal_cat_id).goal_percentage
                    percentage_data = (variable_obj / 100)
                    amt = cal_cash_flow(float(goal.amount), percentage_data)
                    bullet_amount = bullet_amount + amt
                bullet_data['year3'] = int(bullet_amount)

            if bullet_data['year3'] == '--':
                bullet_data['year3'] = 0
            total_data['year3'] = int(float(bullet_data['year3']) + float(annual_data['year0']))

            if goal_obj and i == 4:
                for goal in goal_obj:
                    variable_obj = Goal_Category.objects.get(goal_cat_id=goal.goal_cat_id.goal_cat_id).goal_percentage
                    percentage_data = (variable_obj / 100)
                    amt = cal_cash_flow(float(goal.amount), percentage_data)
                    bullet_amount = bullet_amount + amt
                bullet_data['year4'] = int(bullet_amount)

            if bullet_data['year4'] == '--':
                bullet_data['year4'] = 0
            total_data['year4'] = int(float(bullet_data['year4']) + float(annual_data['year0']))

            if goal_obj and i == 5:
                for goal in goal_obj:
                    variable_obj = Goal_Category.objects.get(goal_cat_id=goal.goal_cat_id.goal_cat_id).goal_percentage
                    percentage_data = (variable_obj / 100)
                    amt = cal_cash_flow(float(goal.amount), percentage_data)
                    bullet_amount = bullet_amount + amt
                bullet_data['year5'] = int(bullet_amount)

            if bullet_data['year5'] == '--':
                bullet_data['year5'] = 0
            total_data['year5'] = int(float(bullet_data['year5']) + float(annual_data['year0']))

            if goal_obj and i == 6:
                for goal in goal_obj:
                    variable_obj = Goal_Category.objects.get(goal_cat_id=goal.goal_cat_id.goal_cat_id).goal_percentage
                    percentage_data = (variable_obj / 100)
                    amt = cal_cash_flow(float(goal.amount), percentage_data)
                    bullet_amount = bullet_amount + amt
                bullet_data['year6'] = int(bullet_amount)

            if bullet_data['year6'] == '--':
                bullet_data['year6'] = 0
            total_data['year6'] = int(float(bullet_data['year6']) + float(annual_data['year0']))

            if goal_obj and i == 7:
                for goal in goal_obj:
                    variable_obj = Goal_Category.objects.get(goal_cat_id=goal.goal_cat_id.goal_cat_id).goal_percentage
                    percentage_data = (variable_obj / 100)
                    amt = cal_cash_flow(float(goal.amount), percentage_data)
                    bullet_amount = bullet_amount + amt
                bullet_data['year7'] = int(bullet_amount)

            if bullet_data['year7'] == '--':
                bullet_data['year7'] = 0
            total_data['year7'] = int(float(bullet_data['year7']) + float(annual_data['year0']))

            if goal_obj and i == 8:
                for goal in goal_obj:
                    variable_obj = Goal_Category.objects.get(goal_cat_id=goal.goal_cat_id.goal_cat_id).goal_percentage
                    percentage_data = (variable_obj / 100)
                    amt = cal_cash_flow(float(goal.amount), percentage_data)
                    bullet_amount = bullet_amount + amt
                bullet_data['year8'] = int(bullet_amount)

            if bullet_data['year8'] == '--':
                bullet_data['year8'] = 0
            total_data['year8'] = int(float(bullet_data['year8']) + float(annual_data['year0']))

            if goal_obj and i == 9:
                for goal in goal_obj:
                    variable_obj = Goal_Category.objects.get(goal_cat_id=goal.goal_cat_id.goal_cat_id).goal_percentage
                    percentage_data = (variable_obj / 100)
                    amt = cal_cash_flow(float(goal.amount), percentage_data)
                    bullet_amount = bullet_amount + amt
                bullet_data['year9'] = int(bullet_amount)

            if bullet_data['year9'] == '--':
                bullet_data['year9'] = 0
            total_data['year9'] = int(float(bullet_data['year9']) + float(annual_data['year0']))

            if goal_obj and i == 10:
                for goal in goal_obj:
                    variable_obj = Goal_Category.objects.get(goal_cat_id=goal.goal_cat_id.goal_cat_id).goal_percentage
                    percentage_data = (variable_obj / 100)
                    amt = cal_cash_flow(float(goal.amount), percentage_data)
                    bullet_amount = bullet_amount + amt
                bullet_data['year10'] = int(bullet_amount)

            if bullet_data['year10'] == '--':
                bullet_data['year10'] = 0
            total_data['year10'] = int(float(bullet_data['year10']) + float(annual_data['year0']))



        cash_flow_list.append(bullet_data)
        cash_flow_list.append(annual_data)
        cash_flow_list.append(unplanned_data)
        cash_flow_list.append(total_data)

        return cash_flow_list,total_data
    except Exception, e:
        print 'Exception==>', e

def get_funding_gap(saving_data,total_overflow):
    try:
        saving_data = saving_data
        total_overflow = total_overflow
        funding_data = {
                        'sr_no': 1, 'funding_gap': 'Funding Gap'
                        }

        if total_overflow['year0'] == '--':
            total_overflow['year0'] = 0
        funding_data['year0'] = int(saving_data['amount']*12) + int(total_overflow['year0'])

        if total_overflow['year1'] == '--':
            total_overflow['year1'] = 0
        funding_data['year1'] = int(saving_data['year1']*12) + int(total_overflow['year1'])

        if total_overflow['year2'] == '--':
            total_overflow['year2'] = 0
        funding_data['year2'] = int(saving_data['year2']*12) + int(total_overflow['year2'])

        if total_overflow['year3'] == '--':
            total_overflow['year3'] = 0
        funding_data['year3'] = int(saving_data['year3']*12) + int(total_overflow['year3'])

        if total_overflow['year4'] == '--':
            total_overflow['year4'] = 0
        funding_data['year4'] = int(saving_data['year4']*12) + int(total_overflow['year4'])

        if total_overflow['year5'] == '--':
            total_overflow['year5'] = 0
        funding_data['year5'] = int(saving_data['year5']*12) + int(total_overflow['year5'])

        if total_overflow['year6'] == '--':
            total_overflow['year6'] = 0
        funding_data['year6'] = int(saving_data['year6']*12) + int(total_overflow['year6'])

        if total_overflow['year7'] == '--':
            total_overflow['year7'] = 0
        funding_data['year7'] = int(saving_data['year7']*12) + int(total_overflow['year7'])

        if total_overflow['year8'] == '--':
            total_overflow['year8'] = 0
        funding_data['year8'] = int(saving_data['year8']*12) + int(total_overflow['year8'])

        if total_overflow['year9'] == '--':
            total_overflow['year9'] = 0
        funding_data['year9'] = int(saving_data['year9']*12) + int(total_overflow['year9'])

        if total_overflow['year10'] == '--':
            total_overflow['year10'] = 0
        funding_data['year10'] = int(saving_data['year10']*12) + int(total_overflow['year10'])

        return funding_data
    except Exception, e:
        print 'Exception==>', e
