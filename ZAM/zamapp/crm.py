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
import datetime
from zamapp.models import *
import datetime
import calendar
import time
from django.db.models import Q
from django.db.models import F

#SERVER_URL = 'http://192.168.0.123:9632'
SERVER_URL='http://ec2-54-179-153-165.ap-southeast-1.compute.amazonaws.com'

# Create your views here.
def crm_index(request):
    if request.user.is_authenticated():
        question_obj = Question.objects.filter(read_status = "Unread")
        question_count = question_obj.count()
        response_obj = Response.objects.filter(read_status = "Unread")
        response_count = response_obj.count()
        responseto_obj = Responseto.objects.filter(read_status = "Unread")
        responseto_count = responseto_obj.count()
        total_count = question_count + response_count + responseto_count
        data = { 'question_count' : question_count, 'response_count' : response_count, 'responseto_count' : responseto_count, 'total_count' : total_count }            	
        return render(request, 'crm_index.html',data)
        form = CaptchaForm()
        return render_to_response('login.html', dict(
            form=form
        ), context_instance=RequestContext(request))


# For the Add Client Page
def add_client(request):
    try:
        print 'ADD_CLIENT'
        question_obj = Question.objects.filter(read_status = "Unread")
        question_count = question_obj.count()
        response_obj = Response.objects.filter(read_status = "Unread")
        response_count = response_obj.count()
        responseto_obj = Responseto.objects.filter(read_status = "Unread")
        responseto_count = responseto_obj.count()
        total_count = question_count + response_count + responseto_count        
        data = {'success': 'true', 'country_list': get_country(request), 'firm_type': get_firmtype(request),
                'priority': get_clientpriority(request), 'asset_class': get_assetclass(request), 
                'question_count' : question_count, 'response_count' : response_count, 
                'responseto_count' : responseto_count, 'total_count' : total_count }
    except Exception, e:
        print 'Exception', e
        data = {'success': 'false'}

    return render(request, 'client_add.html', data)


# For the Communication details page
def communication_details(request):
    ##    pdb.set_trace()
    print '========in communication========'
    client_id = request.GET.get('client_id', '')
    try:
        print 'Communication List'
        communication_list = ClientCommunicationDetailsTbl.objects.filter(client_id=client_id)
        communicate_list = []
        for communication in communication_list:
            abc = communication.communication_desc[:10]
            commn_list = {
                'success': 'true',
                'comm_id': communication.communication_Id or '',
                'comm_date': communication.communication_date.strftime('%d/%m/%Y') or '',
                'comm_type': communication.communicationtype_id.communicationtype_name or '',
                'comm_zam_person': communication.zam_person_id or '',
                'comm_person': communication.contact_person_id.contact_person_first_name or '',
                'comm_desc': abc + '...' or ''
            }
            communicate_list.append(commn_list)

        data = {'contact_person_list': get_contact_person(request), 'communication_list': communicate_list,
                'zam_contact_person_list': get_zam_contact_person(request), 'com_types': get_commtype(request),
                'client_id': client_id}
    except Exception, e:
        print 'Exception', e
        data = {'success': 'false'}
    return render(request, 'client_communicaton.html', data)


# For Search Communication
def search_communication(request):
    ##    pdb.set_trace()
    print '---in search communication'
    print 'id', request.GET.get("zam_contact")
    try:
        comm_list = []
        comm_month = request.GET.get('comm_month')

        filter_args = {}
        filter_client_id_args = {}
        filter_contact_person_id_args={}
        filter_communicationtype_id_args = {}
        filter_zam_person_id_args = {}
        filter_communication_date__range_args = {}

        if request.GET.get('comm_type'):
            filter_communicationtype_id_args['communicationtype_id'] = request.GET.get('comm_type')
            
        if request.GET.get('contact_person'):
            filter_contact_person_id_args['contact_person_id'] = request.GET.get('contact_person')     

        if request.GET.get('comm_month'):
            comm_date = calculate_duration(datetime.datetime.now(), comm_month)
            filter_args['communication_date__range'] = [comm_date, datetime.datetime.now()]

        print 'comm_type', request.GET.get('comm_type')

        if request.GET.get('client_id'):
            filter_client_id_args['client_id'] = request.GET.get('client_id')

        print 'client_id', request.GET.get('client_id')

        if request.GET.get('zam_contact'):
            filter_zam_person_id_args['zam_person_id'] = request.GET.get('zam_contact')

        print 'zam_contact', request.GET.get('zam_contact')

        commList = ClientCommunicationDetailsTbl.objects.filter(Q(**filter_args) & Q(
            communicationtype_id=CommunicationTypes.objects.filter(**filter_communicationtype_id_args)) &
            Q(contact_person_id= ContactPersonDetails.objects.filter(**filter_contact_person_id_args)) & 
                                                                Q(client_id=ClientDetailsTbl.objects.filter(
                                                                    **filter_client_id_args)) & Q(
            zam_person_id=ZAMPerson.objects.filter(**filter_zam_person_id_args))
                                                                )

        print "communication", commList
        for comm in commList:
            comm_list.append(
                {'comm_type': comm.communicationtype_id.communicationtype_name,
                 'comm_zam_person': comm.zam_person_id.zam_person_name,
                 'comm_person': comm.contact_person_id.contact_person_first_name, 'comm_id': comm.communication_Id,
                 'comm_desc': comm.communication_desc[:10] + '..',
                 'comm_date': comm.communication_date.strftime('%d/%m/%Y')})

        print 'details', comm_list
        data = {'communication_list': comm_list}

    except Exception, e:
        print 'Exception', e
        data = {'success': 'false'}
    return HttpResponse(json.dumps(data), content_type='application/json')


