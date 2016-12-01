import pdb
import re
from django.shortcuts import render
from zamapp.models import *
from django.http import HttpResponse
import json
from django.shortcuts import render_to_response
# from django.core.context_processors import csrf
from django.views.decorators.csrf import csrf_exempt
from datetime import date, timedelta
from zamapp.captcha_form import CaptchaForm
from django.template import RequestContext


# Create your views here.

def open_trade(request):
    if request.user.is_authenticated():
        return render(request, 'trade_index.html')
    else:
        form = CaptchaForm()
        return render_to_response('login.html', dict(
            form=form
        ), context_instance=RequestContext(request))


def open_add_trade(request):
    security = []
    if request.user.is_authenticated():
        assets_class = Asset_Class_Details.objects.all()
        assets_sub_class = Asset_Sub_Class_Details.objects.all()
        security_obj = Security_Details.objects.filter(record_status = "Active").values_list('security_name').distinct()
        for sec in security_obj:
            security.append({'value' : sec[0] , 'data' : sec[0]})
        security = json.dumps(security)
        #print security
        data = {'securities': security}
        return render(request, 'trade_add.html', data)
    else:
        form = CaptchaForm()
        return render_to_response('login.html', dict(
            form=form
        ), context_instance=RequestContext(request))


@csrf_exempt
def view_security_list(request):
    try:
        # pdb.set_trace()
        data_list = []
        search_txt = request.POST['search_txt']
        # print search_txt
        security_obj = Security_Details.objects.filter(security_name=search_txt ,record_status = "Active")
        # print security_obj
        if security_obj:
            for security in security_obj:
                data_obj = {
                    'security': security.security_name,
                    'b_ticker': security.security_bloomer_ticker,
                    'asset_cls': security.asset_sub_class_id.asset_class_id.asset_class_name,
                    'asset_sub_cls': security.asset_sub_class_id.asset_sub_class_name,
                    'country': security.security_local_currency.country_id.country_name,
                    'add_btn': '<button id="' + security.security_name + '" name="' + str(
                        security.security_id) + '" value="'+ str(security.security_lot_size) +'" onclick="add_trade_form(this.id,this.name,this.value)" class="btn btn-default btn-primary2 btn-xs btn-outline">Add</button>'
                }
                data_list.append(data_obj)
            data = {'success': 'true', 'data_list': data_list}
            #print data
        else:
            print "None"
            data = {'success': 'false'}
            # print data
    except Security_Details.DoesNotExist as e:
        print 'Exception', e
        data = {'success': 'false'}
    except Exception as e:
        print 'Exception', e
        data = {'success': 'false'}
    return HttpResponse(json.dumps(data), content_type='application/json')

@csrf_exempt
def check_price(request):
    try:
        trade_quantity = 0
        security_id = request.POST['sec_id']
        trade_obj = Trade_Details.objects.filter(security_id = security_id, record_status="Active")
        for trade in trade_obj:
            if trade.buy_sell_indicator == "Buy":
                trade_quantity = trade_quantity + int(trade.trade_security_quantity)
            elif trade.buy_sell_indicator == "Sell":
                trade_quantity = trade_quantity - int(trade.trade_security_quantity)
        print "Trade Quantity: ",trade_quantity
        security_price = Security_Price_Details.objects.filter(security_id = security_id)
        if security_price:
            security_price = "Yes"
        else:
            security_price = "No"
        data = {"security_price" : security_price, "trade_quantity" : trade_quantity}
    except Exception as e:
        print 'Exception', e
    return HttpResponse(json.dumps(data), content_type='application/json')

