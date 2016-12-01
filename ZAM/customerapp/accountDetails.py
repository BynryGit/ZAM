__author__ = 'vikas kumawat'

from customerapp.myplan import *
from customerapp.meter_gauge import *
from zamapp.captcha_form import CaptchaForm
from zamapp.models import *

import logging
import logging.handlers
from xhtml2pdf import pisa
import cStringIO as StringIO
from cgi import escape
from django.template.loader import get_template
from django.template import Context
from django.http import HttpResponse
import numpy
#form datetime import timedelta

import datetime

logging.basicConfig()


# def customer_report(request):
#     data = {'success':'true'}
#     return render(request, 'customer_report.html', data)

@csrf_exempt
def customer_report(request):
    bank_saving, start_saving, pension, other_saving, mutual_fund, direct_equity = 0, 0, 0, 0, 0, 0
    property_amount, gold_amount, mortgage, credit_card_deb, other_loans, housing = 0, 0, 0, 0, 0, 0
    utilities, groceries, education, transportation, car_loan, shopping, eating_out = 0, 0, 0, 0, 0, 0, 0
    personal_care, others, total_essential, total_choices, total_expense, age = 0, 0, 0, 0, 0, 0
    emergency_fund, monthly_salary, sum, product_amount, total_sum, saving_needed, monthly_savings = 0, 0, 0, 0, 0, 0, 0
    finacial_priorities, under_budget, essential_precentage, choices_precentage, expense_precentage = 0, 0, 0, 0, 0
    other_essentials, spending_look_like = 0, 0
    review_date, prepared_date,description,user_gender = 'N/A','N/A','',''
    goal_per_obj = []
    var, variables_list,cibil_score = '','','N/A'
    check_obj = UserProfile.objects.get(user_id=request.session['customer_id'])
    first_name = check_obj.user_first_name
    last_name = check_obj.user_last_name
    product_list = Customer_Product.objects.filter(user_id=check_obj.user_id, row_status='Active')
    days_per_month = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    try:
        customer_obj = CustomerPersonalInfo.objects.get(user=check_obj)
        if customer_obj:
            if customer_obj.user_title:
                user_gender = customer_obj.user_title

            pre_date = datetime.datetime.now()
            if customer_obj.cibil_score:
                cibil_score = int(customer_obj.cibil_score)

            if customer_obj.report_description:
                description = customer_obj.report_description
            else:
                description = ''

            prepared_date, review_date = report_dates(pre_date,customer_obj)

            age = customer_obj.age
            monthly_salary = int(customer_obj.total_salary)

            if customer_obj.mortgage:
                mortgage = int(customer_obj.mortgage)
            if customer_obj.credit_card_deb:
                credit_card_deb = int(customer_obj.credit_card_deb)
            if customer_obj.other_loans:
                other_loans = int(customer_obj.other_loans)
            if customer_obj.start_saving:
                start_saving = int(customer_obj.start_saving)

            cust_var_obj = CustomerVariable.objects.filter(customer_id=customer_obj, row_status='Active')
            for variables in cust_var_obj:
                if variables.variable.variable_id == 2:
                    housing = int(float(variables.amount))
                if variables.variable.variable_id == 3:
                    utilities = int(float(variables.amount))
                if variables.variable.variable_id == 4:
                    groceries = int(float(variables.amount))
                if variables.variable.variable_id == 5:
                    education = int(float(variables.amount))
                if variables.variable.variable_id == 6:
                    transportation = int(float(variables.amount))
                if variables.variable.variable_id == 7:
                    car_loan = int(float(variables.amount))

                if variables.variable.variable_id == 8:
                    shopping = int(float(variables.amount))
                if variables.variable.variable_id == 9:
                    eating_out = int(float(variables.amount))
                if variables.variable.variable_id == 10:
                    personal_care = int(float(variables.amount))
                if variables.variable.variable_id == 11:
                    others = int(float(variables.amount))

            other_essentials = car_loan + education
            total_essential = housing + utilities + groceries + transportation + other_essentials
            total_choices = eating_out + shopping + personal_care + others
            total_expense = total_essential + total_choices
            monthly_savings = int(monthly_salary - total_expense)
            salary_pre = int(monthly_salary) * 20 /100
            if salary_pre > monthly_savings:
                saving_needed = salary_pre
            else:
                saving_needed = monthly_savings
            spending_look_like = monthly_salary - saving_needed
            essential_precentage = (float(total_essential)/float(monthly_salary)) * 100.0
            choices_precentage = (float(total_choices)/float(monthly_salary)) * 100.0
            expense_precentage = (float(total_expense)/float(monthly_salary)) * 100.0


        bank_obj = CustomerBankAccountDetails.objects.filter(user=check_obj, row_status='Active')
        bank_saving = 0
        if bank_obj:
            for banks in bank_obj:
                bank_saving = bank_saving + int(banks.amount)

        for products in product_list:
            if products.product_id.product_id == 3:
                other_saving = other_saving + int(float(products.amount))
            if products.product_id.product_id == 2:

                pension = int(pension) + int((float(products.amount)) * 100000)
                #print "pension product", pension
            if products.product_id.product_id == 5:
                direct_equity = direct_equity + int(float(products.amount))
            if products.product_id.product_id == 6:
                property_amount = property_amount + int(float(products.amount))
            if products.product_id.product_id == 7:
                mutual_fund = mutual_fund + int(float(products.amount))
            if products.product_id.product_id == 8:
                gold_amount = gold_amount + int(float(products.amount))

        var, variables_list = view_variable_details(request)
        product_amount = get_net_worth(request)
        total_sum = int(product_amount - var['sum'])
        sum = var['sum']
        finacial_priorities = 0
        pres_date = datetime.datetime.now()

        pre_year = int(pres_date.year)
        ##pre_date = pre_date.strftime('%d/%m/%Y')
        year_salary = int(monthly_salary) * 12
        goal_data = Goal.objects.filter(user_id=check_obj, row_status='Active').order_by('goal_cat_id__goal_priorities')
        salary_data, expence_list, new_balance_data, year_list, temp_desc, end_saving = view_asset_analysis(request)
        total_goal, goal_amount = 0, 0

        if goal_data:
            i = 0

            emergency_fund = 6 * monthly_salary
            for goals in goal_data:
                i = i + 1
                saving_amount = int(end_saving[pre_year])
                amount_required = int(goals.amount) - bank_saving
                if amount_required <= 0:
                    amount_required = 0
                if goals.amount_allocated:
                    goal_amount_allocated = int(goals.amount_allocated)
                else:
                    goal_amount_allocated = 0


                # if goals.goal_cat_id.goal_priorities == '1':
                #     total_goal = 0
                #     goal_amount = int(goals.amount)
                # elif goals.goal_cat_id.goal_priorities == '2':
                #     total_goal = total_sum - goal_amount
                #     goal_amount = int(goals.amount)
                # else:
                #     total_goal = total_goal - goal_amount
                #     goal_amount = int(goals.amount)

                # if goals.goal_cat_id.goal_priorities == '1':
                #     if bank_saving > int(goals.amount):
                #         goal_status = 'Met'
                # elif total_goal > int(goals.amount):
                #     goal_status = 'Met'
                # else:
                #     goal_status = 'Not Met'

                if goals.goal_cat_id.goal_priorities == '3':
                    annual_income, precentage, retirement_emi, income_retirement, precentage_retirement = retirement_calc(
                        age, monthly_salary, goal_amount_allocated)

                    goal_obj = {
                        'index': i,
                        'goal_name': goals.goal_name,
                        'goal_cat_name': goals.goal_cat_id.goal_cat,
                        'goal_status': 'Not Met',
                        'goal_amount': annual_income,
                        'goal_amount_required': amount_required,
                        'goal_saving_amount': saving_amount,
                        'goal_amount_allocated': goal_amount_allocated,
                        'goal_target_year': goals.goal_target_date.strftime('%d %b %Y'),
                        'goal_zero': implementation_debt_equity_calc(goals, 0.052),
                        'goal_low': implementation_debt_equity_calc(goals, 0.111),
                        'goal_blnc': implementation_debt_equity_calc(goals, 0.1346),
                        'goal_agg': implementation_debt_equity_calc(goals, 0.17),
                        'goal_final_value': income_retirement,
                        'goal_emi': retirement_emi,
                        'goal_pre_precentage': precentage,
                        'goal_future_precentage': int(precentage_retirement)
                    }
                    #goal_per_obj.append(goal_obj)

                else:
                    goal_obj = {
                        'index': i,
                        'goal_name': goals.goal_name,
                        'goal_cat_name': goals.goal_cat_id.goal_cat,
                        'goal_status': 'Not Met',
                        'goal_amount': goals.amount,
                        'goal_amount_required': amount_required,
                        'goal_saving_amount': saving_amount,
                        'goal_amount_allocated': goal_amount_allocated,
                        'goal_target_year': goals.goal_target_date.strftime('%d %b %Y'),
                        'goal_zero': implementation_debt_equity_calc(goals,0.052),
                        'goal_low': implementation_debt_equity_calc(goals,0.111),
                        'goal_blnc': implementation_debt_equity_calc(goals,0.1346),
                        'goal_agg': implementation_debt_equity_calc(goals,0.17),
                        'goal_final_value':implementation_final_value(goals),
                        'goal_emi':implementation_year_calc(goals),
                        'goal_pre_precentage':percentage_calc(int(goals.amount),year_salary),
                        'goal_future_precentage':percentage_calc(implementation_final_value(goals),year_salary)
                    }
                goal_per_obj.append(goal_obj)

            for goals in goal_data:
                if goals.amount_allocated:
                    goal_amount_allocated = int(goals.amount_allocated)
                else:
                    goal_amount_allocated = 0
                finacial_priorities = finacial_priorities + goal_amount_allocated
        under_budget = int(monthly_salary - total_expense - finacial_priorities)
    except CustomerPersonalInfo.DoesNotExist, e:
        print 'Exception :', e

    data = {'first_name': first_name, 'last_name': last_name, 'monthly_salary': monthly_salary, 'saving_needed':saving_needed,
            'bank_saving': bank_saving, 'pension': pension, 'other_saving': other_saving, 'start_saving':start_saving,
            'provident_fund': pension, 'mutual_fund': mutual_fund, 'gold_amount': gold_amount,'monthly_savings':monthly_savings,
            'direct_equity': direct_equity, 'property_amount': property_amount, 'mortgage': mortgage,'user_gender':user_gender,
            'credit_card_deb': credit_card_deb, 'other_loans': other_loans, 'sum': sum,'description':description,'cibil_score':cibil_score,
            'product_amount': int(product_amount), 'total_sum': total_sum, 'housing': housing, 'utilities': utilities,
            'groceries': groceries, 'total_choices':total_choices, 'total_essential': total_essential,'total_expense':total_expense,
            'education': education, 'transportation': transportation, 'car_loan': car_loan,'age':age, 'emergency_fund':emergency_fund,
            'shopping': shopping, 'eating_out': eating_out, 'personal_care': personal_care, 'others': others,
            'finacial_priorities':finacial_priorities, 'under_budget':under_budget,'goal_per_obj':goal_per_obj,
            'essential_precentage':round(essential_precentage,2),'choices_precentage':round(choices_precentage,2),'expense_precentage':round(expense_precentage,2),
            'pagesize': 'A4','pre_date':prepared_date, 'nxt_date':review_date, 'other_essentials':other_essentials, 'spending_look_like':spending_look_like}

    template = get_template('customer_report.html')
    html = template.render(Context(data))
    result = StringIO.StringIO()

    pdf = pisa.pisaDocument(StringIO.StringIO(html.encode("utf-8")), result)

    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return HttpResponse('We had some errors<pre>%s</pre>' % escape(html))

