import pdb
import re
from django.http import HttpResponse
from django.shortcuts import render_to_response, render, redirect
from django.views.decorators.csrf import csrf_exempt
from models import *
import json
from zamapp.captcha_form import CaptchaForm
from django.template import RequestContext


def open_security_price_page(request):
    if request.user.is_authenticated():
        return render(request, 'price_index.html')
    else:
        form = CaptchaForm()
        return render_to_response('login.html', dict(
            form=form
        ), context_instance=RequestContext(request))


def open_add_security_price_page(request):
    if request.user.is_authenticated():
        asset_class_list = add_to_dropdown(Asset_Class_Details)
        data = {'asset_class_list': asset_class_list}
        return render(request, 'price_add.html', data)
    else:
        form = CaptchaForm()
        return render_to_response('login.html', dict(
            form=form
        ), context_instance=RequestContext(request))


def open_add_bulk_security_price_page(request):
    if request.user.is_authenticated():
        return render(request, 'price_bulk_add.html')
    else:
        form = CaptchaForm()
        return render_to_response('login.html', dict(
            form=form
        ), context_instance=RequestContext(request))


def open_add_bulk_security_price_page(request):
    if request.user.is_authenticated():
        asset_class_list = add_to_dropdown(Asset_Class_Details)
        data = {'asset_class_list': asset_class_list}
        return render(request, 'price_bulk_add.html', data)
    else:
        form = CaptchaForm()
        return render_to_response('login.html', dict(
            form=form
        ), context_instance=RequestContext(request))


@csrf_exempt
def save_security_price_details(request):
    try:
        # pdb.set_trace()
        print '=======================save data=========================='
        print request.POST
        print request.POST['selectBloombergTicker']
        securityPrice_obj = Security_Price_Details()
        securityPrice_obj.security_id = Security_Details.objects.get(security_id=request.POST['selectBloombergTicker'])
        securityPrice_obj.security_price_date = datetime.strptime(request.POST['price_date'], '%d/%m/%Y').date()
        securityPrice_obj.security_in_price = check_float_val(request.POST['txtInPrice'])
        securityPrice_obj.security_last_price = check_float_val(request.POST['txtLastPrice'])
        securityPrice_obj.security_one_d = check_float_val(request.POST['txt1D'])
        securityPrice_obj.security_fx_rate_in = check_float_val(request.POST['txtInFxRate'])
        securityPrice_obj.security_fx_rate_last = check_float_val(request.POST['txtLastFxRate'])
        securityPrice_obj.security_usd_in = check_float_val(request.POST['txtUsdIn'])
        securityPrice_obj.security_usd_last = check_float_val(request.POST['txtUsdLast'])
        securityPrice_obj.record_status = 'Active'
        securityPrice_obj.security_price_created_by = request.session['login_user']
        securityPrice_obj.security_price_updated_by = request.session['login_user']
        securityPrice_obj.security_price_created_date = datetime.now()
        securityPrice_obj.security_price_updated_date = datetime.now()
        securityPrice_obj.save()
        result = {'success': 'true'}
    except Exception, e:
        print 'Exception', e
        result = {'success': 'false'}
    return HttpResponse(json.dumps(result), content_type='application/json')
    # return redirect('/open-security-price-page/')


def check_float_val(str):
    try:
        float(str)
        return str
    except Exception, e:
        print 'security.py|check_float_val| Exception',e
        str=None
    return str