@csrf_exempt
def view_security_lists(request):
    try:
        # pdb.set_trace()
        data_list = []
        search_txt = request.POST['search_txt']
        # print search_txt
        security_obj = Security_Details.objects.filter(security_name__istartswith=search_txt ,record_status = "Active")
        # print security_obj
        if security_obj:
            for security in security_obj:
                data_obj = {
                    'security': security.security_name,
                    'b_ticker': security.security_bloomer_ticker,
                    'asset_cls': security.asset_sub_class_id.asset_class_id.asset_class_name,
                    'asset_sub_cls': security.asset_sub_class_id.asset_sub_class_name,
                    'country': security.security_local_currency.country_id.country_name,
                    'add_btn': '<button id="' + security.security_name + '" name="' + str(
                        security.security_id) + '" value="'+ str(security.security_lot_size) +'" onclick="add_trade_form(this.id,this.name,this.value)" class="btn btn-default btn-primary2 btn-xs btn-outline">Add</button>'
                }
                data_list.append(data_obj)
            data = {'success': 'true', 'data_list': data_list}
            print data
        else:
            print "None"
            data = {'success': 'false'}
            # print data
    except Security_Details.DoesNotExist as e:
        print 'Exception', e
        data = {'success': 'false'}
    except Exception as e:
        print 'Exception', e
        data = {'success': 'false'}
    return HttpResponse(json.dumps(data), content_type='application/json')


def open_view_trade(request):
    try:
        # pdb.set_trace()
        trade = request.GET.get('trade_id')
        type = request.GET.get('type')
        trade_quantity = 0
        trade_obj = Trade_Details.objects.get(trade_id=trade)
        security_id = trade_obj.security_id.security_id
        trades = Trade_Details.objects.filter(security_id = security_id, record_status="Active")
        for trade in trades:
            if trade.buy_sell_indicator == "Buy":
                trade_quantity = trade_quantity + int(trade.trade_security_quantity)
            elif trade.buy_sell_indicator == "Sell":
                trade_quantity = trade_quantity - int(trade.trade_security_quantity)
        #print "Trade id: ", trade
        #print "Type: ", type
        trade_data = {
            'trade_id': trade_obj.trade_id,
            'trade_date': str(trade_obj.trade_date.strftime('%d/%m/%Y')),
            'buy_sell_indicator': trade_obj.buy_sell_indicator,
            'trade_security_quantity': trade_obj.trade_security_quantity,
            'trade_amount': trade_obj.trade_amount,
            'trade_price': trade_obj.trade_price,
            'fx_price': trade_obj.fx_price,
            'broker': trade_obj.broker,
            'lot_size': trade_obj.lot_size,
            'security_id': trade_obj.security_id.security_id,
            'security_name': trade_obj.security_id.security_name,
            'present_quantity' : trade_quantity
        }
        data = {'trade_obj': trade_data, 'type' : type}
        #print data
    except Exception, e:
        print 'Exception', e
        data = {'success': 'false'}
    return render(request, 'trade_view.html', data)


def open_add_bulk_trade(request):
    if request.user.is_authenticated():
        return render(request, 'trade_bulk_add.html')
    else:
        form = CaptchaForm()
        return render_to_response('login.html', dict(
            form=form
        ), context_instance=RequestContext(request))


@csrf_exempt
def asset_subclass(request):
    try:
        asset_id = request.GET.get('asset_id')
        asset_sub_obj = Asset_Sub_Class_Details.objects.filter(asset_class_id=asset_id)
        options = []
        for asset_sub in asset_sub_obj:
            options_data = '<option value=' + str(
                asset_sub.asset_sub_class_id) + '>' + asset_sub.asset_sub_class_name + '</option>'
            options.append(options_data)
        print options
        data = {'options': options}
    except Exception, e:
        print e
        data = {'success': 'false'}
    return HttpResponse(json.dumps(data), content_type='application/json')


@csrf_exempt
def append_security(request):
    try:
        asset_sub_id = request.GET.get('asset_sub_id')
        print asset_sub_id
        security_obj = Security_Details.objects.filter(asset_sub_class_id=asset_sub_id)
        print security_obj
        options = []
        for security in security_obj:
            options_data = '<option value=' + str(security.security_id) + '>' + security.security_name + '</option>'
            options.append(options_data)
        print options
        data = {'options': options}
    except Exception, e:
        print e
        data = {'success': 'false'}
    return HttpResponse(json.dumps(data), content_type='application/json')


