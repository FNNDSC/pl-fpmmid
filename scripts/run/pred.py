"""
This module infer predictions for multi-class segmentation
layers of a 3D MRI scan volume based on FPMMID trained network
"""

import os
# To disable Tensorflow unnecessary logins, log level should be set
# right after import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '1'

import time
import logging
import pickle
import numpy as np
from .modules import unet as un
from .modules import seg_utility as seg_u
from .modules import vol_reader as vlr
from .data import Subject
import tensorflow as tf
from tensorflow import keras as ks

def main(input_path, out_dir, root_dir):
    """
    This function executes the inference and data modules on a
    given MRI scan
    """
    # Create a logger object
    logger = logging.getLogger()
            
    # set level 
    logger.setLevel(logging.INFO)
    
    # lets create a log file in the o/p directory first
    log_file = os.path.join(root_dir,'pred.log')
            
    lf = open(log_file,"w")
    
                
    # now create and configure logger
    file_handler = logging.FileHandler(log_file)
        
    # add handler
    logger.addHandler(file_handler)
    st_ = time.time()
    model_name = "fpmmid"

    input_data = Subject(model_name)
    dims, num_channels, num_classes, sid, vol = input_data.prep_data(input_path, \
                                                                root_dir)

    et_1 = time.time()
    model = Pred(model_name,out_dir)
    model.run_pred(dims, num_channels, num_classes, out_dir, root_dir, sid, vol, logger)
    et_2 = time.time()

    logging.basicConfig(filename = os.path.join(root_dir, "pred.log"), \
    filemode = 'a',level = logging.INFO)
    logging.info("Elapsed Time - Total: %.2f sec", (et_2 - st_))
    logging.info("Elapsed Time - Data Prep: %.2f sec", (et_1 - st_))
    logging.info("Elapsed Time - Inference: %.2f sec", (et_2 - et_1))
    
    # Close logging
    logger.removeHandler(file_handler)
    file_handler.close()
    lf.close()

class Config:
    """
    This class provides inputs and outputs and pre-post configs
    to the Pred Class
    """
    def __init__(self, name,out_dir):
        self.name = name
        self.batch_size = 1
        self.shuffle_buffer_size = 1
        self.alpha1 = 0
        self.activation = 'relu'
        self.scale = 4
        self.d_rate = 0.2
        self.init_fil = 64
        self.init_lr = 0.001
        self.is_parallel = "false"
        # input paths
        self.model_path = '/usr/local/src/model'
        self.weights_file = 'cw.pickle'
        self.model_file = 'cp.ckpt'
        self.log_file = 'pred.log'
        self.out_path = out_dir
        self.out_file_type = 'PNVM'
        self.out_file_format = '.nii.gz'
        self.out_image_format = '.png'

    def find_weights(self):
        """
        This method will find the class weights for each segmented layer
        based on the averaged trained class weigths
        """
        with open(os.path.join(self.model_path, self.weights_file), 'rb') as outfile:
            class_weights = pickle.load(outfile)
            return class_weights

    def write_nifti(self, vol_pred, sid):
        """ 
        write back nifti images
        """
        vlr.volume_writer(vol_pred, os.path.join(self.out_path, sid \
                                                     + '_' \
                                                     + self.out_file_type \
                                                     + self.out_file_format))

    def write_image(self, vol_input, vol_pred, out_dir, sid):
        """write back 2D mid-slice images"""
        seg_u.mask_show(vol_input, vol_pred, \
                        os.path.join(out_dir, sid \
	                    + '_' \
                        + self.out_file_type \
                        + self.out_image_format), self.out_file_type)

class Pred:
    """
    This class provides the inference for a given MRI scan
    """
    def __init__(self, name, out_dir):
        self.name = name
        self.obj_config = Config(name, out_dir)

    def run_pred(self, dims, num_channels, num_classes, out_dir, root_dir, sid, vol, logger):
        """
        This method will build the inference model for a given MRI scan volume
        """

        logging.info("Inference - Started...")

        # load weights
        class_weights = self.obj_config.find_weights()

        # building the UNET model
        inputs = ks.Input((dims[0], dims[1], dims[2], num_channels))
        outputs = un.network(inputs, num_classes, self.obj_config.d_rate, \
                             self.obj_config.init_fil, self.obj_config.scale, \
                             self.obj_config.activation)

        # Create the model
        model_final = un.create_model(self.obj_config.init_lr, inputs, \
                                      self.obj_config.is_parallel, \
									  outputs, sample_weight=class_weights)
        # Inference
        model_final.load_weights(os.path.join(self.obj_config.model_path, \
                                 self.obj_config.model_file)).expect_partial()
        mask_pred = model_final.predict(vol)
        logging.info("Inference - Finished.")

        # Write nifti
        self.obj_config.write_nifti(np.argmax(mask_pred[0], axis = 3), sid)
        
        # Write image
        self.obj_config.write_image(vol[0], mask_pred[0], out_dir, sid)


if __name__ == "__main__":
    main()
