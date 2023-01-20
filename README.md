# model_seg_rabbit_axon-myelin_bf
## Model overview

Standard 2-class segmentation model for ADS trained on rabbit samples (Virginia Commonwealth University)

## Segment (ADS)
To segment an image using this model, use the following command in an `axondeepseg` virtual environment:
```
axondeepseg -t BF -i <IMG_PATH> -m <path/to/model_seg_rabbit_axon-myelin_bf> -s <PIXEL_SIZE>
```

## Train and test (ivadomed)
This model was trained and tested with [ivadomed](https://ivadomed.org/). We recommend you install ivadomed in a virtual environment to reproduce the original training steps. The specific revision hash of the version used for training is documented in the _version_info.log_ file.

### Clone this repository
You will need the model's JSON configuration file named *model_seg_rabbit_axon-myelin_bf.json* located in this repo.
```
git clone https://github.com/axondeepseg/model_seg_rabbit_axon-myelin_bf
```

### Get the data
The dataset used to train this model is hosted on git-annex at `data.neuro.polymtl.ca:datasets/data_axondeepseg_vcu`.

### Train this model
To train the model, please first update the following fields in the training config file:
- `gpu_ids`: specific to your hardware
- `path_output`: where the model will be saved
- `loader_parameters:path_data`: path to training data
- `loader_parameters:fname_split`: None (***NOTE*** this training configuration did not use a joblib split file. The specific training image hashes can be found at the bottom of the config file)
- `bids_config`: path to the custom bids config usually located in ivadomed/config/config_bids.json

Then, you can train the model with
```
ivadomed --train -c path_to_config_file.json
```
The trained model file will be saved under the `path_output` directory. For more information about training models in `ivadomed`, please refer to the following [tutorial](https://ivadomed.org/tutorials/two_class_microscopy_seg_2d_unet.html).

### Evaluate this model
To test the performance of this model, use
```
ivadomed --test -c path_to_config_file.json
```
The evaluation results will be saved in `"path_output"/results_eval/evaluation_3Dmetrics.csv`
