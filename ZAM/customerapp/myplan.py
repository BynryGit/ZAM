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


# import cStringIO as StringIO
# from xhtml2pdf import pisa
# from django.template.loader import get_template
# from django.template import Context
# from django.http import HttpResponse
# from cgi import escape



def open_myplan(request):
    if request.user.is_authenticated():
        try:
            check_obj = UserProfile.objects.get(user_id=request.session['customer_id'])
            customer_obj = CustomerPersonalInfo.objects.get(user=check_obj)
            bank_amount = 0
            list1 = []
            list2 = []
            bank_obj = CustomerBankAccountDetails.objects.filter(user=check_obj, row_status='Active')
            if bank_obj:
                i = 1
                for banks in bank_obj:
                    bank_amount = float(bank_amount) + float(banks.amount)

            info, asset_list = view_asset_details(request)
            var, variables_list = view_variable_details(request)
            product_amount = get_net_worth(request)
            if bank_amount != 0:
                bank_percentage = round((bank_amount / product_amount) * 100, 0)
                bank_percentage = int(bank_percentage)
            else:
                bank_percentage = 0
            list1.append('Bank')
            list2.append(bank_percentage)

            cust_var_obj = Customer_Product.objects.filter(user_id=check_obj, row_status='Active')
            for variables in asset_list:
                list1.append(str(variables['variable']))
                pro_percentage = round((float(variables['amount']) / product_amount) * 100, 0)
                list2.append(pro_percentage)

            bank_amount = int(round(bank_amount,0))
            total_sum = int(round(product_amount - var['sum'],0))
            product_amount = int(round(float(product_amount),0))

            data = {'success': 'true', 'produc_name': list1, 'product_percentage': list2, 'info': info, 'var': var,
                    'bank': 'Bank', 'bank_amount': bank_amount, 'variables_list': variables_list,
                    'asset_list': asset_list, 'product_amount': int(product_amount), 'total_sum': int(total_sum)}
        except CustomerPersonalInfo.DoesNotExist, e:
            print 'Exception ', e
            list1 = []
            list2 = []
            info = {}
            info['sum'] = 0
            info['customer_age'] = '--'
            total_sum, product_amount = 0, 0
            data = {'success': 'true', 'info': info, 'produc_name': list1, 'product_percentage': list2,
                    'product_amount': product_amount, 'total_sum': total_sum}
        return render(request, 'myplan.html', data)
    else:
        form = CaptchaForm()
        return render_to_response('login.html', dict(
            form=form
        ), context_instance=RequestContext(request))


def view_variable_details(request):
    ##    pdb.set_trace()
    try:
        check_obj = UserProfile.objects.get(user_id=request.session['customer_id'])
        var = {}
        sum = 0
        customer_obj = CustomerPersonalInfo.objects.get(user=check_obj)
        if customer_obj.mortgage == None:
            mortgage = 0
        else:
            mortgage = customer_obj.mortgage
        if customer_obj.credit_card_deb == None:
            credit_card_deb = 0
        else:
            credit_card_deb = customer_obj.credit_card_deb
        if customer_obj.other_loans == None:
            other_loans = 0
        else:
            other_loans = customer_obj.other_loans
        variables_list = []
        sum = sum + int(round(mortgage,0))
        variables_data = {
            'variable': 'Mortgage',
            'amount': int(round(mortgage,0))
        }
        variables_list.append(variables_data)

        sum = sum + int(round(credit_card_deb,0))
        variables_data = {
            'variable': 'Credit Card Debit',
            'amount': int(round(credit_card_deb,0))
        }
        variables_list.append(variables_data)

        sum = sum + int(round(other_loans,0))
        variables_data = {
            'variable': 'Other Loans',
            'amount': int(round(other_loans,0))
        }
        variables_list.append(variables_data)
        var = {'sum': int(sum)}

    except Exception, e:
        print 'Exception ', e
    return var, variables_list


