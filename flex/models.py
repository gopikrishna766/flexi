from __future__ import unicode_literals

from django.db import models
import timedelta
# Create your models here.

class Process(models.Model):
	name = models.CharField(max_length=200)
	
	def __str__(self):
		return self.name

class ProcessChild(models.Model):
	process_id = models.CharField(max_length=20)
	name = models.ForeignKey('Process')
	start_time = models.DateTimeField()
	end_time = models.DateTimeField(blank = True, null = True)
	status = models.BooleanField(default=False)
	duration = models.FloatField(default=0)
	
	def __str__(self):
		return self.process_id

	def __unicode__(self):
		return self.process_id	
