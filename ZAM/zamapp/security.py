import pdb
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.views.decorators.csrf import csrf_exempt
from zamapp.captcha_form import CaptchaForm
from zamapp.models import *
import datetime
import json


def open_security_page(request):
    if request.user.is_authenticated():
        return render(request,'security_index.html')

    form = CaptchaForm()
    return render_to_response('login.html', dict(
            form=form
        ), context_instance=RequestContext(request))


def open_add_bulk_security_page(request):
    if request.user.is_authenticated():
        return render(request,'security_bulk_add.html')
    form = CaptchaForm()
    return render_to_response('login.html', dict(
            form=form
        ), context_instance=RequestContext(request))


def get_securitydata_list(request):
    try:
        securityobj_list = Security_Details.objects.filter(record_status='Active')
        security_list = []
        for security in securityobj_list:
            view =   '<a href=/view-security-details/?security_id='+ str(security.security_id)  +'&flag=view'+' class="infont"> ''<i class="fa fa-eye"></i></i></a>'
            edit = '<a href="/edit-security-details/?security_id=' + str(security.security_id) +'&flag=edit'+'"class="infont">' + '<i class="fa fa-edit"></i></i>  </a>'    
            delete = '<a ' + str(
                security.security_id) + '" class="infont delete"> ' + '<i class="fa fa-trash-o"></i></i>  </a>' 

            security_obj = {
                'id':security.security_id,
                'security': security.security_name,
                'bloombergTicker': security.security_bloomer_ticker,
                'type': security.security_type.securitytype,
                'benchmarkIndex': security.security_benchmark_index.benchmarkindex,
                'currency': security.security_local_currency.currency,
                'beta': security.security_beta,
                'updatedDate':security.security_updated_date.strftime('%d/%m/%Y'),
                'view': view,
                'edit': edit,
                'delete':delete
            }
            security_list.append(security_obj)
        data = {'data': security_list}
    except Exception, e:
        print 'Exception at security list: ', e
        data = {'data': 'none'}
    return HttpResponse(json.dumps(data), content_type='application/json')


def open_add_security_page(request):   
##    pdb.set_trace()
    try:
        data = {}
        asset_class_list = add_to_dropdown(Asset_Class_Details)
        sub_asset_class_list = add_to_dropdown(Asset_Sub_Class_Details)
        country_list = add_to_dropdown(SecurityCountry)
        currency_list = add_to_dropdown(Currency)
        state_list = add_to_dropdown(SecurityState)
        securitytype_list = add_to_dropdown(SecurityType)
        benchmarkindex_list = add_to_dropdown(BenchmarkIndex)
        sector_list = add_to_dropdown(SecuritySector)
        print '===============Currency=================='
        print currency_list
        print '===============End Currency=================='
        print asset_class_list
        data = {'asset_class_list': asset_class_list,
                'sub_asset_class_list': sub_asset_class_list,
                'country_list': country_list,
                'currency_list': currency_list,
                'state_list': state_list,
                'securitytype_list': securitytype_list,
                'benchmarkindex_list': benchmarkindex_list,
                'sector_list':sector_list,               
                }
        print '===============Data=================='
        print data
    except Exception, e:
        print e;
    print '----------------End-----------------'
    return render(request, 'security_add.html', data)


@csrf_exempt
def save_security_details(request):
    print '==============security save===================',request.POST
    #pdb.set_trace()
    try:
        print request.POST
        if request.method == "POST":
            ticker=check_security_bloomer_ticker_insave(request.POST['txtbloombergticker'])
            if ticker=='not_available':
                security_obj = Security_Details(
                    asset_sub_class_id=Asset_Sub_Class_Details.objects.get(asset_sub_class_id=request.POST['selectAssetSubClass']),
                    security_name=request.POST['txtSecurity'],
                    security_isin=request.POST['txtIsin'],
                    security_type=SecurityType.objects.get(securitytype_id=request.POST['selectType']),
                    security_benchmark_index=BenchmarkIndex.objects.get(
                    benchmarkindex_id=request.POST['selectBenchmarkIndex']),
                    security_bloomer_ticker=request.POST['txtbloombergticker'],
                    security_security_state=SecurityState.objects.get(state_id=request.POST['selectSecurityState']),
                    security_local_currency=Currency.objects.get(currency_id=request.POST['selectCurrency']),
                    country_id=SecurityCountry.objects.get(country_id=request.POST['selectCountry']),
                    sector_id=SecuritySector.objects.get(sector_id=request.POST['selectSector']),
                    security_beta=check_float_val(request.POST['txtBeta']),
                    security_lot_size=check_int_val(request.POST['txtLotSize']),
                    record_status='Active',
                    security_created_by=request.session['login_user'],
                    security_updated_by=request.session['login_user'],
                    security_updated_date=datetime.datetime.now(),
                    security_created_date=datetime.datetime.now()
                )
                security_obj.save()
                result={'success':'true'}
            elif ticker=='available':
                result={'success':'ticker_available'}
            else:
                raise "ticker error!"
    except Exception, e:
        print 'Exception: ' + e
        result={'success':'false'}
    #return redirect('/open-security-page/')
    return HttpResponse(json.dumps(result), content_type='application/json')

