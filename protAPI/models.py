from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class ModelTrained(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=250)
    file = models.FileField(null=True)
    public = models.BooleanField(default=False)

class StatusTraining(models.Model):
    description = models.CharField(max_length=250)
    active = models.BooleanField(default=True)

class Training(models.Model):
    # author = models.ForeignKey(ProtUser, on_delete=models.CASCADE)
    # name = models.CharField(max_length=100)
    # description = models.CharField(max_length=250)
    dataset_url = models.CharField(max_length=250)
    start_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField(auto_now=True)
    status = models.ForeignKey(StatusTraining, null=True, on_delete=models.CASCADE)
    trained_model = models.ForeignKey(ModelTrained, null=True, on_delete=models.CASCADE)

class StatusJob(models.Model):
    description = models.CharField(max_length=250)
    active = models.BooleanField(default=True)

class Job(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    duration = models.FloatField(null=True)
    description = models.CharField(max_length=200, null=True)
    status = models.ForeignKey(StatusJob, on_delete=models.CASCADE, null=True)
    model = models.ForeignKey(ModelTrained, null=True, on_delete=models.CASCADE)
    pdb = models.FileField(null=True)

    def __str__(self):
        return '%d: %s' % (self.pk, self.description)