@csrf_exempt
def get_price(request):
    try:
        security = request.POST['security_id']
        # print security
        security_price_obj = Security_Price_Details.objects.filter(security_id=security).order_by(
            '-security_price_created_date')
        s_id = security_price_obj.first()

        # sp_obj = Security_Price_Details.objects.get(security_id=s_id)
        security_price = s_id.security_last_price
        # print security_price
        data = {'success': 'true', 'security_price': security_price}
    except Exception, e:
        print e
        data = {'success': 'false'}
    return HttpResponse(json.dumps(data), content_type='application/json')


@csrf_exempt
def add_trade(request):
    try:
        print "adding trade"
        print request.POST
        a = 0
        date = request.POST.getlist('date')
        sec_id = request.POST.getlist('security_id')
        tr_type = request.POST.getlist('trade_type')
        quantity = request.POST.getlist('quantity')
        trade_price = request.POST.getlist('trade_price')
        fx_price = request.POST.getlist('fx_price')
        amount = request.POST.getlist('amount')
        broker = request.POST.getlist('broker')
        lot_size = request.POST.getlist('lot_size')
        for i in range(len(sec_id)):
            print type(amount[i])
            if date[i] == '':
                continue
            else:
                a = 1
                print date[i]
                security_obj = Security_Details.objects.get(security_id=sec_id[i])
                trade_obj = Trade_Details(
                    security_id=security_obj,
                    trade_date=datetime.strptime(date[i], '%d/%m/%Y').date(),
                    buy_sell_indicator=tr_type[i],
                    trade_security_quantity=quantity[i],
                    trade_amount=amount[i],
                    trade_price=trade_price[i],
                    fx_price=fx_price[i],
                    broker=broker[i],
                    lot_size = lot_size[i],
                    record_status="Active",
                    trade_created_by=request.session['login_user'],
                    trade_updated_by=request.session['login_user'],
                    trade_created_date=datetime.now(),
                    trade_updated_date=datetime.now(),
                )
                trade_obj.save()
        data = {'success': 'true', 'sts':a}
    except Exception, e:
        print e
        data = {'success': 'false'}
    return HttpResponse(json.dumps(data), content_type='application/json')


@csrf_exempt
def view_trades(request):
    trade_obj = Trade_Details.objects.filter(record_status="Active")
    trade_list = []
    for trade in trade_obj:
        view_btn = '<a href="/open-view-trade/?trade_id=' + str(
            trade.trade_id) + '&type=view" class="infont"> ' + '<i class="fa fa-eye"></i></i>  </a>'
        edit_btn = '<a href="/open-view-trade/?trade_id=' + str(
            trade.trade_id) + '&type=edit" class="infont"> ' + '<i class="fa fa-edit"></i></i>  </a>'
        delete_btn = '<a id="'+str(trade.trade_id)+'" onclick=delete_trade(this.id) class="infont"> ' + '<i class="fa fa-trash-o"></i></i>  </a>'
        trade_data = {
            'date': str(trade.trade_date.strftime('%d/%m/%Y')),
            'security': trade.security_id.security_name,
            'trade_type': trade.buy_sell_indicator,
            'quantity': trade.trade_security_quantity,
            'trade_price': trade.trade_price,
            'fx_price': trade.fx_price,
            'trade_amount': trade.trade_amount,
            'broker': trade.broker,
            'view_btn': view_btn,
            'edit_btn': edit_btn,
            'delete_btn': delete_btn,
        }
        trade_list.append(trade_data)
    data = {'data': trade_list}
    #print data
    return HttpResponse(json.dumps(data), content_type='application/json')