@csrf_exempt
def update_security_details(request):
    try:
        #pdb.set_trace()
        print request.POST
        if request.method == "POST":

            ticker=check_security_bloomer_ticker_inupdate(request.POST['txtbloombergticker'],request.POST['txtSecurity_id'])
            if ticker=='not_available':
                security_obj=Security_Details.objects.get(security_id=request.POST['txtSecurity_id'])
                security_obj.record_status='Inactive'
                security_obj.security_updated_by=request.session['login_user']
                security_obj.security_updated_date=datetime.datetime.now().date()
                security_obj.save()

                security_new_obj=Security_Details()
                security_new_obj.asset_sub_class_id=Asset_Sub_Class_Details.objects.get(asset_sub_class_id=request.POST['selectAssetSubClass'])
                security_new_obj.security_name=request.POST['txtSecurity']
                security_new_obj.security_isin=request.POST['txtIsin']
                security_new_obj.security_type=SecurityType.objects.get(securitytype_id=request.POST['selectType'])
                security_new_obj.security_bloomer_ticker=request.POST['txtbloombergticker']
                security_new_obj.security_benchmark_index=BenchmarkIndex.objects.get(benchmarkindex_id=request.POST['selectBenchmarkIndex'])
                security_new_obj.security_security_state=SecurityState.objects.get(state_id=request.POST['selectSecurityState'])
                security_new_obj.security_local_currency=Currency.objects.get(currency_id=request.POST['selectCurrency'])
                security_new_obj.country_id=SecurityCountry.objects.get(country_id=request.POST['selectCountry'])
                security_new_obj.sector_id=SecuritySector.objects.get(sector_id=request.POST['selectSector'])
                security_new_obj.security_beta=check_float_val(request.POST['txtBeta'])
                #print '==========>value check',check_float_val(request.POST['txtLotSize'])
                security_new_obj.security_lot_size=check_int_val(request.POST.get('txtLotSize'))
                security_new_obj.record_status='Active'
                security_new_obj.security_created_by=security_obj.security_created_by
                security_new_obj.security_created_date=security_obj.security_created_date
                security_new_obj.security_updated_by=request.session['login_user']
                security_new_obj.security_updated_date=datetime.datetime.now().date()
                security_new_obj.save()

                security_price_list=Security_Price_Details.objects.filter(security_id=security_obj,record_status='Active')
                if security_price_list:
                    for price in security_price_list:
                        price.security_id=security_new_obj
                        price.save()

                trade_list=Trade_Details.objects.filter(security_id=security_obj,record_status='Active')
                if trade_list:
                    for trade in trade_list:
                        trade.security_id=security_new_obj
                        trade.save()
                result={'success':'true'}
            elif ticker=='available':
                result={'success':'ticker_available'}
            else:
                raise "ticker error!"
    except Exception, e:
        print 'Security.py|update_security_details|Exception: ', e
        result={'success':'false'}
    return HttpResponse(json.dumps(result), content_type='application/json')


