from django.db import transaction
from django.shortcuts import render
from django.shortcuts import render_to_response
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
import pdb
import json
import datetime
from ZAM.config import *
from zamapp.models import *
import datetime
import calendar
import time
from django.db.models import Q
from django.db.models import F


def open_analyst(request):
    tab_id = request.GET.get('tab_id')
    data = {'tab_id': tab_id, 'zam_contact_person_list': get_zam_contact_person(request),
            'com_types': get_atttype(request)}
    return render(request, 'research.html', data)


def add_focus_list(request):
    currency_obj = Currency.objects.all()
    data = {'success': 'true', 'country_list': get_country(request),'com_types': get_atttype(request), 'currency_obj':currency_obj}
    return render(request, 'add_focus_list.html', data)


def add_active_list(request):
    country_obj = SecurityCountry.objects.all()
    currency_obj = Currency.objects.all()
    data = {'country_obj': country_obj,'com_types': get_atttype(request), 'currency_obj':currency_obj}
    return render(request, 'add_active_list.html', data)


def add_portfolio_list(request):
    currency_obj = Currency.objects.all()
    data = {'success': 'true', 'country_list': get_country(request),'com_types': get_atttype(request), 'currency_obj':currency_obj}
    return render(request, 'add_portfolio_list.html', data)

def save_focuslist_attachments(attachment_list,focuslist_company_id):
    try:
        attachment_list = attachment_list.split(',')
        attachment_list = filter(None, attachment_list)
        print "save attachments"
        print attachment_list
        print focuslist_company_id
        for attached_id in attachment_list:
            attachment_obj = FocusListMiscleneousAttachment.objects.get(misleneous_attechment_id=attached_id)
            attachment_obj.focuslist_company_id = focuslist_company_id
            attachment_obj.save()

        data = {'success': 'true'}
    except Exception, e:
        print 'Exception ', e
    return HttpResponse(json.dumps(data), content_type='application/json')

@csrf_exempt
def save_focuslist_company(request):
    ##    pdb.set_trace()
    try:
        if request.method == "POST":
            focus_list_obj = Focus_List(
                company_name=request.POST.get('txt_company_name'),
                country_id=SecurityCountry.objects.get(country_id=request.POST.get('txt_country_name')),
                local_currency=Currency.objects.get(currency_id=request.POST.get('txt_currency_name')),
                bloomberg_ticker=request.POST.get('txt_bloomberg_ticker'),
                source=request.POST.get('txt_source'),
                mkt_cap=request.POST.get('txt_mkt_cap'),
                daily_turnover=request.POST.get('txt_daily_turnover'),
                target_price=check_float_val(request.POST.get('txt_vt_price')),
                cmp=request.POST.get('txt_cmp'),
                move_since_inseption=request.POST.get('txt_msi'),
                up_down_side=check_float_val(request.POST.get('txt_updn')),
                management_quality=request.POST.get('txt_mgmt'),
                created_by=request.session['login_user'],
                updated_by=request.session['login_user'],
                created_date=datetime.datetime.now(),
                updated_date=datetime.datetime.now()

            )
            focus_list_obj.save()
            focuslist_company_id=focus_list_obj.focuslist_company_id
            attachment_list = []
            attachment_list = request.POST.get('focus_attachment')
            print "attach", attachment_list
            save_focuslist_attachments(attachment_list,focus_list_obj)
            data = {'success': 'true','focuslist_company_id':focuslist_company_id}
        else:
            data = {'success': 'false'}
    except Exception, e:
        print 'Exception :', e
        data = {'data': 'none'}
    return HttpResponse(json.dumps(data), content_type='application/json')


def get_focus_list(request):
    ##    pdb.set_trace()
    try:
        print 'Focus List'
        focus_list = Focus_List.objects.filter(company_record_status='Active')

        focus_company_list = []
        for company in focus_list:
            ##            view = '<a href="/view-focuslist-company/?company_id=' + str(
            ##                company.focuslist_company_id) + '" class="infont"> ' + '<i class="fa fa-eye"></i></i>  </a>'
            edit = '<a href="/edit-focuslist-company/?company_id=' + str(
                company.focuslist_company_id) + '" class="infont"> ' + '<i class="fa fa-edit"></i></i>  </a>'

            comm = '<a id=' + str(
                company.focuslist_company_id) + ' onclick=opencommunication(' + str(
                company.focuslist_company_id) + ',"focus") class="infont"> ''<i class="fa fa-comment-o"></i></i></a>'

            delete = '<a ' + str(
                company.focuslist_company_id) + '" class="infont delete"> ' + '<i class="fa fa-trash-o"></i></i>  </a>'

            temp_obj = {
                'id': company.focuslist_company_id,
                'comp_name': company.company_name,
                'country': company.country_id.country_name,
                'bloomberg_tick': company.bloomberg_ticker,
                'source': company.source,
                'mkt_cap': company.mkt_cap,
                'tprice': company.target_price,
                'cmp_price': company.cmp,
                'up-down': company.up_down_side,
                'edit': edit,
                'comm': comm,
                'delete': delete

            }
            focus_company_list.append(temp_obj)

        data = {'data': focus_company_list}
        print data

    except Exception, e:
        print 'Exception : ', e
        data = {'data': 'none'}
    return HttpResponse(json.dumps(data), content_type='application/json')


def edit_focuslist_company(request):
    ##    pdb.set_trace()
    try:
        company_obj = Focus_List.objects.get(focuslist_company_id=request.GET.get('company_id'))
        communicate_list = []
        attch_paths =[]
        attch_files =[]
        attach_id=[]
        

        attch_obj = FocusListMiscleneousAttachment.objects.filter(focuslist_company_id = company_obj)
        for attch in attch_obj:
            attch_path = SERVER_URL + attch.attachment_path.url
            attch_file = str(attch.attachment_path)[32:]
            attahment_id=str(attch.misleneous_attechment_id)
            
            attch_paths.append(attch_path)
            attch_files.append(attch_file)
            attach_id.append(attahment_id)
            
        att=','.join(attach_id)
        print "Chek1",att 

        focus_dict = {
            'success': 'true',
            'id': company_obj.focuslist_company_id,
            'txt_company_name': company_obj.company_name,
            'txt_country_name': company_obj.country_id,
            'txt_currency_name': company_obj.local_currency,
            'txt_bloomberg_ticker': company_obj.bloomberg_ticker,
            'txt_source': company_obj.source,
            'txt_mkt_cap': company_obj.mkt_cap,
            'txt_daily_turnover': company_obj.daily_turnover,
            'txt_vt_price': company_obj.target_price or '',
            'txt_cmp': company_obj.cmp,
            'txt_msi': company_obj.move_since_inseption,
            'txt_updn': company_obj.up_down_side,
            'txt_mgmt': company_obj.management_quality,
            'attachment': attch_paths,
            'file_name':attch_files,
            'attachment_id':att
        }

        try:
            communication_list = FocusListResearchLog.objects.filter(focuslist_company_id=company_obj)

            for communication in communication_list:

                if communication.communicationtype_id == None:
                    comm_id = ""
                else:
                    comm_id = communication.communicationtype_id.communicationtype_name

                if communication.log_attachment == "":
                    att_path = ""
                else:
                    att_path = SERVER_URL + communication.log_attachment.url

                commn_list = {
                    'success': 'true',
                    'comm_id': communication.focus_researchlog_Id or '',
                    'comm_date': communication.log_date.strftime('%d/%m/%Y') or '',
                    'comm_type': comm_id,
                    'comm_zam_person': communication.communication_created_by or '',
                    'comm_att': att_path,
                    ##                    'comm_desc': abc + '...' or ''
                }
                communicate_list.append(commn_list)

        except FocusListResearchLog.DoesNotExist as err:
            print 'Log is not Exists'
            communication_list = {}
        currency_obj = Currency.objects.all()
        com_types = ResearchAttachmentTypes.objects.all()
        zam_contact_person_list = ZAMPerson.objects.all()
        data = {'focus': focus_dict, 'country_list': get_country(request), 'zam_contact_person_list':zam_contact_person_list, 'com_types':com_types, 'communication_list': communicate_list, 'currency_obj':currency_obj}

    except Exception, e:
        print 'Exception ', e
        data = {'success': 'false'}
    return render(request, 'focus_list_view.html', data)


