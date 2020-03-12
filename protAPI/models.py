from django.db import models

# Create your models here.


class ProtUser(models.Model):
    name = models.CharField(max_length=250)
    email = models.CharField(max_length=250)
    password = models.CharField(max_length=250)


class ModelTrained(models.Model):
    author = models.ForeignKey(ProtUser, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=250)
    file = models.FileField(null=True)


class StatusJob(models.Model):
    description = models.CharField(max_length=250)
    active = models.BooleanField(default=True)

class Job(models.Model):
    user = models.ForeignKey(ProtUser, related_name='jobs', on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    duration = models.FloatField()
    description = models.CharField(max_length=200)
    status = models.ForeignKey(StatusJob, on_delete=models.CASCADE)
    model = models.ForeignKey(ModelTrained, null=True, on_delete=models.CASCADE)
    pdb = models.FileField(null=True)

    def __str__(self):
        return '%d: %s' % (self.pk, self.description)


