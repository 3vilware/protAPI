# This file is part of the OpenProtein project.
#
# @author Jeppe Hallgren
#
# For license information, please see the LICENSE file in the root directory.

import torch
from protAPI.proteinnet.util import *
from protMaster import settings

def init():
    input_sequences = ["VLSAADKTNVKAAWSKVGGHAGEYGAEALERMFLGFPTTKTYFPHFDLSHGSAQVKAHGKKVADGLTLAVGHLDDLPGALSDLSNLHAHKLRVDPVNFKLLSHCLLSTLAVHLPNDFTPAVHASLDKFLSSVSTVLTSKYR"]
    # input_sequences = ["SRSLVISTINQISEDSKEFYFTLDNGKTMFPSNSQAWGGEKFENGQRAFVIFNELEQPVNGYDYNIQVRDITKVLTKEIVTMDDEENTEEKIGDDKINATYMWISKDKKYLTIEFQYYSTHSEDKKHFLNLVINNKDNTDDEYINLEFRHNSERDSPDHLGEGYVSFKLDKIEEQIEGKKGLNIRVRTLYDGIKNYKVQFP"]
    #input_sequences = ["MNVVIVRYGEIGTKSRQTRSWFEKILMNNIREALVTEEVPYKEIFSRHGRIIVKTNSPKEAANVLVRVFGIVSISPAMEVEASLEKINRTALLMFRKKAKEVGKERPKFRVTARRITKEFPLDSLEIQAKVGEYILNNENCEVDLKNYDIEIGIEIMQGKAYIYTEKIKGWGGLPIGTEGRMIGILHDELSALAIFLMMKRGVEVIPVYIGKDDKNLEKVRSLWNLLKRYSYGSKGFLVVAESFDRVLKLIRDFGVKGVIKGLRPNDLNSEVSEITEDFKMFPVPVYYPLIALPEEYIKSVKERLGL"]
    model_path = settings.BASE_DIR + "/protAPI/proteinnet/output/models/2020-02-27_05_47_39-TRAIN-LR0_01-MB5.model"

    model = torch.load(model_path)
    input_senquences_encoded = list(torch.LongTensor(encode_primary_string(aa)) for aa in input_sequences)

    predicted_dihedral_angles, predicted_backbone_atoms, batch_sizes = model(input_senquences_encoded)

    write_to_pdb(
        get_structure_from_angles(input_senquences_encoded[0], predicted_dihedral_angles[:,0]),
        "myprediction"
    )

    print("Wrote prediction to output/protein_myprediction.pdb")


def run_job(aa_chain, model="", job_id=""):
    input_sequences = [aa_chain]
    model_path = settings.BASE_DIR + "/protAPI/proteinnet/output/models/2020-02-27_05_47_39-TRAIN-LR0_01-MB5.model"


    model = torch.load(model_path)
    input_senquences_encoded = list(torch.LongTensor(encode_primary_string(aa)) for aa in input_sequences)

    predicted_dihedral_angles, predicted_backbone_atoms, batch_sizes = model(input_senquences_encoded)

    write_to_pdb(
        get_structure_from_angles(input_senquences_encoded[0], predicted_dihedral_angles[:,0]),
        job_id
    )

    print("Wrote prediction to output/protein_{}.pdb".format(job_id))

    return "protein_{}.pdb".format(job_id)