@csrf_exempt
def update_focuslist_company(request):
    ##    pdb.set_trace()
    try:
        company_obj = Focus_List.objects.get(focuslist_company_id=request.POST.get('company_id'))
        company_obj.company_name = request.POST.get('txt_company_name')
        company_obj.country_id = SecurityCountry.objects.get(country_id=request.POST.get('txt_country_name'))
        company_obj.local_currency=Currency.objects.get(currency_id=request.POST.get('txt_currency_name'))
        company_obj.bloomberg_ticker = request.POST.get('txt_bloomberg_ticker')
        company_obj.source = request.POST.get('txt_source')
        company_obj.mkt_cap = request.POST.get('txt_mkt_cap')
        company_obj.daily_turnover = request.POST.get('txt_daily_turnover')
        company_obj.target_price = check_float_val(request.POST.get('txt_vt_price'))
        company_obj.cmp = request.POST.get('txt_cmp')
        company_obj.move_since_inseption=request.POST.get('txt_msi')
        company_obj.up_down_side = check_float_val(request.POST.get('txt_updn'))
        company_obj.management_quality = request.POST.get('txt_mgmt')

        company_obj.save()
        print company_obj.focuslist_company_id
        attachment_list = []
        attachment_list = request.POST.get('attachment1')
        print "attach", attachment_list
        save_focuslist_attachments(attachment_list,company_obj) 
        data = {'success': 'true'}
    except Exception, e:
        print 'Exception ', e
        data = {'success': 'false'}
    return HttpResponse(json.dumps(data), content_type='application/json')


def check_float_val(str):
    # pdb.set_trace()
    try:
        if str.strip() == "":
            str = None
    except Exception, e:
        print 'Exception', e
        str = None
    return str


@csrf_exempt
def change_company_status(request):
    ##    pdb.set_trace()
    try:
        stat = request.GET.get('company_id')
        print 'id--', stat
        stat_obj = Focus_List.objects.get(focuslist_company_id=stat)
        stat_obj.company_record_status = "Inactive"
        stat_obj.save()
        data = {'success': 'true'}
    except Exception, e:
        print 'Exception : ', e
        data = {'data': 'error_msg'}

    return HttpResponse(json.dumps(data), content_type='application/json')

def save_portfoliolist_attachments(attachment_list,portfolio_company_id):
    try:
        attachment_list = attachment_list.split(',')
        attachment_list = filter(None, attachment_list)
        print "save attachments"
        print attachment_list
        print portfolio_company_id
        for attached_id in attachment_list:
            attachment_obj = PortfolioMiscleneousAttachment.objects.get(misleneous_attechment_id=attached_id)
            attachment_obj.portfolio_company_id = portfolio_company_id
            attachment_obj.save()

        data = {'success': 'true'}
    except Exception, e:
        print 'Exception ', e
    return HttpResponse(json.dumps(data), content_type='application/json')

@csrf_exempt
def save_portfoliolist_company(request):
    ##    pdb.set_trace()
    try:

        portfolio_list_obj = Portfolio_List(
            company_name=request.POST.get('txt_company_name'),
            country_id=SecurityCountry.objects.get(country_id=request.POST.get('txt_country_name')),
            local_currency=Currency.objects.get(currency_id=request.POST.get('txt_currency_name')),
            bloomberg_ticker=request.POST.get('txt_bloomberg_ticker'),
            target_price=check_float_val(request.POST.get('txt_vt_price')),
            cmp=request.POST.get('txt_cmp'),
            move_since_inseption =request.POST.get('txt_msi'),
            up_down_side=check_float_val(request.POST.get('txt_updn')),
            created_by=request.session['login_user'],
            updated_by=request.session['login_user'],
            created_date=datetime.datetime.now(),
            updated_date=datetime.datetime.now()

        )
        portfolio_list_obj.save()
        portfolio_company_id=portfolio_list_obj.portfolio_company_id
        
        if request.POST['check_invst'] == "1":
            print request.FILES['invst_file']
            portfolio_list_obj.investment_note_file = request.FILES['invst_file']
            portfolio_list_obj.investment_note = datetime.datetime.now()
            portfolio_list_obj.save()

        if request.POST['check_model'] == "1":
            print request.FILES['model_file']
            portfolio_list_obj.model_file = request.FILES['model_file']
            portfolio_list_obj.model_updated_date = datetime.datetime.now()
            portfolio_list_obj.save()

        if request.POST['check_mnmt'] == "1":
            print request.FILES['mgmt_file']
            portfolio_list_obj.last_management_call_file = request.FILES['mgmt_file']
            portfolio_list_obj.last_management_call_date = datetime.datetime.now()
            portfolio_list_obj.save()
            
        print portfolio_list_obj.portfolio_company_id
        attachment_list = []
        attachment_list = request.POST.get('attachment')
        print "attach", attachment_list
        save_portfoliolist_attachments(attachment_list,portfolio_list_obj)      

        data = {'success': 'true','portfolio_company_id':portfolio_company_id}

    except Exception, e:
        print 'Exception :', e
        data = {'data': 'none'}
    return HttpResponse(json.dumps(data), content_type='application/json')