def percentage_calc(amount,salary):
    precentage = float(amount)/float(salary)*100
    return int(precentage)

def report_dates(pre_date,customer_obj):
    days_per_month = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    days, next_days = 0, 0
    date_format = "%m/%d/%Y"
    month_days = 0
    if customer_obj.registration_date:
        goal_date = customer_obj.registration_date
        pre_date = pre_date.strftime("%m/%d/%Y")
        goals_date = goal_date.strftime("%m/%d/%Y")
        a = datetime.datetime.strptime(pre_date, date_format)
        b = datetime.datetime.strptime(goals_date, date_format)

        for i in range(3):
            if b.month + i > 12:
                pre_month = b.month + i - 12
                month_days = month_days + days_per_month[pre_month - 1]
                if pre_month == 2 and b.year + years + 1 % 4 == 0:
                    month_days = month_days + 1
            else:
                month_days = month_days + days_per_month[b.month - 1 + i]
                if b.month == 2 and b.year + years + 1 % 4 == 0:
                    month_days = month_days + 1

        days_diff = (b - a) * -1
        months = b.month - a.month
        years = b.year - a.year
        pre_month = a.month - 1

        if months < 0 and int(days_diff.days) <= month_days:
            goal_date = customer_obj.registration_date
            prepared_date, review_date = date_calc(goal_date, month_days + 1)

        elif months < 0:
            months = months * -1
            if months % 3 == 0:
                months = months
            else:
                months = months - (months % 3)
            if months == 0:
                prepared_month = b.month + 1
            for i in range(months):
                days = days + days_per_month[b.month - 1 + i]
                prepared_month = b.month + 1 + i
                if prepared_month == 2 and b.year % 4 == 0:
                    days = days + 1
            for i in range(3):
                print "prepared_month",prepared_month
                month_index = prepared_month - 1 + i
                if month_index >= 12:
                    month_index = month_index - 12
                print "month_index",month_index
                next_days = next_days + days_per_month[month_index]
            goal_date = customer_obj.registration_date + datetime.timedelta(days=days)
            prepared_date, review_date = date_calc(goal_date,next_days + 1)

        elif months >= 0 and months < 3:
            for i in range(3):
                print "=============",pre_month + i
                month_index = pre_month + i
                if month_index >= 12:
                    month_index = month_index - 12
                print "month_index",month_index
                days = days + days_per_month[month_index]
            goal_date = customer_obj.registration_date
            prepared_date, review_date = date_calc(goal_date, days + 1)

        else:
            #print months
            if months % 3 == 0:
                months = months
            else:
                months = months - (months % 3)
            for i in range(months):
                if b.month + i > 12:
                    pre_month = b.month + i - 12
                    days = days + days_per_month[pre_month - 1]
                    if pre_month == 2 and b.year + years + 1 % 4 == 0:
                        days = days + 1
                else:
                    days = days + days_per_month[b.month - 1 + i]
                    if pre_month == 2 and b.year % 4 == 0:
                        days = days + 1
            goal_date = customer_obj.registration_date
            prepared_date, review_date = date_calc(goal_date, days + 1)

    else:
        #goal_date = datetime.datetime.now()
        #prepared_date, review_date = date_calc(goal_date)
        prepared_date, review_date = 'N/A','N/A'#date_calc(goal_date)
    return prepared_date,review_date