def view_asset_details(request):
    ##    pdb.set_trace()
    #print 'Asset List'
    try:
        check_obj = UserProfile.objects.get(user_id=request.session['customer_id'])
        info = {}
        customer_obj = CustomerPersonalInfo.objects.get(user=check_obj)
        product_list = Product.objects.all()
        variable_list = []
        for product in product_list:
            sum = 0
            name = ''
            cust_var_obj = Customer_Product.objects.filter(user_id=check_obj, product_id=product.product_id,
                                                           row_status='Active')
            if cust_var_obj:

                for variables in cust_var_obj:
                    sum = (float(sum + float(variables.amount)))
                    if variables.product_id.product_id == 2:
                        sum = sum #* 100000
                        #sum = int(round(sum,0))
                    name = variables.product_id.product
                if name != "Pension Product":
                    variables_data = {
                        'variable': name,
                        'amount': int(round(sum,0))
                    }
                else:
                    variables_data = {
                        'variable': name,
                        'amount': round(sum,2)
                    }
                variable_list.append(variables_data)
                #print "VARIABLE_LIST", variable_list

        for variables in variable_list:
            if variables['variable'] == "Pension Product":
                variables['amount'] = int(float(variables['amount']) * 100000)
        info = {'sum': sum}

    except Exception, e:
        print 'Exception ', e
    return info, variable_list


def open_new_worth(request):
    if request.user.is_authenticated():
        try:
            bank_amount = 0
            check_obj = UserProfile.objects.get(user_id=request.session['customer_id'])
            try:
                pension = 0
                pension_objs = Customer_Product.objects.filter(user_id=check_obj, product_id='2', row_status='Active')
                for pension_obj in pension_objs:
                    pension = pension + float(pension_obj.amount)
            except Customer_Product.DoesNotExist, e:
                pension = 0
            customer_obj = CustomerPersonalInfo.objects.get(user=check_obj)

            bank_obj = CustomerBankAccountDetails.objects.filter(user=check_obj, row_status='Active')
            if bank_obj:
                i = 1
                for banks in bank_obj:
                    bank_amount = int(round(bank_amount,0)) + int(round(banks.amount,0))
            #print bank_amount

            info, asset_list = view_asset_details(request)
            var, variables_list = view_variable_details(request)
            salary_data, expence_list, new_balance_data, year_list, temp_desc, end_saving_data = view_asset_analysis(request)
            product_amount = int(get_net_worth(request))
            new_goal_data, new_total_data  = get_goals_details(request)
            funding_gap_data = get_funding_gaps(check_obj,temp_desc, new_total_data)
            total_sum = int(round(product_amount - var['sum'],0))
            var, variables_list = view_variable_details(request)
            #ret_year_list, ret_age_list, ret_amount_list = get_retirement_data(customer_obj)
            retirement_list = get_retirements_data(customer_obj)

            data = {'success': 'true', 'info': var, 'asset_list': asset_list,
                    'total_sum': total_sum,
                    'balance_data': new_balance_data, 'product_amount': product_amount,
                    'variables_list': variables_list, 'funding_gap_data': funding_gap_data, 'bank': 'Bank',
                    'bank_amount': bank_amount, 'pension': pension,'new_goal':new_goal_data,
                    'retirement_list': retirement_list,
                    'salary_data': salary_data, 'expence_list': expence_list, 'year_list': year_list}
        except CustomerPersonalInfo.DoesNotExist, e:
            print 'Exception ', e
            info = {}
            info['sum'] = 0
            info['customer_age'] = '--'
            total_sum, product_amount = 0, 0
            data = {'success': 'true', 'info': info, 'pension': pension, 'product_amount': int(product_amount),
                    'total_sum': int(total_sum)}
        return render(request, 'net_worth.html', data)
        # return render_to_pdf('net_worth.html', {'pagesize':'A4','data': data})
    else:
        form = CaptchaForm()
        return render_to_response('login.html', dict(
            form=form
        ), context_instance=RequestContext(request))