def get_portfolio_list(request):
    ##    pdb.set_trace()
    try:
        print 'PortFolio List'
        portfolio_list = Portfolio_List.objects.filter(company_record_status='Active')

        portfolio_company_list = []
        for company in portfolio_list:
            ##            view = '<a href="/view-focuslist-company/?company_id=' + str(
            ##                company.focuslist_company_id) + '" class="infont"> ' + '<i class="fa fa-eye"></i></i>  </a>'
            edit = '<a href="/edit-portfoliolist-company/?company_id=' + str(
                company.portfolio_company_id) + '" class="infont"> ' + '<i class="fa fa-edit"></i></i>  </a>'

            comm = '<a ' + str(
                company.portfolio_company_id) + ' onclick=opencommunication(' + str(
                company.portfolio_company_id) + ',"portfolio") class="infont"> ''<i class="fa fa-comment-o"></i></i></a>'

            delete = '<a ' + str(
                company.portfolio_company_id) + '" class="infont delete"> ' + '<i class="fa fa-trash-o"></i></i>  </a>'

            if company.investment_note_file == "":
                analyst_path = ""
            else:
                analyst_path = SERVER_URL + company.investment_note_file.url
                print 'company.investment_not',company.investment_note
                analyst_path = '<a href="' + analyst_path + '" download="'+company.investment_note_file.url[28:]+'" style="text-decoration: underline;color: #00004A;"> ' + str(
                    company.investment_note.strftime('%d/%m/%Y')) + ' </a>'
            
            
            if company.model_file == "":
                model_path = ""
            else:
                model_path = SERVER_URL + company.model_file.url
                model_path = '<a href="' + model_path + '" download="'+company.investment_note_file.url[28:]+ '" style="text-decoration: underline;color: #00004A;"> ' + str(
                    company.model_updated_date.strftime('%d/%m/%Y')) + ' </a>'

            temp_obj = {
                'id': company.portfolio_company_id,
                'comp_name': company.company_name,
                'country': company.country_id.country_name,
                'bloomberg_tick': company.bloomberg_ticker,
                'last_analyst_call': analyst_path,
                'model': model_path,
                'tprice': company.target_price,
                'cmp_price': company.cmp,
                'up-down': company.up_down_side,
                'edit': edit,
                'comm': comm,
                'delete': delete

            }
            portfolio_company_list.append(temp_obj)

        data = {'data': portfolio_company_list}

    except Exception, e:
        print 'Exception : ', e
        data = {'data': 'none'}
    return HttpResponse(json.dumps(data), content_type='application/json')


@csrf_exempt
def change_portfolio_company_status(request):
    ##    pdb.set_trace()
    try:
        stat = request.GET.get('pcompany_id')
        print 'id--', stat
        stat_obj = Portfolio_List.objects.get(portfolio_company_id=stat)
        stat_obj.company_record_status = "Inactive"
        stat_obj.save()
        data = {'success': 'true'}
    except Exception, e:
        print 'Exception : ', e
        data = {'data': 'error_msg'}

    return HttpResponse(json.dumps(data), content_type='application/json')


def edit_portfoliolist_company(request):
    ##    pdb.set_trace()
    try:
        attch_paths =[]
        attch_files =[]
        company_obj = Portfolio_List.objects.get(portfolio_company_id=request.GET.get('company_id'))
        communicate_list = []
        attach_id=[]

        if company_obj.model_file == "":
            model_path = ""
            manage_file = ""
        else:
            model_path = SERVER_URL + company_obj.model_file.url
            manage_file = "Download"

        if company_obj.last_management_call_file == "":
            last_management_path = ""
            modal_file = ""
        else:
            last_management_path = SERVER_URL + company_obj.last_management_call_file.url
            modal_file = "Download"

        if company_obj.investment_note_file == "":
            inst_path = ""
            inst_file = ""
        else:
            investment_path = SERVER_URL + company_obj.investment_note_file.url
            inst_file = "Download"
         
        attch_obj = PortfolioMiscleneousAttachment.objects.filter(portfolio_company_id = company_obj)
        for attch in attch_obj:
            attch_path = SERVER_URL + attch.attachment_path.url
            attch_file = str(attch.attachment_path)[32:]
            attahment_id=str(attch.misleneous_attechment_id)
            
            attch_paths.append(attch_path)
            attch_files.append(attch_file)
            attach_id.append(attahment_id)
            
        att=','.join(attach_id)
        print "Chek1",att    

        portfolio_dict = {
            'success': 'true',
            'id': company_obj.portfolio_company_id,
            'txt_company_name': company_obj.company_name,
            'txt_country_name': company_obj.country_id,
            'txt_currency_name': company_obj.local_currency,
            'txt_bloomberg_ticker': company_obj.bloomberg_ticker,
            'txt_vt_price': company_obj.target_price or '',
            'txt_cmp': company_obj.cmp,
            'txt_msi': company_obj.move_since_inseption,
            'txt_updn': company_obj.up_down_side or '',
            'model': model_path,
            'management': last_management_path,
            'investment': investment_path,
            'manage_file': manage_file,
            'modal_file': modal_file,
            'inst_file': inst_file,
            'attachment': attch_paths,
            'file_name':attch_files,
            'attachment_id':att
        }
        
        print "-------"
        print "PORTFOLIO_DICT",portfolio_dict

        try:
            communication_list = PortfolioListResearchLog.objects.filter(portfolio_company_id=company_obj)

            for communication in communication_list:

                if communication.communicationtype_id == None:
                    comm_id = ""
                else:
                    comm_id = communication.communicationtype_id.communicationtype_name

                if communication.log_attachment == "":
                    att_path = ""
                else:
                    att_path = SERVER_URL + communication.log_attachment.url

                commn_list = {
                    'success': 'true',
                    'comm_id': communication.portfolio_researchlog_Id or '',
                    'comm_date': communication.log_date.strftime('%d/%m/%Y') or '',
                    'comm_type': comm_id,
                    'comm_zam_person': communication.zam_person_id or '',
                    'comm_att': att_path,
                    ##                    'comm_desc': abc + '...' or ''
                }
                communicate_list.append(commn_list)

        except PortfolioListResearchLog.DoesNotExist as err:
            print 'Log is not Exists'
            communication_list = {}
        com_types = ResearchAttachmentTypes.objects.all()
        zam_contact_person_list = ZAMPerson.objects.all()
        currency_obj = Currency.objects.all()
        #currency_obj = Currency.objects.all()
        data = {'portfolio': portfolio_dict, 'country_list': get_country(request), 'zam_contact_person_list':zam_contact_person_list,
                'communication_list': communicate_list, 'currency_obj':currency_obj, 'com_types':com_types}

    except Exception, e:
        print 'Exception ', e
        data = {'success': 'false'}
    return render(request, 'portfolio_list_view.html', data)


@csrf_exempt
def update_portfoliolist_company(request):
    ##    pdb.set_trace()
    try:
        company_obj = Portfolio_List.objects.get(portfolio_company_id=request.POST.get('pcompany_id'))
        company_obj.company_name = request.POST.get('txt_company_name')
        company_obj.country_id = SecurityCountry.objects.get(country_id=request.POST.get('txt_country_name'))
        company_obj.local_currency=Currency.objects.get(currency_id=request.POST.get('txt_currency_name'))
        company_obj.bloomberg_ticker = request.POST.get('txt_bloomberg_ticker')
        company_obj.target_price = check_float_val(request.POST.get('txt_vt_price'))
        company_obj.cmp = request.POST.get('txt_cmp')
        company_obj.move_since_inseption = request.POST.get('txt_msi')
        company_obj.up_down_side = check_float_val(request.POST.get('txt_updn'))
        company_obj.save()

        if request.POST['check_invst'] == "1":
            print request.FILES['invst_file']
            company_obj.investment_note_file = request.FILES['invst_file']
            company_obj.investment_note = datetime.datetime.now()
            company_obj.save()

        if request.POST['check_model'] == "1":
            print request.FILES['model_file']
            company_obj.model_file = request.FILES['model_file']
            company_obj.model_updated_date = datetime.datetime.now()
            company_obj.save()

        if request.POST['check_mnmt'] == "1":
            print request.FILES['mgmt_file']
            company_obj.last_management_call_file = request.FILES['mgmt_file']
            company_obj.last_management_call_date = datetime.datetime.now()
            company_obj.save()
            
        print company_obj.portfolio_company_id
        attachment_list = []
        attachment_list = request.POST.get('attachment1')
        print "attach", attachment_list
        save_portfoliolist_attachments(attachment_list,company_obj)     

        data = {'success': 'true'}
    except Exception, e:
        print 'Exception ', e
        data = {'success': 'false'}
    return HttpResponse(json.dumps(data), content_type='application/json')