# For calculate the duration
def calculate_duration(sourcedate, months):
    print sourcedate
    print months
    try:
        month = sourcedate.month - 1 - int(months)
        year = int(sourcedate.year + month / 12)
        month = month % 12 + 1
        day = min(sourcedate.day, calendar.monthrange(year, month)[1])
    except Exception, e:
        print 'Exception ', e
        # return datetime.date(date,month,year)
    return datetime.date(year, month, day)


# TO SAVE THE CLIENT
@csrf_exempt
def save_client(request):
    ##    pdb.set_trace()
    try:
        if request.method == "POST":
            client_obj = ClientDetailsTbl(
                client_firm=request.POST.get('txt_firm_name'),
                firmtype_id=Firmtype.objects.get(firmtype_id=request.POST.get('select_firm_type')),
                client_phone=request.POST.get('txt_firm_contact_no'),
                client_contact_email=request.POST.get('txt_firm_email_add'),
                client_relationship_manager=request.POST.get('txt_rln_manag'),
                client_office_address_line_1=request.POST.get('txt_address_line1'),
                client_office_address_line_2=request.POST.get('txt_address_line2'),
                country_id=Country.objects.get(country_id=request.POST.get('client_country')),
                state_name=request.POST.get('select_state'),
                city_name=request.POST.get('select_city'),
                client_pincode=request.POST.get('txt_pin_code'),
                client_comment=request.POST.get('txt_note'),
                priority_id=Clientpriority.objects.get(priority_id=request.POST.get('client_priority')),
                client_reference_person=request.POST.get('refrence_person'),
                client_created_by =request.session['login_user'],
                client_updated_by = request.session['login_user'],
                client_created_date = datetime.datetime.now(),
                client_updated_date = datetime.datetime.now()

            )
            client_obj.save()
            client_id = client_obj.client_id
            print client_id
            data = {'success': 'true', 'client_id': client_id}
        else:
            data = {'success': 'false'}
    except Exception, e:
        print 'Exception :', e
        data = {'data': 'none'}
    return HttpResponse(json.dumps(data), content_type='application/json')


# TO SAVE THE CLIENT IP
@csrf_exempt
def save_client_ip(request):
##    pdb.set_trace()
    print request.POST
    try:
        if request.method == "POST":
            client_ip_obj = ClientIPDetailsTbl(
                client_id=ClientDetailsTbl.objects.get(client_id=request.POST.get('client_id')),
                client_ecv=check_float_val(request.POST.get('txt_client_ecv')),
                asset_class_one_name=Asset_Class_Details(asset_class_id=request.POST.get('txt_first_asset_class')),
                asset_class_one_percentage=check_float_val(request.POST.get('txt_first_asset_class_per')),
                asset_class_two_name=Asset_Class_Details(asset_class_id=request.POST.get('txt_second_asset_class')),
                asset_class_two_percentage=check_float_val(request.POST.get('txt_second_asset_class_per')),
                asset_class_three_name=Asset_Class_Details(asset_class_id=request.POST.get('txt_third_asset_class')),
                asset_class_three_percentage=check_float_val(request.POST.get('txt_third_asset_class_per')),
                client_risk_category=request.POST.get('risk_cat'),
                client_ip_created_by = request.session['login_user'],
                client_ip_updated_by =request.session['login_user'],
                client_ip_created_date = datetime.datetime.now(),
                client_ip_updated_date = datetime.datetime.now()
            )

            client_ip_obj.save()
            data = {'success': 'true'}
        else:
            data = {'success': 'false'}
    except Exception, e:
        print 'Exception :', e
        data = {'success': 'false'}
    return HttpResponse(json.dumps(data), content_type='application/json')

def check_float_val(str):
    #pdb.set_trace()
    try:
        if str.strip()=="":
            str=None
    except Exception, e:
        print 'CRM.py|check_float_val| Exception',e
        str=None
    return str
        

