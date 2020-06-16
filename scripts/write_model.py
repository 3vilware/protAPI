try:
    import importlib
    from protAPI.proteinnet.preprocessing import *
    # from protAPI.proteinnet.custom_models import *
    from protAPI.proteinnet.training import train_model
    from protAPI.proteinnet.util import *
    from protAPI.mailing import send_report_mail
    from protAPI.models import ModelTrained, ModelStructure
    from django.contrib.auth.models import User
except:
    print("Import error")
    import time
    time.sleep(5)
    from preprocessing import *
    from custom_models import *
    from training import train_model
import argparse


def run(*args):
    #
    model_name = args[0]
    model_from_db = ModelStructure.objects.get(name=model_name)
    file_path = settings.BASE_DIR + "/protAPI/proteinnet/custom_models.py"
    f = open(file_path, "a")
    f.write(model_from_db.code)
    f.close()