# TO GET THE COUNTRY
def get_country(request):
    ##    pdb.set_trace()
    country_list = []
    try:
        countries = SecurityCountry.objects.filter(row_status="Active")
        for cntry in countries:
            country_list.append({'country_id': cntry.country_id, 'country_name': cntry.country_name})

    except Exception, e:
        print 'Exception ', e
    return country_list

@csrf_exempt
def get_price_msi(request):
    try:
        sec_name = request.POST['sec_name']
        bloomberg_ticker = request.POST['bloomberg_ticker']
        sec_obj = Security_Details.objects.filter(security_name = sec_name,security_bloomer_ticker = bloomberg_ticker,record_status="Active").order_by(
            '-security_created_date')
        sec_obj = sec_obj.first()
        print sec_obj
        price_obj = Security_Price_Details.objects.filter(security_id= sec_obj,record_status="Active").order_by(
            '-security_price_created_date')
        price_obj = price_obj.first()
        price = price_obj.security_in_price
        fx_rate = price_obj.security_fx_rate_in
        data = {'success': 'true', 'price':price, 'fx_rate':fx_rate}
    except Exception, e:
        print 'Exception ', e
        data = {'success': 'false'}
    return HttpResponse(json.dumps(data), content_type='application/json')


def save_activelist_attachments(attachment_list,activelist_company_id):
    try:
        attachment_list = attachment_list.split(',')
        attachment_list = filter(None, attachment_list)
        print "save attachments"
        print attachment_list
        print activelist_company_id
        for attached_id in attachment_list:
            attachment_obj = ActiveListMiscleneousAttachment.objects.get(misleneous_attechment_id=attached_id)
            attachment_obj.activelist_company_id = activelist_company_id
            attachment_obj.save()

        data = {'success': 'true'}
    except Exception, e:
        print 'Exception ', e
    return HttpResponse(json.dumps(data), content_type='application/json')


@csrf_exempt
def save_activelist_company(request):
    ##    pdb.set_trace()
    try:
        country_obj = SecurityCountry.objects.get(country_id=request.POST['txt_country_name'])
        currency_obj = Currency.objects.get(currency_id=request.POST['txt_currency_name'])
        print country_obj
        active_list_obj = Active_List(
            company_name=request.POST['txt_company_name'],
            country_id=country_obj,
            local_currency=currency_obj,
            bloomberg_ticker=request.POST['txt_bloomberg_ticker'],
            congruence=request.POST['drp_congruence'],
            industry_analysis=request.POST['drp_indusrty'],
            target_price=request.POST['txt_vt_price'],
            cmp=request.POST['txt_cmp'],
            move_since_inseption = request.POST['txt_msi'],
            up_down_side=request.POST['txt_updn'],
            created_by=request.session['login_user'],
            updated_by=request.session['login_user'],
            created_date=datetime.datetime.now(),
            updated_date=datetime.datetime.now(),
            row_status="Active"
        )
        active_list_obj.save()
        activelist_company_id= active_list_obj.activelist_company_id

        if request.POST['check_invst'] == "1":
            print request.FILES['invst_file']
            active_list_obj.investment_note_file = request.FILES['invst_file']
            active_list_obj.investment_note = datetime.datetime.now()
            active_list_obj.save()

        if request.POST['check_model'] == "1":
            print request.FILES['model_file']
            active_list_obj.model_file = request.FILES['model_file']
            active_list_obj.model_updated_date = datetime.datetime.now()
            active_list_obj.save()

        if request.POST['check_ana'] == "1":
            print request.FILES['analyst_file']
            active_list_obj.analyst_interview_file = request.FILES['analyst_file']
            active_list_obj.analyst_interview_date = datetime.datetime.now()
            active_list_obj.save()
          
        print active_list_obj.activelist_company_id
        attachment_list = []
        print"List",request.POST.get('attachment')
        attachment_list = request.POST.get('attachment')
        print "attach", attachment_list
        save_activelist_attachments(attachment_list,active_list_obj)  



        data = {'success': 'true','activelist_company_id':activelist_company_id}
    except Exception, e:
        print 'Exception :', e
        data = {'data': 'none'}
    return HttpResponse(json.dumps(data), content_type='application/json')


def view_activelist_company(request):
##    pdb.set_trace()
    try:
        active_list_obj = Active_List.objects.filter(row_status="Active")
        act_list = []
        for active_list in active_list_obj:
            edit_btn = '<td class="text-center"><a href="/edit-activelist-company/?activelist_id=' + str(
                active_list.activelist_company_id) + '"  class="infont"> <i class="fa fa-edit"></i></i></a></td>'

            comm = '<a ' + str(
                active_list.activelist_company_id) + ' onclick=opencommunication(' + str(
                active_list.activelist_company_id) + ',"active") class="infont"> ''<i class="fa fa-comment-o"></i></i></a>'

            delete_btn = '<td class="text-center"><a id="' + str(
                active_list.activelist_company_id) + '" onclick="delete_active(this.id)" class="infont"> <i class="fa fa-trash-o"></i></i></a></td>'

            
            if active_list.investment_note_file == "":
                analyst_path = ""
            else:
                analyst_path = SERVER_URL + active_list.investment_note_file.url
                analyst_path = '<a href="' + analyst_path + '" download="'+active_list.investment_note_file.url + '" style="text-decoration: underline;color: #00004A;"> ' + str(
                    active_list.investment_note.strftime('%d/%m/%Y')) + ' </a>'
            if active_list.model_file == "":
                model_path = ""
            else:
                model_path = SERVER_URL + active_list.model_file.url
                model_path = '<a href="' + model_path + '" download="'+active_list.model_file.url + '" style="text-decoration: underline;color: #00004A;"> ' + str(
                    active_list.model_updated_date.strftime('%d/%m/%Y')) + ' </a>'
                    
                    

            active_data = {
                'company': active_list.company_name,
                'country': active_list.country_id.country_name,
                'b_ticker': active_list.bloomberg_ticker,
                'model': model_path,
                'ana_intr': analyst_path,
                'val': active_list.target_price,
                'cmp': active_list.cmp,
                'upside': active_list.up_down_side,
                'edit_btn': edit_btn,
                'comm': comm,
                'delete_btn': delete_btn,
                
            }
            act_list.append(active_data)

        data = {'data': act_list}
        print "Final Data",data
    except Exception, e:
        print e
        data = {'data': ""}
    return HttpResponse(json.dumps(data), content_type='application/json')