@csrf_exempt
def update_security_price_details(request):
    try:
        #pdb.set_trace()
        print '=======================update data==========================',request.POST
        print request.POST
        if request.method == "POST":
            securityPrice_obj = Security_Price_Details.objects.get(security_price_id=request.POST['security_price_id'])
            securityPrice_obj.record_status = 'Inactive'
            securityPrice_obj.security_price_updated_by = request.session['login_user']
            securityPrice_obj.security_price_updated_date = datetime.now()
            securityPrice_obj.save()

            securityPriceNew_obj = Security_Price_Details()
            securityPriceNew_obj.security_id = Security_Details.objects.get(security_id=request.POST['selectBloombergTicker'])
            securityPriceNew_obj.security_price_date = datetime.strptime(request.POST['price_date'], '%d/%m/%Y').date()
            securityPriceNew_obj.security_in_price = check_float_val(request.POST['txtInPrice'])
            securityPriceNew_obj.security_last_price = check_float_val(request.POST['txtLastPrice'])
            securityPriceNew_obj.security_one_d = check_float_val(request.POST['txt1D'])
            securityPriceNew_obj.security_fx_rate_in = check_float_val(request.POST['txtInFxRate'])
            securityPriceNew_obj.security_fx_rate_last = check_float_val(request.POST['txtLastFxRate'])
            securityPriceNew_obj.security_usd_in = check_float_val(request.POST['txtUsdIn'])
            securityPriceNew_obj.security_usd_last = check_float_val(request.POST['txtUsdLast'])
            securityPriceNew_obj.record_status = 'Active'
            securityPriceNew_obj.security_price_created_by = request.session['login_user']
            securityPriceNew_obj.security_price_updated_by = request.session['login_user']
            securityPriceNew_obj.security_price_created_date = datetime.now()
            securityPriceNew_obj.security_price_updated_date = datetime.now()
            securityPriceNew_obj.save()
            result = {'success': 'true'}
        else:
            result = {'success': 'true'}
    except Exception, e:
        print 'Exception', e
        result = {'success': 'false'}
    return HttpResponse(json.dumps(result), content_type='application/json')
    # return redirect('/open-security-price-page/')


def get_securityprice_list(request):
    try:
        securityPriceobj_list = Security_Price_Details.objects.filter(record_status='Active')
        securityprice_list = []
        print '=================123==========='
        for securityprice in securityPriceobj_list:
            print securityprice.security_id
            print '=================='
            view = '<a href=/view-security-price-details/?securityPrice_id=' + str(
                securityprice.security_price_id)+'&flag=view'+'>' + '<i class="fa fa-eye"></i></i></a>'

            edit = '<a href="/view-security-price-details/?securityPrice_id=' + str(securityprice.security_price_id) +'&flag=edit'+'"class="infont">' + '<i class="fa fa-edit"></i></i>  </a>'
            delete = '<a  onclick=delete_pirce(' + str(securityprice.security_price_id) + ') class="infont delete"> ' + '<i class="fa fa-trash-o"></i></i>  </a>'

            security_obj = {
                'security': securityprice.security_id.security_name,
                'assetclass': securityprice.security_id.asset_sub_class_id.asset_class_id.asset_class_name,
                'subassetclass': securityprice.security_id.asset_sub_class_id.asset_sub_class_name,
                'in_price': securityprice.security_in_price,
                'last_price': securityprice.security_last_price,
                'usd_in': securityprice.security_usd_in,
                'usd_last': securityprice.security_usd_last,
                'updatedDate': securityprice.security_price_date.strftime('%d/%m/%Y'),
                'view': view,
                'edit':edit,
                'delete':delete,
            }
            securityprice_list.append(security_obj)
        data = {'data': securityprice_list}
    except Exception, e:
        print 'Exception at security list: ', e
        data = {'data': 'none'}
    return HttpResponse(json.dumps(data), content_type='application/json')


