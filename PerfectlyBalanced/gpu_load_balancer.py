import os
import argparse
import datetime
import subprocess
from tqdm import tqdm

print 'Current PID:',os.getpid()

parser = argparse.ArgumentParser()
parser.add_argument('--gpus',type=str, default='0,1,2,3',help='Available gpus separated by comma.')
parser.add_argument('--max_concurrent',type=int, default=24, help='Number of concurrent processes')

parser.add_argument('--dataset',type=str, default='mnist', choices=['mnist', 'cifar'])
FLAGS = parser.parse_args()

SETTINGS  = []

COMMAND = 'python main.py --dataset {dataset} --model {model}'

def write_commands(command_stack):
    with open('command_stack', 'w') as command_stack_file:
        for command in command_stack:
            command_stack_file.write(command)

def pop_command():
    with open('command_stack', 'r') as command_stack_file:
        command_stack = command_stack_file.readlines()

    write_commands(command_stack[1:])
    return command_stack[0]


command_stack = []
for setting in SETTINGS:
    command_stack.append(
        COMMAND.format(
            dataset=,
            model=,

        )
    )

write_commands(command_stack)

# LOGGING
now = datetime.datetime.now()
print 'Starting @', now.strftime("%Y-%m-%d %H:%M")
print 'Total jobs to run:', len(stack)

gpus = { gpu:[] for gpu in FLAGS.gpus.split(',')}
num_per_gpu = FLAGS.max_concurrent / len(gpus)

# PROGRESS BAR
pbar = tqdm(total=len(stack))

while stack:
    for gpu_id in gpus:
        while len(gpus[gpu_id]) < num_per_gpu:
            command = pop_command()
            proc = subprocess.Popen([command + ' --gpu %s' % gpu_id],shell=True,stdout=open(os.devnull, 'w'), stderr=subprocess.STDOUT)

            gpus[gpu_id].append(proc)

    GPUS_FULL = True
    while GPUS_FULL:
        for gpu_id in gpus:
            for i in range(len(gpus[gpu_id])-1,-1,-1):
                if gpus[gpu_id][i].poll() is not None:
                    gpus[gpu_id].pop(i)
                    GPUS_FULL = False
                    pbar.update(1)
                    break

pbar.close()