def edit_activelist_company(request):
##    pdb.set_trace()
    try:
        communicate_list = []
        attch_paths =[]
        attch_files =[]
        attach_id=[]
        activelist_id = request.GET.get('activelist_id')
        print activelist_id
        activelist_obj = Active_List.objects.get(activelist_company_id=activelist_id)

        if activelist_obj.management_interview_file == "":
            mng_path = ""
            manage_file = ""
        else:
            mng_path = SERVER_URL + activelist_obj.management_interview_file.url
            manage_file = "Download"

        if activelist_obj.analyst_interview_file == "":
            analyst_path = ""
            ana_file = ""
        else:
            analyst_path = SERVER_URL + activelist_obj.analyst_interview_file.url
            ana_file = "Download"

        if activelist_obj.model_file == "":
            model_path = ""
            modal_file = ""
        else:
            model_path = SERVER_URL + activelist_obj.model_file.url
            modal_file = "Download"

        if activelist_obj.investment_note_file == "":
            inst_path = ""
            inst_file = ""
        else:
            inst_path = SERVER_URL + activelist_obj.investment_note_file.url
            inst_file = "Download"

        print model_path

        attch_obj = ActiveListMiscleneousAttachment.objects.filter(activelist_company_id = activelist_obj)
        for attch in attch_obj:
            attch_path = SERVER_URL + attch.attachment_path.url
            attch_file = str(attch.attachment_path)[32:]
            attahment_id=str(attch.misleneous_attechment_id)
            
            attch_paths.append(attch_path)
            attch_files.append(attch_file)
            attach_id.append(attahment_id)
            
        att=','.join(attach_id)
        print "Chek1",att 
        active_data = {
            'active_id': activelist_obj.activelist_company_id,
            'company_name': activelist_obj.company_name,
            'country': activelist_obj.country_id.country_id,
            'currency': activelist_obj.local_currency.currency_id,
            'b_ticker': activelist_obj.bloomberg_ticker,
            'congruence': activelist_obj.congruence,
            'ind_ana': activelist_obj.industry_analysis,
            'val': activelist_obj.target_price,
            'cmp': activelist_obj.cmp,
            'msi': activelist_obj.move_since_inseption,
            'updn': activelist_obj.up_down_side,
            'manage_path': mng_path,
            'manage_file': manage_file,
            'ana_path': analyst_path,
            'ana_file': ana_file,
            'model_path': model_path,
            'modal_file': modal_file,
            'inst_path': inst_path,
            'inst_file': inst_file,
            'attachment1': attch_paths,
            'file_name1':attch_files,
            'attachment_id':att
        }
        
        print "--------"
        print "Path",active_data

        country_obj = SecurityCountry.objects.all()

        try:
            communication_list = ActiveListResearchLog.objects.filter(activelist_company_id=activelist_obj)

            for communication in communication_list:

                if communication.communicationtype_id == None:
                    comm_id = ""
                else:
                    comm_id = communication.communicationtype_id.communicationtype_name

                commn_list = {
                    'success': 'true',
                    'comm_id': communication.active_researchlog_Id or '',
                    'comm_date': communication.log_date.strftime('%d/%m/%Y') or '',
                    'comm_type': comm_id,
                    'comm_zam_person': communication.zam_person_id or '',
                    ##                    'comm_desc': abc + '...' or ''
                }
                communicate_list.append(commn_list)

        except PortfolioListResearchLog.DoesNotExist as err:
            print 'Log is not Exists'
            communication_list = {}

        com_types = ResearchAttachmentTypes.objects.all()
        zam_contact_person_list = ZAMPerson.objects.all()
        currency_obj = Currency.objects.all()
        data = {'active_data': active_data, 'country_obj': country_obj, 'communication_list': communicate_list, 'com_types':com_types, 'zam_contact_person_list':zam_contact_person_list, 'currency_obj':currency_obj}
        
    except Exception, e:
        print 'Exception', e
        data = {'success': 'false'}
    return render(request, 'edit_active_list.html', data)

@csrf_exempt
def get_focus_researchlog(request):
    try:
        active_log_id = request.POST['active_log_id']
        log_obj = FocusListResearchLog.objects.get(focus_researchlog_Id = active_log_id)
        if log_obj.communicationtype_id==None:
            comm_type = ""
        else:
            comm_type = log_obj.communicationtype_id.communicationtype_id
        comm_date = log_obj.log_date.strftime('%d/%m/%Y')
        comm_typename=log_obj.communicationtype_id.communicationtype_name
        comm_type = comm_type
        comm_person = log_obj.communication_created_by
        company_personel=log_obj.company_personel or ''
        designation=log_obj.designation or ''
        bank_name=log_obj.bank_name or ''
        analyst_name=log_obj.analyst_name or ''
        comm_desc = log_obj.log_desc
        comm_desc = "\n"+comm_desc
        data = {'success': 'true','comm_typename':comm_typename, 'comm_date':comm_date,'company_personel':company_personel,'designation':designation,'bank_name':bank_name,'analyst_name':analyst_name, 'comm_type':comm_type, 'comm_desc':comm_desc, 'comm_person':comm_person}
        print "data",data
    except Exception, e:
        print 'Exception ', e
        data = {'success': 'false'}
    return HttpResponse(json.dumps(data), content_type='application/json')

@csrf_exempt
def get_active_researchlog(request):
    try:
        active_log_id = request.POST['active_log_id']
        log_obj = ActiveListResearchLog.objects.get(active_researchlog_Id = active_log_id)
        if log_obj.communicationtype_id==None:
            comm_type = ""
        else:
            comm_type = log_obj.communicationtype_id.communicationtype_id
        comm_date = log_obj.log_date.strftime('%d/%m/%Y')
        comm_typename=log_obj.communicationtype_id.communicationtype_name
        comm_type = comm_type
        comm_person = log_obj.communication_created_by
        company_personel=log_obj.company_personel or ''
        designation=log_obj.designation or ''
        bank_name=log_obj.bank_name or ''
        analyst_name=log_obj.analyst_name or ''
        comm_desc = log_obj.log_desc
        comm_desc = "\n"+comm_desc
        data = {'success': 'true','comm_typename':comm_typename,'comm_date':comm_date,'company_personel':company_personel,'designation':designation,'bank_name':bank_name,'analyst_name':analyst_name, 'comm_type':comm_type, 'comm_desc':comm_desc, 'comm_person':comm_person}
    except Exception, e:
        print 'Exception ', e
        data = {'success': 'false'}
    return HttpResponse(json.dumps(data), content_type='application/json')

@csrf_exempt
def get_port_researchlog(request):
    try:
        active_log_id = request.POST['active_log_id']
        print active_log_id
        log_obj = PortfolioListResearchLog.objects.get(portfolio_researchlog_Id= active_log_id)
        if log_obj.communicationtype_id==None:
            comm_type = ""
        else:
            comm_type = log_obj.communicationtype_id.communicationtype_id
        comm_date = log_obj.log_date.strftime('%d/%m/%Y')
        comm_typename=log_obj.communicationtype_id.communicationtype_name
        comm_type = comm_type
        comm_person = log_obj.communication_created_by
        company_personel=log_obj.company_personel or ''
        designation=log_obj.designation or ''
        bank_name=log_obj.bank_name or ''
        analyst_name=log_obj.analyst_name or ''
        comm_desc = log_obj.log_desc
        comm_desc = "\n"+comm_desc
        data = {'success': 'true','comm_typename':comm_typename, 'comm_date':comm_date,'company_personel':company_personel,'designation':designation,'bank_name':bank_name,'analyst_name':analyst_name, 'comm_type':comm_type, 'comm_desc':comm_desc, 'comm_person':comm_person}
    except Exception, e:
        print 'Exception ', e
        data = {'success': 'false'}
    return HttpResponse(json.dumps(data), content_type='application/json')

