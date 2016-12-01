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
from django.shortcuts import redirect


def view_question(request):
    try:
        color = ["categoryBlue","categoryPurple","categoryGreen","categoryYellow"]
        i = 0
        quetype_obj = QuestionType.objects.filter(record_status="Active")
        question_type_list = []

        for quetype in quetype_obj:  # Start of loop 1
            QR = []
            que_obj = quetype.qtype_id.filter(record_status="Active").order_by('-question_ask_date')[:2]
            i = i + 1
            if i == 4 :
            	i = 0

            for que in que_obj:  # start of loop 2
                question = {
                    'question_id': que.question_id,
                    'question_txt': que.question,
                    'full_name': que.user_id.user_first_name + " " + que.user_id.user_last_name,
                    'question_ask_date': que.question_ask_date.strftime('%d/%m/%Y'),
                    'user_role': que.user_id.role_id.role
                }
                responses = que.quest_id.filter(record_status="Active").order_by('-response_date')
                response_list = []
                for res in responses:  # start of loop 3
                    responsesto_obj = res.respon_id.filter(record_status="Active")
                    responseto_list = []
                    counter = len(responsesto_obj)
                    count = 0
                    for resp in responsesto_obj:  # start of loop 4
                        count = count + 1
                        #print "count", count
                        responseto = {
                            'responseto_id': resp.responseto_id,
                            'responseto': resp.responseto,
                            'full_name': resp.user_id.user_first_name + " " + resp.user_id.user_last_name,
                            'responseto_date': resp.responseto_date.strftime('%d/%m/%Y'),
                            'user_role': resp.user_id.role_id.role

                        }
                        responseto_list.append(responseto)
                    # End of loop 4


                    response = {
                        'response_id': res.response_id,
                        'response': res.response,
                        'full_name': res.user_id.user_first_name + " " + res.user_id.user_last_name,
                        'response_date': res.response_date.strftime('%d/%m/%Y'),
                        'user_role': res.user_id.role_id.role,
                        'respond2': responseto_list,
                        'counter': counter
                    }
                    response_list.append(response)
                # End of loop 3
                QR.append({'Q': question, 'R': response_list, 'response_count': len(response_list)})
            # End of loop 2
            questiontype = {
                'questiontype_id': quetype.question_type_id,
                'question_type': quetype.question_type,
                'questions': QR,
                'clr_cls':color[i]
            }
            question_type_list.append(questiontype)
            # End of loop 1

    except Exception, e:
        print 'Exception : ', e
        data = {'success': 'false'}
    return question_type_list


def open_marketing_manager(request):
    try:
        print 'Marketing Manager'
        #print request.session['user_role']
        if request.session['user_role'] == "Marketing Manager":        	
            status = unread_to_read()
            print status
        data = {'success': 'true', 'question_list': get_question_types(request),
                'all_questions': view_question(request)}
        #print data
    except Exception, e:
        print 'Exception', e
        data = {'success': 'false'}
    return render(request, 'marketing_manager.html', data)


def get_question_types(request):
    question_type_list = []
    try:
        question_types = QuestionType.objects.filter(record_status="Active")
        for type in question_types:
            question_type_list.append(
                {'question_type_id': type.question_type_id, 'question_type': type.question_type})

    except Exception, e:
        print 'Exception ', e
    return question_type_list


def unread_to_read():
    try:
        question_obj = Question.objects.filter(read_status = "Unread")
        for questions in question_obj:
                questions.read_status = "Read"
                questions.save() 	 
        response_obj = Response.objects.filter(read_status = "Unread")
        for response in response_obj:
                response.read_status = "Read"
                response.save()        
        responseto_obj = Responseto.objects.filter(read_status = "Unread")
        for response in responseto_obj:
                response.read_status = "Read"
                response.save()        
        data = "true"
    except Exception, e:
        print 'Exception :', e
        data = "false"
    return data

