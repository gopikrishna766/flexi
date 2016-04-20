import iso8601, datetime
from django.utils.safestring import mark_safe
from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import send_mail


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

def process_list(request):
	now = datetime.datetime.now()
	today = now.replace(hour=0, minute=0, second=0, microsecond=0)
	table = ProcessChild.objects.filter(start_time__gte=today)
	a = ProcessChild.objects.filter(start_time__gte=today).exclude(end_time=None)
	values = []
	for b in a:
		values.append([b.name.name, b.duration])
	return render(request, "flex/process_list.html", {"a":table, "values":values})

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

def chart_view(request, b_name_id):
	pro = Process.objects.get(id=b_name_id)
	child_set = pro.processchild_set.all().order_by("-id")[:9].reverse()
	values = []
	for child in child_set:
		values.append([child.start_time, child.duration])
	return render(request, 'flex/graph.html', {'values': values})
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
	message = "please go through the reports shown in the table below"
	from_email = email.EMAIL_HOST_USER
	email_to = ['gopikrishna766@gmail.com']
	if subject and message and from_email:
		send_mail(subject, message, from_email, email_to, fail_silently=False)
		return HttpResponse('/contact/thanks/')
	else:
		return HttpResponse('Make sure all fields are entered and valid.')    
		