@csrf_exempt
def update_active_researchlog(request):
    try:
        active_log_id = request.POST.get('company_id')
        date = request.POST.get('desc_date')
        log_obj = ActiveListResearchLog.objects.get(active_researchlog_Id = active_log_id)

        old_desc = log_obj.log_desc
        old_desc = old_desc.replace("\n","")
        comm_descs = request.POST.get('cdesc')
        comm_desc = comm_descs.replace("\n","")
        if old_desc == comm_desc:
            desc = old_desc
        else:
            full_name = request.user.first_name + " " + request.user.last_name
            desc = "On " + date + ", " + full_name + " wrote:" + "\n\t" + comm_descs

        log_obj.log_desc = desc
##        log_obj.zam_person_id=ZAMPerson.objects.get(zam_person_id=request.POST.get('zam_person'))
        log_obj.company_personel=request.POST.get('company_personnel')
        log_obj.designation=request.POST.get('designation')
        log_obj.bank_name=request.POST.get('bank')
        log_obj.analyst_name=request.POST.get('analyst')
        log_obj.log_date=datetime.datetime.strptime(request.POST.get('cdate'), '%d/%m/%Y').date()
        log_obj.communication_updated_by=request.session['login_user']
        log_obj.communication_updated_date=datetime.datetime.now()
        log_obj.save()

        if request.POST.get('select_contact_type') != 'null':
            log_obj.communicationtype_id = ResearchAttachmentTypes.objects.get(
                communicationtype_id=request.POST.get('select_contact_type'))
            log_obj.save()
            attachment_list = request.POST.get('attachment')
            print "attach", attachment_list
            save_active_attachments(attachment_list, log_obj)

        data = {'success': 'true'}#, 'comm_date':comm_date, 'comm_type':comm_type, 'comm_desc':comm_desc, 'comm_person':comm_person}
    except Exception, e:
        print 'Exception ', e
        data = {'success': 'false'}
    return HttpResponse(json.dumps(data), content_type='application/json')

@csrf_exempt
def update_port_researchlog(request):
    try:
        active_log_id = request.POST.get('company_id')
        date = request.POST.get('desc_date')
        log_obj = PortfolioListResearchLog.objects.get(portfolio_researchlog_Id = active_log_id)

        old_desc = log_obj.log_desc
        old_desc = old_desc.replace("\n","")
        comm_descs = request.POST.get('cdesc')
        comm_desc = comm_descs.replace("\n","")
        if old_desc == comm_desc:
            desc = old_desc
        else:
            full_name = request.user.first_name + " " + request.user.last_name
            desc = "On " + date + ", " + full_name + " wrote:" + "\n\t" + comm_descs

        log_obj.log_desc = desc
##        log_obj.zam_person_id=ZAMPerson.objects.get(zam_person_id=request.POST.get('zam_person'))
        log_obj.company_personel=request.POST.get('company_personnel')
        log_obj.designation=request.POST.get('designation')
        log_obj.bank_name=request.POST.get('bank')
        log_obj.analyst_name=request.POST.get('analyst')
        log_obj.log_date=datetime.datetime.strptime(request.POST.get('cdate'), '%d/%m/%Y').date()
        log_obj.communication_updated_by=request.session['login_user']
        log_obj.communication_updated_date=datetime.datetime.now()
        log_obj.save()

        if request.POST.get('select_contact_type') != 'null':
            log_obj.communicationtype_id = ResearchAttachmentTypes.objects.get(
                communicationtype_id=request.POST.get('select_contact_type'))
            log_obj.save()
            attachment_list = request.POST.get('attachment')
            print "attach", attachment_list
            save_port_attachments(attachment_list, log_obj)

        data = {'success': 'true'}#, 'comm_date':comm_date, 'comm_type':comm_type, 'comm_desc':comm_desc, 'comm_person':comm_person}
    except Exception, e:
        print 'Exception ', e
        data = {'success': 'false'}
    return HttpResponse(json.dumps(data), content_type='application/json')

@csrf_exempt
def update_focus_researchlog(request):
    try:
        active_log_id = request.POST.get('company_id')
        date = request.POST.get('desc_date')
        log_obj = FocusListResearchLog.objects.get(focus_researchlog_Id = active_log_id)

        old_desc = log_obj.log_desc
        old_desc = old_desc.replace("\n","")
        comm_descs = request.POST.get('cdesc')
        comm_desc = comm_descs.replace("\n","")
        if old_desc == comm_desc:
            desc = old_desc
        else:
            full_name = request.user.first_name + " " + request.user.last_name
            desc = "On " + date + ", " + full_name + " wrote:" + "\n\t" + comm_descs

        log_obj.log_desc = desc
##        log_obj.zam_person_id=ZAMPerson.objects.get(zam_person_id=request.POST.get('zam_person'))
        log_obj.company_personel=request.POST.get('company_personnel')
        log_obj.designation=request.POST.get('designation')
        log_obj.bank_name=request.POST.get('bank')
        log_obj.analyst_name=request.POST.get('analyst')
        log_obj.log_date=datetime.datetime.strptime(request.POST.get('cdate'), '%d/%m/%Y').date()
        log_obj.communication_updated_by=request.session['login_user']
        log_obj.communication_updated_date=datetime.datetime.now()
        log_obj.save()

        if request.POST.get('select_contact_type') != 'null':
            log_obj.communicationtype_id = ResearchAttachmentTypes.objects.get(
                communicationtype_id=request.POST.get('select_contact_type'))
            log_obj.save()
            attachment_list = request.POST.get('attachment')
            print "attach", attachment_list
            save_focus_attachments(attachment_list, log_obj)

        data = {'success': 'true'}#, 'comm_date':comm_date, 'comm_type':comm_type, 'comm_desc':comm_desc, 'comm_person':comm_person}
    except Exception, e:
        print 'Exception ', e
        data = {'success': 'false'}
    return HttpResponse(json.dumps(data), content_type='application/json')

@csrf_exempt
def update_activelist_company(request):
##    pdb.set_trace()
    try:
        # print request.POST['active_id']
        country_obj = SecurityCountry.objects.get(country_id=request.POST['txt_country_name'])
        active_list_obj = Active_List.objects.get(activelist_company_id=request.POST['active_id'])
        active_list_obj.company_name = request.POST['txt_company_name']
        active_list_obj.country_id = country_obj
        active_list_obj.bloomberg_ticker = request.POST['txt_bloomberg_ticker']
        active_list_obj.congruence = request.POST['drp_congruence']
        active_list_obj.industry_analysis = request.POST['drp_indusrty']
        active_list_obj.target_price = request.POST['txt_vt_price']
        active_list_obj.cmp = request.POST['txt_cmp']
        active_list_obj.up_down_side = request.POST['txt_updn']
        active_list_obj.updated_by = request.session['login_user']
        active_list_obj.updated_date = datetime.datetime.now()

        active_list_obj.save()

        if request.POST['check_invst'] == "1":
            print request.FILES['invst_file']
            active_list_obj.investment_note_file = request.FILES['invst_file']
            active_list_obj.investment_note = datetime.datetime.now()
            active_list_obj.save()

        if request.POST['check_model'] == "1":
            print request.FILES['model_file']
            active_list_obj.model_file = request.FILES['model_file']
            active_list_obj.model_updated_date = datetime.datetime.now()
            active_list_obj.save()

        if request.POST['check_ana'] == "1":
            print request.FILES['analyst_file']
            active_list_obj.analyst_interview_file = request.FILES['analyst_file']
            active_list_obj.analyst_interview_date = datetime.datetime.now()
            active_list_obj.save()

