import pdb
import re
from sets import Set
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Sum,Avg
from django.shortcuts import render
from zamapp.models import *
from django.http import HttpResponse
import json
from django.shortcuts import render_to_response

from django.views.decorators.csrf import csrf_exempt
from zamapp.captcha_form import CaptchaForm
from django.template import RequestContext


# Create your views here.

def open_postion(request):
    if request.user.is_authenticated():
        position_calculation(request,'load')
        total_trade = Trade_Details.objects.filter(record_status='Active').values('buy_sell_indicator').annotate(
            total_amount=Sum('trade_amount'), total_quantity=Sum('trade_security_quantity'))
        if not total_trade:
            data = {'data': 'None'}
            return render(request, 'position_index.html', data)

        fund_size = 0
        total_shares = 0
        net_principal = 0
        total_pnl = 0

        for trade in total_trade:
            if trade['buy_sell_indicator'] == 'Buy' or trade['buy_sell_indicator']=='Cover Short':
                fund_size = fund_size + trade['total_amount']
                total_shares = total_shares + trade['total_quantity']
            elif trade['buy_sell_indicator'] == 'Sell' or trade['buy_sell_indicator']=='Sell Short':
                fund_size = fund_size - trade['total_amount']
                total_shares = total_shares - trade['total_quantity']

        pos_list = Position_Details.objects.filter(position_status='Active')
        for pos in pos_list:
            net_principal = net_principal + pos.market_value
            total_pnl = total_pnl + pos.profit_and_loss

        print 'total',net_principal
        net_principal_percentage = round((net_principal / fund_size), 2)
        total_pnl_percentage = round((total_pnl / fund_size), 2)

        gross_principl = abs(net_principal)
        gross_principal_percentage=abs(net_principal_percentage)
        total_pnl_percentage = round(total_pnl_percentage/fund_size,2)

        data = {'fund_size': fund_size, 'total_shares': total_shares, 'net_principal': net_principal,
                'net_principal_percentage': net_principal_percentage, 'gross_principl': gross_principl,
                'gross_principal_percentage': gross_principal_percentage, 'total_pnl': total_pnl,
                'total_pnl_percentage': total_pnl_percentage,
                }
        return render(request, 'position_index.html', data)
    else:
        form = CaptchaForm()
        return render_to_response('login.html', dict(
        form=form
    ), context_instance=RequestContext(request))


def get_security_position(request):
    try:
        data = {'data': get_position_list_by_security(request.GET.get('position_date'))}
        print 'request.GET.get(position_date)==>',request.GET.get('position_date')
        print 'get-security-position====>',data
    except Exception, e:
        print 'position.py|get_security_position|error', e
        data = {'success': 'false'}
    return HttpResponse(json.dumps(data), content_type='application/json')


def open_add_bulk_position(request):
    return render(request, 'position_bulk_add.html')


def get_position_list_by_security(position_date):
    #pdb.set_trace()
    position_list = []
    try:
        pos_list = Position_Details.objects.filter(position_status='Active',
                                                   position_date__startswith=datetime.strptime(position_date, '%d/%m/%Y').date())
        for pos in pos_list:
            view = '<a onclick=get_tread(' + str(pos.position_id) + ') class="infont"><i class="fa fa-plus"></i></a>',
            position_list.append({
                'view': view,
                'trading': pos.security_id.security_bloomer_ticker,
                'security': pos.security_id.security_name,
                'last_price': pos.last_price,
                'position': pos.position,
                'move_since_incepton': pos.move_since_incepton,
                'total_quantity': pos.position_security_quntity,
                'in_principal': pos.in_principal,
                'in_price': pos.in_price,
                'market_value': pos.market_value,
                'beta_adj': pos.beta_adj,
                'profit_and_loss': pos.profit_and_loss,
                'contrib_daily': pos.contrib_daily,
                'portfolio_return_contrib': pos.portfolio_return_contrib,
                'FX': pos.FX,
                'beta': pos.beta,
                'FX_in': 1, 'fx_contrib': pos.fx_contrib})
    except Exception, e:
        print 'position.py|get_position_list_by_security|error', e
        data = {'success': 'false'}
    return position_list


