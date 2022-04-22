import os
import subprocess

# =============================================================================
# Top layer python script to set multiple jobs going on the cluster. 
# =============================================================================

filepath = '/Example/MeerKAT/Mosaic_Planes/'

f = os.listdir(filepath)

for filename in f:

    folder = filepath + filename + '/'

    qsub_command = """qsub  -v FILENAME='{0}' -N baneJob /Example/MeerKAT/run_bane.sh""".format(folder)

    print('Submitting job')

    exit_status = subprocess.call(qsub_command, shell=True)

    if exit_status is 1:
        print('Job failed to submit')

print('Done submitting jobs!')