# for get the client-list
def get_client_list(request):
    try:
        #pdb.set_trace();
        print 'Client List'
        client_list = ClientDetailsTbl.objects.filter(client_record_status='Active')
        #client_ip_list = ClientIPDetailsTbl.objects.filter(client_ip_record_status="Active")

        clie_list = []
        for client in client_list:   
            view = '<a href="/view-client/?client_id=' + str(
                client.client_id) + '" class="infont"> ' + '<i class="fa fa-eye"></i></i>  </a>'
            edit = '<a href="/edit-client/?client_id=' + str(
                client.client_id) + '" class="infont"> ' + '<i class="fa fa-edit"></i></i>  </a>'
            comm = '<a ' + str(
                client.client_id) +' onclick=opencommunication('+ str(client.client_id)  +') class="infont"> ''<i class="fa fa-comment-o"></i></i></a>'
            
            delete = '<a ' + str(
                client.client_id) + '" class="infont delete"> ' + '<i class="fa fa-trash-o"></i></i>  </a>'        
            ab_list = client.clientid.filter(client_ip_record_status="Active")
            
            #ab_list = ClientIPDetailsTbl.objects.filter(client_id=client.client_id,client_ip_record_status="Active")
            
            if client.client_reference_person == "":
                ref = "--"
            else:
                ref = client.client_reference_person
                
            if client.client_phone == "":
                phone = "--"
            else:
                phone = client.client_phone    
                
            
            ecv = '--';
            if ab_list:
                ecv = ab_list[0].client_ecv
            
            
                
            temp_obj = {
                'id':client.client_id,
                'firm': client.client_firm,
                'firm_type': client.firmtype_id.firm_name,
                'location': client.country_id.country_name,
                'contact_no': phone,
                'ecv': ecv,
                'refrence_person': ref,
                'view': view,
                'edit':edit,
                'comm':comm,
                'delete':delete

            }
            clie_list.append(temp_obj)

        data = {'data': clie_list}

    except Exception, e:
        print 'Exception : ', e
        data = {'data': 'none'}
    return HttpResponse(json.dumps(data), content_type='application/json')

@csrf_exempt
def change_status(request):
##    pdb.set_trace()
    try:
        stat = request.GET.get('client_id')
        print 'id--', stat
        stat_obj=ClientDetailsTbl.objects.get(client_id=stat)
        stat_obj.client_record_status="Inactive"
        stat_obj.save()
        data={'success':'true'}
    except Exception, e:
        print 'Exception : ', e
        data = {'data': 'error_msg'}    
    
    return HttpResponse(json.dumps(data), content_type='application/json')
    