def view_asset_analysis(request):
    #print 'Asset Analysis List'
    try:
        variable_obj = Variable.objects.filter(row_status='Active')
        check_obj = UserProfile.objects.get(user_id=request.session['customer_id'])
        customer_obj = CustomerPersonalInfo.objects.get(user=check_obj)
        retirement_age = 60
        cust_age = customer_obj.age
        age_gap = retirement_age - cust_age
        pre_date = datetime.now()
        pre_year = pre_date.year
        year_list = []
        assets_list2 = []
        salary = customer_obj.total_salary
        saving = customer_obj.start_saving

        if age_gap != 0:
            no_years = int(age_gap / 5)
            retirement_year = (age_gap % 5) + 1
            round_year = pre_year % 5
            if round_year != 0:
                ex_year = pre_year + 5 - round_year
            else:
                ex_year = pre_year
            year_list.append(pre_year)
            year_list.append(ex_year)

            for y in range(no_years):
                year_list.append(ex_year + (y * 5))

        year_list.append(int(pre_year + age_gap))
        year_list.append(int(pre_year + age_gap + 1))

        year_list = set(year_list)
        year_list = list(year_list)
        year_list.sort()

        #print "year_list:",year_list

        i = 1

        percentage = 1 + (Variable.objects.get(variable='Salary (Net)').percentage / 100)
        new_data = {
            'sr_no': i,
            'variable': 'Salary (Net)',
        }

        for x in range(age_gap + 2):
            pre_years = pre_year + x
            new_data[pre_years] = get_year_calculationss(int(round(salary,0)), percentage, x)

        assets_list2.append(new_data)
        assets_list = []
        sum = 0

        cust_var_obj = CustomerVariable.objects.filter(customer_id=customer_obj, row_status='Active')
        for variables in cust_var_obj:
            sum = sum + variables.amount
            i = i + 1
            percentage = Variable.objects.get(variable_id=variables.variable.variable_id).percentage
            currect_percentage = (1 + percentage / 100)
            new_data = {
                'sr_no': i,
                'variable': variables.variable.variable,
            }
            for x in range(age_gap + 2):
                pre_years = pre_year + x
                new_data[pre_years] = get_year_calculationss(int(round(variables.amount,0)), currect_percentage, x)
            assets_list.append(new_data)

        temp_desc = {
            'sr_no': '',
            'variable': 'Saving',
        }

        for x in range(age_gap + 2):
            pre_years = pre_year + x
            temp_desc[pre_years] = 0

        for asset in assets_list:
            for x in range(age_gap + 2):
                pre_years = pre_year + x
                temp_desc[pre_years] = temp_desc[pre_years] + asset[pre_years]

        for asset in assets_list2:
            for x in range(age_gap + 2):
                pre_years = pre_year + x
                temp_desc[pre_years] = asset[pre_years] - temp_desc[pre_years]

        assets_list.append(temp_desc)

        percentage = Variable.objects.get(variable='Investment return assumption').percentage
        invest_percentage = (percentage / 100)

        saving_data = {
            'sr_no': 1,
            'balance_sheet': 'Start Saving',
            pre_year: int(round(customer_obj.start_saving,0))
        }
        new_saving_data = {
            'sr_no': 2,
            'balance_sheet': 'New Saving',
            pre_year: int(round(temp_desc[pre_year] * 12,0))
        }
        investment_data = {
            'sr_no': 3,
            'balance_sheet': 'Investment returns',
            pre_year: int(round(get_year_calculations(saving_data[pre_year], invest_percentage),0))
        }
        end_saving_data = {
            'sr_no': '',
            'balance_sheet': 'End Saving',
            pre_year: int(round(saving_data[pre_year] + new_saving_data[pre_year] + investment_data[pre_year],0))
        }

        balance_data = []

        for x in range(age_gap + 1):
            pre_yearss = pre_year + x + 1
            pre_years = pre_year + x
            saving_data[pre_yearss] = end_saving_data[pre_years]
            new_saving_data[pre_yearss] = temp_desc[pre_yearss] * 12
            investment_data[pre_yearss] = get_year_calculations(saving_data[pre_yearss], invest_percentage)
            end_saving_data[pre_yearss] = saving_data[pre_yearss] + new_saving_data[pre_yearss] + investment_data[
                pre_yearss]

        balance_data.append(saving_data)
        balance_data.append(new_saving_data)
        balance_data.append(investment_data)
        balance_data.append(end_saving_data)
    except Exception, e:
        print 'Exception ', e
    return assets_list2, assets_list, balance_data, year_list, temp_desc, end_saving_data


