from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.template import RequestContext
from django.views.decorators.csrf import csrf_exempt

import django

import json
import requests
from datetime import datetime, timedelta


# Create your views here.


def index(request):
	return render(request,'index.html')

@csrf_exempt
def fetch_info(request):
	url = request.POST.get('url','')
	if url == '': # if user hasn't enetered any URL and clicked on go, take user back to home page
		return redirect('/')
	repo_url = strip_url(url) # strips the URL and finds the username and repo name
	total_issues = issues_count(repo_url) # finds out the total isssues with the repo

	now = datetime.now() # gives current time
	last_24_issues = last_24(repo_url,now) # issues in the last 24 hours
	before_24_less_than_7_issues = before_24_less_than_7(repo_url,last_24_issues,now) # issues that are more than 24 hours ago but less than 7 days ago
	greater_than_7_issues = greater_than_7(last_24_issues,before_24_less_than_7_issues,total_issues) #  issues that are more than 7 days ago

	return HttpResponse(json.dumps({'url':url,
									'total_issues':total_issues,
									'last_24_issues': last_24_issues,
									'before_24_less_than_7_issues':before_24_less_than_7_issues,
									'greater_than_7_issues':greater_than_7_issues})
									,content_type='application/json')	
	# send response as json which can be manipulated by javascript/ jquery that made the call

def strip_url(url):
	index = url.index('github.com/') # find index of github.com
	length = len('github.com/') # find length of github.com
	repo_url = url[index+length:].strip('/') # return string (starting from index position of github.com + length of github.com) which in turn would return only that part of the URL after github.com (username and repo name)
	return repo_url

def issues_count(url):
	r = requests.get('https://api.github.com/repos/'+url) # make a request to api.github.com to fetch information about the URL
	json_text = json.loads(r.text) # convert response to json

	if 'message' in json_text and 'documentation_url' in json_text:
		return "API limit exceeded"

	issues_count = json_text["open_issues_count"] # find out open issues count
	return issues_count

def last_24(url,now):
	this_time_yesterday = now - timedelta(hours=24) # subtract 24 hours from current date
	this_time_yesterday = this_time_yesterday.strftime('%Y-%m-%dT%H:%M:%SZ') # convert into date time format understood by github API
	r = requests.get('https://api.github.com/repos/'+url+'/issues',params={'since':this_time_yesterday}) # make request with a parameter since passing date value
	json_text = json.loads(r.text) # convert response to json

	if 'message' in json_text and 'documentation_url' in json_text:
		return "API limit exceeded"

	return len(json_text) # find out length which in turn would be the result

def before_24_less_than_7(url,last_24_issues_count,now):
	seven_days_back = now - timedelta(days=7) # subtract 7 days from current date
	seven_days_back = seven_days_back.strftime('%Y-%m-%dT%H:%M:%SZ') # convert into date time format understood by github API
	
	r = requests.get('https://api.github.com/repos/'+url+'/issues',params={'since':seven_days_back}) # make request with a parameter since passing date value
	json_text = json.loads(r.text) # convert response to json

	if 'message' in json_text and 'documentation_url' in json_text:
		return "API limit exceeded"

	last_7_days_issues_count = len(json_text) # find out length which would be the issues for the last 7 days
	result = last_7_days_issues_count - last_24_issues_count # result would be above minus issues raised last 24 hours, since we don't require the ones that were raised last 24 hours

	if result < 0:
		return 0 # there is a possibility that after subtraction it could go negative, since last 24 hours there might have been issue, but not 7 days before that, as a result make it zero if it is -ve
	else:
		return result

def greater_than_7(last_24_issues,before_24_less_than_7_issues,total_issues):
	if last_24_issues == "API limit exceeded" or before_24_less_than_7 == "API limit exceeded" or total_issues == "API limit exceeded":
		return "API limit exceeded"
		
	return total_issues - (last_24_issues + before_24_less_than_7_issues) #older than 7 days would be the total issues minus the issues that were raised up until 7 days back


def snake(request):
	return render(request,'issues.html')
	
