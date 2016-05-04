from __future__ import unicode_literals
from django.db import models
# Create your models here.

class Process(models.Model):
	name = models.CharField(max_length=200)

	def __str__(self):
		return self.name

class ProcessChild(models.Model):
	STATUS_CHOICES = (
        ('failed', 'failed'),
        ('success', 'success'),
    )
	process_id = models.CharField(max_length=20)
	name = models.ForeignKey('Process')
	start_time = models.DateTimeField()
	end_time = models.DateTimeField(blank = True, null = True)
	status = models.BooleanField(default=False)
	duration = models.FloatField(blank = True, null = True)

	def __str__(self):
		return self.process_id

	def __unicode__(self):
		return self.process_id
