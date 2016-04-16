import ipdb
import iso8601

from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from .models import Process, ProcessChild
# Create your views here.

def home(request):
	return render(request, "flex/home.html")

@csrf_exempt
def insert_process(request):
	if request.method == "POST":
		got = request.POST
		a = Process.objects.get_or_create(name = got.get('name'))
		if got.get('start_time'): 
			start_time = iso8601.parse_date(got.get('start_time'))
			ProcessChild.objects.create(process_id = got.get('process_id'), name=Process.objects.get(id= a[0].id), start_time=start_time)
		elif got.get('end_time'): 
			end_time = iso8601.parse_date(got.get('end_time'))
			target = ProcessChild.objects.get(process_id = got.get('process_id'), name=Process.objects.get(id= a[0].id))
			target.end_time = end_time
			target.status = True
			duration_sec = end_time - target.start_time
			target.duration = duration_sec.total_seconds()
			print(duration_sec.total_seconds())
			target.save()
		else:
			return HttpResponse("No data found")	 
	return HttpResponse()

def process_list(request):
	a = ProcessChild.objects.all()
	return render(request, "flex/process_list.html", {"a":a})

def overview(request):
	processes = Process.objects.all()
	content = []
	for pro in processes:
		process_name = pro.name
		children_count = pro.processchild_set.all().count()
		process_children = pro.processchild_set.all()
		total_duration = 0.0
		for child in process_children:
			total_duration = total_duration + child.duration
			print(total_duration)
		avg = total_duration/children_count
		content_child = {
		"name" : process_name,
		"average" : avg
		}	
		content.append(content_child)
	print(type(content))	
	return render(request, 'flex/overview.html', {"content":content})