def date_calc(goal_date,days):
    prepared_date = goal_date.strftime('%d %b %Y')
    goals_date = goal_date + datetime.timedelta(days=days)
    review_date = goals_date.strftime('%d %b %Y')
    return prepared_date,review_date

def retirement_calc(current_age,current_salary,current_saving):
    retirement_age = 60
    age_gap = retirement_age - current_age
    dis_gap = (current_age - retirement_age) * -1
    print dis_gap
    inflation = 1.06
    income_at_retirement = (current_salary * (inflation**(age_gap))) * 0.7
    real_return = 1.8867924528301883
    year_post_retirement = 20

    payment = income_at_retirement * 12
    corpus_for_retirement = numpy.pv(real_return/100, year_post_retirement, payment, 0, 1)

    if age_gap == 0:
        emi = 'N/A'
    else:
        emi = numpy.pmt(0.12 / 12, age_gap * 12, 0, corpus_for_retirement, 1)
        emi = int(round(emi,0))

    corpus_at_retirement = numpy.fv(0.12/12,age_gap*12,current_saving,0,1)
    real_return = float(real_return)/100
    annual_income_at_retirement = numpy.pmt(real_return/12,year_post_retirement*12,corpus_at_retirement,0,1) * 12
    annual_income_at_current_price = numpy.pv(0.06, dis_gap, 0, annual_income_at_retirement, 1)

    current_salary_for_year = current_salary * 12
    precentage = float(annual_income_at_current_price)/float(current_salary_for_year) * 100

    income_at_retirement = round(current_salary * 0.7 *12,0)
    precentage_retirement = float(income_at_retirement)/float(current_salary_for_year) * 100
    precentage_retirement = round(precentage_retirement,1)



    return int(round(annual_income_at_current_price * -1,0)), round(precentage * -1,1), emi, int(round(income_at_retirement,0)),precentage_retirement
    #return int(annual_income_at_current_price * -1), int(round(precentage * -1,0)), int(emi),income_at_retirement,precentage_retirement


