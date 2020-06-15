from django.db import models
from django.contrib.auth.models import User
from protAPI import cloud_storage
from django.db.models.signals import post_save, post_delete

# Create your models here.

class ModelStructure(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=100, unique=True)
    description = models.CharField(max_length=250)
    code = models.TextField(null=True)
    fecha = models.DateField(auto_now=True)
    epochs = models.IntegerField(default=10)
    # file = models.FileField(null=True)
    # public = models.BooleanField(default=False)



class ModelTrained(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=250)
    file = models.FileField(null=True)
    public = models.BooleanField(default=False)

def upload_model(sender, **kwargs):
    instance = kwargs['instance']
    try:
        file_path = "media/" + str(instance.file)
        to_storage = cloud_storage.upload_file(file_path, 'protein-public', str(instance.file))
    except:
        file_path = str(instance.file)
        to_storage = cloud_storage.upload_file(file_path, 'protein-public', str(instance.file))

    if to_storage:
        print("Uploaded to s3")
    else:
        print("Error uploading to s3")

post_save.connect(upload_model, sender=ModelTrained)


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

def upload_pdb(sender, **kwargs):
    instance = kwargs['instance']
    file_path = "media/" + str(instance.pdb)
    to_storage = cloud_storage.upload_file(file_path, 'protein-public', str(instance.pdb))

    if to_storage:
        print("Uploaded to s3")
    else:
        print("Error uploading to s3")

post_save.connect(upload_pdb, sender=Job)