@csrf_exempt
def edit_trade(request):
    try:
        print "editng trade"
        security_price_obj = Security_Details.objects.get(security_id=request.POST['security_id'])

        trade_obj = Trade_Details.objects.get(trade_id=request.POST['trade_id'])
        trade_obj.record_status = "Inactive"
        trade_obj.trade_updated_by = request.session['login_user']
        trade_obj.trade_updated_date = datetime.now()
        trade_obj.save()

        trade_new_obj = Trade_Details()
        trade_new_obj.security_id = security_price_obj
        trade_new_obj.trade_date = datetime.strptime(request.POST['date'], '%d/%m/%Y').date()
        trade_new_obj.buy_sell_indicator = request.POST['trade_type']
        trade_new_obj.trade_security_quantity = request.POST['quantity']
        trade_new_obj.trade_amount = request.POST['total_amount']
        trade_new_obj.record_status = "Active"
        trade_new_obj.trade_price = request.POST['trd_price']
        trade_new_obj.fx_price = request.POST['fx_price']
        trade_new_obj.broker = request.POST['broker']
        trade_new_obj.lot_size = request.POST['lot_size']
        trade_new_obj.trade_created_by = request.session['login_user']
        trade_new_obj.trade_created_date = datetime.now()
        trade_new_obj.trade_updated_by = request.session['login_user']
        trade_new_obj.trade_updated_date = datetime.now()
        trade_new_obj.save()

        # print trade_obj
        data = {'success': 'true'}
    except Exception, e:
        print e
        data = {'success': 'false'}
    return HttpResponse(json.dumps(data), content_type='application/json')

@csrf_exempt
def delete_trade(request):
    try:
        print "deleting trade"
        trade_obj = Trade_Details.objects.get(trade_id=request.POST['trade_id'])
        trade_obj.record_status = "Inactive"
        trade_obj.save()
        # print trade_obj
        data = {'success': 'true'}
    except Exception, e:
        print e
        data = {'success': 'false'}
    return HttpResponse(json.dumps(data), content_type='application/json')

