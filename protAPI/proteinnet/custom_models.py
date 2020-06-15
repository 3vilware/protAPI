# This file is part of the OpenProtein project.
#
# @author Jeppe Hallgren
#
# For license information, please see the LICENSE file in the root directory.

import torch.autograd as autograd
import torch.nn as nn
import torch.nn.utils.rnn as rnn_utils
import time
import numpy as np
try:
    from protAPI.proteinnet import openprotein
    from protMaster import settings
    from protAPI.proteinnet.util import *
    base_dir = settings.BASE_DIR + "/protAPI/proteinnet/"
except:
    import openprotein
    from util import *
    import pathlib
    base_dir = str(pathlib.Path().absolute()) + "/"

# seed random generator for reproducibility
torch.manual_seed(1)
ANGLE_ARR = torch.tensor([[-120, 140, -370], [0, 120, -150], [25, -120, 150]]).float()


class newModel(openprotein.BaseModel):
    def __init__(self, embedding_size, use_gpu):
        super(newModel, self).__init__(use_gpu, embedding_size)
        self.use_gpu = use_gpu
        self.number_angles = 3
        self.input_to_angles = nn.Linear(embedding_size, self.number_angles)


    def _get_network_emissions(self, original_aa_string):
        embedded_input = self.embed(original_aa_string)
        emissions_padded = self.input_to_angles(embedded_input)

        emissions = emissions_padded.transpose(0, 1)  # minibatch_size, self.mixture_size, -1

        probabilities = torch.softmax(emissions, 2) # p

        output_angles = torch.matmul(probabilities, ANGLE_ARR).transpose(0, 1)
        
        batch_sizes = list([a.size() for a in original_aa_string])

        return output_angles, [], batch_sizes

# Escribe tu modelo. Puedes sobre escribir esta plantilla (Python 3.8)
class MyModelA(openprotein.BaseModel):
    def __init__(self, embedding_size, use_gpu=False):
        super(MyModelA, self).__init__(use_gpu, embedding_size)
        self.use_gpu = use_gpu
        self.number_angles = 3
        self.input_to_angles = nn.Linear(embedding_size, self.number_angles)


    def _get_network_emissions(self, original_aa_string):
        embedded_input = self.embed(original_aa_string)
        emissions_padded = self.input_to_angles(embedded_input)

        emissions = emissions_padded.transpose(0, 1)  # minibatch_size, self.mixture_size, -1

        probabilities = torch.softmax(emissions, 2) # p

        output_angles = torch.matmul(probabilities, ANGLE_ARR).transpose(0, 1)
        
        batch_sizes = list([a.size() for a in original_aa_string])

        return output_angles, [], batch_sizes# Escribe tu modelo. Puedes sobre escribir esta plantilla (Python 3.8)
class q2(openprotein.BaseModel):
    def __init__(self, embedding_size, use_gpu=False):
        super(q2, self).__init__(use_gpu, embedding_size)
        self.use_gpu = False
        self.number_angles = 3
        self.input_to_angles = nn.Linear(embedding_size, self.number_angles)


    def _get_network_emissions(self, original_aa_string):
        embedded_input = self.embed(original_aa_string)
        emissions_padded = self.input_to_angles(embedded_input)

        emissions = emissions_padded.transpose(0, 1)  # minibatch_size, self.mixture_size, -1

        probabilities = torch.softmax(emissions, 2) # p

        output_angles = torch.matmul(probabilities, ANGLE_ARR).transpose(0, 1)
        
        batch_sizes = list([a.size() for a in original_aa_string])

        return output_angles, [], batch_sizes# Escribe tu modelo. Puedes sobre escribir esta plantilla (Python 3.8)
class Q1(openprotein.BaseModel):
    def __init__(self, embedding_size, use_gpu=False):
        super(Q1, self).__init__(use_gpu, embedding_size)
        self.use_gpu = use_gpu
        self.number_angles = 3
        self.input_to_angles = nn.Linear(embedding_size, self.number_angles)


    def _get_network_emissions(self, original_aa_string):
        embedded_input = self.embed(original_aa_string)
        emissions_padded = self.input_to_angles(embedded_input)

        emissions = emissions_padded.transpose(0, 1)  # minibatch_size, self.mixture_size, -1

        probabilities = torch.softmax(emissions, 2) # p

        output_angles = torch.matmul(probabilities, ANGLE_ARR).transpose(0, 1)
        
        batch_sizes = list([a.size() for a in original_aa_string])

        return output_angles, [], batch_sizes# Escribe tu modelo. Puedes sobre escribir esta plantilla (Python 3.8)