def view_security_details(request):
    #pdb.set_trace()
    print '===================view security==============='
    try:
        if request.method=='GET':
            print "security_id ",request.GET.get('security_id')
            flag = request.GET.get('flag', '')
            print "FLAG",flag
            security_obj=Security_Details.objects.get(security_id=request.GET['security_id'])
            print '====security Object==='
            print security_obj
            asset_class_list = add_to_dropdown(Asset_Class_Details)
            sub_asset_class_list = Asset_Sub_Class_Details.objects.filter(asset_class_id=security_obj.asset_sub_class_id.asset_class_id)
            benchmarkindex_list = add_to_dropdown(BenchmarkIndex)
            country_list = add_to_dropdown(SecurityCountry)
            currency_list=add_to_dropdown(Currency)
            #currency_list=Currency.objects.filter(country_id=security_obj.security_local_currency.country_id)
            state_list = add_to_dropdown(SecurityState)
            securitytype_list = add_to_dropdown(SecurityType)
            sector_list = add_to_dropdown(SecuritySector)

            data={
                'success':'true',
                'asset_class_list':asset_class_list,
                'sub_asset_class_list':sub_asset_class_list,
                'benchmarkindex_list':benchmarkindex_list,
                'country_list':country_list,
                'state_list':state_list,
                'securitytype_list':securitytype_list,
                'currency_list':currency_list,
                'sector_list':sector_list,
                'flag':flag,
                'security_lot_size':security_obj.security_lot_size,
                'asset_class_id':security_obj.asset_sub_class_id.asset_class_id,
                'asset_sub_class_id':security_obj.asset_sub_class_id,
                'security_benchmark_index':security_obj.security_benchmark_index,
                'country':security_obj.country_id,
                'security_local_currency':security_obj.security_local_currency,
                'security_type':security_obj.security_type,
                'security_security_state':security_obj.security_security_state,

                'sector':security_obj.sector_id.sector_id,
                'security_id':security_obj.security_id,
                'security_name':security_obj.security_name,
                'security_isin':security_obj.security_isin,
                'security_bloomer_ticker':security_obj.security_bloomer_ticker,
                'security_beta':security_obj.security_beta,
                'record_status':security_obj.record_status,
                'security_created_by':security_obj.security_created_by,
                'security_updated_by':security_obj.security_updated_by,
                'security_created_date':security_obj.security_created_date.strftime('%d/%m/%Y'),
                'security_updated_date':security_obj.security_updated_date.strftime('%d/%m/%Y'),
            }
            print '========success Data==========='
            print data
            return render(request, 'security_view.html', data)
        else:
            data={'success':'false'}
    except Exception,e:
        print '----error----'
        print e
        data={'success':'false'}
    return render(request, 'security_view.html', data)

def add_currency_security(request):
    try:
        result_list = []
        country_obj = SecurityCountry.objects.get(country_id=request.GET["id"])
        currency_list = Currency.objects.filter(country_id=country_obj)
        for currency in currency_list:
            result_list.append({
                'id': currency.currency_id,
                'name': currency.currency,
            })
        data = {'success': 'true', 'result': result_list}
        print data
    except Exception, e:
        print e
        data = {'success': 'false'}
    return HttpResponse(json.dumps(data), content_type='application/json')



def add_bloombergTicker_list(request):
    try:
        result_list = []
        subassetclass_obj = Asset_Sub_Class_Details.objects.get(asset_sub_class_id=request.GET["id"])
        security_list = Security_Details.objects.filter(asset_sub_class_id=subassetclass_obj,record_status='Active')
        for security in security_list:
            result_list.append({
                'id': security.security_id,
                'name': security.security_bloomer_ticker,
            })
        data = {'success': 'true', 'result': result_list}
        print 'data: change event'
        print data
    except Exception, e:
        print e
        data = {'success': 'false'}
    return HttpResponse(json.dumps(data), content_type='application/json')


def add_security_intextbox(request):
    try:
        security_list = Security_Details.objects.get(security_id=request.GET.get("id"),record_status='Active')
        data = {'success': 'true', 'result': security_list.security_name}
        print data
    except Exception, e:
        print e
        data = {'success': 'false'}
    return HttpResponse(json.dumps(data), content_type='application/json')


def add_securities_list(request):
    try:
        result_list = []
        subassetclass_obj = Asset_Sub_Class_Details.objects.get(asset_sub_class_id=request.GET["id"])
        security_list = Security_Details.objects.filter(asset_sub_class_id=subassetclass_obj,record_status='Active')
        for security in security_list:
            result_list.append({
                'id': security.security_id,
                'name': security.security_name,
            })
        data = {'success': 'true', 'result': result_list}
        print 'data: change event'
        print data
    except Exception, e:
        print e
        data = {'success': 'false'}
    return HttpResponse(json.dumps(data), content_type='application/json')


def add_subassetclass_security(request):
##    pdb.set_trace()
    try:
        result_list = []
        assetclass_obj = Asset_Class_Details.objects.get(asset_class_id=request.GET["id"])
        print assetclass_obj
        print '----------------------------'
        subassetclass_list = Asset_Sub_Class_Details.objects.filter(asset_class_id=assetclass_obj)
        print subassetclass_list
        for subassetclass in subassetclass_list:
            result_list.append({
                'id': subassetclass.asset_sub_class_id,
                'name': subassetclass.asset_sub_class_name,
            })
        data = {'success': 'true', 'result': result_list}
        print data
    except Exception, e:
        print '---exception----'
        print e
        data = {'success': 'false'}
    return HttpResponse(json.dumps(data), content_type='application/json')