@csrf_exempt
def add_bulk_trade(request):
    # pdb.set_trace()
    try:
        bulk_data = request.POST.get('totalData')
        bulk_data_info = json.loads(bulk_data)
        data_list = []
        trade_data = []
        check_list = []
        for data in bulk_data_info:

            security = data.get('Security*')
            b_ticker = data.get('Bloomberg Ticker*')
            as_cls = data.get('Asset Class*')
            as_sub_cls = data.get('Asset Sub Class*')
            quantity = data.get('Quantity*')
            trade_price = data.get('Trade Price*')
            fx_price = data.get('FX Price*')
            Trade_Type = data.get('Trade Type*')
            lot_size = data.get('Lot Size')
            total_amount = data.get('Total Amount')
            broker = data.get('Broker')
            status = '<td class="text-center "><span class="label label-danger " style="cursor: pointer;">Mismatch</span></td>'

            asset_obj = check_asset_obj(as_cls);
            if asset_obj == "error":
                asset_obj = '<td class="text-center "><span class="label label-danger ">' + as_cls + '</span></td>'
                as_sub_obj = "error"
            else:
                as_sub_obj = check_as_sub_obj(as_sub_cls,asset_obj);
                asset_obj = as_cls

            if as_sub_obj == "error":
                security_obj = "error"
                as_sub_obj = '<td class="text-center "><span class="label label-danger ">' + as_sub_cls + '</span></td>'
            else:
                security_obj = check_sec_obj(security,as_sub_obj,b_ticker);
                as_sub_obj = as_sub_cls

            if security_obj == "error" or security_obj == "Add Price":
                if security_obj == "error":
                    security_obj = '<td class="text-center "><span class="label label-danger ">' + security + '</span></td>'
                    blm_ticker = '<td class="text-center "><span class="label label-danger ">' + b_ticker + '</span></td>'
                    status = '<td class="text-center "><span class="label label-danger" style="cursor: pointer;" title="Security not Found">' \
                             'Mismatch</span></td>'
                elif security_obj == "Add Price":
                    security_obj = '<td class="text-center "><span class="label label-danger ">' + security + '</span></td>'
                    blm_ticker = '<td class="text-center "><span class="label label-danger ">' + b_ticker + '</span></td>'
                    status = '<td class="text-center "><span class="label label-warning " style="cursor: pointer;" title="Please add price \nfor this security \nto add trade">' \
                             'Add Price</span></td>'
                else:
                    security_obj = security


                if data.get('Trade Type*') != "Buy" and data.get('Trade Type*') != "Sell" and data.get('Trade Type*') != "Sell Short" and data.get('Trade Type*') != "Cover Short":
                    if data.get('Trade Type*') == "":
                        Trade_Type = '<td class="text-center "><span class="label label-danger ">null</span></td>'
                    else:
                        Trade_Type = '<td class="text-center "><span class="label label-danger ">' + data.get(
                            'Trade Type*') + '</span></td>'

                if quantity == "":
                    quantity = '<td class="text-center "><span class="label label-danger ">null</span></td>'

                if trade_price == "":
                    trade_price = '<td class="text-center "><span class="label label-danger ">null</span></td>'

                if fx_price == "":
                    fx_price = '<td class="text-center "><span class="label label-danger ">null</span></td>'

                data_obj = {'date': data.get('Date*'),
                            'security': security_obj,
                            'b_ticker': blm_ticker,
                            'as_cls': asset_obj,
                            'as_sub_cls': as_sub_obj,
                            'trade_type': Trade_Type,
                            'quantity': quantity,
                            'trade_price': trade_price,
                            'fx_price': fx_price,
                            'lot_size': lot_size,
                            'total_amount': total_amount,
                            'broker': broker,
                            'status': status
                            }
                data_list.append(data_obj)
            else:
                
                if security_obj and data.get('Date*') != "" and data.get('Trade Type*') == "Buy" or data.get(
                        'Trade Type*') == "Sell" or data.get('Trade Type*') == "Sell Short" or data.get('Trade Type*') == "Cover Short" and data.get('Quantity*') != "" and data.get('Trade Price*') != "":
                    #print "security_obj: ",security_obj
                    trade_obj = {
                                    'security_obj':int(security_obj.security_id),
                                    'trade_type':data.get('Trade Type*'),
                                    'quantity':quantity
                                }
                    trade_data.append(trade_obj)
                    
                    data_obj = {'date': data.get('Date*'),
                        'security': int(security_obj.security_id),
                        'security_id': int(security_obj.security_id),
                        'b_ticker': data.get('Bloomberg Ticker*'),
                        'as_cls': asset_obj,
                        'as_sub_cls': as_sub_obj,
                        'trade_type': data.get('Trade Type*'),
                        'quantity': quantity,
                        'trade_price': trade_price,
                        'fx_price': fx_price,
                        'lot_size': lot_size,
                        'total_amount': total_amount,
                        'broker': broker,
                        'status': status
                        }
                    check_list.append(data_obj)   
        
        #print "trade_data: ",trade_data
        
        chck_quantity = check_quantity(trade_data)
        flag = 0
        for check_trd in check_list:
            val = chck_quantity[check_trd['security']]
            if val < 0 :
                flag = 1
                check_trd['status'] = '<td class="text-center "><span class="label label-warning " style="cursor: pointer;" title="Sell trade quantity is\ngreater then buy trade\nquantity">' \
                             'Invalid Data</span></td>'
                check_trd['trade_type'] = '<td class="text-center "><span class="label label-danger ">'+ check_trd['trade_type'] +'</span></td>'
                check_trd['quantity'] = '<td class="text-center "><span class="label label-danger ">'+ check_trd['quantity'] +'</span></td>'
                #print "Security.........false",check_trd['security']
                security = Security_Details.objects.get(security_id=check_trd['security'])
                check_trd['security'] = security.security_name
            else: 
                check_trd['status'] = '<td class="text-center "><span class="label label-success " style="cursor: pointer;">' \
                             'Valid Data</span></td>'
                #print "Security.........ture",check_trd['security']
                security = Security_Details.objects.get(security_id=check_trd['security'])
                check_trd['security'] = security.security_name
        
        if flag == 1 or data_list != []:
            data_list.extend(check_list)
        else:
            sv_trade = save_trades(check_list,request)
            if sv_trade == "saved":
                data_list = []

        if data_list == []:
            data = {'success': 'true', 'data_list': data_list}
        else:
            data = {'success': 'false', 'data_list': data_list}
    except Exception as e:
        print "Exception: ",e
        data = {'success': 'false', 'data_list':''}
    return HttpResponse(json.dumps(data), content_type='application/json')