def get_position_list_by_country(request):
    # pdb.set_trace()
    position_list = []
    print '---------------get position list by country----------------------', request.GET
    try:
        position_obj = Position_Details.objects.filter(position_status='Active',
                                                       position_date__startswith=datetime.strptime(request.GET.get('position_date'),
                                                                                       '%d/%m/%Y').date()).values(
            'security_id__country_id').annotate(net=Sum('market_value'), beta_adj=Sum('beta_adj'))
        for pos in position_obj:
            position_list.append({
                'country': SecurityCountry.objects.get(country_id=pos['security_id__country_id']).country_name,
                'net': round(pos['net'], 2),
                'gross': round(abs(pos['net']), 2),
                'beta_adj': round(pos['beta_adj'], 2)
            })
        data = 'position_list'
        data = {'data': position_list}
    except Exception, e:
        print 'position.py|get_position_list_by_security|error', e
        data = {'success': 'false'}
    return HttpResponse(json.dumps(data), content_type='application/json')


def get_position_list_by_assetclass(request):
    # pdb.set_trace()
    position_list = []
    print '---------------get position list by Asset----------------------', request.GET
    try:
        position_obj = Position_Details.objects.filter(position_status='Active',
                                                       position_date__startswith=datetime.strptime(request.GET.get('position_date'),
                                                                                       '%d/%m/%Y').date()).values(
            'security_id__asset_sub_class_id__asset_class_id').annotate(net=Sum('market_value'),
                                                                        beta_adj=Sum('beta_adj'))
        for pos in position_obj:
            position_list.append({
                'assetclass': Asset_Class_Details.objects.get(
                    asset_class_id=pos['security_id__asset_sub_class_id__asset_class_id']).asset_class_name,
                'net': round(pos['net'], 2),
                'gross': round(abs(pos['net']), 2),
                'beta_adj': round(pos['beta_adj'], 2)
            })
        data = {'data': position_list}
    except Exception, e:
        print 'position.py|get_position_list_by_security|error', e
        data = {'success': 'false'}
    return HttpResponse(json.dumps(data), content_type='application/json')


def check_val(value):
    if value:
        return value
    else:
        return 0


def get_price(type, security_id,position_date):
    try:
        print '--------------------get_price------------------------',security_id
        print type,security_id,position_date
        security_price_obj = Security_Price_Details.objects.filter(record_status='Active',security_id=security_id,security_price_date__lte=position_date).order_by('-security_price_date')
        print 'security_price_obj==========Last Record: 01',security_price_obj
        print '--------------------'
        scrty_id = security_price_obj.first()
        print 'security_price_obj==========Last Record: 02',scrty_id
        security_price = 0
        if type == 'last_price':
            security_price = scrty_id.security_last_price
        elif type == 'in_price':
            security_price = scrty_id.security_in_price
        elif type == 'security_one_d':
            security_price = scrty_id.security_one_d
    except Exception, e:
        print 'Position.py|get_price|error', e
        security_price = 0
    print scrty_id.security_price_date,security_price
    return security_price


@csrf_exempt
#@login_required(login_url='/open-login-page/')
def generate_position(request):
    data=position_calculation(request,'click')
    return HttpResponse(json.dumps(data), content_type='application/json')