@csrf_exempt
def save_question(request):
##    pdb.set_trace()
    try:

        username = request.POST.get('username')

        if request.method == "POST":
            question_obj = Question(
                question_type=QuestionType.objects.get(question_type_id=request.POST.get('qtype')),
                question=request.POST.get('question'),
                read_status="Unread",
                user_id=UserProfile.objects.get(user_id=username)
            )
            question_obj.save()
            data = {
                    'success': 'true','question':question_obj.question, 'user_role': question_obj.user_id.role_id.role,
                    'question_id':question_obj.question_id,'user_id':str(question_obj.user_id.user_id),
                    'question_ask_date':question_obj.question_ask_date.strftime('%d/%m/%Y'),
                    'fullname':  question_obj.user_id.user_first_name + " " + question_obj.user_id.user_last_name,
                    'question_type':question_obj.question_type.question_type_id
                    }
        else:
            data = {'success': 'false'}
    except Exception, e:
        print 'Exception :', e
        data = {'data': 'none'}
    return HttpResponse(json.dumps(data), content_type='application/json')


@csrf_exempt
def save_response(request):
    #print '===========================================================',request.POST
    #pdb.set_trace()
    try:
        username = request.POST.get('response_by')
        if request.method == "POST":
            response_obj = Response(
                question_id=Question.objects.get(question_id=request.POST.get('question_id')),
                response=request.POST.get('response'),
                read_status="Unread",
                user_id=UserProfile.objects.get(user_id=username)
            )
            response_obj.save()
            response_objs = Response.objects.filter(question_id=request.POST.get('question_id'), record_status="Active")
            print str(response_obj.user_id.user_id)
            data = {
                        'success': 'true','response':response_obj.response,
                        'response_date':response_obj.response_date.strftime('%d/%m/%Y'),
                        'response_id':response_obj.response_id,
                        'full_name': response_obj.user_id.user_first_name + " " + response_obj.user_id.user_last_name,
                        'user_role': response_obj.user_id.role_id.role,'counter':response_objs.count(),'user_id':str(response_obj.user_id.user_id)
                    }
        else:
            data = {'success': 'false'}
    except Exception, e:
        print 'Exception :', e
        data = {'data': 'none'}
    return HttpResponse(json.dumps(data), content_type='application/json')
    #return redirect('/open-marketing-manager/')


@csrf_exempt
def save_responseto(request):
    #pdb.set_trace()
    try:
        username = request.POST.get('responseto_by')
        print username
        if request.method == "POST":
            responseto_obj = Responseto(
                response_id=Response.objects.get(response_id=request.POST.get('response_id')),
                responseto=request.POST.get('responseto'),
                read_status="Unread",
                user_id=UserProfile.objects.get(user_id=username)
            )
            responseto_obj.save()
            response_objs = Responseto.objects.filter(response_id=request.POST.get('response_id'), record_status="Active")
            data = {
                        'success': 'true', 'response_id':str(responseto_obj.response_id), 
                        'full_name':responseto_obj.user_id.user_first_name + " " + responseto_obj.user_id.user_last_name,
                        'user_role':responseto_obj.user_id.role_id.role, 'responseto_date':responseto_obj.responseto_date.strftime('%d/%m/%Y'),
                        'responseto_id':responseto_obj.responseto_id,'responseto':responseto_obj.responseto, 'counter':response_objs.count()
                    }
        else:
            data = {'success': 'false'}
    except Exception, e:
        print 'Exception :', e
        data = {'data': 'none'}
    return HttpResponse(json.dumps(data), content_type='application/json')
    #return redirect('/open-marketing-manager/')


@csrf_exempt
def view_questions_typewise01(request):
    ##    pdb.set_trace()
    try:
        qestiontype_id = request.GET.get('qtype')
        que_obj = Question.objects.filter(record_status="Active", question_type=qestiontype_id).order_by(
            '-question_ask_date')
        #print 'Question text: ', que_obj
        QR = []

        qtype = QuestionType.objects.get(question_type_id=qestiontype_id)
        for que in que_obj:
            question = {
                'question_id': que.question_id,
                'question_txt': que.question,
                'question_type': que.question_type.question_type,
                'full_name': que.user_id.user_first_name + " " + que.user_id.user_last_name,
                'question_ask_date': que.question_ask_date.strftime('%d/%m/%Y'),
                'user_role': que.user_id.role_id.role
            }

            responses = que.quest_id.filter(record_status="Active").order_by('-response_date')
            response_list = []

            for res in responses:
                responsesto_obj = res.respon_id.filter(record_status="Active")
                responseto_list = []
                counter = len(responsesto_obj)
                count = 0
                for resp in responsesto_obj:
                    count = count + 1
                    #print "count", count
                    responseto = {
                        'responseto_id': resp.responseto_id,
                        'responseto': resp.responseto,
                        'full_name': resp.user_id.user_first_name + " " + resp.user_id.user_last_name,
                        'responseto_date': resp.responseto_date.strftime('%d/%m/%Y'),
                        'user_role': resp.user_id.role_id.role

                    }
                    responseto_list.append(responseto)
                response = {
                    'response_id': res.response_id,
                    'response': res.response,
                    'full_name': res.user_id.user_first_name + " " + res.user_id.user_last_name,
                    'response_date': res.response_date.strftime('%d/%m/%Y'),
                    'user_role': res.user_id.role_id.role,
                    'respond2': responseto_list,
                    'counter': counter
                }
                response_list.append(response)
            QR.append({'Q': question, 'R': response_list, 'response_count': len(response_list)})
            #print 'Questions List', QR
        data = {'success': 'true', 'quelist': QR, 'qtype': qtype.question_type}
    except Exception, e:
        print 'Exception :', e
        data = {'success': 'false'}
    return render(request, 'questions_detail_view.html', data)