def check_sec_obj(security,as_sub_obj,b_ticker):
    try:
        sec_obj = Security_Details.objects.get(security_name=security,asset_sub_class_id=as_sub_obj,
                                               security_bloomer_ticker=b_ticker,record_status="Active")
        if sec_obj:
            sec_price = Security_Price_Details.objects.filter(security_id = sec_obj, record_status="Active")
            if sec_price:
                sec_obj = sec_obj
            else:
                sec_obj = "Add Price"
    except Security_Details.DoesNotExist, e:
        sec_obj = "error"
    #print sec_obj
    return sec_obj


def check_asset_obj(as_cls):
    try:
        ast_obj = Asset_Class_Details.objects.get(asset_class_name=as_cls,row_status="Active")
    except Asset_Class_Details.DoesNotExist, e:
        ast_obj = "error"
    return ast_obj

def check_as_sub_obj(as_sub_cls,asset_obj):
    try:
        ast_sub_obj = Asset_Sub_Class_Details.objects.get(asset_sub_class_name=as_sub_cls,
                                                          asset_class_id = asset_obj,row_status="Active")
    except Asset_Sub_Class_Details.DoesNotExist, e:
        ast_sub_obj = "error"
    return ast_sub_obj

def check_quantity(trade_data):

    total_quantity = 0
    sec_list = []
    list2 = []            
    dis = []    
    
    for trade in trade_data:
        if trade["trade_type"]=="Sell" or trade["trade_type"]=="Sell":
            sec_list.append(trade["security_obj"])
        
    unique_list=list(set(sec_list))
    #print "unique_list: ",unique_list

    trd_data = []
    for i in unique_list:
        trd_obj = Trade_Details.objects.filter(security_id=i,record_status="Active")
        for trd in trd_obj:
            trds_obj = {
                'security_obj':int(i),
                'trade_type':trd.buy_sell_indicator,
                'quantity':trd.trade_security_quantity
            }
            trd_data.append(trds_obj)
    #print "trd_data:", trd_data
    trade_data.extend(trd_data)

    test_desc={}    
    for security in trade_data:
        if test_desc.has_key(security['security_obj']):
            if security['trade_type']=='Buy':
                test_desc[security['security_obj']]=test_desc[security['security_obj']]+int(security['quantity'])
            else:
                test_desc[security['security_obj']]=test_desc[security['security_obj']]-int(security['quantity'])
        else:
            if security['trade_type']=='Buy':
                test_desc[security['security_obj']]=0+int(security['quantity'])
            else:
                test_desc[security['security_obj']]=0-int(security['quantity'])
    #print test_desc
    return test_desc

def save_trades(check_list,request):
    try:
        for check_trd in check_list:
            print "saving........"
            security_obj = Security_Details.objects.get(security_id=check_trd['security_id'])
            trade_obj = Trade_Details(
                security_id=security_obj,
                trade_date=datetime.strptime(check_trd['date'], '%d/%m/%Y').date(),
                buy_sell_indicator=check_trd['trade_type'],
                trade_security_quantity=check_trd['quantity'],
                trade_price=check_trd['trade_price'],
                fx_price=check_trd['fx_price'],
                trade_amount=check_trd['total_amount'],
                broker=check_trd['broker'],
                lot_size=check_trd['lot_size'],
                record_status="Active",
                trade_created_by=request.session['login_user'],
                trade_updated_by=request.session['login_user'],
                trade_created_date=datetime.now(),
                trade_updated_date=datetime.now(),
            )
            trade_obj.save()
        trade_status = "saved"
    except Exception as e:
        print "Exception: ",e
        trade_status = "error"
    return trade_status

