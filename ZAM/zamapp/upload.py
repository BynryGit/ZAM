from django.db import models
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
##from zamapp.forms import UploadFileForm

import MySQLdb, sys
import datetime
import time
import pdb
import json
from zamapp.models import *


# This is temporary for checking images
@csrf_exempt
def imageupload(request):
    print "in the upload image"
##    pdb.set_trace()
    try:
        print request.FILES['file[]']
        if request.method == 'POST':
            attachment_file   =   ClientCommunicationAttachmentsDetailsTbl(attachment_file_path   = request.FILES['file[]'])
            attachment_file.save()
            data = {'success' : 'true','attachid':attachment_file.attachment_id}
            print data
        else:
            data = {'success': 'false'}
            print data
    except MySQLdb.OperationalError, e:
        data = {'success': 'invalid request'}
    return HttpResponse(json.dumps(data), content_type='application/json')


# @csrf_exempt
def remove_image(request):
##    pdb.set_trace()
    print "in the remove image"
    print request.GET
    try:
        attachment_id=request.GET.get('attachid')
        print 'image id : - >',image_id
        attachment= ClientCommunicationAttachmentsDetailsTbl.objects.get(attachment_file_path=attachid)
        attachment.delete()
        data = {'success': 'true'}
    except MySQLdb.OperationalError, e:
        data = {'success': 'false'}
    return HttpResponse(json.dumps(data), content_type='application/json')

@csrf_exempt
def active_file_upload(request):
    print "in the upload image"
##    pdb.set_trace()
    try:
        print request.FILES['file[]']
        if request.method == 'POST':
            attachment_file   =   ActiveListAttechment(attachment_path   = request.FILES['file[]'])
            attachment_file.save()
            data = {'success' : 'true','attachid':attachment_file.attechment_id}
            print data
        else:
            data = {'success': 'false'}
            print data
    except MySQLdb.OperationalError, e:
        data = {'success': 'invalid request'}
    return HttpResponse(json.dumps(data), content_type='application/json')

@csrf_exempt
def focus_file_upload(request):
    print "in the upload image"
##    pdb.set_trace()
    try:
        print request.FILES['file[]']
        if request.method == 'POST':
            attachment_file   =   FocusListAttechment(attachment_path   = request.FILES['file[]'])
            attachment_file.save()
            data = {'success' : 'true','attachid':attachment_file.attechment_id}
            print data
        else:
            data = {'success': 'false'}
            print data
    except MySQLdb.OperationalError, e:
        data = {'success': 'invalid request'}
    return HttpResponse(json.dumps(data), content_type='application/json')

@csrf_exempt
def portfolio_file_upload(request):
    print "in the upload image"
##    pdb.set_trace()
    try:
        print request.FILES['file[]']
        if request.method == 'POST':
            attachment_file   =   PortfolioListAttechment(attachment_path   = request.FILES['file[]'])
            attachment_file.save()
            data = {'success' : 'true','attachid':attachment_file.attechment_id}
            print data
        else:
            data = {'success': 'false'}
            print data
    except MySQLdb.OperationalError, e:
        data = {'success': 'invalid request'}
    return HttpResponse(json.dumps(data), content_type='application/json')

# @csrf_exempt
def focus_file_remove(request):
    print "in the remove image"
    print request.GET
    try:
        attachment_id=request.GET.get('attachid')
        print 'image id : - >',image_id
        attachment= FocusListAttechment.objects.get(attachment_path=attachid)
        attachment.delete()
        data = {'success': 'true'}
    except MySQLdb.OperationalError, e:
        data = {'success': 'false'}
    return HttpResponse(json.dumps(data), content_type='application/json')

# @csrf_exempt
def active_file_remove(request):
    print "in the remove image"
    print request.GET
    try:
        attachment_id=request.GET.get('attachid')
        print 'image id : - >',image_id
        attachment= ActiveListAttechment.objects.get(attachment_path=attachid)
        attachment.delete()
        data = {'success': 'true'}
    except MySQLdb.OperationalError, e:
        data = {'success': 'false'}
    return HttpResponse(json.dumps(data), content_type='application/json')

# @csrf_exempt
def portfolio_file_remove(request):
    print "in the remove image"
    print request.GET
    try:
        attachment_id=request.GET.get('attachid')
        print 'image id : - >',image_id
        attachment= PortfolioListAttechment.objects.get(attachment_path=attachid)
        attachment.delete()
        data = {'success': 'true'}
    except MySQLdb.OperationalError, e:
        data = {'success': 'false'}
    return HttpResponse(json.dumps(data), content_type='application/json')

@csrf_exempt
def focuslist_file_upload(request):
    print "in the upload image"
##    pdb.set_trace()
    try:
        print request.FILES['file[]']
        if request.method == 'POST':
            attachment_file   =   FocusListMiscleneousAttachment(attachment_path   = request.FILES['file[]'])
            attachment_file.save()
            data = {'success' : 'true','attachid':attachment_file.misleneous_attechment_id}
            print data
        else:
            data = {'success': 'false'}
            print data
    except MySQLdb.OperationalError, e:
        data = {'success': 'invalid request'}
    return HttpResponse(json.dumps(data), content_type='application/json')