def implementation_debt_equity_calc(goal_obj,rate):
    try:
        pre_date = datetime.datetime.now()
        pre_year = pre_date.year

        goal_date = goal_obj.goal_target_date
        year, month = calc_year_month(pre_date, goal_date)
        final_value = calculate_final_value(goal_obj, year)
        emi = round(numpy.pmt(float(rate) / 12, month, 0, float(final_value)), 0) * -1

    except Exception, e:
        print 'Exception==>', e
    return int(emi)

def implementation_final_value(goal_obj):
    try:
        pre_date = datetime.datetime.now()
        goal_date = goal_obj.goal_target_date
        year, month = calc_year_month(pre_date, goal_date)
        final_value = calculate_final_value(goal_obj, year)

    except Exception, e:
        print 'Exception==>', e
    return int(round(final_value,0))

def implementation_year_calc(goal_obj):
    try:
        goal_date = goal_obj.goal_target_date
        goal_year = 0
        pre_date = datetime.datetime.now()
        end_date = pre_date + datetime.timedelta(366 * int(goal_year))
        year, month = calc_year_month(end_date,goal_date)
        final_value = calculate_final_value(goal_obj,year)
        emi = round(numpy.pmt(0.1/12,month,0,float(final_value)),0)*-1
    except Exception, e:
        print 'Exception==>', e
    return int(emi)


def calc_year_month(pre_date,target_date):
    date_format = "%m/%d/%Y"
    pre_date = pre_date.strftime("%m/%d/%Y")
    goal_date = target_date.strftime("%m/%d/%Y")
    a = datetime.datetime.strptime(pre_date, date_format)
    b = datetime.datetime.strptime(goal_date, date_format)
    delta = b - a
    day = int(delta.days) + 1
    month = ((b.year - a.year)) * 12 + (b.month - a.month) + 1
    year = 0.00273790926 * float(day)
    return year, month

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

def open_add_details(request):
    if request.user.is_authenticated():
        check_obj = UserProfile.objects.get(user_id=request.session['customer_id'])
        account_type = get_account_type(request)
        currency = get_currency(request)
        data = {'success': 'true', 'products': get_product(request), 'account_type': account_type, 'currency': currency}
        return render(request, 'add_details.html', data)
    else:
        form = CaptchaForm()
        return render_to_response('login.html', dict(
            form=form
        ), context_instance=RequestContext(request))


def get_product_data(request):
    ##    pdb.set_trace()
    try:
        check_obj = UserProfile.objects.get(user_id=request.session['customer_id'])
        cust_pro_obj = Customer_Product.objects.filter(user_id=check_obj, row_status='Active')
        product_list = []
        bank_amount = 0

        bank_obj = CustomerBankAccountDetails.objects.filter(user=check_obj, row_status='Active')
        if bank_obj:
            i = 0
            for banks in bank_obj:
                data = str(banks.CustomerBankAccount_id) + '|$|' + str(banks.bank) + '|$|' + str(
                    banks.account_id.account_id) + '|$|' + str(banks.currency.currency_id) + '|$|' + str(banks.amount)
                edit_btn = '<a name=' + str(
                    data) + ' onclick="edit_bank(this.name)" class="infont"> ' + '<i class="fa fa-edit"></i></i>  </a>'
                delete_btn = '<a onclick="delete_bank(' + str(
                    banks.CustomerBankAccount_id) + ')" class="infont"> ' + '<i class="fa fa-trash-o"></i></i>  </a>'
                i = i + 1
                bank_list = {
                    'count': i,
                    'product': 'Bank',
                    'product_name': banks.bank,
                    'product_amount': "{0:.2f}".format(banks.amount),
                    'edit_btn': edit_btn,
                    'delete_btn': delete_btn
                }
                product_list.append(bank_list)

        else:
            i = 0

        for cust_pro in cust_pro_obj:
            i = i + 1
            product_str = str(cust_pro.customer_product_id) + '_' + str(cust_pro.product_name)
            edit_btn = '<a id="' + product_str + '" name="' + str(
                cust_pro.amount) + '" onclick="edit_product(this.id,this.name)" class="infont"> ' + '<i class="fa fa-edit"></i></i>  </a>'
            delete_btn = '<a id="' + str(
                cust_pro.customer_product_id) + '" onclick="delete_product(this.id)" class="infont"> ' + '<i class="fa fa-trash-o"></i></i>  </a>'
            pro_obj = {
                'count': i,
                'product': cust_pro.product_id.product,
                'product_name': cust_pro.product_name,
                'product_amount': "{0:.2f}".format(float(cust_pro.amount)),
                'edit_btn': edit_btn,
                'delete_btn': delete_btn
            }
            product_list.append(pro_obj)

        data = {'data': product_list}

    except Exception, e:
        print 'Exception :', e
        data = {'data': 'none'}
    return HttpResponse(json.dumps(data), content_type='application/json')


