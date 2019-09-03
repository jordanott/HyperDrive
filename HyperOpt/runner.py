import sherpa
import argparse
import datetime
import itertools

from utils import build_directory

parser = argparse.ArgumentParser()
parser.add_argument('--name', type=str, default='OutputDir', help='name for output folder')
parser.add_argument('--gpus',type=str, default='',help='Available gpus separated by comma.')
parser.add_argument('--max_concurrent',type=int, default=1, help='Number of concurrent processes')

parser.add_argument('--max_layers',type=int, default=3)
parser.add_argument('--epochs', type=int, default=100)
parser.add_argument('--save_model', type=str, default='none', choices=['none', 'json', 'all'])
FLAGS = parser.parse_args()

parameters = [
    sherpa.Choice('number_of_layers', [2, FLAGS.max_layers]),
    sherpa.Choice('lr', [0.01, 0.001, 0.0001]),
    sherpa.Choice('batch_size', [32]),
    # sherpa.Choice('activation', ['relu', 'prelu', 'elu', 'leaky_relu', 'sigmoid']),
    # sherpa.Choice('kernel_initializer', ['glorot_normal', 'glorot_uniform', 'he_normal', 'he_uniform']),
]

for k,v in vars(FLAGS).iteritems():
    parameters.append(
        sherpa.Choice(k, [v])
    )

# Run on local machine.
gpus = [int(x) for x in FLAGS.gpus.split(',')]
processes_per_gpu = FLAGS.max_concurrent//len(gpus)
assert FLAGS.max_concurrent%len(gpus) == 0
resources = list(itertools.chain.from_iterable(itertools.repeat(x, processes_per_gpu) for x in gpus))

sched = sherpa.schedulers.LocalScheduler(resources=resources)
alg = sherpa.algorithms.RandomSearch(max_num_trials=150)

build_directory('SherpaResults/' + FLAGS.name + '/Models')

sherpa.optimize(
    parameters=parameters,
    algorithm=alg,
    lower_is_better=True,
    command='python main.py',
    scheduler=sched,
    max_concurrent=FLAGS.max_concurrent,
    output_dir='SherpaResults/' + FLAGS.name +'/'
)