# for the view client 
def view_client(request):
    ##    pdb.set_trace()
    try:
        cnt_list = []
        contact_person_list = []
        communicate_list = []
        client_obj = ClientDetailsTbl.objects.get(client_id=request.GET.get('client_id'))
        question_obj = Question.objects.filter(read_status = "Unread")
        question_count = question_obj.count()
        response_obj = Response.objects.filter(read_status = "Unread")
        response_count = response_obj.count()
        responseto_obj = Responseto.objects.filter(read_status = "Unread")
        responseto_count = responseto_obj.count()
        total_count = question_count + response_count + responseto_count           

        client_dict = {
            'success': 'true',
            'txt_firm_name': client_obj.client_firm,
            'select_firm_type': client_obj.firmtype_id,
            'txt_firm_contact_no': client_obj.client_phone,
            'txt_firm_email_add': client_obj.client_contact_email,
            'txt_rln_manag': client_obj.client_relationship_manager or '',
            'txt_address_line1': client_obj.client_office_address_line_1,
            'txt_address_line2': client_obj.client_office_address_line_2 or '',
            'client_country': client_obj.country_id,
            'select_state': client_obj.state_name,
            'select_city': client_obj.city_name,
            'txt_pin_code': client_obj.client_pincode,
            'txt_note': client_obj.client_comment or '',
            'client_priority': client_obj.priority_id,
            'refrence_person': client_obj.client_reference_person or '',
            'client_id': client_obj.client_id
        }

        try:
            clientip_obj = ClientIPDetailsTbl.objects.get(client_id=client_obj,client_ip_record_status="Active")
            #ab_list = ClientIPDetailsTbl.objects.filter(client_id=client.client_id,client_ip_record_status="Active")
            #clientip_obj=ab_list[0]
            client_ip_dict = {
                'success': 'true',
                'txt_client_ecv': clientip_obj.client_ecv or '',
                'txt_first_asset_class': clientip_obj.asset_class_one_name or '',
                'txt_first_asset_class_per': clientip_obj.asset_class_one_percentage or '',
                'txt_second_asset_class': clientip_obj.asset_class_two_name or '',
                'txt_second_asset_class_per': clientip_obj.asset_class_two_percentage or '',
                'txt_third_asset_class': clientip_obj.asset_class_three_name or '',
                'txt_third_asset_class_per': clientip_obj.asset_class_three_percentage or '',
                'risk_cat': clientip_obj.client_risk_category or '',
                'client_ip_id': clientip_obj.client_ip_id
            }
            print '-------------'
            print clientip_obj.client_ip_id
            print '--------'

        except ClientIPDetailsTbl.DoesNotExist as err:
            print 'Client IP is not Exists'
            client_ip = {}
            client_ip_dict = {'success': 'false', 'client_ip_id': 'clientIPNotAvailable'}

        try:
            contact_list = ContactPersonDetails.objects.filter(client_id=client_obj)

            for cnt in contact_list:
                cntact_list = {
                    'success': 'true',
                    'first_name': cnt.contact_person_first_name or '',
                    'last_name': cnt.contact_person_last_name or '',
                    'contact_person_contact_no': cnt.contact_person_contact_no or '',
                    'contact_person_email_id': cnt.contact_person_email_id or ''
                }
                cnt_list.append(cntact_list)

        except ContactPersonDetails.DoesNotExist as err:
            print 'Contact Person is not Exists'
            cntact_list = {}

        try:
            communication_list = ClientCommunicationDetailsTbl.objects.filter(client_id=client_obj)

            for communication in communication_list:
                abc = communication.communication_desc[:10]
                commn_list = {
                    'success': 'true',
                    'comm_id': communication.communication_Id or '',
                    'comm_date': communication.communication_date.strftime('%d/%m/%Y') or '',
                    'comm_type': communication.communicationtype_id.communicationtype_name or '',
                    'comm_zam_person': communication.zam_person_id or '',
                    'comm_person': communication.contact_person_id.contact_person_first_name or '',
                    'comm_desc': abc + '...' or ''
                }
                communicate_list.append(commn_list)

        except ClientCommunicationDetailsTbl.DoesNotExist as err:
            print 'Communication is not Exists'
            communication_list = {}

        data = {'client': client_dict, 'client_ip': client_ip_dict, 'contact_list': cnt_list,
                'communication_list': communicate_list,
                'contact_person_list': get_contact_persons(request), 'firm_type': get_firmtype(request),
                'country_list': get_country(request), 'com_types': get_commtype(request),
                'zam_contact_person_list': get_zam_contact_person(request),
                'priority': get_clientpriority(request), 'asset_class': get_assetclass(request),
                'flag':'view', 'question_count' : question_count, 'response_count' : response_count, 
                'responseto_count' : responseto_count, 'total_count' : total_count 
                }
    except Exception, e:
        print 'Exception ', e
        data = {'success': 'false'}
    return render(request, 'client_view.html', data)

