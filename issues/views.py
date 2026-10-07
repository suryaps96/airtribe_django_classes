from django.shortcuts import render
from .models import Issue, Reporter, CriticalIssue, LowPriorityIssue
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from django.http import HttpResponse
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

def hello_world(request):
    return HttpResponse("Hello World")

def read_reporters():
    with open('issues/reporters.json', 'r') as file:
        reporters = json.load(file)
    return reporters

def read_issues():
    with open('issues/issues.json', 'r') as file:
        issues = json.load(file)
    return issues

@csrf_exempt
def reporter(request):
    reporters = read_reporters()
    
    if request.method == "GET":
         if request.GET.get('id') != None:
             req_id = int(request.GET.get('id'))
        
             for reporter in reporters:
                 if reporter['id'] == req_id :
                     return JsonResponse(reporter,safe=False)
                
            
             return JsonResponse("enter correct id",safe=False)    
            
        
         else:
              return JsonResponse(reporters,safe=False)
    elif request.method == "POST":
        data = json.loads(request.body)
        try:
            rep_data = Reporter(id=data.get('id'),name=data.get('name'),email=data.get('email'),team=data.get('team'))
            rep_data.validate()
        except ValueError as e:
            return JsonResponse({"error": str(e)}, status= 400)
       
        reporters = read_reporters()
        reporters.append(rep_data.to_dict())
        with open('issues/reporters.json', 'w') as file:
            json.dump(reporters, file, indent=4)
        return JsonResponse(rep_data.to_dict(), status= 201)

@csrf_exempt
def issue(request):
    if request.method == "GET":

          if request.GET.get('id') != None:
            req_id = int(request.GET.get('id'))
            issues = read_issues()

            for issue in issues:
                if issue['id'] == req_id :
                    return JsonResponse(issue,safe=False)
            return JsonResponse("enter correct id",safe=False)

          elif request.GET.get('status') != None:
                status = request.GET.get('status')
                matching_issues = []
                issues = read_issues()

                for issue in issues:
                    if issue['status'] == status :
                        matching_issues.append(issue)
                if matching_issues != []:
                    return JsonResponse(matching_issues,safe=False)
                else:
                    return JsonResponse("no issues found",safe=False)

          else:
                issues = read_issues()
                return JsonResponse(issues,safe=False)
    elif request.method == "POST":
        data = json.loads(request.body)
        reporters = read_reporters()
        for reporter in reporters:
            if data.get('reporter_id') == reporter['id']:
                 try:
                  if data.get('priority') == 'critical':
                   item = CriticalIssue(id=data.get('id'),title=data.get('title'),description=data.get('description'),status=data.get('status'),reporter_id=data.get('reporter_id'),priority=data.get('priority'))
                
           
                  elif data.get('priority') == 'low':
                   item = LowPriorityIssue(id=data.get('id'),title=data.get('title'),description=data.get('description'),status=data.get('status'),reporter_id=data.get('reporter_id'),priority=data.get('priority'))
                
                
                  else:
                   item = Issue(id=data.get('id'),title=data.get('title'),description=data.get('description'),status=data.get('status'),reporter_id=data.get('reporter_id'),priority=data.get('priority'))
               
                  item.validate()

                 except ValueError as e:
                  return JsonResponse({"error": str(e)}, status= 400)
 
                 item_dict = item.to_dict()
                 item_dict['message'] = item.describe()
                 issues = read_issues()
                 issues.append(item_dict)
                 with open('issues/issues.json', 'w') as file:
                    json.dump(issues, file, indent=4)
                 return JsonResponse(item_dict,safe=False, status= 201)

        return JsonResponse("reporter not found", safe=False, status= 404)
      

        
        
            
    