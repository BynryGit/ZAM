from datetime import datetime
import json
import pdb
from django.http import HttpResponse
from django.shortcuts import render, render_to_response
from django.template import RequestContext
from zamapp.models import Variable,VariableType,Full_Asset_Tool,Goal_Setting_Parameter,Goal_Parameter_Year
from customerapp.models import *
from zamapp.captcha_form import CaptchaForm
from django.views.decorators.csrf import csrf_exempt

__author__ = 'hduser'


def open_YFinAdvisor_index(request):
    if request.user.is_authenticated():
	print "-----OPEN PAGE----"
        type=VariableType.objects.filter(row_status='Active')
        data={'variableType':type,'account_type': get_account_type(request),'parameter_year':get_goal_parameter_year(request)}
        return render(request, 'yfinAdvisor_data.html',data)
    else:
        form = CaptchaForm()
        return render_to_response('login.html', dict(
            form=form
        ), context_instance=RequestContext(request))

def open_YFinAdvisor_customer(request):
    if request.user.is_authenticated():
        return render(request, 'yfin_customer.html')
    else:
        form = CaptchaForm()
        return render_to_response('login.html', dict(
            form=form
        ), context_instance=RequestContext(request))

@csrf_exempt
def save_variables(request):
    if request.user.is_authenticated():
        try:
            print '<===================save varialbes======================>'
            print
            variables_obj= Variable(
                variable =  request.POST.get('txt_variable'),
                variableType_id =  VariableType.objects.get(variableType_id=request.POST.get('selectVariableType')),
                percentage =  request.POST.get('txt_percentage'),
                created_by = request.session['login_user'],
                updated_by = request.session['login_user'],
                row_status='Active',
                updated_date= datetime.now(),
                created_date= datetime.now(),
            )
            variables_obj.save();
            data={'success':'true'}
        except Exception,e:
            print 'Exception ',e
            data={'success':'false'}
        return HttpResponse(json.dumps(data), content_type='application/json')
    else:
        form = CaptchaForm()
        return render_to_response('login.html', dict(
            form=form
        ), context_instance=RequestContext(request))


def get_variable_list(request):
    #pdb.set_trace()
    try:
        variable_obj = Variable.objects.filter(row_status='Active')
        variable_list = []
        i=0;
        for variable in variable_obj:
            delete = '<a onclick=delete_variable(' + str(variable.variable_id) + ')  class="infont delete"> ' + '<i class="fa fa-trash-o"></i></i>  </a>'
            edit = '<a onclick="edit_varialbe('+ str(variable.variable_id) +')" class="infont">' + '<i class="fa fa-edit"></i></i>  </a>'
            i=i+1;
            variable_obj = {
                'sr_no':i,
                'type': variable.variableType_id.variableType,
                'variable': variable.variable,
                'percentage': variable.percentage,
                'edit':edit,
                'delete':delete
            }
            variable_list.append(variable_obj)
        data = {'data': variable_list}
    except Exception, e:
        print 'Exception at variable delete: ', e
        data = {'data': 'none'}
    return HttpResponse(json.dumps(data), content_type='application/json')

@csrf_exempt
def delete_variable(request):
    #pdb.set_trace()
    try:
        variable_obj = Variable.objects.get(variable_id=request.POST.get('id'))
        customer_boj=CustomerVariable.objects.filter(variable=variable_obj)
        variable_obj.row_status='Inactive'
        variable_obj.save()
        if customer_boj:
            for cutomer in customer_boj:
                cutomer.row_status='Inactive'
                cutomer.save()
        data = {'success': 'true'}
    except Exception, e:
        print 'Exception at variable delete: ', e
        data = {'success': 'false'}
    return HttpResponse(json.dumps(data), content_type='application/json')


@csrf_exempt
def edit_variable(request):
    #pdb.set_trace()
    try:
        print '====================Edit Page=========>'
        variable_obj = Variable.objects.get(variable_id=request.POST.get('variable_id_edit'))
        variable_obj.variable =  request.POST.get('txt_variable_edit')
        variable_obj.percentage =  request.POST.get('txt_percentage_edit')
        variable_obj.updated_by = request.session['login_user']
        variable_obj.updated_date= datetime.datetime.now()
        variable_obj.save()
        data = {'success': 'true'}
    except Exception, e:
        print 'Exception at variable delete: ', e
        data = {'success': 'false'}
    return HttpResponse(json.dumps(data), content_type='application/json')