# for the view client 
def edit_client(request):
    ##    pdb.set_trace()
    try:
        cnt_list = []
        contact_person_list = []
        communicate_list = []
        client_obj = ClientDetailsTbl.objects.get(client_id=request.GET.get('client_id'))
        question_obj = Question.objects.filter(read_status = "Unread")
        question_count = question_obj.count()
        response_obj = Response.objects.filter(read_status = "Unread")
        response_count = response_obj.count()
        responseto_obj = Responseto.objects.filter(read_status = "Unread")
        responseto_count = responseto_obj.count()
        total_count = question_count + response_count + responseto_count         

        client_dict = {
            'success': 'true',
            'txt_firm_name': client_obj.client_firm,
            'select_firm_type': client_obj.firmtype_id,
            'txt_firm_contact_no': client_obj.client_phone,
            'txt_firm_email_add': client_obj.client_contact_email,
            'txt_rln_manag': client_obj.client_relationship_manager or '',
            'txt_address_line1': client_obj.client_office_address_line_1,
            'txt_address_line2': client_obj.client_office_address_line_2 or '',
            'client_country': client_obj.country_id,
            'select_state': client_obj.state_name,
            'select_city': client_obj.city_name,
            'txt_pin_code': client_obj.client_pincode,
            'txt_note': client_obj.client_comment or '',
            'client_priority': client_obj.priority_id,
            'refrence_person': client_obj.client_reference_person or '',
            'client_id': client_obj.client_id
        }

        try:
            clientip_obj = ClientIPDetailsTbl.objects.get(client_id=client_obj,client_ip_record_status="Active")
            client_ip_dict = {
                'success': 'true',
                'txt_client_ecv': clientip_obj.client_ecv or '',
                'txt_first_asset_class': clientip_obj.asset_class_one_name or '',
                'txt_first_asset_class_per': clientip_obj.asset_class_one_percentage or '',
                'txt_second_asset_class': clientip_obj.asset_class_two_name or '',
                'txt_second_asset_class_per': clientip_obj.asset_class_two_percentage or '',
                'txt_third_asset_class': clientip_obj.asset_class_three_name or '',
                'txt_third_asset_class_per': clientip_obj.asset_class_three_percentage or '',
                'risk_cat': clientip_obj.client_risk_category or '',
                'client_ip_id': clientip_obj.client_ip_id
            }
            print '-------------'
            print clientip_obj.client_ip_id
            print '--------'

        except ClientIPDetailsTbl.DoesNotExist as err:
            print 'Client IP is not Exists'
            client_ip = {}
            client_ip_dict = {'success': 'false', 'client_ip_id': 'clientIPNotAvailable'}

        try:
            contact_list = ContactPersonDetails.objects.filter(client_id=client_obj)

            for cnt in contact_list:
                cntact_list = {
                    'success': 'true',
                    'first_name': cnt.contact_person_first_name or '',
                    'last_name': cnt.contact_person_last_name or '',
                    'contact_person_contact_no': cnt.contact_person_contact_no or '',
                    'contact_person_email_id': cnt.contact_person_email_id or ''
                }
                cnt_list.append(cntact_list)

        except ContactPersonDetails.DoesNotExist as err:
            print 'Contact Person is not Exists'
            cntact_list = {}

        try:
            communication_list = ClientCommunicationDetailsTbl.objects.filter(client_id=client_obj)

            for communication in communication_list:
                abc = communication.communication_desc[:10]
                commn_list = {
                    'success': 'true',
                    'comm_id': communication.communication_Id or '',
                    'comm_date': communication.communication_date.strftime('%d/%m/%Y') or '',
                    'comm_type': communication.communicationtype_id.communicationtype_name or '',
                    'comm_zam_person': communication.zam_person_id or '',
                    'comm_person': communication.contact_person_id.contact_person_first_name or '',
                    'comm_desc': abc + '...' or ''
                }
                communicate_list.append(commn_list)

        except ClientCommunicationDetailsTbl.DoesNotExist as err:
            print 'Communication is not Exists'
            communication_list = {}

        data = {'client': client_dict, 'client_ip': client_ip_dict, 'contact_list': cnt_list,
                'communication_list': communicate_list,
                'contact_person_list': get_contact_persons(request), 'firm_type': get_firmtype(request),
                'country_list': get_country(request), 'com_types': get_commtype(request),
                'zam_contact_person_list': get_zam_contact_person(request),
                'priority': get_clientpriority(request), 'asset_class': get_assetclass(request),
                'flag':'edit', 'question_count' : question_count, 'response_count' : response_count, 
                'responseto_count' : responseto_count, 'total_count' : total_count 
                }
    except Exception, e:
        print 'Exception ', e
        data = {'success': 'false'}
    return render(request, 'client_view.html', data)


def get_communication_list(request):
    try:
        print '==========check======================'
        client_id = request.GET.get('client_id')
        communication_list = ClientCommunicationDetailsTbl.objects.filter(client_id=client_id)
        communicate_list = []
        for communication in communication_list:
            abc = communication.communication_desc[:10]
            commn_list = {
                'success': 'true',
                'comm_id': communication.communication_Id or '',
                'comm_date': communication.communication_date.strftime('%d/%m/%Y') or '',
                'comm_type': communication.communicationtype_id.communicationtype_name or '',
                'comm_zam_person': communication.zam_person_id.zam_person_name or '',
                'comm_person': communication.contact_person_id.contact_person_first_name or '',
                'comm_desc': abc + '...' or ''
            }

        communicate_list.append(commn_list)
        data = {'data': communicate_list}
        print data
    except Exception, e:
        print 'Exception at security list: ', e
        data = {'data': 'none'}
    return HttpResponse(json.dumps(data), content_type='application/json')

@csrf_exempt
# To Save The Contact Person    
def add_contact_person(request):
    # pdb.set_trace()
    try:

        if request.method == "POST":
            contactperson_obj = ContactPersonDetails(
                client_id=ClientDetailsTbl.objects.get(client_id=request.POST.get('client_id')),
                contact_person_first_name=request.POST.get('txt_firm_contact_person'),
                contact_person_last_name=request.POST.get('txt_firm_last_contact_person'),
                contact_person_contact_no=request.POST.get('txt_firm_contact_pareson_contact_no'),
                contact_person_email_id=request.POST.get('txt_contact_email_add'),
                contact_person_created_by  = request.session['login_user'],
                contact_person_updated_by  = request.session['login_user'],
                contact_person_created_date = datetime.datetime.now(),
                contact_person_updated_date = datetime.datetime.now()
            )
            contactperson_obj.save()
            contact_list = get_contact_person_list(request.POST.get('client_id'))
            data = {'success': 'true', 'contact_person_list': contact_list}

        else:
            data = {'success': 'false'}
    except Exception, e:
        print 'Exception :', e
        data = {'data': 'none'}
    return HttpResponse(json.dumps(data), content_type='application/json')