def view_security_price_details(request):
    # pdb.set_trace()
    data = {'abc': 'xyz'}

    print '===================view security price==============='
    try:
        if request.method == 'GET':
            securityprice_obj = Security_Price_Details.objects.get(security_price_id=request.GET['securityPrice_id'])
            print securityprice_obj

            asset_class_list = add_to_dropdown(Asset_Class_Details)
            sub_asset_class_list = Asset_Sub_Class_Details.objects.filter(
                asset_class_id=securityprice_obj.security_id.asset_sub_class_id.asset_class_id)
            security_list = Security_Details.objects.filter(
                asset_sub_class_id=securityprice_obj.security_id.asset_sub_class_id)

            data = {'asset_class_list': asset_class_list,
                    'sub_asset_class_list': sub_asset_class_list,
                    'security_list': security_list,
                    'security_id': securityprice_obj.security_id.security_id,
                    'security_price_id': securityprice_obj.security_price_id,
                    'security_price_date': str(securityprice_obj.security_price_date.strftime('%d/%m/%Y')),
                    'assetclass_id': securityprice_obj.security_id.asset_sub_class_id.asset_class_id.asset_class_id,
                    'subassetclass_id': securityprice_obj.security_id.asset_sub_class_id.asset_sub_class_id,
                    'security_last_price': securityprice_obj.security_last_price,
                    'security_in_price': securityprice_obj.security_in_price,
                    'security_usd_in': securityprice_obj.security_usd_in,
                    'security_usd_last': securityprice_obj.security_usd_last,
                    'security_one_d': securityprice_obj.security_one_d,
                    'security_fx_rate_in': securityprice_obj.security_fx_rate_in,
                    'security_fx_rate_last': securityprice_obj.security_fx_rate_last,
                    'record_status': securityprice_obj.record_status,
                    'security_price_created_by': securityprice_obj.security_price_created_by,
                    'security_price_updated_by': securityprice_obj.security_price_updated_by,
                    'security_price_created_date': securityprice_obj.security_price_created_date.strftime('%d/%m/%Y'),
                    'security_price_updated_date': securityprice_obj.security_price_updated_date.strftime('%d/%m/%Y'),
                    'flag':request.GET['flag'],}
            print '========success Data==========='
            print data
            return render(request, 'price_view.html', data)
        else:
            data = {'success': 'false'}
    except Exception, e:
        print '----error----'
        print e
        data = {'success': 'false'}
    return render(request, 'price_view.html', data)


def add_to_dropdown(table_name):
    data_list = table_name.objects.filter(row_status='Active')
    print data_list
    return data_list