@csrf_exempt
def get_variable_data(request):
    #pdb.set_trace()
    try:
        variable_obj = Variable.objects.get(variable_id=request.POST.get('id'))
        id=variable_obj.variable_id
        variable=variable_obj.variable
        percentage=variable_obj.percentage
        data = {'success': 'true','id':id,'variable':variable,'percentage':percentage}
    except Exception, e:
        print 'Exception at variable delete: ', e
        data = {'success': 'false'}
    return HttpResponse(json.dumps(data), content_type='application/json')

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


@csrf_exempt
def save_full_asset_tool(request):
    if request.user.is_authenticated():
        try:
            print '<===================save full asset tool======================>'
            
            if (request.POST.get('product')=='Bank Account'):
            
                asset_obj= Full_Asset_Tool(
                    product =  request.POST.get('product'),
                    account_id =  AccountType(account_id=request.POST.get('account_type')),
                    product_name =  request.POST.get('pname'),
                    balance =  request.POST.get('balance'),
                    duration =  request.POST.get('duration'),
                    pretax_rate =  request.POST.get('pretax'),
                    posttax_return =  request.POST.get('posttax'),
                    liquidity =  request.POST.get('liquidity'),
                    created_by = request.session['login_user'],
                    updated_by = request.session['login_user'],
                    updated_date= datetime.now(),
                    created_date= datetime.now(),
                )
                asset_obj.save();
                data={'success':'true'}
            else:
                asset_obj= Full_Asset_Tool(
                    product =  request.POST.get('product'),
                    product_name =  request.POST.get('pname'),
                    balance =  request.POST.get('balance'),
                    duration =  request.POST.get('duration'),
                    pretax_rate =  request.POST.get('pretax'),
                    posttax_return =  request.POST.get('posttax'),
                    liquidity =  request.POST.get('liquidity'),
                    created_by = request.session['login_user'],
                    updated_by = request.session['login_user'],
                    updated_date= datetime.now(),
                    created_date= datetime.now(),
                )
                asset_obj.save();
                data={'success':'true'}
  
        except Exception,e:
            print 'Exception ',e
            data={'success':'false'}
        return HttpResponse(json.dumps(data), content_type='application/json')
    else:
        form = CaptchaForm()
        return render_to_response('login.html', dict(
            form=form
        ), context_instance=RequestContext(request))
        
        
def get_full_asset_tool_list(request):
    #pdb.set_trace()
    print "---------------IN ASSET TOOL-----------"
    try:

        asset_obj = Full_Asset_Tool.objects.filter(row_status='Active')
        print "ASSET OBJECT",asset_obj
        asset_list = []

        for asset in asset_obj:
            delete = '<a onclick=delete_product(' + str(asset.full_asset_id) + ')  class="infont delete"> ' + '<i class="fa fa-trash-o"></i></i>  </a>'
            if asset.product=="Bank Account":
                edit = '<a onclick="editbank('+ str(asset.full_asset_id) +')" class="infont">' + '<i class="fa fa-edit"></i></i>  </a>'
            else:    
                edit = '<a onclick="editproduct('+ str(asset.full_asset_id) +')" class="infont">' + '<i class="fa fa-edit"></i></i>  </a>'
            asset_obj = {
                'product':asset.product,
                'asset_name': asset.product_name,
                'balance': asset.balance,
                'duration': asset.duration,
                'pretax':asset.pretax_rate,
                'posttax':asset.posttax_return,
                'liquidity':asset.liquidity,
                'edit':edit,
                'delete':delete
            }
            asset_list.append(asset_obj)
        data = {'data': asset_list}
        print "ASSET DATA",asset_list
    except Exception, e:
        print 'Exception at variable delete: ', e
        data = {'data': 'none'}
    return HttpResponse(json.dumps(data), content_type='application/json')