def save_attachments(attachment_list, communication_Id):
    try:
        attachment_list = attachment_list.split(',')
        attachment_list = filter(None, attachment_list)
        print attachment_list
        for attached_id in attachment_list:
            attachment_obj = ClientCommunicationAttachmentsDetailsTbl.objects.get(attachment_id=attached_id)
            attachment_obj.communication_Id = communication_Id
            attachment_obj.save()

        data = {'success': 'true'}
    except Exception, e:
        print 'Exception ', e
    return HttpResponse(json.dumps(data), content_type='application/json')


@csrf_exempt
# To Save The Communication   
def add_communication(request):
    # pdb.set_trace()
    try:
        print '---------in communication---------------'
        if request.method == "POST":
            communication_obj = ClientCommunicationDetailsTbl(
                client_id=ClientDetailsTbl.objects.get(client_id=request.POST.get('client_id')),
                contact_person_id=ContactPersonDetails.objects.get(contact_person_id=request.POST.get('person')),
                zam_person_id=ZAMPerson.objects.get(zam_person_id=request.POST.get('zam_person')),
                communicationtype_id=CommunicationTypes.objects.get(
                communicationtype_id=request.POST.get('select_contact_type')),
                communication_date=datetime.datetime.strptime(request.POST.get('cdate'), '%d/%m/%Y').date(),
                communication_desc=request.POST.get('cdesc'),
                communication_created_by  =request.session['login_user'],
                communication_updated_by  = request.session['login_user'],
                communication_created_date  = datetime.datetime.now(),
                communication_updated_date  = datetime.datetime.now()
            )
            communication_obj.save()
            print communication_obj.communication_Id
            attachment_list = []
            attachment_list = request.POST.get('attachments')
            print "attach", attachment_list
            save_attachments(attachment_list, communication_obj)
            data = {'success': 'true'}
        else:
            data = {'success': 'false'}
    except Exception, e:
        print 'Exception :', e
        data = {'data': 'none'}
    return HttpResponse(json.dumps(data), content_type='application/json')


# TO GET THE COMMUNICATION TYPE
def get_commtype(request):
    ##    pdb.set_trace()
    commtype_list = []
    try:
        comtypes = CommunicationTypes.objects.all()
        for comtype in comtypes:
            commtype_list.append(
                {'com_type_id': comtype.communicationtype_id, 'com_type_name': comtype.communicationtype_name})

    except Exception, e:
        print 'Exception ', e
    return commtype_list


# Contact Person List
def get_contact_persons(request):
##    pdb.set_trace()
    contact_person_list = []
    print 'client_id', request.GET.get('client_id')
    try:
        communication_person = ContactPersonDetails.objects.filter(client_id=request.GET.get('client_id'))
        for contact in communication_person:
            contact_person_list.append(
                {'contact_person': contact.contact_person_id, 'person_name': contact.contact_person_first_name})
                
        data = {'success': 'true', 'contact_person_listt': contact_person_list,'zam_contact_person_list': get_zam_contact_person(request),'com_types': get_commtype(request)}
   
    except Exception, e:
        print 'Exception ', e
    return contact_person_list

# Contact Person List
def get_contact_person(request):
##    pdb.set_trace()
    contact_person_list = []
    print 'client_id', request.GET.get('client_id')
    try:
        communication_person = ContactPersonDetails.objects.filter(client_id=request.GET.get('client_id'))
        for contact in communication_person:
            contact_person_list.append(
                {'contact_person': contact.contact_person_id, 'person_name': contact.contact_person_first_name})
                
        data = {'success': 'true', 'contact_person_listt': contact_person_list,'zam_contact_person_list': get_zam_contact_person(request),'com_types': get_commtype(request)}
   
    except Exception, e:
        print 'Exception ', e
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


def get_contact_person_list(client_id):
    contact_person_list = []
    print client_id
    try:
        communication_person = ContactPersonDetails.objects.filter(client_id=client_id)
        for contact in communication_person:
            contact_person_list.append(
                {'contact_person_id': contact.contact_person_id, 'person_first_name': contact.contact_person_first_name,
                 'person_last_name': contact.contact_person_last_name,
                 'contact_person_contact_no': contact.contact_person_contact_no,
                 'contact_person_email_id': contact.contact_person_email_id
                 })
    except Exception, e:
        print 'Exception ', e
    return contact_person_list