##        if request.POST['check_mnmt'] == "1":
##            print request.FILES['mgmt_file']
##            active_list_obj.management_interview_file = request.FILES['mgmt_file']
##            active_list_obj.management_interview_date = datetime.datetime.now()
##            active_list_obj.save()
            
        print active_list_obj.activelist_company_id
        attachment_list = []
        attachment_list = request.POST.get('attachment1')
        print "attach", request.POST.get('attachment1')
        save_activelist_attachments(attachment_list,active_list_obj)  

        data = {'success': 'true'}
    except Exception, e:
        print 'Exception :', e
        data = {'data': 'none'}
    return HttpResponse(json.dumps(data), content_type='application/json')


def delete_activelist_company(request):
    try:
        activelist_id = request.GET.get('activelist_id')
        print activelist_id
        activelist_obj = Active_List.objects.get(activelist_company_id=activelist_id)
        activelist_obj.row_status = "Inactive"
        activelist_obj.save()
        data = {'success': 'true'}
    except Exception, e:
        print 'Exception :', e
        data = {'data': 'none'}
    return HttpResponse(json.dumps(data), content_type='application/json')


# GET ZAM Contact Person List
def get_zam_contact_person(request):
    zam_contact_person_list = []
    try:
        zam_communication_person = ZAMPerson.objects.filter(row_status="Active")
        for contact in zam_communication_person:
            zam_contact_person_list.append(
                {'zam_contact_person': contact.zam_person_id, 'zam_person_name': contact.zam_person_name})

    except Exception, e:
        print 'Exception ', e
    return zam_contact_person_list


# TO GET THE COMMUNICATION TYPE
def get_atttype(request):
    ##    pdb.set_trace()
    commtype_list = []
    try:
        comtypes = ResearchAttachmentTypes.objects.filter(record_status="Active")
        for comtype in comtypes:
            commtype_list.append(
                {'com_type_id': comtype.communicationtype_id, 'com_type_name': comtype.communicationtype_name})

    except Exception, e:
        print 'Exception ', e
    return commtype_list

def save_focus_attachments(attachment_list, communication_Id):
    try:
        attachment_list = attachment_list.split(',')
        attachment_list = filter(None, attachment_list)
        print "save attachments"
        print attachment_list
        print communication_Id
        for attached_id in attachment_list:
            attachment_obj = FocusListAttechment.objects.get(attechment_id=attached_id)
            attachment_obj.focus_researchlog_Id = communication_Id
            attachment_obj.save()

        data = {'success': 'true'}
    except Exception, e:
        print 'Exception ', e
    return HttpResponse(json.dumps(data), content_type='application/json')

@csrf_exempt
# To Save The Communication   
def add_log_focus_list(request):
##    pdb.set_trace()
    print request.POST
    full_name = request.user.first_name + " " + request.user.last_name
    desc = "On " + request.POST.get('desc_date') + ", " + full_name + " wrote:" + "\n\t" + request.POST.get(
        'cdesc')
    try:
        print '---------in communication---------------'
        print 'contact type', request.POST.get('select_contact_type')
        print 'Company----Id',request.POST.get('company_id')
        log_obj = FocusListResearchLog(

            focuslist_company_id=Focus_List.objects.get(focuslist_company_id=request.POST.get('company_id')),
##            zam_person_id=ZAMPerson.objects.get(zam_person_id=request.POST.get('zam_person')),
            log_date=datetime.datetime.strptime(request.POST.get('cdate'), '%d/%m/%Y').date(),
            log_desc=desc,
            company_personel=request.POST.get('company_personnel'),
            designation=request.POST.get('designation'),
            bank_name=request.POST.get('bank'),
            analyst_name=request.POST.get('analyst'),
            communication_created_by=request.session['login_user'],
            communication_updated_by=request.session['login_user'],
            communication_created_date=datetime.datetime.now(),
            communication_updated_date=datetime.datetime.now()
        )
        log_obj.save()
        if request.POST.get('select_contact_type') != 'null':
            log_obj.communicationtype_id = ResearchAttachmentTypes.objects.get(
                communicationtype_id=request.POST.get('select_contact_type'))
            log_obj.save()
            attachment_list = request.POST.get('attachment')
            print "attach", attachment_list
            save_focus_attachments(attachment_list, log_obj)

        data = {'success': 'true'}

    except Exception, e:
        print 'Exception :', e
        data = {'data': 'none'}
    return HttpResponse(json.dumps(data), content_type='application/json')

def save_active_attachments(attachment_list, communication_Id):
    try:
        attachment_list = attachment_list.split(',')
        attachment_list = filter(None, attachment_list)
        print "save attachments"
        print attachment_list
        print communication_Id
        for attached_id in attachment_list:
            attachment_obj = ActiveListAttechment.objects.get(attechment_id=attached_id)
            attachment_obj.active_researchlog_id = communication_Id
            attachment_obj.save()

        data = {'success': 'true'}
    except Exception, e:
        print 'Exception ', e
    return HttpResponse(json.dumps(data), content_type='application/json')

@csrf_exempt
# To Save The Communication   
def add_log_active_list(request):
##    pdb.set_trace()
    # user.first_name + " " + user.last_name
    print request.POST
    full_name = request.user.first_name + " " + request.user.last_name
    desc = request.POST.get('ac_cdesc').replace("\n","")
    desc = desc.replace("\t","")
    if desc=="":
        desc = ""
    else:
        desc = "On " + request.POST.get('ac_desc_date') + ", " + full_name + " wrote:" + "\n\t" + request.POST.get(
        'ac_cdesc')
    try:
        log_obj = ActiveListResearchLog(
            activelist_company_id=Active_List.objects.get(activelist_company_id=request.POST.get('ac_company_id')),
##            zam_person_id=ZAMPerson.objects.get(zam_person_id=request.POST.get('ac_zam_person')),
            log_date=datetime.datetime.strptime(request.POST.get('ac_cdate'), '%d/%m/%Y').date(),
            log_desc=desc,
            company_personel=request.POST.get('company_personnel'),
            designation=request.POST.get('designation'),
            bank_name=request.POST.get('bank'),
            analyst_name=request.POST.get('analyst'),
            communication_created_by=request.session['login_user'],
            communication_updated_by=request.session['login_user'],
            communication_created_date=datetime.datetime.now(),
            communication_updated_date=datetime.datetime.now()
        )
        log_obj.save()
        #
        print "type: ",request.POST.get('ac_select_contact_type')
        if request.POST.get('ac_select_contact_type') != 'null':
            log_obj.communicationtype_id = ResearchAttachmentTypes.objects.get(
                communicationtype_id=request.POST.get('ac_select_contact_type'))
            log_obj.save()
            attachment_list = request.POST.get('ac_attachment')
            print "attach", attachment_list
            save_active_attachments(attachment_list, log_obj)
        #
        # if request.POST['check_att'] == "1":
        #     print request.FILES['att_file']
        #     log_obj.log_attachment = request.FILES['att_file']
        #     log_obj.save()



        data = {'success': 'true'}

    except Exception, e:
        print 'Exception :', e
        data = {'data': 'none'}
    return HttpResponse(json.dumps(data), content_type='application/json')