def position_calculation(request,event):
    try:
        print '=============vikram chandel========================', request.POST
        #--------Delete Position------------------
        position_date=""
        if event=='click':
            position_date=datetime.strptime(request.POST.get('price_date'),'%d/%m/%Y').date()
        elif event=='load':
            position_date=datetime.now().date()
        position_objList = Position_Details.objects.filter(position_date__startswith=position_date)
        print 'position_objList',position_objList
        if position_objList:
            for ps in position_objList:
                ps.delete()

        #---------------------get fund size and total security------------------------------
        total_trade = Trade_Details.objects.filter(record_status='Active').values('buy_sell_indicator').annotate(
            total_amount=Sum('trade_amount'), total_quantity=Sum('trade_security_quantity'))
        fund_size = 0
        total_shares = 0
        for trade in total_trade:
            if trade['buy_sell_indicator'] == 'Buy' or trade['buy_sell_indicator']=='Cover Short':
                fund_size = fund_size + trade['total_amount']
                total_shares = total_shares + trade['total_quantity']
            elif trade['buy_sell_indicator'] == 'Sell' or trade['buy_sell_indicator']=='Sell Short':
                fund_size = fund_size - trade['total_amount']
                total_shares = total_shares - trade['total_quantity']

        #---------------------Calculate position from trade------------------------------
        security_list = Set()
        position_obj = Trade_Details.objects.filter(record_status='Active',trade_date__lte=position_date).values('security_id',
                                                                                   'buy_sell_indicator').annotate(
            total_amount=Sum('trade_amount'), total_quantity=Sum('trade_security_quantity'),in_principal=Sum('trade_amount'),in_price=Avg('trade_price'))
        print 'position_obj',position_obj
        for position in position_obj:
            security_list.add(str(position['security_id']))

        for security in security_list:
            total_quantity = 0
            total_amount = 0
            in_principal=0
            in_price=0

            for position in position_obj:
                if str(position['security_id']) == security:
                    if position['buy_sell_indicator'] == 'Buy' or position['buy_sell_indicator']=='Cover Short':
                        total_amount = total_amount + position['total_amount']
                        total_quantity = total_quantity + position['total_quantity']
                        in_principal=in_principal+position['in_principal']
                    elif position['buy_sell_indicator'] == 'Sell' or position['buy_sell_indicator']=='Sell Short':
                        total_amount = total_amount - position['total_amount']
                        total_quantity = total_quantity - position['total_quantity']
                        in_principal=in_principal-position['in_principal']

            fx_in = 1  # don't know how to calculate
            r = 1  # don't know how to calculate

            #pdb.set_trace()
            print '--------------------Calculation---------------------------',security
            beta = check_val(Security_Details.objects.get(security_id=security).security_beta)
            if not beta:
                beta=0
            last_price = get_price('last_price', security,position_date)
            security_lot_size=float(Security_Details.objects.get(security_id=security).security_lot_size)

            #in_principal=round(in_principal/security_lot_size,2)
            in_price = round((total_amount/security_lot_size)/total_quantity,2)
            security_one_d = get_price('security_one_d', security,position_date)
            market_value = round(((total_quantity * last_price * security_lot_size) / r), 2)
            profit_and_loss = round((market_value-in_principal), 2)
            position_value = round((market_value / fund_size)*100, 2)
            move_since_incepton = round((profit_and_loss / abs(market_value)), 2)
            beta_adj = round((market_value * beta), 2)
            contrib_daily = round(((security_one_d / fund_size) * 10000), 2)
            portfolio_return_contrib = round(((profit_and_loss / fund_size) * 10000), 2)
            fx_contrib = round(((r / fx_in - 1) * position_value * 100 * 100), 2)

            print '--------------------Position data store---------------------------'
            save_position = Position_Details()
            save_position.security_id = Security_Details.objects.get(security_id=security)
            save_position.in_price = in_price
            save_position.last_price=last_price
            save_position.position = position_value
            save_position.move_since_incepton = move_since_incepton
            save_position.position_security_quntity = total_quantity
            save_position.in_principal = in_principal
            save_position.market_value = market_value
            save_position.beta_adj = beta_adj
            save_position.profit_and_loss = profit_and_loss
            save_position.contrib_daily = contrib_daily
            save_position.portfolio_return_contrib = portfolio_return_contrib
            save_position.FX = Security_Details.objects.get(
                security_id=security).security_local_currency.currency
            save_position.beta = beta
            save_position.FX_in = 1
            save_position.fx_contrib = fx_contrib
            #save_position.position_date = datetime.now().date()
            #save_position.position_date = datetime.strptime(request.POST['price_date'], '%d/%m/%Y').date()
            save_position.position_date = position_date
            save_position.position_status = 'Active'
            save_position.position_created_by = request.session['login_user']
            save_position.position_updated_by = request.session['login_user']
            save_position.position_created_date = datetime.now()
            save_position.position_updated_date = datetime.now()
            save_position.save()
        data = {'success': 'true'}
    except Exception, e:
        print 'Position.py|generate_position|error', e
        data = {'success': 'false'}
    return data

@csrf_exempt
def get_trades(request):
    trade_list = []
    try:
        positionId = request.POST.get('position_id')
        position_obj = Position_Details.objects.get(position_id=positionId)
        tradeList = Trade_Details.objects.filter(security_id=position_obj.security_id, record_status='Active',
                                                 trade_date__lte=position_obj.position_date)
        for trade in tradeList:
            trade_list.append({'date': trade.trade_date.strftime('%d/%m/%Y'),
                               'security': trade.security_id.security_name,
                               'trade_type': trade.buy_sell_indicator,
                               'quantity': trade.trade_security_quantity,
                               'in_price': trade.trade_price,
                               'total_amount': trade.trade_amount})
        data = {'success': 'true', 'data_list': trade_list}
        print data
    except Exception, e:
        print 'Position.py|get_trades|error', e
        data = {'success': 'false'}
    return HttpResponse(json.dumps(data), content_type='application/json')
