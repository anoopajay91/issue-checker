from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.template import RequestContext

import django

import json
import requests
from datetime import datetime, timedelta

# Create your views here.


def index(request):
	return render(request,'index.html')


def fetch_info(request):
	url = request.POST.get('url','')
	if url == '':
		return redirect('/')
	#https://github.com/Shippable/support
	repo_url = strip_url(url)
	total_issues = issues_count(repo_url)

	now = datetime.now()
	last_24_issues = last_24(repo_url,now)
	before_24_less_than_7_issues = before_24_less_than_7(repo_url,last_24_issues,now)
	greater_than_7_issues = greater_than_7(last_24_issues,before_24_less_than_7_issues,total_issues)

	return HttpResponse(json.dumps({'url':url,
									'total_issues':total_issues,
									'last_24_issues': last_24_issues,
									'before_24_less_than_7_issues':before_24_less_than_7_issues,
									'greater_than_7_issues':greater_than_7_issues})
									,content_type='application/json')

def strip_url(url):
	index = url.index('github.com/')
	length = len('github.com/')
	repo_url = url[index+length:].strip('/')
	return repo_url

def issues_count(url):
	r = requests.get('https://api.github.com/repos/'+url)
	json_text = json.loads(r.text)
	issues_count = json_text["open_issues_count"]
	return issues_count

def last_24(url,now):
	this_time_yesterday = now - timedelta(hours=24)
	this_time_yesterday = this_time_yesterday.strftime('%Y-%m-%dT%H:%M:%SZ')
	r = requests.get('https://api.github.com/repos/'+url+'/issues',params={'since':this_time_yesterday})
	json_text = json.loads(r.text)
	return len(json_text)

def before_24_less_than_7(url,last_24_issues_count,now):
	seven_days_back = now - timedelta(days=7)
	seven_days_back = seven_days_back.strftime('%Y-%m-%dT%H:%M:%SZ')
	
	r = requests.get('https://api.github.com/repos/'+url+'/issues',params={'since':seven_days_back})
	json_text = json.loads(r.text)
	last_7_days_issues_count = len(json_text)
	result = last_7_days_issues_count - last_24_issues_count

	if result < 0:
		return 0
	else:
		return result

def greater_than_7(last_24_issues,before_24_less_than_7_issues,total_issues):
	return total_issues - (last_24_issues + before_24_less_than_7_issues)