@csrf_exempt
def edit_bank_data(request):
    ##    pdb.set_trace()
    try:
        print "------Edit Banks-----"
        bank_obj = CustomerBankAccountDetails.objects.get(CustomerBankAccount_id=request.POST.get('bank_id'))
        bank_obj.bank = request.POST.get('bank')
        bank_obj.currency = Currency.objects.get(currency_id=request.POST.get('currency'))
        bank_obj.account_id = AccountType.objects.get(account_id=request.POST.get('account_type'))
        bank_obj.amount = request.POST.get('amount')
        bank_obj.updated_by = request.session['login_user']
        bank_obj.updated_date = datetime.datetime.now()
        bank_obj.save()
        try:
            check_obj = UserProfile.objects.get(user_id=request.session['customer_id'])
            customer_obj = CustomerPersonalInfo.objects.get(user=check_obj)
            customer_obj.profile_updated = 'YES'
            customer_obj.report_description = ''
            customer_obj.save()
        except CustomerPersonalInfo.DoesNotExist:
            print "-------No Personal Info------"
        data = {'success': 'true'}
    except Exception, e:
        print 'Exception :', e
        data = {'success': 'false'}
    return HttpResponse(json.dumps(data), content_type='application/json')


@csrf_exempt
def delete_bank_data(request):
    try:
        bank_obj = CustomerBankAccountDetails.objects.get(CustomerBankAccount_id=request.POST.get('bank_id'))
        bank_obj.row_status = 'Inactive'
        bank_obj.save()
        try:
            check_obj = UserProfile.objects.get(user_id=request.session['customer_id'])
            customer_obj = CustomerPersonalInfo.objects.get(user=check_obj)
            customer_obj.profile_updated = 'YES'
            customer_obj.report_description = ''
            customer_obj.save()
        except CustomerPersonalInfo.DoesNotExist:
            print "-------No Personal Info------"
        data = {'success': 'true'}
    except Exception, e:
        print e
        data = {'success': 'false'}
    return HttpResponse(json.dumps(data), content_type='application/json')


# TO GET THE PRODUCT
def get_product(request):
    ##    pdb.set_trace()
    product_list = []
    try:
        products_list = Product.objects.all()
        for products in products_list:
            product_list.append(
                {'product_id': products.product_id, 'product': products.product})

    except Exception, e:
        print 'Exception ', e
    return product_list


@csrf_exempt
def save_product(request):
    # pdb.set_trace()
    try:
        check_obj = UserProfile.objects.get(user_id=request.session['customer_id'])

        product_obj = Product.objects.get(product_id=request.POST.get('product_id'))
        cust_pro_obj = Customer_Product.objects.get(user_id=check_obj, product_name=request.POST.get('product_name'),
                                                    product_id=product_obj, row_status='Active')
        amount = cust_pro_obj.amount
        total_amount = float(amount) + float(request.POST.get('product_amount'))
        cust_pro_obj.amount = total_amount
        cust_pro_obj.save()
        try:
            customer_obj = CustomerPersonalInfo.objects.get(user=check_obj)
            customer_obj.profile_updated = 'YES'
            customer_obj.report_description = ''
            customer_obj.save()
        except CustomerPersonalInfo.DoesNotExist:
            print "-------No Personal Info------"
        data = {'success': 'true'}
    except Customer_Product.DoesNotExist, e:
        cust_pro_obj = Customer_Product(
            user_id=check_obj,
            product_id=product_obj,
            product_name=request.POST.get('product_name'),
            amount=request.POST.get('product_amount'),
            row_status='Active',
            created_by=request.session['login_user'],
            updated_by=request.session['login_user'],
            created_date=datetime.datetime.now(),
            updated_date=datetime.datetime.now()
        )
        cust_pro_obj.save()
        #print cust_pro_obj
        data = {'success': 'true'}
    except Exception, e:
        print 'Exception :', e
        data = {'data': 'none'}
    return HttpResponse(json.dumps(data), content_type='application/json')