class Q2(openprotein.BaseModel):
    def __init__(self, embedding_size, use_gpu=False):
        super(Q2, self).__init__(use_gpu, embedding_size)
        self.use_gpu = use_gpu
        self.number_angles = 3
        self.input_to_angles = nn.Linear(embedding_size, self.number_angles)


    def _get_network_emissions(self, original_aa_string):
        embedded_input = self.embed(original_aa_string)
        emissions_padded = self.input_to_angles(embedded_input)

        emissions = emissions_padded.transpose(0, 1)  # minibatch_size, self.mixture_size, -1

        probabilities = torch.softmax(emissions, 2) # p

        output_angles = torch.matmul(probabilities, ANGLE_ARR).transpose(0, 1)
        
        batch_sizes = list([a.size() for a in original_aa_string])

        return output_angles, [], batch_sizes# Escribe tu modelo. Puedes sobre escribir esta plantilla (Python 3.8)
class aa(openprotein.BaseModel):
    def __init__(self, embedding_size, use_gpu=False):
        super(aa, self).__init__(use_gpu, embedding_size)
        self.use_gpu = use_gpu
        self.number_angles = 3
        self.input_to_angles = nn.Linear(embedding_size, self.number_angles)


    def _get_network_emissions(self, original_aa_string):
        embedded_input = self.embed(original_aa_string)
        emissions_padded = self.input_to_angles(embedded_input)

        emissions = emissions_padded.transpose(0, 1)  # minibatch_size, self.mixture_size, -1

        probabilities = torch.softmax(emissions, 2) # p

        output_angles = torch.matmul(probabilities, ANGLE_ARR).transpose(0, 1)
        
        batch_sizes = list([a.size() for a in original_aa_string])

        return output_angles, [], batch_sizes# Escribe tu modelo. Puedes sobre escribir esta plantilla (Python 3.8)
# Escribe tu modelo. Puedes sobre escribir esta plantilla (Python 3.8)
class ss(openprotein.BaseModel):
    def __init__(self, embedding_size, use_gpu=False):
        super(ss, self).__init__(use_gpu, embedding_size)
        self.use_gpu = use_gpu
        self.number_angles = 3
        self.input_to_angles = nn.Linear(embedding_size, self.number_angles)


    def _get_network_emissions(self, original_aa_string):
        embedded_input = self.embed(original_aa_string)
        emissions_padded = self.input_to_angles(embedded_input)

        emissions = emissions_padded.transpose(0, 1)  # minibatch_size, self.mixture_size, -1

        probabilities = torch.softmax(emissions, 2) # p

        output_angles = torch.matmul(probabilities, ANGLE_ARR).transpose(0, 1)
        
        batch_sizes = list([a.size() for a in original_aa_string])

        return output_angles, [], batch_sizes# Escribe tu modelo. Puedes sobre escribir esta plantilla (Python 3.8)
class zz(openprotein.BaseModel):
    def __init__(self, embedding_size, use_gpu=False):
        super(zz, self).__init__(use_gpu, embedding_size)
        self.use_gpu = use_gpu
        self.number_angles = 3
        self.input_to_angles = nn.Linear(embedding_size, self.number_angles)


    def _get_network_emissions(self, original_aa_string):
        embedded_input = self.embed(original_aa_string)
        emissions_padded = self.input_to_angles(embedded_input)

        emissions = emissions_padded.transpose(0, 1)  # minibatch_size, self.mixture_size, -1

        probabilities = torch.softmax(emissions, 2) # p

        output_angles = torch.matmul(probabilities, ANGLE_ARR).transpose(0, 1)
        
        batch_sizes = list([a.size() for a in original_aa_string])

        return output_angles, [], batch_sizes# Escribe tu modelo. Puedes sobre escribir esta plantilla (Python 3.8)
class xx(openprotein.BaseModel):
    def __init__(self, embedding_size, use_gpu=False):
        super(xx, self).__init__(use_gpu, embedding_size)
        self.use_gpu = use_gpu
        self.number_angles = 3
        self.input_to_angles = nn.Linear(embedding_size, self.number_angles)


    def _get_network_emissions(self, original_aa_string):
        embedded_input = self.embed(original_aa_string)
        emissions_padded = self.input_to_angles(embedded_input)

        emissions = emissions_padded.transpose(0, 1)  # minibatch_size, self.mixture_size, -1

        probabilities = torch.softmax(emissions, 2) # p

        output_angles = torch.matmul(probabilities, ANGLE_ARR).transpose(0, 1)
        
        batch_sizes = list([a.size() for a in original_aa_string])

        return output_angles, [], batch_sizes# Escribe tu modelo. Puedes sobre escribir esta plantilla (Python 3.8)
class VM(openprotein.BaseModel):
    def __init__(self, embedding_size, use_gpu=False):
        super(VM, self).__init__(use_gpu, embedding_size)
        self.use_gpu = use_gpu
        self.number_angles = 3
        self.input_to_angles = nn.Linear(embedding_size, self.number_angles)


    def _get_network_emissions(self, original_aa_string):
        embedded_input = self.embed(original_aa_string)
        emissions_padded = self.input_to_angles(embedded_input)

        emissions = emissions_padded.transpose(0, 1)  # minibatch_size, self.mixture_size, -1

        probabilities = torch.softmax(emissions, 2) # p

        output_angles = torch.matmul(probabilities, ANGLE_ARR).transpose(0, 1)
        
        batch_sizes = list([a.size() for a in original_aa_string])

        return output_angles, [], batch_sizes# Escribe tu modelo. Puedes sobre escribir esta plantilla (Python 3.8)
