import os
import argparse
import numpy as np
import tensorflow as tf

from model import Model

parser = argparse.ArgumentParser()
parser.add_argument("--notsherpa", default=False, action='store_true')
parser.add_argument("--seed", type=int, default=None)
parser.add_argument('--gpu', type=str, default='')
args =  parser.parse_args()

tf.set_random_seed(0); np.random.seed(0)

gpu = os.environ.get("SHERPA_RESOURCE", '')
os.environ['CUDA_VISIBLE_DEVICES'] = str(gpu or args.gpu)

config = tf.ConfigProto(); config.gpu_options.allow_growth=True
sess = tf.Session(config=config)

##############################
import sherpa
client = sherpa.Client()
trial = client.get_trial()
##############################

model = Model(trial.parameters)



model.save_model(
    'SherpaResults/{name}/Models/{id}.h5'.format(
        name=trial.parameters['name'],
        id='%05d' % trial.id
    )
)