@csrf_exempt
def add_bulk_price(request):
    try:
        bulk_data = request.POST.get('totalData')
        bulk_data_info = json.loads(bulk_data)
        data_list = []
        for data in bulk_data_info:
            security = data.get('Security*')
            bloombergTicker=data.get('Bloomberg Ticker*')
            try:
                security_obj = Security_Details.objects.get(security_bloomer_ticker=bloombergTicker,security_name=security,record_status="Active")
                # security_obj = Security_Details.objects.filter(security_name=security).order_by(
                #     '-security_created_date')
                # security = security_obj.first()
                # security_obj = Security_Details.objects.get(security_id=security.security_id)


                date = data.get('Date*')
                last_price = float(data.get('Last Price*'))
                in_price = float(data.get('In Price*'))
                one_d = data.get('%1D')
                #print one_d
                if one_d =="":
                    one_d = 0
                else:
                    one_d = float(data.get('%1D'))

                in_fx_rate = float(data.get('In FX Rate*'))
                last_fx_rate = float(data.get('Last FX Rate*'))
                usd_in = in_price/in_fx_rate
                usd_last = last_price/last_fx_rate

                if security_obj and data.get('Last Price*') != "" and data.get('In Price*') != "" and data.get(
                        'In FX Rate*') != "" and data.get('Last FX Rate*') != "":
                    print "adding price object"
                    securityPrice_obj = Security_Price_Details(
                        security_id=security_obj,
                        security_price_date = datetime.strptime(data.get('Date*'),'%d/%m/%Y').date(),
                        security_last_price=last_price,
                        security_in_price=in_price,
                        security_usd_in = usd_in,
                        security_usd_last = usd_last,
                        security_fx_rate_in=in_fx_rate,
                        security_fx_rate_last=last_fx_rate,
                        security_one_d=one_d,
                        record_status='Active',
                        security_price_created_by='Admin',
                        security_price_updated_by='Admin',
                        security_price_created_date=datetime.now(),
                        security_price_updated_date=datetime.now(),
                    )
                    securityPrice_obj.save()
                    print securityPrice_obj
                    data = {'success': 'true'}

                else:
                    date = data.get('Date*')
                    last_price = data.get('Last Price*')
                    in_price = data.get('In Price*')
                    one_d = data.get('%1D')
                    in_fx_rate = data.get('In FX Rate*')
                    last_fx_rate = data.get('Last FX Rate*')

                    if date == "":
                        date = '<td class="text-center "><span class="label label-danger ">null</span></td>'

                    if last_price == "":
                        last_price = '<td class="text-center "><span class="label label-danger ">null</span></td>'

                    if in_price == "":
                        in_price = '<td class="text-center "><span class="label label-danger ">null</span></td>'

                    if in_fx_rate == "":
                        in_fx_rate = '<td class="text-center "><span class="label label-danger ">null</span></td>'
                    ##
                    if last_fx_rate == "":
                        last_fx_rate = '<td class="text-center "><span class="label label-danger ">null</span></td>'

                    data_obj = {
                        'date':date,
                        'bloombergTicker':data.get('Bloomberg Ticker*'),
                        'security': data.get('Security*'),
                        'last_price': last_price,
                        'in_price': in_price,
                        'one_d': one_d,
                        'in_fx_rate': in_fx_rate,
                        'last_fx_rate': last_fx_rate,
                        'status': '<td class="text-center "><span class="label label-danger ">Mismatch</span></td>'
                    }
                    data_list.append(data_obj)

            except Security_Details.DoesNotExist, e:
                print "object error: ", e
                date = data.get('Date*')
                last_price = data.get('Last Price*')
                in_price = data.get('In Price*')
                one_d = data.get('%1D')
                in_fx_rate = data.get('In FX Rate*')
                last_fx_rate = data.get('Last FX Rate*')

                if re.match("^\d+?\.\d+?$", last_price) is None:
                    if not last_price.isdigit():
                        last_price = '<td class="text-center "><span class="label label-danger ">' + data.get(
                            'Last Price*') + '</span></td>'

                if re.match("^\d+?\.\d+?$", in_price) is None:
                    if not in_price.isdigit():
                        in_price = '<td class="text-center "><span class="label label-danger ">' + data.get(
                            'In Price*') + '</span></td>'

                if re.match("^\d+?\.\d+?$", in_fx_rate) is None:
                    if not in_fx_rate.isdigit():
                        in_fx_rate = '<td class="text-center "><span class="label label-danger ">' + data.get(
                            'In FX Rate*') + '</span></td>'

                if re.match("^\d+?\.\d+?$", last_fx_rate) is None:
                    if not last_fx_rate.isdigit():
                        last_fx_rate = '<td class="text-center "><span class="label label-danger ">' + data.get(
                            'Last FX Rate*') + '</span></td>'

                data_obj = {
                    'date':date,
                    'bloombergTicker':'<td class="text-center "><span class="label label-danger ">' + data.get(
                        'Bloomberg Ticker*') + '</span></td>',
                    'security': '<td class="text-center "><span class="label label-danger ">' + data.get(
                        'Security*') + '</span></td>',
                    'last_price': last_price,
                    'in_price': in_price,
                    'one_d': one_d,
                    'in_fx_rate': in_fx_rate,
                    'last_fx_rate': last_fx_rate,
                    'status': '<td class="text-center "><span class="label label-danger ">Mismatch</span></td>'
                }
                data_list.append(data_obj)

            except AttributeError, e:
                print "AttributeError: ", e
                date = data.get('Date*')
                last_price = data.get('Last Price*')
                in_price = data.get('In Price*')
                one_d = data.get('%1D')
                in_fx_rate = data.get('In FX Rate*')
                last_fx_rate = data.get('Last FX Rate*')

                if re.match("^\d+?\.\d+?$", last_price) is None:
                    if not last_price.isdigit():
                        last_price = '<td class="text-center "><span class="label label-danger ">' + data.get(
                            'Last Price*') + '</span></td>'

                if re.match("^\d+?\.\d+?$", in_price) is None:
                    if not in_price.isdigit():
                        in_price = '<td class="text-center "><span class="label label-danger ">' + data.get(
                            'In Price*') + '</span></td>'

                if re.match("^\d+?\.\d+?$", in_fx_rate) is None:
                    if not in_fx_rate.isdigit():
                        in_fx_rate = '<td class="text-center "><span class="label label-danger ">' + data.get(
                            'In FX Rate*') + '</span></td>'

                if re.match("^\d+?\.\d+?$", last_fx_rate) is None:
                    if not last_fx_rate.isdigit():
                        last_fx_rate = '<td class="text-center "><span class="label label-danger ">' + data.get(
                            'Last FX Rate*') + '</span></td>'

                data_obj = {
                    'date':date,
                    'bloombergTicker':'<td class="text-center "><span class="label label-danger ">' + data.get(
                        'Bloomberg Ticker*') + '</span></td>',
                    'security': '<td class="text-center "><span class="label label-danger ">' + data.get(
                        'Security*') + '</span></td>',
                    'last_price': last_price,
                    'in_price': in_price,
                    'one_d': one_d,
                    'in_fx_rate': in_fx_rate,
                    'last_fx_rate': last_fx_rate,
                    'status': '<td class="text-center "><span class="label label-danger ">Mismatch</span></td>'
                }
                data_list.append(data_obj)

            except ValueError as e:
                print "Value error: ", e
                date = data.get('Date*')
                last_price = data.get('Last Price*')
                in_price = data.get('In Price*')
                one_d = data.get('%1D')
                in_fx_rate = float(data.get('In FX Rate*'))
                last_fx_rate = float(data.get('Last FX Rate*'))

                if re.match("^\d+?\.\d+?$", last_price) is None:
                    if not last_price.isdigit():
                        last_price = '<td class="text-center "><span class="label label-danger ">' + data.get(
                            'Last Price*') + '</span></td>'

                if re.match("^\d+?\.\d+?$", in_price) is None:
                    if not in_price.isdigit():
                        in_price = '<td class="text-center "><span class="label label-danger ">' + data.get(
                            'In Price*') + '</span></td>'

                if re.match("^\d+?\.\d+?$", in_fx_rate) is None:
                    if not in_fx_rate.isdigit():
                        in_fx_rate = '<td class="text-center "><span class="label label-danger ">' + data.get(
                            'In FX Rate*') + '</span></td>'

                if re.match("^\d+?\.\d+?$", last_fx_rate) is None:
                    if not last_fx_rate.isdigit():
                        last_fx_rate = '<td class="text-center "><span class="label label-danger ">' + data.get(
                            'Last FX Rate*') + '</span></td>'

                data_obj = {
                    'date':date,
                    'bloombergTicker':data.get('Bloomberg Ticker*'),
                    'security': data.get('Security*'),
                    'last_price': last_price,
                    'in_price': in_price,
                    'one_d': one_d,
                    'in_fx_rate': in_fx_rate,
                    'last_fx_rate': last_fx_rate,
                    'status': '<td class="text-center "><span class="label label-danger ">Mismatch</span></td>'
                }
                data_list.append(data_obj)

        if data_list == []:
            print data_list
            data = {'success': 'true', 'data_list': data_list}
        else:
            data = {'success': 'false', 'data_list': data_list}
    except Exception, e:
        print "Exception: ", e
        data = {'success': 'false', 'data_list': data_list}
    return HttpResponse(json.dumps(data), content_type='application/json')