# TO GET THE FIRMTYPE
def get_firmtype(request):
    ##    pdb.set_trace()
    firmtype_list = []
    try:
        firmtypes = Firmtype.objects.all()
        for firms in firmtypes:
            firmtype_list.append({'firm_type_id': firms.firmtype_id, 'firm_type_name': firms.firm_name})

    except Exception, e:
        print 'Exception ', e
    return firmtype_list


# TO GET THE CLIENT PRIORITY
def get_clientpriority(request):
    ##    pdb.set_trace()
    priority_list = []
    try:
        priorities = Clientpriority.objects.all()
        for priority in priorities:
            priority_list.append({'priority_id': priority.priority_id, 'priority_name': priority.priority_name})

    except Exception, e:
        print 'Exception ', e
    return priority_list


# TO GET THE COUNTRY
def get_country(request):
    ##    pdb.set_trace()
    country_list = []
    try:
        countries = Country.objects.all()
        for cntry in countries:
            country_list.append({'country_id': cntry.country_id, 'country_name': cntry.country_name})

    except Exception, e:
        print 'Exception ', e
    return country_list


# TO GET THE ASSETCLASS
def get_assetclass(request):
    ##    pdb.set_trace()
    assetclass_list = []
    try:
        assets = Asset_Class_Details.objects.all()
        for asset in assets:
            assetclass_list.append({'assetclass_id': asset.asset_class_id, 'assetclass_name': asset.asset_class_name})

    except Exception, e:
        print 'Exception ', e
    return assetclass_list


@csrf_exempt
# TO GET THE STATE
# def get_state(request):
#     ##    pdb.set_trace()
#     state_list = []
#     print 'in state mode'
#     try:
#         states = State.objects.filter(country_id=request.GET.get('country_id'))
#         for state in states:
#             state_list.append({'state_id': state.state_id, 'state_name': state.state_name})
#
#         data = {'success': 'true', 'states': state_list}
#     except Exception, e:
#         print 'Exception ', e
#     return HttpResponse(json.dumps(data), content_type='application/json')


# TO GET THE CITY
# def get_city(request):
#     ##    pdb.set_trace()
#     print 'in city mode'
#     city_list = []
#     print
#     try:
#         cities = City.objects.filter(state_id=request.GET.get("state_id"))
#         for city in cities:
#             city_list.append({'city_id': city.city_id, 'city_name': city.city_name})
#
#         data = {'success': 'true', 'city': city_list}
#     except Exception, e:
#         print 'Exception ', e
#     return HttpResponse(json.dumps(data), content_type='application/json')



@csrf_exempt
# Update The Basic Info
def update_basic_info(request):
    print 'in update basic info'
    ##    pdb.set_trace()
    try:
        if request.method == "POST":
            client_obj = ClientDetailsTbl.objects.get(client_id=request.POST.get('client_id'))
            client_obj.client_updated_by = request.session['login_user']
            client_obj.client_updated_date = datetime.datetime.now()
            client_obj.client_record_status ="Inactive"
            client_obj.save()
            
            client_new_obj = ClientDetailsTbl()
            client_new_obj.client_firm=request.POST.get('txt_firm_name')
            client_new_obj.firmtype_id=Firmtype.objects.get(firmtype_id=request.POST.get('select_firm_type'))
            client_new_obj.client_phone=request.POST.get('txt_firm_contact_no')
            client_new_obj.client_contact_email=request.POST.get('txt_firm_email_add')
            client_new_obj.client_relationship_manager=request.POST.get('txt_rln_manag')
            client_new_obj.client_office_address_line_1=request.POST.get('txt_address_line1')
            client_new_obj.client_office_address_line_2=request.POST.get('txt_address_line2')
            client_new_obj.country_id=Country.objects.get(country_name=request.POST.get('client_country'))
            client_new_obj.state_name=request.POST.get('select_state')
            client_new_obj.city_name=request.POST.get('select_city')
            client_new_obj.client_pincode=request.POST.get('txt_pin_code')
            client_new_obj.client_comment=request.POST.get('txt_note')
            client_new_obj.priority_id=Clientpriority.objects.get(priority_id=request.POST.get('client_priority'))
            client_new_obj.client_reference_person=request.POST.get('refrence_person')

            client_new_obj.save()
            
            clientIp_obj= ClientIPDetailsTbl.objects.get(client_id=client_obj,client_ip_record_status="Active")
            clientIp_obj.client_id=client_new_obj        
            clientIp_obj.save()
            
            data = {'success': 'true'}
        else:
            data = {'success': 'false'}
    except Exception, e:
        print 'Exception :', e
        data = {'data': 'none'}
    return HttpResponse(json.dumps(data), content_type='application/json')