@csrf_exempt
def edit_product_data(request):
    ##    pdb.set_trace()
    try:
        check_obj = UserProfile.objects.get(user_id=request.session['customer_id'])
        cust_pro_obj = Customer_Product.objects.get(user_id=check_obj,
                                                    customer_product_id=request.POST.get('product_id'))
        cust_pro_obj.amount = float(request.POST.get('product_amount'))
        cust_pro_obj.save()
        try:
            customer_obj = CustomerPersonalInfo.objects.get(user=check_obj)
            customer_obj.profile_updated = 'YES'
            customer_obj.report_description = ''
            customer_obj.save()
        except CustomerPersonalInfo.DoesNotExist:
            print "-------No Personal Info------"
        data = {'success': 'true'}
    except Exception, e:
        print 'Exception :', e
        data = {'success': 'false'}
    return HttpResponse(json.dumps(data), content_type='application/json')


def get_product_list(request):
    try:
        print '==========check======================'
        #print 'request.session[user_id]', request.session['user_id']
        check_obj = UserProfile.objects.get(user_id=request.session['customer_id'])
        product_list = Customer_Product.objects.filter(user_id=check_obj.user_id)
        product_log_list = []
        i = 0
        for product in product_list:
            i = i + 1
            temp_obj = {
                'success': 'true',
                'sr_no': i,
                'product_name': product.product_id.product,
                'product_amount': product.amount
            }
            print "List", temp_obj
            product_log_list.append(temp_obj)
        data = {'data': product_log_list}
        #print data
    except Exception, e:
        print 'Exception at product list: ', e
        data = {'data': 'none'}
    return HttpResponse(json.dumps(data), content_type='application/json')


@csrf_exempt
def delete_product_data(request):
    try:
        cust_pro_obj = Customer_Product.objects.get(customer_product_id=request.POST.get('cust_pro_id'))
        cust_pro_obj.row_status = 'Inactive'
        cust_pro_obj.save()
        data = {'success': 'true'}
    except Exception, e:
        print e
        data = {'success': 'false'}
    return HttpResponse(json.dumps(data), content_type='application/json')


def setting_goals(request):
    ##    pdb.set_trace()
    if request.user.is_authenticated():
        check_obj = UserProfile.objects.get(user_id=request.session['customer_id'])
        product_list = Customer_Product.objects.filter(user_id=check_obj.user_id,row_status='Active')
        pension = 0
        for products in product_list:
            if products.product_id.product_id == 2:
                pension = pension + float(products.amount)
        var_category = ''
        goal_list = Goal.objects.filter(user_id=check_obj.user_id)

        for goal in goal_list:
            var_category = var_category + ',' + str(goal.goal_cat_id.goal_cat_id)
        #print var_category
        data = {'success': 'true', 'var_category': var_category, 'goal_cat': get_goal_category(request),
                'goal_target_year': get_goal_target_year(request), 'pension':pension}
        return render(request, 'setting_goal.html', data)
    else:
        form = CaptchaForm()
        return render_to_response('login.html', dict(
            form=form
        ), context_instance=RequestContext(request))


# TO GET THE GOAL CATEGORY
def get_goal_category(request):
    ##    pdb.set_trace()
    goal_list = []
    try:
        cat_list = Goal_Category.objects.all()
        for goal in cat_list:
            goal_list.append(
                {'goal_cat_id': goal.goal_cat_id, 'goal': goal.goal_cat})

    except Exception, e:
        print 'Exception ', e
    return goal_list


@csrf_exempt
def get_variable_data(request):
    # pdb.set_trace()
    try:
        variable_obj = Variable.objects.filter(variableType_id=4, row_status='Active')
        variable_list = []

        for var in variable_obj:
            variable_list.append(
                {'var_id': var.variable_id, 'variable': var.variable})

    except Exception, e:
        print 'Exception at variable delete: ', e
    return variable_list


# TO GET THE GOAL TARGET YEAR
def get_goal_target_year(request):
    ##    pdb.set_trace()
    target_year_list = []
    try:
        year_list = Goal_Target_Year.objects.all()
        for year in year_list:
            target_year_list.append(
                {'tar_year_id': year.goal_target_year_id, 'tar_year': year.goal_target_year})

    except Exception, e:
        print 'Exception ', e
    return target_year_list


@csrf_exempt
def save_goal(request):
    # pdb.set_trace()
    try:
        check_obj = UserProfile.objects.get(user_id=request.session['customer_id'])
        target_date = request.POST.get('txt_target_date')
        target_date = target_date.split('/')
        if request.method == "POST":
            goal_obj = Goal(
                user_id=check_obj,
                goal_cat_id=Goal_Category.objects.get(goal_cat_id=request.POST.get('goal_cat')),
                amount=request.POST.get('amount'),
                amount_allocated=request.POST.get('amount_allocated'),
                goal_name=request.POST.get('txt_name'),
                goal_target_year=target_date[2],
                goal_target_date=datetime.datetime.strptime(request.POST.get('txt_target_date'), '%d/%m/%Y').date(),
                row_status='Active',
                created_by=request.session['login_user'],
                updated_by=request.session['login_user'],
                created_date=datetime.datetime.now(),
                updated_date=datetime.datetime.now()
            )
            goal_obj.save()
            try:
                customer_obj = CustomerPersonalInfo.objects.get(user=check_obj)
                customer_obj.profile_updated = 'YES'
                customer_obj.report_description = ''
                customer_obj.save()
            except CustomerPersonalInfo.DoesNotExist:
                print "-------No Personal Info------"
            data = {'success': 'true'}
        else:
            data = {'success': 'false'}
    except Exception, e:
        print 'Exception :', e
        data = {'data': 'none'}
    return HttpResponse(json.dumps(data), content_type='application/json')