def save_port_attachments(attachment_list, communication_Id):

    try:
        attachment_list = attachment_list.split(',')
        attachment_list = filter(None, attachment_list)
        print "save attachments"
        print attachment_list
        print communication_Id
        for attached_id in attachment_list:
            attachment_obj = PortfolioListAttechment.objects.get(attechment_id=attached_id)
            attachment_obj.portfolio_researchlog_Id = communication_Id
            attachment_obj.save()

        data = {'success': 'true'}
    except Exception, e:
        print 'Exception ', e
    return HttpResponse(json.dumps(data), content_type='application/json')

@csrf_exempt
# To Save The Communication   
def add_log_portfolio_list(request):
    ##    pdb.set_trace()
    print request.POST
    full_name = request.user.first_name + " " + request.user.last_name
    if request.POST.get('cdesc')=="":
        desc = ""
    else:
        desc = "On " + request.POST.get('desc_date') + ", " + full_name + " wrote:" + "\n\t" + request.POST.get(
        'cdesc')
    try:
        print '---------in communication---------------'
        log_obj = PortfolioListResearchLog(
            portfolio_company_id=Portfolio_List.objects.get(portfolio_company_id=request.POST.get('company_id')),
##            zam_person_id=ZAMPerson.objects.get(zam_person_id=request.POST.get('zam_person')),
            log_date=datetime.datetime.strptime(request.POST.get('cdate'), '%d/%m/%Y').date(),
            log_desc=desc,
            company_personel=request.POST.get('company_personnel'),
            designation=request.POST.get('designation'),
            bank_name=request.POST.get('bank'),
            analyst_name=request.POST.get('analyst'),
            communication_created_by=request.session['login_user'],
            communication_updated_by=request.session['login_user'],
            communication_created_date=datetime.datetime.now(),
            communication_updated_date=datetime.datetime.now()
        )
        log_obj.save()

        if request.POST.get('select_contact_type') != 'null':
            log_obj.communicationtype_id = ResearchAttachmentTypes.objects.get(
                communicationtype_id=request.POST.get('select_contact_type'))
            log_obj.save()
            attachment_list = request.POST.get('attachment')
            print "attach", attachment_list
            save_port_attachments(attachment_list, log_obj)

        data = {'success': 'true'}

    except Exception, e:
        print 'Exception :', e
        data = {'data': 'none'}
    return HttpResponse(json.dumps(data), content_type='application/json')


def get_focus_communication_msg(request):
    try:
        attch_paths = []
        attch_files = []
        if request.method == "GET":
            communication_id = request.GET['communication_id']
            comb_obj = FocusListResearchLog.objects.get(focus_researchlog_Id=communication_id)

            if comb_obj.communicationtype_id == None:
                comm_id = ""
            else:
                comm_id = comb_obj.communicationtype_id.communicationtype_name

            attch_obj = FocusListAttechment.objects.filter(focus_researchlog_Id = comb_obj)
            for attch in attch_obj:
                attch_path = SERVER_URL + attch.attachment_path.url
                attch_file = str(attch.attachment_path)[32:]
                attch_paths.append(attch_path)
                attch_files.append(attch_file)

            print communication_id
            data = {'success': 'true',
                    'communication_date': comb_obj.log_date.strftime('%d/%m/%Y') or '',
                    'communication_desc': comb_obj.log_desc,
                    'communication_type': comm_id,
                    'company_personel':comb_obj.company_personel or '',
                    'designation':comb_obj.designation or '',
                    'bank_name':comb_obj.bank_name or '',
                    'analyst_name':comb_obj.analyst_name or '',
                    'zam_contact_person': comb_obj.communication_created_by,
                    'attachment': attch_paths,
                    'file_name': attch_files
                    }
            print "Data",data       
        else:
            data = {'success': 'false'}
    except Exception, e:
        print 'Exception :', e
        data = {'success': 'error'}
    return HttpResponse(json.dumps(data), content_type='application/json')


def get_portfolio_communication_msg(request):
    try:
        attch_paths = []
        attch_files = []
        if request.method == "GET":
            communication_id = request.GET['communication_id']
            comb_obj = PortfolioListResearchLog.objects.get(portfolio_researchlog_Id=communication_id)

            if comb_obj.communicationtype_id == None:
                comm_id = ""
            else:
                comm_id = comb_obj.communicationtype_id.communicationtype_name

            attch_obj = PortfolioListAttechment.objects.filter(portfolio_researchlog_Id = comb_obj)
            for attch in attch_obj:
                attch_path = SERVER_URL + attch.attachment_path.url
                attch_file = str(attch.attachment_path)[36:]
                attch_paths.append(attch_path)
                attch_files.append(attch_file)

            print communication_id
            data = {'success': 'true',
                    'communication_date': comb_obj.log_date.strftime('%d/%m/%Y') or '',
                    'communication_desc': comb_obj.log_desc,
                    'communication_type': comm_id,
                    'company_personel':comb_obj.company_personel or '',
                    'designation':comb_obj.designation or '',
                    'bank_name':comb_obj.bank_name or '',
                    'analyst_name':comb_obj.analyst_name or '',
                    'zam_contact_person': comb_obj.communication_created_by,
                    'attachment': attch_paths,
                    'file_name':attch_files
                    }
        else:
            data = {'success': 'false'}
    except Exception, e:
        print 'Exception :', e
        data = {'success': 'error'}
    return HttpResponse(json.dumps(data), content_type='application/json')


def get_active_communication_msg(request):
    try:
        attch_paths = []
        attch_files = []
        if request.method == "GET":
            communication_id = request.GET['communication_id']
            comb_obj = ActiveListResearchLog.objects.get(active_researchlog_Id=communication_id)

            if comb_obj.communicationtype_id == None:
                comm_id = ""
            else:
                comm_id = comb_obj.communicationtype_id.communicationtype_name

            attch_obj = ActiveListAttechment.objects.filter(active_researchlog_id = comb_obj)
            for attch in attch_obj:
                attch_path = SERVER_URL + attch.attachment_path.url
                attch_file = str(attch.attachment_path)[33:]
                attch_paths.append(attch_path)
                attch_files.append(attch_file)

            print communication_id
            data = {'success': 'true',
                    'communication_date': comb_obj.log_date.strftime('%d/%m/%Y') or '',
                    'communication_desc': comb_obj.log_desc,
                    'communication_type': comb_obj.communicationtype_id.communicationtype_name,
                    'company_personel':comb_obj.company_personel or '',
                    'designation':comb_obj.designation or '',
                    'bank_name':comb_obj.bank_name or '',
                    'analyst_name':comb_obj.analyst_name or '',
                    'zam_contact_person': comb_obj.communication_created_by,
                    'attachment': attch_paths,
                    'file_name':attch_files
                    }
        else:
            data = {'success': 'false'}
    except Exception, e:
        print 'Exception :', e
        data = {'success': 'error'}
    return HttpResponse(json.dumps(data), content_type='application/json')
