# Achieved: Use pedestrian safety pipeline repo instead

## Pedestrain_Trajectory
Pedestrain prediction based on GAN (base code source -Agrim Gupta and Justin Johnson)
Base code owners give full permission for use ,copy, modification and/or merging free of charge 
under the MIT License

The following notice is required by authours to be included in all copies or susbstential portions of the software.

MIT License

Copyright (c) 2018 Agrim Gupta Justin Johnson

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.


## How it works

The base code, as mentioned above is from Pedestrian Prediction paper based on GAN.
For more info on how the base code works, refer the orignal md files:
- training.md  for training your own models
- model zoo - to use pre trained models
- SGAN - for general navigation of base code

the orignal work can be found [HERE](https://github.com/agrimgupta92/sgan.git)

## Integration With ROS
 
The prediction and integration with ROS is done in [evaluation_with_ROS.py](https://github.com/AV-Lab/Pedestrain_Trajectory/blob/main/evaluate_with_ROS.py)
In the main function, the "path" to a pre-traned model is selcted. As default the pre-trained model used is zara_8 model.
Change the models according to your needs. If a new model is trained the choice of model for prediction should chnage as well.

The ROS implementation can be found in the main function. one of the most important parameters in the evualtion_with_ROs is the number of predicted trajectories, 
which can be changed from evaluate funtion. By deafult the number of predicted trajectories is 12. 

## Note
before runnning the code make sure ROS is set properly and all the required files are downloaded.
Models and Datasets can be downloaded via [download_models](https://github.com/AV-Lab/Pedestrain_Trajectory/blob/main/download_models.sh) and [download_datasets](https://github.com/AV-Lab/Pedestrain_Trajectory/blob/main/download_data.sh) respectivelys.
- Model folder contains all the models (if model folder is already downloaded, there is no need to use the above mentioned method). 
     The dataset,however, contains only one datset (Zara) to make it easier for testing without downloading everything. 
     If you wish to download the rest of the datasets please use the above mentioned shell code.