@csrf_exempt
def view_full_asset_tool(request):
##    pdb.set_trace()
    try:
        print "---------View Asset Tool---------"
        full_asset_id = request.POST['id']
        asset_obj = Full_Asset_Tool.objects.get(full_asset_id=full_asset_id)
       
        full_asset_id=asset_obj.full_asset_id
        product=asset_obj.product
        asset_name= asset_obj.product_name
        balance=asset_obj.balance
        duration= asset_obj.duration
        pretax=asset_obj.pretax_rate
        posttax=asset_obj.posttax_return
        liquidity=asset_obj.liquidity
    
        data = {'success': 'true','product':product,'asset_name':asset_name,'balance':balance,'duration':duration,
        'pretax':pretax,'posttax':posttax,'liquidity':liquidity,'asset_id':full_asset_id
        }
        print "view",data
    except Exception, e:
        print 'Exception: ', e
        data = {'data': 'none'}
    return HttpResponse(json.dumps(data), content_type='application/json')

@csrf_exempt
def view_full_bank_asset_tool(request):
##    pdb.set_trace()
    try:
        print "---------View Bank Asset Tool---------"
        full_asset_id = request.POST['id']
        asset_obj = Full_Asset_Tool.objects.get(full_asset_id=full_asset_id)
       
        full_asset_id=asset_obj.full_asset_id
        account_type=asset_obj.account_id.account_id
        product=asset_obj.product
        asset_name= asset_obj.product_name
        balance=asset_obj.balance
        duration= asset_obj.duration
        pretax=asset_obj.pretax_rate
        posttax=asset_obj.posttax_return
        liquidity=asset_obj.liquidity
    
        data = {'success': 'true','product':product,'asset_name':asset_name,'balance':balance,'duration':duration,
        'pretax':pretax,'posttax':posttax,'liquidity':liquidity,'account_type':account_type,'bank_id':full_asset_id
        }
        print "view",data
    except Exception, e:
        print 'Exception: ', e
        data = {'data': 'none'}
    return HttpResponse(json.dumps(data), content_type='application/json')


@csrf_exempt
def update_full_asset_tool(request):
##    pdb.set_trace()
    try:
        print "---------Update Asset Tool---------"
        if (request.POST.get('product_name')=='Bank Account'):
            id=request.POST.get('bank_id')
            print "Bank Id",id
            asset_obj= Full_Asset_Tool.objects.get(full_asset_id=id)

            asset_obj.product =  request.POST.get('product_name')
            asset_obj.account_id =  AccountType(account_id=request.POST.get('account_type'))
            asset_obj.product_name =  request.POST.get('pname')
            asset_obj.balance =  request.POST.get('balance')
            asset_obj.duration =  request.POST.get('duration')
            asset_obj.pretax_rate =  request.POST.get('pretax')
            asset_obj.posttax_return =  request.POST.get('posttax')
            asset_obj.liquidity =  request.POST.get('liquidity')
            asset_obj.created_by = request.session['login_user']
            asset_obj.updated_by = request.session['login_user']
            asset_obj.updated_date= datetime.now()
            asset_obj.created_date= datetime.now()
                    
            asset_obj.save();
            data={'success':'true'}
        else:   
            id=request.POST.get('product_id')
            asset_obj= Full_Asset_Tool.objects.get(full_asset_id=id) 
            asset_obj.product_name =  request.POST.get('pname')
            asset_obj.balance =  request.POST.get('balance')
            asset_obj.duration =  request.POST.get('duration')
            asset_obj.pretax_rate =  request.POST.get('pretax')
            asset_obj.posttax_return =  request.POST.get('posttax')
            asset_obj.liquidity =  request.POST.get('liquidity')
            asset_obj.created_by = request.session['login_user']
            asset_obj.updated_by = request.session['login_user']
            asset_obj.updated_date= datetime.now()
            asset_obj.created_date= datetime.now()
                    
            asset_obj.save();
            data={'success':'true'}
        
        
    except Exception, e:
        print 'Exception: ', e
        data = {'data': 'none'}
    return HttpResponse(json.dumps(data), content_type='application/json')   

@csrf_exempt
def delete_product(request):
    #pdb.set_trace()
    try:
        full_asset_id = request.POST['id']
        asset_obj = Full_Asset_Tool.objects.get(full_asset_id=full_asset_id)
        asset_obj.row_status='Inactive'
        asset_obj.save()
        
        data = {'success': 'true'}
    except Exception, e:
        print 'Exception at variable delete: ', e
        data = {'success': 'false'}
    return HttpResponse(json.dumps(data), content_type='application/json')   