@csrf_exempt
def add_bulk_price01(request):
    try:
        bulk_data = request.POST.get('totalData')
        bulk_data_info = json.loads(bulk_data)
        data_list = []
        for data in bulk_data_info:
            security = data.get('Security*')
            bloombergTicker=data.get('Bloomberg Ticker*')
            try:
                #security_obj = Security_Details.objects.get(security_bloomer_ticker=bloombergTicker,record_status="Active")


                security_obj = Security_Details.objects.filter(security_name=security).order_by(
                    '-security_created_date')
                security = security_obj.first()
                security_obj = Security_Details.objects.get(security_id=security.security_id)


                date = data.get('Date*')
                last_price = float(data.get('Last Price*'))
                in_price = float(data.get('In Price*'))
                one_d = data.get('%1D')
                #print one_d
                if one_d =="":
                    one_d = 0
                else:
                    one_d = float(data.get('%1D'))

                in_fx_rate = float(data.get('In FX Rate*'))
                last_fx_rate = float(data.get('Last FX Rate*'))
                usd_in = in_price/in_fx_rate
                usd_last = last_price/last_fx_rate

                if security_obj and data.get('Last Price*') != "" and data.get('In Price*') != "" and data.get(
                        'In FX Rate*') != "" and data.get('Last FX Rate*') != "":
                    print "adding price object"
                    securityPrice_obj = Security_Price_Details(
                        security_id=security_obj,
                        security_price_date = datetime.strptime(data.get('Date*'),'%d/%m/%Y').date(),
                        security_last_price=last_price,
                        security_in_price=in_price,
                        security_usd_in = usd_in,
                        security_usd_last = usd_last,
                        security_fx_rate_in=in_fx_rate,
                        security_fx_rate_last=last_fx_rate,
                        security_one_d=one_d,
                        record_status='Active',
                        security_price_created_by='Admin',
                        security_price_updated_by='Admin',
                        security_price_created_date=datetime.now(),
                        security_price_updated_date=datetime.now(),
                    )
                    securityPrice_obj.save()
                    print securityPrice_obj
                    data = {'success': 'true'}

                else:
                    date = data.get('Date*')
                    last_price = data.get('Last Price*')
                    in_price = data.get('In Price*')
                    one_d = data.get('%1D')
                    in_fx_rate = data.get('In FX Rate*')
                    last_fx_rate = data.get('Last FX Rate*')

                    if date == "":
                        date = '<td class="text-center "><span class="label label-danger ">null</span></td>'

                    if last_price == "":
                        last_price = '<td class="text-center "><span class="label label-danger ">null</span></td>'

                    if in_price == "":
                        in_price = '<td class="text-center "><span class="label label-danger ">null</span></td>'

                    if in_fx_rate == "":
                        in_fx_rate = '<td class="text-center "><span class="label label-danger ">null</span></td>'
                    ##
                    if last_fx_rate == "":
                        last_fx_rate = '<td class="text-center "><span class="label label-danger ">null</span></td>'

                    data_obj = {
                        'date':date,
                        'security': data.get('Security*'),
                        'last_price': last_price,
                        'in_price': in_price,
                        'one_d': one_d,
                        'in_fx_rate': in_fx_rate,
                        'last_fx_rate': last_fx_rate,
                        'status': '<td class="text-center "><span class="label label-danger ">Mismatch</span></td>'
                    }
                    data_list.append(data_obj)

            except Security_Details.DoesNotExist, e:
                print "object error: ", e
                date = data.get('Date*')
                last_price = data.get('Last Price*')
                in_price = data.get('In Price*')
                one_d = data.get('%1D')
                in_fx_rate = data.get('In FX Rate*')
                last_fx_rate = data.get('Last FX Rate*')

                if re.match("^\d+?\.\d+?$", last_price) is None:
                    if not last_price.isdigit():
                        last_price = '<td class="text-center "><span class="label label-danger ">' + data.get(
                            'Last Price*') + '</span></td>'

                if re.match("^\d+?\.\d+?$", in_price) is None:
                    if not in_price.isdigit():
                        in_price = '<td class="text-center "><span class="label label-danger ">' + data.get(
                            'In Price*') + '</span></td>'

                if re.match("^\d+?\.\d+?$", in_fx_rate) is None:
                    if not in_fx_rate.isdigit():
                        in_fx_rate = '<td class="text-center "><span class="label label-danger ">' + data.get(
                            'In FX Rate*') + '</span></td>'

                if re.match("^\d+?\.\d+?$", last_fx_rate) is None:
                    if not last_fx_rate.isdigit():
                        last_fx_rate = '<td class="text-center "><span class="label label-danger ">' + data.get(
                            'Last FX Rate*') + '</span></td>'

                data_obj = {
                    'date':date,
                    'bloombergTicker':data.get('Bloomberg Ticker*'),
                    'security': '<td class="text-center "><span class="label label-danger ">' + data.get(
                        'Security*') + '</span></td>',
                    'last_price': last_price,
                    'in_price': in_price,
                    'one_d': one_d,
                    'in_fx_rate': in_fx_rate,
                    'last_fx_rate': last_fx_rate,
                    'status': '<td class="text-center "><span class="label label-danger ">Mismatch</span></td>'
                }
                data_list.append(data_obj)

            except AttributeError, e:
                print "AttributeError: ", e
                date = data.get('Date*')
                last_price = data.get('Last Price*')
                in_price = data.get('In Price*')
                one_d = data.get('%1D')
                in_fx_rate = data.get('In FX Rate*')
                last_fx_rate = data.get('Last FX Rate*')

                if re.match("^\d+?\.\d+?$", last_price) is None:
                    if not last_price.isdigit():
                        last_price = '<td class="text-center "><span class="label label-danger ">' + data.get(
                            'Last Price*') + '</span></td>'

                if re.match("^\d+?\.\d+?$", in_price) is None:
                    if not in_price.isdigit():
                        in_price = '<td class="text-center "><span class="label label-danger ">' + data.get(
                            'In Price*') + '</span></td>'

                if re.match("^\d+?\.\d+?$", in_fx_rate) is None:
                    if not in_fx_rate.isdigit():
                        in_fx_rate = '<td class="text-center "><span class="label label-danger ">' + data.get(
                            'In FX Rate*') + '</span></td>'

                if re.match("^\d+?\.\d+?$", last_fx_rate) is None:
                    if not last_fx_rate.isdigit():
                        last_fx_rate = '<td class="text-center "><span class="label label-danger ">' + data.get(
                            'Last FX Rate*') + '</span></td>'

                data_obj = {
                    'date':date,
                    'security': '<td class="text-center "><span class="label label-danger ">' + data.get(
                        'Security*') + '</span></td>',
                    'last_price': last_price,
                    'in_price': in_price,
                    'one_d': one_d,
                    'in_fx_rate': in_fx_rate,
                    'last_fx_rate': last_fx_rate,
                    'status': '<td class="text-center "><span class="label label-danger ">Mismatch</span></td>'
                }
                data_list.append(data_obj)

            except ValueError as e:
                print "Value error: ", e
                date = data.get('Date*')
                last_price = data.get('Last Price*')
                in_price = data.get('In Price*')
                one_d = data.get('%1D')
                in_fx_rate = float(data.get('In FX Rate*'))
                last_fx_rate = float(data.get('Last FX Rate*'))

                if re.match("^\d+?\.\d+?$", last_price) is None:
                    if not last_price.isdigit():
                        last_price = '<td class="text-center "><span class="label label-danger ">' + data.get(
                            'Last Price*') + '</span></td>'

                if re.match("^\d+?\.\d+?$", in_price) is None:
                    if not in_price.isdigit():
                        in_price = '<td class="text-center "><span class="label label-danger ">' + data.get(
                            'In Price*') + '</span></td>'

                if re.match("^\d+?\.\d+?$", in_fx_rate) is None:
                    if not in_fx_rate.isdigit():
                        in_fx_rate = '<td class="text-center "><span class="label label-danger ">' + data.get(
                            'In FX Rate*') + '</span></td>'

                if re.match("^\d+?\.\d+?$", last_fx_rate) is None:
                    if not last_fx_rate.isdigit():
                        last_fx_rate = '<td class="text-center "><span class="label label-danger ">' + data.get(
                            'Last FX Rate*') + '</span></td>'

                data_obj = {
                    'date':date,
                    'bloombergTicker':data.get('Bloomberg Ticker*'),
                    'security': data.get('Security*'),
                    'last_price': last_price,
                    'in_price': in_price,
                    'one_d': one_d,
                    'in_fx_rate': in_fx_rate,
                    'last_fx_rate': last_fx_rate,
                    'status': '<td class="text-center "><span class="label label-danger ">Mismatch</span></td>'
                }
                data_list.append(data_obj)

        if data_list == []:
            print data_list
            data = {'success': 'true', 'data_list': data_list}
        else:
            data = {'success': 'false', 'data_list': data_list}
    except Exception, e:
        print "Exception: ", e
        data = {'success': 'false', 'data_list': data_list}
    return HttpResponse(json.dumps(data), content_type='application/json')




@csrf_exempt
def delete_security_price(request):
    try:
        price_id = request.GET.get('price_id')
        price=Security_Price_Details.objects.get(security_price_id=price_id)
        price.record_status='Inactive'
        price.save()
        data={'success':'true'}
    except Exception, e:
        print 'Exception : ', e
        data = {'data': 'error_msg'}
    return HttpResponse(json.dumps(data), content_type='application/json')