def check_security_bloomer_ticker_insave(ticker):
    try:
        security_obj=Security_Details.objects.filter(security_bloomer_ticker=ticker,record_status='Active')
        if security_obj:
            return 'available'
        else:
            return 'not_available'
    except Exception,e:
        print 'security.py|security_bloomer_ticker|error ',e
        return 'error'


def check_security_bloomer_ticker_inupdate(ticker,security):
    try:
        #pdb.set_trace()
        #security_obj=Security_Details.objects.get(security_id=security)
        security_obj=Security_Details.objects.exclude(security_id=security).filter(security_bloomer_ticker=ticker,record_status='Active')
        if security_obj:
            return 'available'
        else:
            return 'not_available'
    except Exception,e:
        print 'security.py|security_bloomer_ticker|error ',e
        return 'error'


def add_to_dropdown(table_name):
    data_list = table_name.objects.filter()
    print data_list
    return data_list


def check_float_val(str):
    try:
        float(str)
        return str
    except Exception, e:
        print 'security.py|check_float_val| Exception',e
        str=None
    return str

def check_int_val(str):
    try:
        int(str)
        return str
    except Exception, e:
        print 'security.py|check_float_val| Exception',e
        str=0
    return str

@csrf_exempt
def add_bulk_security(request):
    try:
        #pdb.set_trace()
        bulk_data = request.POST.get('totalData')
        bulk_data_info = json.loads(bulk_data)
        data_list = []
        for data in bulk_data_info:
            security = data.get('Security*')
            as_cls = data.get('Asset Class*')
            as_sub_cls = data.get('Asset Sub Class*')
            sector = data.get('Sector*')
            bench_index = data.get('Benchmark Index*')
            curncy = data.get('Currency*')
            sec_type = data.get('Type*')
            sec_state = data.get('State*')
            country  = data.get('Country*')
            lot_size  = data.get('Lot Size*')
            isin = data.get('ISIN')
            bloom_ticker = data.get('Bloomberg Ticker*')
            sec_beta = data.get('Beta')
            try:
                print "Checking objects"
                asset_obj = check_asset_obj(as_cls);
                if asset_obj == "error":
                    as_sub_obj = "error"
                else:
                    as_sub_obj = check_as_sub_obj(as_sub_cls,asset_obj);

                sec_type_obj = check_sec_type_obj(sec_type)
                bench_in_obj = check_bench_in_obj(bench_index)
                sec_state_obj = check_sec_state_obj(sec_state)
                curncy_obj = check_curncy_obj(curncy)
                sector_obj = check_sector_obj(sector)
                country_obj = check_country_obj(country)
                ticker=check_security_bloomer_ticker_insave(bloom_ticker)

                if asset_obj == "error" or as_sub_obj == "error" or sec_type_obj == "error" or bench_in_obj == "error" or sec_state_obj == "error" or curncy_obj == "error" or sector_obj=="error"  or country_obj == "error" or ticker=='available':
                    status='<td class="text-center "><span class="label label-danger ">Mismatch</span></td>'
                    if asset_obj == "error":
                        asset_obj = '<td class="text-center "><span class="label label-danger ">' + as_cls + '</span></td>'
                    else:
                        asset_obj = as_cls
                    if as_sub_obj == "error":
                        as_sub_obj = '<td class="text-center "><span class="label label-danger ">' + as_sub_cls + '</span></td>'
                    else:
                        as_sub_obj = as_sub_cls
                    if sec_type_obj == "error":
                        sec_type_obj = '<td class="text-center "><span class="label label-danger ">'+ sec_type +'</span></td>'
                    else:
                        sec_type_obj = sec_type
                    if bench_in_obj == "error":
                        bench_in_obj = '<td class="text-center "><span class="label label-danger ">'+ bench_index +'</span></td>'
                    else:
                        bench_in_obj = bench_index
                    if sec_state_obj == "error":
                        sec_state_obj = '<td class="text-center "><span class="label label-danger ">'+ sec_state +'</span></td>'
                    else:
                        sec_state_obj = sec_state
                    if curncy_obj == "error":
                        curncy_obj = '<td class="text-center "><span class="label label-danger ">'+ curncy +'</span></td>'
                    else:
                        curncy_obj = curncy

                    if sector_obj == "error":
                        sector_obj = '<td class="text-center "><span class="label label-danger ">'+ sector +'</span></td>'
                    else:
                        sector_obj = sector
                        
                    if country_obj == "error":
                        country_obj = '<td class="text-center "><span class="label label-danger ">'+ country +'</span></td>'
                    else:
                        country_obj = country

                    if ticker=='available':
                        bloom_ticker = '<td class="text-center "><span class="label label-danger ">'+ bloom_ticker +'</span></td>'
                        status='<td class="text-center "><span style="cursor:pointer;" title="Bloomberg Ticker aleardy exists" class="label label-danger ">Aleardy Exists</span></td>'

                    data_obj = {
                        'security' : security,
                        'as_cls' : asset_obj,
                        'as_sub_cls' : as_sub_obj,
                        'sector':sector_obj,
                        'bench_index' : bench_in_obj,
                        'currency' : curncy_obj,
                        'sec_type' : sec_type_obj,
                        'sec_state' : sec_state_obj ,
                        'country' : country_obj,
                        'lot_size' : lot_size,
                        'isin' : isin,
                        'bloom_ticker' : bloom_ticker,
                        'sec_beta' : sec_beta,
                        'status':status
                        }
                    data_list.append(data_obj)
                else:
                    security_objs = Security_Details(
                        asset_sub_class_id = as_sub_obj,
                        security_name = security,
                        country_id = country_obj,
                        sector_id=sector_obj,
                        security_isin = isin,
                        security_type = sec_type_obj,
                        security_benchmark_index = bench_in_obj,
                        security_bloomer_ticker = bloom_ticker,
                        security_security_state = sec_state_obj,
                        security_local_currency = curncy_obj,
                        security_lot_size = lot_size,
                        security_beta = sec_beta,
                        record_status='Active',
                        security_created_by=request.session['login_user'],
                        security_updated_by=request.session['login_user'],
                        security_created_date=datetime.datetime.now(),
                        security_updated_date=datetime.datetime.now()
                    )
                    security_objs.save()
                    print security_objs
                    data = {'success': 'true'}

            except ValueError,e:
                print "Value error: ",e
        if data_list == []:
            print data_list
            data = {'success': 'true','data_list':data_list}
        else:
            data = {'success': 'false','data_list':data_list}
    except Exception,e:
        print "Exception: ",e
        data={'success':'false','data_list':data_list}
    return HttpResponse(json.dumps(data),content_type='application/json')