@csrf_exempt
def activelist_file_upload(request):
    print "in the upload image"
##    pdb.set_trace()
    try:
        print request.FILES['file[]']
        if request.method == 'POST':
            attachment_file   =   ActiveListMiscleneousAttachment(attachment_path   = request.FILES['file[]'])
            attachment_file.save()
            data = {'success' : 'true','attachid':attachment_file.misleneous_attechment_id}
            print data
        else:
            data = {'success': 'false'}
            print data
    except MySQLdb.OperationalError, e:
        data = {'success': 'invalid request'}
    return HttpResponse(json.dumps(data), content_type='application/json')


@csrf_exempt
def portfoliolist_file_upload(request):
    print "in the upload image"
##    pdb.set_trace()
    try:
        print request.FILES['file[]']
        if request.method == 'POST':
            attachment_file   =   PortfolioMiscleneousAttachment(attachment_path   = request.FILES['file[]'])
            attachment_file.save()
            data = {'success' : 'true','attachid':attachment_file.misleneous_attechment_id}
            print data
        else:
            data = {'success': 'false'}
            print data
    except MySQLdb.OperationalError, e:
        data = {'success': 'invalid request'}
    return HttpResponse(json.dumps(data), content_type='application/json')

@csrf_exempt
def update_focus_file_upload(request):
    print "in the updated upload image"
##    pdb.set_trace()
    try:
        
        print request.FILES
        if request.method == 'POST':
            if request.FILES:
                attachment_file   =   FocusListMiscleneousAttachment(attachment_path   = request.FILES['file'])
            attachment_file.save()
            data = {'success' : 'true','attachid':attachment_file.misleneous_attechment_id}
            print data
        else:
            data = {'success': 'false'}
            print data
    except Exception as e:
        print 'Error ------------> ',e
        data = {'success': 'invalid request'}
    return HttpResponse(json.dumps(data), content_type='application/json')

@csrf_exempt
def update_activelist_file_upload(request):
    print "in the updated upload image"
##    pdb.set_trace()
    try:
        
        print request.FILES
        if request.method == 'POST':
            if request.FILES:
                attachment_file   =   ActiveListMiscleneousAttachment(attachment_path   = request.FILES['file'])
            attachment_file.save()
            data = {'success' : 'true','attachid':attachment_file.misleneous_attechment_id}
            print data
        else:
            data = {'success': 'false'}
            print data
    except Exception as e:
        print 'Error ------------> ',e
        data = {'success': 'invalid request'}
    return HttpResponse(json.dumps(data), content_type='application/json')

@csrf_exempt
def update_portfoliolist_file_upload(request):
    print "in the upload image"
##    pdb.set_trace()
    try:
        print request.FILES['file']
        if request.method == 'POST':
            attachment_file   =   PortfolioMiscleneousAttachment(attachment_path   = request.FILES['file'])
            attachment_file.save()
            data = {'success' : 'true','attachid':attachment_file.misleneous_attechment_id}
            print data
        else:
            data = {'success': 'false'}
            print data
    except Exception as e:
        print 'Error ------------> ',e
        data = {'success': 'invalid request'}
    return HttpResponse(json.dumps(data), content_type='application/json')

@csrf_exempt
def remove_focuslistmisc_image(request):
##    pdb.set_trace()
    print "in the remove image"
    print request.GET
    try:
        image_id=request.GET.get('image_id')
##        temp=str(image_id).replace("]", "")
##        print 'image id : - >',temp.replace("]", "")
##        temp=str(image_id).replace("[", "")
##        print 'image1 id : - >',temp.replace("[", "")
        
        image= FocusListMiscleneousAttachment.objects.get(misleneous_attechment_id=image_id)
        image.delete()
        data = {'success': 'true'}
    except MySQLdb.OperationalError, e:
        data = {'success': 'false'}
    return HttpResponse(json.dumps(data), content_type='application/json')

@csrf_exempt
def remove_activelistmisc_image(request):
    #pdb.set_trace()
    print "in the remove image"
    print request.GET
    try:
        image_id=request.GET.get('image_id')
##        temp=str(image_id).replace("L]", "")
##        print 'image id : - >',temp.replace("L]", "")
        
        image= ActiveListMiscleneousAttachment.objects.get(misleneous_attechment_id=image_id)
        image.delete()
        data = {'success': 'true'}
    except MySQLdb.OperationalError, e:
        data = {'success': 'false'}
    return HttpResponse(json.dumps(data), content_type='application/json')


@csrf_exempt
def remove_portfoliolistmisc_image(request):
##    pdb.set_trace()
    print "in the remove image"
    print request.GET
    try:
        image_id=request.GET.get('image_id')
##        temp=str(image_id).replace("L]", "")
##        print 'image id : - >',temp.replace("L]", "")
        image= PortfolioMiscleneousAttachment.objects.get(misleneous_attechment_id=image_id)
        image.delete()
        data = {'success': 'true'}
    except MySQLdb.OperationalError, e:
        data = {'success': 'false'}
    return HttpResponse(json.dumps(data), content_type='application/json')