def get_year_calculation(amount, percentage, year):
    try:
        # return int(amount * (percentage**year))
        return int(round(amount * percentage,0))
    except Exception, e:
        print 'Exception==>', e


def get_year_calculationss(amount, percentage, year):
    try:
        return int(round(amount * (percentage ** year),0))
        # return int(amount * percentage)
    except Exception, e:
        print 'Exception==>', e


def get_year_calculations(amount, percentage):
    try:
        return int(round(amount * percentage,0))
    except Exception, e:
        print 'Exception==>', e


def cal_bal_sheet(amount, percentage):
    try:
        return int(round(amount * percentage,0))
    except Exception, e:
        print 'Exception==>', e


def get_net_worth(request):
    try:
        check_obj = UserProfile.objects.get(user_id=request.session['customer_id'])
        cust_pro_obj = Customer_Product.objects.filter(user_id=check_obj, row_status='Active')
        bank_obj = CustomerBankAccountDetails.objects.filter(user=check_obj, row_status='Active')
        bank_amount = 0
        product_amont = 0
        if bank_obj:
            for banks in bank_obj:
                bank_amount = float(bank_amount) + float(banks.amount)
        for cust_pro in cust_pro_obj:
            amount = 0
            if cust_pro.product_id.product_id == 2:
                amount = float(cust_pro.amount) * 100000
            else:
                amount = float(cust_pro.amount)
            product_amont = float(product_amont) + amount
        product_amont = product_amont + bank_amount
        #print product_amont
        return round(product_amont,0)
    except Exception, e:
        print 'Exception==>', e


def get_goals_details(request):
    try:
        check_obj = UserProfile.objects.get(user_id=request.session['customer_id'])
        cash_flow_list = []
        customer_obj = CustomerPersonalInfo.objects.get(user=check_obj)
        retirement_age = 60
        cust_age = customer_obj.age
        age_gap = retirement_age - cust_age
        pre_date = datetime.now()
        pre_year = pre_date.year

        bullet_data = {
            'sr_no': 1, 'cash_flow': 'Bullet Outflow',
        }
        annual_data = {
            'sr_no': 2, 'cash_flow': 'Annual Outflow',
        }
        total_data = {
            'sr_no': '', 'cash_flow': 'Total Outflow',
        }

        for x in range(age_gap + 2):
            pre_years = pre_year + x
            annual_data[pre_years] = 0
            bullet_data[pre_years] = 0
            total_data[pre_years] = 0

        goal_cat_obj = Goal_Category.objects.get(goal_cat="Payback Loans")
        goal_per_obj = Goal.objects.filter(user_id=check_obj, goal_cat_id=goal_cat_obj, row_status='Active')
        for goals_vac in goal_per_obj:
            if goals_vac:
                for x in range(age_gap + 2):
                    pre_years = pre_year + x
                    annual_data[pre_years] = annual_data[pre_years] + int(goals_vac.amount)

        goal_cat_objs = Goal_Category.objects.get(goal_cat="Emergency Fund")
        goal_per_obj = Goal.objects.filter(user_id=check_obj, goal_cat_id=goal_cat_objs, row_status='Active')
        for goals_vac in goal_per_obj:
            if goals_vac:
                for x in range(age_gap + 2):
                    pre_years = pre_year + x
                    annual_data[pre_years] = annual_data[pre_years] + int(goals_vac.amount)

        for x in range(age_gap + 2):
            pre_years = pre_year + x
            #goal_target_year_id = Goal_Target_Year.objects.get(goal_target_year=pre_years)
            goal_obj = Goal.objects.filter(user_id=check_obj, row_status='Active',
                                           goal_target_year=pre_years)
            goal_obj = goal_obj.exclude(goal_cat_id=goal_cat_obj)
            goal_obj = goal_obj.exclude(goal_cat_id=goal_cat_objs)
            bullet_data[pre_years] = int(calculate_bullet_outflow(goal_obj, x))
            total_data[pre_years] = int(round(float(bullet_data[pre_years]) + float(annual_data[pre_years]),0))

        cash_flow_list.append(bullet_data)
        cash_flow_list.append(annual_data)
        cash_flow_list.append(total_data)

        return cash_flow_list, total_data#, bullet_data
    except Exception, e:
        print 'Exception==>', e

