try:
    import importlib
    from protAPI.proteinnet.preprocessing import *
    # from protAPI.proteinnet.custom_models import *
    from protAPI.proteinnet.training import train_model
    from protAPI.proteinnet.util import *
except:
    print("Import error")
    import time
    time.sleep(5)
    from preprocessing import *
    from custom_models import *
    from training import train_model
import argparse




# pre-process data
process_raw_data(False, force_pre_processing_overwrite=False)

# run experiment
# training_file = args.input_file
training_file = settings.BASE_DIR + "/protAPI/proteinnet/data/preprocessed/sample.txt.hdf5"
validation_file = settings.BASE_DIR + "/protAPI/proteinnet/data/preprocessed/sample.txt.hdf5"
# validation_file = args.input_file

dinamic_model = getattr(importlib.import_module("protAPI.proteinnet.custom_models"), "MyModel")

model = dinamic_model(21, 5, use_gpu=False)  # embed size = 21


train_loader = contruct_dataloader_from_disk(training_file, 5)
validation_loader = contruct_dataloader_from_disk(validation_file, 5)

train_model_path = train_model(data_set_identifier="TRAINXX",
                               model=model,
                               train_loader=train_loader,
                               validation_loader=validation_loader,
                               learning_rate=0.1,
                               minibatch_size=5,
                               eval_interval=5,
                               hide_ui=True,
                               use_gpu=False,
                               minimum_updates=1) # Epochs

print("Completed training, trained model stored at:")
print(train_model_path)