def get_goal_list(request):
    ##    pdb.set_trace()
    try:
        print '==========check======================'
        #print 'request.session[user_id]', request.session['user_id']
        check_obj = UserProfile.objects.get(user_id=request.session['customer_id'])
        goal_list = Goal.objects.filter(user_id=check_obj.user_id, row_status='Active')
        goal_log_list = []

        for goal in goal_list:
            if goal.goal_name == "":
                goalname = "--"
            else:
                goalname = goal.goal_name
            if not goal.amount_allocated:
                amount_allocated = 0
            else:
                amount_allocated = goal.amount_allocated
            if goal.goal_target_date:
                goal_date = goal.goal_target_date.strftime('%d/%m/%Y')
            else:
                goal_date = ''
            data = '"'+str(goal.goal_id) + '|$|' + str(goal.goal_name) + '|$|' + str(goal.amount) +  '|$|' + str(
                goal.goal_cat_id.goal_cat_id) + '|$|' + str(goal_date) + '|$|' + str(amount_allocated) + '"'
            edit_btn = '<a name=' + str(
                data) + ' onclick="edit_goal(this.name)" class="infont"> ' + '<i class="fa fa-edit"></i></i>  </a>'
            delete_btn = '<a onclick="delete_goal(' + str(
                goal.goal_id) + ')" class="infont"> ' + '<i class="fa fa-trash-o"></i></i>  </a>'
            temp_obj = {
                'success': 'true',
                'goal_category': goal.goal_cat_id.goal_cat,
                'goal_name': goalname,
                'goal_amount': goal.amount,
                'goal_amount_allocated': goal.amount_allocated,
                'goal_tr_year': goal_date,
                'edit_btn': edit_btn,
                'delete_btn': delete_btn
            }

            goal_log_list.append(temp_obj)
        data = {'data': goal_log_list}
        # print "FINAL_DATA", data
        # print data
    except Exception, e:
        print 'Exception at goal list: ', e
        data = {'data': 'none'}
    return HttpResponse(json.dumps(data), content_type='application/json')


@csrf_exempt
def delete_goal_data(request):
    try:
        goal_obj = Goal.objects.get(goal_id=request.POST.get('goal_id'))
        goal_obj.row_status = 'Inactive'
        goal_obj.save()
        data = {'success': 'true'}
        try:
            check_obj = UserProfile.objects.get(user_id=request.session['customer_id'])
            customer_obj = CustomerPersonalInfo.objects.get(user=check_obj)
            customer_obj.profile_updated = 'YES'
            customer_obj.report_description = ''
            customer_obj.save()
        except CustomerPersonalInfo.DoesNotExist:
            print "-------No Personal Info------"
    except Exception, e:
        print e
        data = {'success': 'false'}
    return HttpResponse(json.dumps(data), content_type='application/json')


@csrf_exempt
def edit_goal_data(request):
    # pdb.set_trace()
    try:
        print "------IN Update GOAL-----"
        target_date = request.POST.get('txt_target_date')
        target_date = target_date.split('/')
        if request.method == "POST":
            goal_obj = Goal.objects.get(goal_id=request.POST.get('goal_id'))
            goal_obj.goal_cat_id = Goal_Category.objects.get(goal_cat_id=request.POST.get('goal_cat'))
            goal_obj.amount = request.POST.get('amount')
            goal_obj.amount_allocated = request.POST.get('amount_allocated')
            goal_obj.goal_name = request.POST.get('txt_name')
            goal_obj.goal_target_year = target_date[2]
            goal_obj.goal_target_date = datetime.datetime.strptime(request.POST.get('txt_target_date'), '%d/%m/%Y').date()
            goal_obj.updated_by = request.session['login_user']
            goal_obj.updated_date = datetime.datetime.now()

            goal_obj.save()
            try:
                check_obj = UserProfile.objects.get(user_id=request.session['customer_id'])
                customer_obj = CustomerPersonalInfo.objects.get(user=check_obj)
                customer_obj.profile_updated = 'YES'
                customer_obj.report_description = ''
                customer_obj.save()
            except CustomerPersonalInfo.DoesNotExist:
                print "-------No Personal Info------"
            #meter_gauge_calculations(request)
            data = {'success': 'true'}
        else:
            data = {'success': 'false'}
    except Exception, e:
        print 'Exception :', e
        data = {'data': 'none'}
    return HttpResponse(json.dumps(data), content_type='application/json')


def open_bank_account(request):
    if request.user.is_authenticated():
        data = {'success': 'true', 'account_type': get_account_type(request), 'currency': get_currency(request)}
        return render(request, 'bank_account.html', data)
    else:
        form = CaptchaForm()
        return render_to_response('login.html', dict(
            form=form
        ), context_instance=RequestContext(request))


# TO GET THE ACCOUNT TYPE
def get_account_type(request):
    ##    pdb.set_trace()
    account_type_list = []
    try:
        acc_type_list = AccountType.objects.all()
        for account in acc_type_list:
            account_type_list.append(
                {'acc_type_id': account.account_id, 'acc_name': account.account_name})

    except Exception, e:
        print 'Exception ', e
    return account_type_list