def calculate_bullet_outflow(goal_obj, i):
    try:
        bullet_amount = 0
        for goal in goal_obj:
            variable_obj = Goal_Category.objects.get(goal_cat_id=goal.goal_cat_id.goal_cat_id).goal_percentage
            percentage_data = (variable_obj / 100)
            amt = cal_cash_flow(float(goal.amount), percentage_data, i)
            bullet_amount = bullet_amount + amt
    except Exception, e:
        print "Exception:",e
    return bullet_amount


def cal_cash_flow(amount, percentage, i):
    try:
        return int(round(amount * ((1 + percentage) ** i),0))
    except Exception, e:
        print 'Exception==>', e


def get_funding_gaps(check_obj,saving_data, total_overflow):
    try:
        cash_flow_list = []
        customer_obj = CustomerPersonalInfo.objects.get(user=check_obj)
        retirement_age = 60
        cust_age = customer_obj.age
        age_gap = retirement_age - cust_age
        pre_date = datetime.now()
        pre_year = pre_date.year

        saving_data = saving_data
        total_overflow = total_overflow
        funding_data = {
            'sr_no': 1, 'funding_gap': 'Funding Gap',
        }

        for x in range(age_gap + 2):
            pre_years = pre_year + x
            funding_data[pre_years] = int(round(saving_data[pre_years] * 12,0)) - int(round(total_overflow[pre_years],0))

        return funding_data
    except Exception, e:
        print 'Exception==>', e


def get_retirements_data(customer_obj):
    try:
        cust_var_obj = CustomerVariable.objects.filter(customer_id=customer_obj, row_status='Active')
        percentage = Variable.objects.get(variable='Cost inflation').percentage
        amount = 0
        retirement_age = 60
        cust_age = customer_obj.age
        age_gap = retirement_age - cust_age
        pre_date = datetime.now()
        pre_year = pre_date.year
        retirement_list = []

        for variables in cust_var_obj:
            amount = amount + variables.amount

        age_data = {
            'sr_no': 1, 'outflow': 'Age',
        }
        retirement_data = {
            'sr_no': 2, 'outflow': 'Cost',
        }

        for x in range(age_gap + 2):
            pre_years = pre_year + x
            age_data[pre_years] = cust_age + x
            if x == 0:
                power = 1
            else:
                power = x
            retirement_data[pre_years] = cal_cost(amount, power, percentage)

        retirement_list.append(age_data)
        retirement_list.append(retirement_data)
        #print retirement_list
        return retirement_list
    except Exception, e:
        print 'Exception==>', e


def cal_cost(amount, power, percentage):
    try:
        if power == 1:
            return int(round(amount,0))
        else:
            return int(round(amount * ((1 + (percentage / 100)) ** power),0))
    except Exception, e:
        print 'Exception==>', e