def get_goal_parameter_year(request):
    ##    pdb.set_trace()
    para_year_list = []
    try:
        year_list = Goal_Parameter_Year.objects.all()
        for year in year_list:
            para_year_list.append(
                {'par_year_id': year.goal_parameter_year_id, 'par_year': year.goal_parameter_year})

    except Exception, e:
        print 'Exception ', e
    return para_year_list

@csrf_exempt
def save_goal_parameter(request):
    if request.user.is_authenticated():
        try:
            print '<===================save goal parameter======================>'
            print
            goal_par_obj= Goal_Setting_Parameter(
                goal_setting_parameter =  request.POST.get('parameter'),
                goal_parameter_year_id =  Goal_Parameter_Year.objects.get(goal_parameter_year_id=request.POST.get('goal_pr_yr')),
                goal_setting_parameter_per =  request.POST.get('goal_per'),
                created_by = request.session['login_user'],
                updated_by = request.session['login_user'],
                updated_date= datetime.now(),
                created_date= datetime.now(),
            )
            goal_par_obj.save();
            data={'success':'true'}
            print "PARAMETER",data
        except Exception,e:
            print 'Exception ',e
            data={'success':'false'}
        return HttpResponse(json.dumps(data), content_type='application/json')
    else:
        form = CaptchaForm()
        return render_to_response('login.html', dict(
            form=form
        ), context_instance=RequestContext(request))


def get_goal_setting_parameter(request):
    #pdb.set_trace()
    print "---------------IN GOAL SETTING PARAMETER-----------"
    try:

        goal_setting_para_obj = Goal_Setting_Parameter.objects.all()
        goal_setting_para_list = []

        for para in goal_setting_para_obj:
            edit = '<a onclick="editgoalparameter('+ str(para.goal_setting_parameter_id) +')" class="infont">' + '<i class="fa fa-edit"></i></i>  </a>'
           
            goal_setting_para_obj = {
                'year':para.goal_parameter_year_id.goal_parameter_year,
                'parameter': para.goal_setting_parameter,
                'percentage': para.goal_setting_parameter_per,
                'edit': edit

            }
            goal_setting_para_list.append(goal_setting_para_obj)
        data = {'data': goal_setting_para_list}
    except Exception, e:
        print 'Exception at goal setting parameter: ', e
        data = {'data': 'none'}
    return HttpResponse(json.dumps(data), content_type='application/json')

@csrf_exempt
def view_goal_parameter(request):
##    pdb.set_trace()
    try:
        print "---------View Goal Parameter---------"
        goal_setting_parameter_id = request.POST['id']
        goal_par_obj = Goal_Setting_Parameter.objects.get(goal_setting_parameter_id=goal_setting_parameter_id)
       
        goal_setting_parameter_id=goal_par_obj.goal_setting_parameter_id
        goal_setting_parameter=goal_par_obj.goal_setting_parameter
        goal_parameter_year_id= goal_par_obj.goal_parameter_year_id.goal_parameter_year_id
        goal_setting_parameter_per=goal_par_obj.goal_setting_parameter_per
    
        data = {'success': 'true','goal_setting_parameter_per':goal_setting_parameter_per,'goal_parameter_year_id':goal_parameter_year_id,
        'goal_setting_parameter':goal_setting_parameter,'goal_setting_parameter_id':goal_setting_parameter_id
        }
        print "view",data
    except Exception, e:
        print 'Exception: ', e
        data = {'data': 'none'}
    return HttpResponse(json.dumps(data), content_type='application/json')


@csrf_exempt
def edit_goal_parameter(request):
##    pdb.set_trace()
    try:
        print '====================Edit Goal Parameter=========>'
        goal_par_obj = Goal_Setting_Parameter.objects.get(goal_setting_parameter_id=request.POST.get('goal_parameter_id'))
        goal_par_obj.goal_setting_parameter =  request.POST.get('parameter')
        goal_par_obj.goal_setting_parameter_per =  request.POST.get('goal_per')
        goal_par_obj.goal_parameter_year_id = Goal_Parameter_Year.objects.get(goal_parameter_year_id= request.POST.get('goal_pr_yr'))
        goal_par_obj.updated_by = request.session['login_user']
        goal_par_obj.updated_date= datetime.now()
        goal_par_obj.save()
        data = {'success': 'true'}
    except Exception, e:
        print 'Exception at variable delete: ', e
        data = {'success': 'false'}
    return HttpResponse(json.dumps(data), content_type='application/json')