# Update CLIENT IP
@csrf_exempt
def update_client_ip(request):
##    pdb.set_trace()
    try:
        if request.method == "POST":
            if request.POST.get('client_ip_id') == 'clientIPNotAvailable':
                client_ip_obj = ClientIPDetailsTbl(
                    client_id=ClientDetailsTbl.objects.get(client_id=request.POST.get('client_id')),
                    client_ecv=check_float_val(request.POST.get('txt_client_ecv')),
                    asset_class_one_name=Asset_Class_Details(asset_class_id=request.POST.get('txt_first_asset_class')),
                    asset_class_one_percentage=check_float_val(request.POST.get('txt_first_asset_class_per')),
                    asset_class_two_name=Asset_Class_Details(asset_class_id=request.POST.get('txt_second_asset_class')),
                    asset_class_two_percentage=check_float_val(request.POST.get('txt_second_asset_class_per')),
                    asset_class_three_name=Asset_Class_Details(
                    asset_class_id=request.POST.get('txt_third_asset_class')),
                    asset_class_three_percentage=check_float_val(request.POST.get('txt_third_asset_class_per')),
                    client_risk_category=request.POST.get('risk_cat'),
                    client_ip_created_by = request.session['login_user'],
                    client_ip_updated_by = request.session['login_user'],
                    client_ip_updated_date = datetime.datetime.now(),
                    client_ip_created_date= datetime.datetime.now(),
                )
                client_ip_obj.save()
                data = {'success': 'true'}
            else:
                    client_ip_obj = ClientIPDetailsTbl.objects.get(client_id=request.POST.get('client_id'),client_ip_record_status ="Active")
                    client_ip_obj.client_ip_updated_by = request.session['login_user']
                    client_ip_obj.client_ip_updated_date = datetime.datetime.now()
                    client_ip_obj.client_ip_record_status ="Inactive"
                    client_ip_obj.save()
                    
                    client_ip_new_obj = ClientIPDetailsTbl()
                    client_ip_new_obj.client_id=ClientDetailsTbl.objects.get(client_id=request.POST.get('client_id'))
                    client_ip_new_obj.client_ecv=check_float_val(request.POST.get('txt_client_ecv'))
                    client_ip_new_obj.asset_class_one_name=Asset_Class_Details(asset_class_id=request.POST.get('txt_first_asset_class'))
                    client_ip_new_obj.asset_class_one_percentage=check_float_val(request.POST.get('txt_first_asset_class_per'))
                    client_ip_new_obj.asset_class_two_name=Asset_Class_Details(asset_class_id=request.POST.get('txt_second_asset_class'))
                    client_ip_new_obj.asset_class_two_percentage=check_float_val(request.POST.get('txt_second_asset_class_per'))
                    client_ip_new_obj.asset_class_three_name=Asset_Class_Details(
                    asset_class_id=request.POST.get('txt_third_asset_class'))
                    client_ip_new_obj.asset_class_three_percentage=check_float_val(request.POST.get('txt_third_asset_class_per'))
                    client_ip_new_obj.client_risk_category=request.POST.get('risk_cat')

                    client_ip_new_obj.save()
                    data = {'success': 'true'}
        else:
            data = {'success': 'false'}
    except Exception, e:
        print 'Exception :', e
        data = {'data': 'none'}
    return HttpResponse(json.dumps(data), content_type='application/json')

def get_communication_msg(request):
    try:
        if request.method == "GET":
            communication_id = request.GET['communication_id']
            comb_obj = ClientCommunicationDetailsTbl.objects.get(communication_Id=communication_id)
            attach_list = comb_obj.communicationId.filter(communication_Id=comb_obj)
            print 'attach_list', attach_list
            attachment_list = []
            if attach_list:
                for attachment in attach_list:
                    attachment_list.append({'attachment_url': SERVER_URL + attachment.attachment_file_path.url,
                                            'attachment_name': str(attachment.attachment_file_path)[6:],
                                            'attachment_id': attachment.attachment_id
                                            })
                print attachment.attachment_file_path.url
                print str(attachment.attachment_file_path)[6:]

            print '-----------------------------------------'
            print communication_id
            data = {'success': 'true',
                    'contact_person': comb_obj.contact_person_id.contact_person_first_name + ' ' + comb_obj.contact_person_id.contact_person_last_name,
                    'communication_date': comb_obj.communication_date.strftime('%d/%m/%Y') or '',
                    'communication_desc': comb_obj.communication_desc,
                    'communication_type': comb_obj.communicationtype_id.communicationtype_name,
                    'zam_contact_person': comb_obj.zam_person_id.zam_person_name,
                    'attachment_list': attachment_list
                    }
        else:
            data = {'success': 'false'}
    except Exception, e:
        print 'Exception :', e
        data = {'success': 'error'}
    return HttpResponse(json.dumps(data), content_type='application/json')