@csrf_exempt
def view_questions_typewise(request):
    ##    pdb.set_trace()
    try:
        qestiontype_id = request.GET.get('qtype')
        qtype = QuestionType.objects.get(question_type_id=qestiontype_id)
        result_question = Question.objects.filter(question_type=qtype.question_type_id,record_status='Active').order_by('-question_ask_date')
        final_result=[]
        #print '====================================================================='
       # print 'result_question:=> ',result_question
        p=0
        ques_arry = []
        for question in result_question:
            p=p+1
            #print 'result p:==>',p

            result_ans = Response.objects.filter(question_id=question.question_id,record_status='Active').order_by('-response_date')
            #print 'question',question
            #print 'result_ans',result_ans
            response_arry = []
            for ans in result_ans:
                result_toans = Responseto.objects.filter(response_id=ans.response_id, record_status='Active').order_by(
                    '-responseto_date')
                responseto_arry = []
                for ans_to in result_toans:
                    responseto_arry.append({
                        'responseto_id': ans_to.responseto_id,
                        'responseto': ans_to.responseto,
                        'full_name': ans_to.user_id.user_first_name + " " + ans_to.user_id.user_last_name,
                        'responseto_date': ans_to.responseto_date.strftime('%d/%m/%Y'),
                        'user_role': ans_to.user_id.role_id.role
                })
                response_arry.append({
                    'response_id': ans.response_id,
                    'response': ans.response,
                    'full_name': ans.user_id.user_first_name + " " + ans.user_id.user_last_name,
                    'response_date': ans.response_date.strftime('%d/%m/%Y'),
                    'user_role': ans.user_id.role_id.role,
                    'respondto': responseto_arry,
                    'counter': len(result_toans)
                })
            ques_arry.append({
                'question_id': question.question_id,
                'question_txt': question.question,
                'question_type': question.question_type.question_type,
                'full_name': question.user_id.user_first_name + " " + question.user_id.user_last_name,
                'question_ask_date': question.question_ask_date.strftime('%d/%m/%Y'),
                'user_role': question.user_id.role_id.role,
                'responses': response_arry,
                'counter': len(result_ans)
            })
        final_result.append({
                'type_id':qtype.question_type_id,
                'type': qtype.question_type,
                'questions': ques_arry
            })
        #print 'Question text:---> ',final_result
        data={'final_result':final_result}
    except Exception, e:
        print 'Exception :', e
        data = {'success': 'false'}
    return render(request, 'question_seemore.html', data)