class timeModel(openprotein.BaseModel):
    def __init__(self, embedding_size, use_gpu=False):
        super(timeModel, self).__init__(use_gpu, embedding_size)
        self.use_gpu = use_gpu
        self.number_angles = 3
        self.input_to_angles = nn.Linear(embedding_size, self.number_angles)


    def _get_network_emissions(self, original_aa_string):
        embedded_input = self.embed(original_aa_string)
        emissions_padded = self.input_to_angles(embedded_input)
        print(emissions_padded)
        import time
        time.sleep(10)

        emissions = emissions_padded.transpose(0, 1)  # minibatch_size, self.mixture_size, -1

        probabilities = torch.softmax(emissions, 2) # p

        output_angles = torch.matmul(probabilities, ANGLE_ARR).transpose(0, 1)
        
        batch_sizes = list([a.size() for a in original_aa_string])

        return output_angles, [], batch_sizes# Escribe tu modelo. Puedes sobre escribir esta plantilla (Python 3.8)
class timeModel2(openprotein.BaseModel):
    def __init__(self, embedding_size, use_gpu=False):
        super(timeModel2, self).__init__(use_gpu, embedding_size)
        self.use_gpu = use_gpu
        self.number_angles = 3
        self.input_to_angles = nn.Linear(embedding_size, self.number_angles)


    def _get_network_emissions(self, original_aa_string):
        embedded_input = self.embed(original_aa_string)
        emissions_padded = self.input_to_angles(embedded_input)
        print(emissions_padded)
        import time
        time.sleep(10)

        emissions = emissions_padded.transpose(0, 1)  # minibatch_size, self.mixture_size, -1

        probabilities = torch.softmax(emissions, 2) # p

        output_angles = torch.matmul(probabilities, ANGLE_ARR).transpose(0, 1)
        
        batch_sizes = list([a.size() for a in original_aa_string])

        return output_angles, [], batch_sizes# Escribe tu modelo. Puedes sobre escribir esta plantilla (Python 3.8)
class liM(openprotein.BaseModel):
    def __init__(self, embedding_size, use_gpu=False):
        super(liM, self).__init__(use_gpu, embedding_size)
        self.use_gpu = use_gpu
        self.number_angles = 3
        self.input_to_angles = nn.Linear(embedding_size, self.number_angles)


    def _get_network_emissions(self, original_aa_string):
        embedded_input = self.embed(original_aa_string)
        emissions_padded = self.input_to_angles(embedded_input)
        emissions_padded = self.input_to_angles(emissions_padded)


        emissions = emissions_padded.transpose(0, 1)  # minibatch_size, self.mixture_size, -1

        probabilities = torch.softmax(emissions, 2) # p

        output_angles = torch.matmul(probabilities, ANGLE_ARR).transpose(0, 1)
        
        batch_sizes = list([a.size() for a in original_aa_string])

        return output_angles, [], batch_sizes# Escribe tu modelo. Puedes sobre escribir esta plantilla (Python 3.8)
class Mcustom(openprotein.BaseModel):
    def __init__(self, embedding_size, use_gpu=False):
        super(Mcustom, self).__init__(use_gpu, embedding_size)
        self.use_gpu = use_gpu
        self.number_angles = 3
        self.input_to_angles = nn.Linear(embedding_size, self.number_angles)


    def _get_network_emissions(self, original_aa_string):
        embedded_input = self.embed(original_aa_string)
        emissions_padded = self.input_to_angles(embedded_input)

        emissions = emissions_padded.transpose(0, 1)  # minibatch_size, self.mixture_size, -1

        probabilities = torch.softmax(emissions, 2) # p

        output_angles = torch.matmul(probabilities, ANGLE_ARR).transpose(0, 1)
        
        batch_sizes = list([a.size() for a in original_aa_string])

        return output_angles, [], batch_sizes# Escribe tu modelo. Puedes sobre escribir esta plantilla (Python 3.8)
class Mcustom2(openprotein.BaseModel):
    def __init__(self, embedding_size, use_gpu=False):
        super(Mcustom2, self).__init__(use_gpu, embedding_size)
        self.use_gpu = use_gpu
        self.number_angles = 3
        self.input_to_angles = nn.Linear(embedding_size, self.number_angles)


    def _get_network_emissions(self, original_aa_string):
        embedded_input = self.embed(original_aa_string)
        emissions_padded = self.input_to_angles(embedded_input)

        emissions = emissions_padded.transpose(0, 1)  # minibatch_size, self.mixture_size, -1

        probabilities = torch.softmax(emissions, 2) # p

        output_angles = torch.matmul(probabilities, ANGLE_ARR).transpose(0, 1)
        
        batch_sizes = list([a.size() for a in original_aa_string])

        return output_angles, [], batch_sizes