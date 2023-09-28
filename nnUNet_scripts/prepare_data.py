#!/usr/bin/env python3
"""Prepares the VCU data for nnUNetv2
The 2 output classes must be put in a single mask with values 1 and 2
(0 is for background). All subjects with annotations are put in the 
training set (nnUNet will do cross-validation automatically). The other 
subjects are put in the testing set.
"""

__author__ = "Armand Collin"
__license__ = "MIT"

import argparse
import json
import cv2
import numpy as np
from pathlib import Path


def main(args):
    datapath = Path(args.DATAPATH)
    derivatives = list((datapath / 'derivatives' / 'labels').glob('sub*'))
    subject_list = [d.name for d in derivatives]
    # create nnUNet_raw folder
    out_folder = Path.cwd() / 'nnUNet_raw' / 'Dataset001_VCU'
    out_folder.mkdir(parents=True, exist_ok=True)
    (out_folder / 'imagesTr').mkdir(exist_ok=True)
    (out_folder / 'labelsTr').mkdir(exist_ok=True)
    (out_folder / 'imagesTs').mkdir(exist_ok=True)
    # create dataset.json
    dataset_info = {
        "channel_names": {
            "0": "rgb_to_0_1"
        },
        "labels": {
            "background": 0,
            "myelin": 1, 
            "axon": 2 
        },
        "numTraining": 8,
        "file_ending": ".png"
    }
    with open('nnUNet_raw/Dataset001_VCU/dataset.json', 'w') as f:
        f.write(json.dumps(dataset_info, indent=1))

    # save correspondence between original fnames and case IDs
    case_id_dict = {sub:i for i,sub in enumerate(subject_list)}

    # put images in imagesTr
    # (convert TIFFs to PNGs! file endings must match)
    for subject in subject_list:
        case_id = case_id_dict[subject]
        # (assuming there is only 1 valid image per subject folder)
        img_fname = next((datapath / subject / 'micr').glob('*.tif'))
        img = cv2.imread(str(img_fname))
        fname = f'VCU_{case_id:03d}_0000.png'
        cv2.imwrite(str(out_folder / 'imagesTr' / fname), img)
        
        # put labels in labelsTr
        ax_path = next((datapath / 'derivatives' / 'labels' / subject / 'micr').glob('*seg-axon-manual*'))
        my_path = next((datapath / 'derivatives' / 'labels' / subject / 'micr').glob('*seg-myelin-manual*'))
        ax = cv2.imread(str(ax_path)) // 255
        my = cv2.imread(str(my_path)) // 255
        label = my + 2 * ax
        fname = f'VCU_{case_id:03d}.png'
        #NOTE: might need to only take one channel for the GT?
        cv2.imwrite(str(out_folder / 'labelsTr' / fname), label)

    # put unannotated images in imagesTs for testing
    # (convert TIFFs to PNGs! file endings must match)
    unnanotated_subjects = list((datapath / 'derivatives' / 'ads-derivatives').glob('sub*'))
    unnanotated_subjects = [d.name for d in unnanotated_subjects]
    test_case_id = max(case_id_dict.values())
    for subject in unnanotated_subjects:
        test_case_id += 1
        img_fname = next((datapath / subject / 'micr').glob('*.tif'))
        img = cv2.imread(str(img_fname))
        fname = f'VCU_{test_case_id:03d}_0000.png'
        cv2.imwrite(str(out_folder / 'imagesTs' / fname), img)
        # add the test subject to case_id_dict
        case_id_dict[subject] = test_case_id
    
    with open('subject_to_case_identifier.json', 'w') as f:
        f.write(json.dumps(case_id_dict, indent=2))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    # Required positional argument
    parser.add_argument("DATAPATH", help="path to VCU dataset (BIDS format)")
    # Optional argument flag which defaults to False
    parser.add_argument(
        "-m", "--move", 
        action="store_true", 
        default=False,
        help='move files instead of copying them')

    args = parser.parse_args()
    main(args)