# TO GET THE CURRENCY
def get_currency(request):
    ##    pdb.set_trace()
    currency_list = []
    try:
        curr_list = Currency.objects.all()
        for cur in curr_list:
            currency_list.append(
                {'curr_id': cur.currency_id, 'currency_type': cur.currency})

    except Exception, e:
        print 'Exception ', e
    return currency_list


@csrf_exempt
def save_bank(request):
    # pdb.set_trace()
    try:
        print "------IN SAVE BANK-----"
        check_obj = UserProfile.objects.get(user_id=request.session['customer_id'])

        if request.method == "POST":
            bank_obj = CustomerBankAccountDetails(
                user=check_obj,
                bank=request.POST.get('bank_add'),
                amount=request.POST.get('amount'),
                currency=Currency.objects.get(currency_id=request.POST.get('currency')),
                account_id=AccountType.objects.get(account_id=request.POST.get('account_type')),
                row_status='Active',
                created_by=request.session['login_user'],
                updated_by=request.session['login_user'],
                created_date=datetime.datetime.now(),
                updated_date=datetime.datetime.now()
            )
            bank_obj.save()
            try:
                #check_obj = UserProfile.objects.get(user_id=request.session['customer_id'])
                customer_obj = CustomerPersonalInfo.objects.get(user=check_obj)
                customer_obj.profile_updated = 'YES'
                customer_obj.report_description = ''
                customer_obj.save()
            except CustomerPersonalInfo.DoesNotExist:
                print "-------No Personal Info------"
            data = {'success': 'true'}
        else:
            data = {'success': 'false'}
    except Exception, e:
        print 'Exception :', e
        data = {'data': 'none'}
    return HttpResponse(json.dumps(data), content_type='application/json')


def save_bank01(request):
    # pdb.set_trace()
    try:
        print "------IN SAVE BANK-----"
        check_obj = UserProfile.objects.get(user_id=request.session['customer_id'])

        if request.method == "POST":
            bank = BankDetails.objects.get(bank_name=request.POST.get('bank_add'))
            #print '================>', bank
            bank_obj = CustomerBankAccountDetails(
                user=check_obj,
                bank=bank,
                amount=request.POST.get('amount'),
                currency=Currency.objects.get(currency_id=request.POST.get('currency')),
                account_id=AccountType.objects.get(account_id=request.POST.get('account_type')),
                row_status='Active',
                created_by=request.session['login_user'],
                updated_by=request.session['login_user'],
                created_date=datetime.datetime.datetime.now(),
                updated_date=datetime.datetime.datetime.now()
            )
            bank_obj.save()
            data = {'success': 'true'}
        else:
            data = {'success': 'false'}
    except BankDetails.DoesNotExist, e:
        print 'Exception :', e
        data = {'success': 'Bank Not Match'}
    except Exception, e:
        print 'Exception :', e
        data = {'data': 'none'}
    return HttpResponse(json.dumps(data), content_type='application/json')


def open_other_saving_product(request):
    if request.user.is_authenticated():
        return render(request, 'other_saving_product.html')
    else:
        form = CaptchaForm()
        return render_to_response('login.html', dict(
            form=form
        ), context_instance=RequestContext(request))


def open_direct_brokrage(request):
    if request.user.is_authenticated():
        return render(request, 'direct_brokrage.html')
    else:
        form = CaptchaForm()
        return render_to_response('login.html', dict(
            form=form
        ), context_instance=RequestContext(request))


def open_mutual_fund(request):
    if request.user.is_authenticated():
        return render(request, 'mutual_fund.html')
    else:
        form = CaptchaForm()
        return render_to_response('login.html', dict(
            form=form
        ), context_instance=RequestContext(request))


def open_pension_product(request):
    if request.user.is_authenticated():
        return render(request, 'pension_product.html')
    else:
        form = CaptchaForm()
        return render_to_response('login.html', dict(
            form=form
        ), context_instance=RequestContext(request))


def open_provident_fund(request):
    if request.user.is_authenticated():
        return render(request, 'provident_fund.html')
    else:
        form = CaptchaForm()
        return render_to_response('login.html', dict(
            form=form
        ), context_instance=RequestContext(request))


def open_property(request):
    if request.user.is_authenticated():
        return render(request, 'property.html')
    else:
        form = CaptchaForm()
        return render_to_response('login.html', dict(
            form=form
        ), context_instance=RequestContext(request))


def open_gold(request):
    if request.user.is_authenticated():
        return render(request, 'gold.html')
    else:
        form = CaptchaForm()
        return render_to_response('login.html', dict(
            form=form
        ), context_instance=RequestContext(request))


def open_implementation(request):
    if request.user.is_authenticated():
        return render(request, 'Implementation.html')
    else:
        form = CaptchaForm()
        return render_to_response('login.html', dict(
            form=form
        ), context_instance=RequestContext(request))


def open_roadmap(request):
    if request.user.is_authenticated():
        return render(request, 'roadmap.html')
    else:
        form = CaptchaForm()
        return render_to_response('login.html', dict(
            form=form
        ), context_instance=RequestContext(request))