@csrf_exempt
def search_question(request):
    #pdb.set_trace()
    try:
        questions_list = []
        print "-----------In Search Question---------------"
        query = request.GET.get('searchQ')
        search_query = query
        response_list = Response.objects.filter(response__icontains=search_query,record_status='Active')
        question_list = Question.objects.filter(question__icontains=search_query,record_status='Active')
        questionType_list = QuestionType.objects.filter(question_type__icontains=search_query,record_status='Active')
        # print 'response_list--->', response_list
        # print 'question_list--->', question_list
        # print 'questionType_list--->', questionType_list

        for response in response_list:
            question_list = question_list.exclude(question_id=response.question_id.question_id)

        for response in response_list:
            questionType_list = questionType_list.exclude(
                question_type_id=response.question_id.question_type.question_type_id)

        for question in question_list:
            questionType_list = questionType_list.exclude(question_type_id=question.question_type.question_type_id)

        # print '------------------AFTER----------------------'
        # print 'response_list--->', response_list
        # print 'question_list--->', question_list
        # print 'questionType_list--->', questionType_list
        test_result = []
        check_quesType_id_list = []
        print '------------------questionType_list---------------------------'
        p=0
        color = ["categoryBlue","categoryPurple","categoryGreen","categoryYellow"]
        i = 0
        for type in questionType_list:
            p=p+1
            i = i + 1
            if i == 4 :
            	i = 0
            print '---------in questionTypeList----------',p
            ques_arry = []
            result_question = Question.objects.filter(question_type=type['question_type'].question_type_id,
                                                      record_status='Active').order_by('-question_ask_date')
            first_question = result_question.first()
            result_ans = Response.objects.filter(question_id=first_question.question_id,
                                                 record_status='Active').order_by('-response_date')
            # print 'question',question
            # print 'result_ans',result_ans
            response_arry = []
            for ans in result_ans:
                result_toans = Responseto.objects.filter(response_id=ans.response_id, record_status='Active').order_by(
                    '-responseto_date')
                responseto_arry = []
                for ans_to in result_toans:
                    responseto_arry.append({
                        'responseto_id': ans_to.responseto_id,
                        'responseto': ans_to.responseto,
                        'full_name': ans_to.user_id.user_first_name + " " + ans_to.user_id.user_last_name,
                        'responseto_date': ans_to.responseto_date.strftime('%d/%m/%Y'),
                        'user_role': ans_to.user_id.role_id.role
                    })
                response_arry.append({
                    'response_id': ans.response_id,
                    'response': ans.response,
                    'full_name': ans.user_id.user_first_name + " " + ans.user_id.user_last_name,
                    'response_date': ans.response_date.strftime('%d/%m/%Y'),
                    'user_role': ans.user_id.role_id.role,
                    'respondto': responseto_arry,
                    'counter': len(result_toans)
                })
            ques_arry.append({
                'question_id': first_question.question_id,
                'question_txt': first_question.question,
                'question_type': first_question.question_type.question_type,
                'full_name': first_question.user_id.user_first_name + " " + first_question.user_id.user_last_name,
                'question_ask_date': first_question.question_ask_date.strftime('%d/%m/%Y'),
                'user_role': first_question.user_id.role_id.role,
                'responses': response_arry,
                'counter': len(result_ans)
            })
            check_quesType_id_list.append(type['question_type'].question_type_id)
            test_result.append({
                'type_id': type['question_type'].question_type_id,
                'type': type['question_type'].question_type,
                'questions': ques_arry,
                'clr_cls':color[i]
            })

        # print '----------------output questionlist type--------------',test_result
        #
        #
        # print '------------------question_list---------------------------'
        p=0
        color = ["categoryBlue","categoryPurple","categoryGreen","categoryYellow"]
        i = 0        
        for question in question_list:
            p=p+1
            i = i + 1
            if i == 4 :
            	i = 0           
            print '---------in question----------',p
            ques_arry = []
            questionType_list = QuestionType.objects.get(question_type_id=question.question_type.question_type_id)
            result_ans = Response.objects.filter(question_id=question.question_id, record_status='Active').order_by(
                '-response_date')

            # print 'question',question
            # print 'result_ans',result_ans

            ans_count=len(result_ans)
            print 'ans_count',ans_count
            print '==============================='
            response_arry = []
            for ans in result_ans:
                result_toans = Responseto.objects.filter(response_id=ans.response_id, record_status='Active').order_by(
                    '-responseto_date')
                responseto_arry = []
                for ans_to in result_toans:
                    responseto_arry.append({
                        'responseto_id': ans_to.responseto_id,
                        'responseto': ans_to.responseto,
                        'full_name': ans_to.user_id.user_first_name + " " + ans_to.user_id.user_last_name,
                        'responseto_date': ans_to.responseto_date.strftime('%d/%m/%Y'),
                        'user_role': ans_to.user_id.role_id.role
                    })
                response_arry.append({
                    'response_id': ans.response_id,
                    'response': ans.response,
                    'full_name': ans.user_id.user_first_name + " " + ans.user_id.user_last_name,
                    'response_date': ans.response_date.strftime('%d/%m/%Y'),
                    'user_role': ans.user_id.role_id.role,
                    'respondto': responseto_arry,
                    'counter': len(result_toans)
                })
            print 'response_arry',response_arry
            ques_arry.append({
                'question_id': question.question_id,
                'question_txt': question.question,
                'question_type': question.question_type.question_type,
                'full_name': question.user_id.user_first_name + " " + question.user_id.user_last_name,
                'question_ask_date': question.question_ask_date.strftime('%d/%m/%Y'),
                'user_role': question.user_id.role_id.role,
                'responses': response_arry,
                'counter': ans_count
            })
            if not questionType_list.question_type_id in check_quesType_id_list:
                check_quesType_id_list.append(questionType_list.question_type_id)
                test_result.append({
                    'type_id': questionType_list.question_type_id,
                    'type': questionType_list.question_type,
                    'questions': ques_arry,
                    'clr_cls':color[i]
                })
            else:
                index = check_quesType_id_list.index(questionType_list.question_type_id)
                # ab = test_result[index]['questions']
                # ab.append(ques_arry)
                test_result[index]['questions'].extend(ques_arry)


        #     print '----------------output question type--------------',test_result
        # #pdb.set_trace()
        # print '----------------output question typeerferf-------------- ',test_result


        ques_arry = []
        check_ques_id_list = []
        print '------------------response_list---------------------------'
        p=0        
        for response in response_list:
            response_arry=[]
            p=p+1             
            print '---------in response----------',p
            result_question = Question.objects.get(question_id=response.question_id.question_id, record_status='Active')
            temp_resp=Response.objects.filter(question_id=result_question.question_id,record_status='Active').count()
            print 'temp_resp',temp_resp
            response_count=0
            result_toans = Responseto.objects.filter(response_id=response.response_id, record_status='Active').order_by(
                '-responseto_date')
            print 'result_question',result_question
            print '================>>',len(result_toans)
            responseto_arry = []
            for ans_to in result_toans:
                responseto_arry.append({
                    'responseto_id': ans_to.responseto_id,
                    'responseto': ans_to.responseto,
                    'full_name': ans_to.user_id.user_first_name + " " + ans_to.user_id.user_last_name,
                    'responseto_date': ans_to.responseto_date.strftime('%d/%m/%Y'),
                    'user_role': ans_to.user_id.role_id.role
                })
            response_arry.append({
                'response_id': response.response_id,
                'response': response.response,
                'full_name': response.user_id.user_first_name + " " + response.user_id.user_last_name,
                'response_date': response.response_date.strftime('%d/%m/%Y'),
                'user_role': response.user_id.role_id.role,
                'respondto': responseto_arry,
                'counter': len(result_toans)
            })
            if not result_question.question_id in check_ques_id_list:
                check_ques_id_list.append(result_question.question_id)
                ques_arry.append({
                    'question_id': result_question.question_id,
                    'question_txt': result_question.question,
                    'question_type': result_question.question_type,
                    'full_name': result_question.user_id.user_first_name + " " + result_question.user_id.user_last_name,
                    'question_ask_date': result_question.question_ask_date.strftime('%d/%m/%Y'),
                    'user_role': result_question.user_id.role_id.role,
                    'responses': response_arry,
                    'counter': temp_resp
                })
            else:
                index = check_ques_id_list.index(result_question.question_id)
                ques_arry[index].responses.extend(response_arry)


        # print '--------------------in response output-----------',ques_arry
        #
        # print '----------------All befor--------------',test_result
        #
        # print '------------------ques_arry---------------------------'
        color = ["categoryBlue","categoryPurple","categoryGreen","categoryYellow"]
        i = 0            
        for ques in ques_arry:
            i = i + 1
            if i == 4 :
            	i = 0             
            print '---------------------------------------------------------------4'
            print 'ques===>', ques['question_type']
            questionType_list = QuestionType.objects.get(question_type_id=ques['question_type'].question_type_id)
            print 'questionType_list.question_type', questionType_list
            if not questionType_list.question_type_id in check_quesType_id_list:
                temp_array = []
                temp_array.append(ques)
                check_quesType_id_list.append(questionType_list.question_type_id)
                test_result.append({
                    'type_id': questionType_list.question_type_id,
                    'type': questionType_list.question_type,
                    'questions': temp_array,
                    'clr_cls':color[i]
                })
            else:
                index = check_quesType_id_list.index(questionType_list.question_type_id)
                #test_result[index].questions.append(ques_arry)
                test_result[index]['questions'].extend(ques_arry)

        print 'test_result---------->', test_result
        if not test_result:
            print "no data"
            error_msg = "Search criteria does not match !!!"
        else:
            error_msg = ""        	                    

        data = { 'final_result' : test_result, 'error_msg' : error_msg }
        # json_data = json.dumps(data);
        # print 'JSON DATA : ', json_data
    except Exception, e:
        print 'Exception :', e
        error_msg = "Search criteria does not match !!!"
        data = {'data': 'none', 'error_msg' : error_msg}
    return render(request, 'search_question.html', data)


