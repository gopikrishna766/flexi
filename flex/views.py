import iso8601, datetime
from django.utils.safestring import mark_safe
from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import send_mail, EmailMultiAlternatives
from django.contrib.auth.decorators import login_required

from .models import Process, ProcessChild
from . import email
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
			target.save()
		else:
			return HttpResponse("No data found")
	return HttpResponse()

@login_required
def process_list(request):
	now = datetime.datetime.now()
	today = now.replace(hour=0, minute=0, second=0, microsecond=0)
	table = ProcessChild.objects.filter(start_time__gte=today)
	a = ProcessChild.objects.filter(start_time__gte=today).exclude(end_time=None)
	values = []
	for b in a:
		values.append([b.name.name, b.duration])
	return render(request, "flex/process_list.html", {"a":table, "values":values})

@login_required
def overview(request):
	processes = Process.objects.all()
	content = []
	for pro in processes:
		process_name = pro.name
		children_count = pro.processchild_set.all().count()
		process_children = pro.processchild_set.all()
		total_duration = 0.0
		for child in process_children:
			total_duration = total_duration + float(child.duration)
		avg = total_duration/children_count
		content_child = {
		"name" : process_name,
		"average" : avg
		}
		content.append(content_child)
	print(type(content))
	return render(request, 'flex/overview.html', {"content":content})

@login_required
def chart_view(request, b_name_id):
	pro = Process.objects.get(id=b_name_id)
	child_set = pro.processchild_set.all().order_by("-id")[:9].reverse()
	values = []
	for child in child_set:
		values.append([child.start_time, child.duration])
	return render(request, 'flex/graph.html', {'values': values})

@login_required
def monthly_report(request, item_name):
	now = datetime.datetime.now()
	day = now.replace(month = now.month-1, hour=0, minute=0, second=0, microsecond=0)
	pro = Process.objects.get(name=item_name)
	child_set = pro.processchild_set.filter(start_time__gte=day).reverse()[:30]
	values = []
	for child in child_set:
		values.append([child.start_time, child.duration])
	return render(request, "flex/graph.html", {'values':values})


def send_email(request):
	print(email.EMAIL_HOST_USER)
	subject = "Daily report"
	message=""
	from_email = email.EMAIL_HOST_USER
	email_to = ['gopikrishna766@gmail.com']
	now = datetime.datetime.now()
	today = now.replace(hour=0, minute=0, second=0, microsecond=0)
	table = ProcessChild.objects.filter(start_time__gte=today)
	a = ProcessChild.objects.filter(start_time__gte=today).exclude(end_time=None)
	attach = '<p>Please go through the reports shown in the table below</p><table border="1"><thead><th>Process Name</th><th>Start Time</th><th>End Time</th><th>Duration</th></thead>'
	for b in a:
		 attach = attach + ("<tr><td>"+str(b.name)+"</td><td>"+ str(b.start_time) + "</td><td>"+str(b.end_time)+"</td><td>"+str(b.duration)+"Seconds</td></tr>")
	attach = attach+"</table>"	 
	if subject and from_email:
		msg = EmailMultiAlternatives(subject, message, from_email, email_to)
		msg.attach_alternative(attach, "text/html")
		msg.send()
		return HttpResponse()
	else:
		return HttpResponse('something is wrong')    
		