@csrf_exempt
def change_status(request):
##    pdb.set_trace()
    try:
        stat = request.GET.get('security_id')
        print 'id--', stat
        stat_obj=Security_Details.objects.get(security_id=stat)
        stat_obj.record_status="Inactive"
        stat_obj.save()

        security_price_list=Security_Price_Details.objects.filter(security_id=stat_obj)
        if security_price_list:
            for price in security_price_list:
                price.record_status='Inactive'
                price.save()

        data={'success':'true'}
    except Exception, e:
        print 'Exception : ', e
        data = {'data': 'error_msg'}
    return HttpResponse(json.dumps(data), content_type='application/json')

def check_as_sub_obj(as_sub_cls,asset_obj):
    try:
        ast_sub_obj = Asset_Sub_Class_Details.objects.get(asset_sub_class_name=as_sub_cls, asset_class_id = asset_obj)
    except Asset_Sub_Class_Details.DoesNotExist, e:
        ast_sub_obj = "error"
    return ast_sub_obj

def check_sec_type_obj(sec_type):
    try:
        sec_type_obj = SecurityType.objects.get(securitytype = sec_type)
    except SecurityType.DoesNotExist,e:
        sec_type_obj = "error"
    return sec_type_obj

def check_bench_in_obj(bench_index):
    try:
        bench_in_obj = BenchmarkIndex.objects.get(benchmarkindex = bench_index)
    except BenchmarkIndex.DoesNotExist,e:
        bench_in_obj = "error"
    return bench_in_obj

def check_sec_state_obj(sec_state):
    try:
        sec_state_obj = SecurityState.objects.get(state = sec_state)
    except SecurityState.DoesNotExist,e:
        sec_state_obj = "error"
    return sec_state_obj

def check_curncy_obj(curncy):
    try:
        curncy_obj = Currency.objects.get(currency = curncy)
    except Currency.DoesNotExist,e:
        curncy_obj = "error"
    return curncy_obj


def check_country_obj(country):
    try:
        #pdb.set_trace()
        country_obj = SecurityCountry.objects.get(country_name = country)
    except SecurityCountry.DoesNotExist,e:
        print 'security.py|check_country_obj|error',e
        country_obj = "error"
    return country_obj

def check_sector_obj(sector):
    try:
        sector_obj = SecuritySector.objects.get(sector_name = sector)
    except SecuritySector.DoesNotExist,e:
        sector_obj = "error"
    return sector_obj

def check_asset_obj(as_cls):
    try:
        ast_obj = Asset_Class_Details.objects.get(asset_class_name=as_cls)
    except Asset_Class_Details.DoesNotExist, e:
        ast_obj = "error"
    return ast_obj