@csrf_exempt
@transaction.atomic
def delete_question(request):
    #pdb.set_trace()
    sid=transaction.savepoint()
    try:
        question_id = request.GET.get('question_id')
        question_obj=Question.objects.get(question_id=question_id)
        question_obj.record_status="Inactive"
        question_obj.save()

        response_list=Response.objects.filter(question_id=question_obj)
        if response_list:
            for response in response_list:
                response.record_status='Inactive'
                response.save()
                resto_list= Responseto.objects.filter(response_id=response)
                if resto_list:
                    for resto in resto_list:
                        resto.record_status='Inactive'
                        resto.save()

        data={'success':'true'}
        transaction.savepoint_commit(sid)
    except Exception, e:
        print 'Exception : ', e
        data = {'data': 'error_msg'}
        transaction.savepoint_rollback(sid)

    return HttpResponse(json.dumps(data), content_type='application/json')

@csrf_exempt
@transaction.atomic
def delete_responses(request):
    #pdb.set_trace()
    sid=transaction.savepoint()
    r_id = []
    try:
        question_id = request.GET.get('question_id')
        question_obj=Question.objects.get(question_id=question_id)

        response_list=Response.objects.filter(question_id=question_obj,record_status='Active')
        if response_list:
            for response in response_list:
                response.record_status='Inactive'
                response.save()
                resto_list= Responseto.objects.filter(response_id=response)
                r_id.append(response.response_id)
                if resto_list:
                    for resto in resto_list:
                        resto.record_status='Inactive'
                        resto.save()

        data={'success':'true','r_id':r_id}
        transaction.savepoint_commit(sid)
    except Exception, e:
        print 'Exception : ', e
        data = {'data': 'error_msg'}
        transaction.savepoint_rollback(sid)

    return HttpResponse(json.dumps(data), content_type='application/json')
    
@csrf_exempt
@transaction.atomic
def delete_response(request):
    #pdb.set_trace()
    sid=transaction.savepoint()
    try:
        response_id = request.GET.get('response_id')
        response=Response.objects.get(response_id=response_id)
        response.record_status='Inactive'
        response.save()
        if response:
                resto_list= Responseto.objects.filter(response_id=response)
                if resto_list:
                    for resto in resto_list:
                        resto.record_status='Inactive'
                        resto.save()
                        
        response_objs = Response.objects.filter(question_id = response.question_id, record_status="Active")
        print "count: ",response_objs.count()
        print str(response.question_id.question_id)
        
        data={'success':'true','counter':response_objs.count(),'question_id':str(response.question_id.question_id)}
        transaction.savepoint_commit(sid)
    except Exception, e:
        print 'Exception : ', e
        data = {'data': 'error_msg'}
        transaction.savepoint_rollback(sid)

    return HttpResponse(json.dumps(data), content_type='application/json')
    
@csrf_exempt
@transaction.atomic
def delete_responseto(request):
    #pdb.set_trace()
    sid=transaction.savepoint()
    try:
        responseto_id = request.GET.get('responseto_id')
        response= Responseto.objects.get(responseto_id=responseto_id)
        response.record_status='Inactive'
        response.save()
        response_objs = Responseto.objects.filter(response_id=response.response_id, record_status="Active")
        print "count: ",response_objs.count()
        data={'success':'true','counter':response_objs.count(),'response_id':str(response.response_id)}
        transaction.savepoint_commit(sid)
    except Exception, e:
        print 'Exception : ', e
        data = {'data': 'error_msg'}
        transaction.savepoint_rollback(sid)

    return HttpResponse(json.dumps(data), content_type='application/json')        