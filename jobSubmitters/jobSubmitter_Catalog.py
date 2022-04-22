import subprocess

# =============================================================================
# Top layer python script to set multiple jobs going on the cluster. 
# =============================================================================

filepath = '/Example/MeerKAT/Mosaic_Planes/'
qsub_command = """qsub   -N catalogJob /Example/MeerKAT/run_catalog.sh"""

print('Submitting job')

exit_status = subprocess.call(qsub_command, shell=True)

if exit_status is 1:
	print('Job failed to submit')

print('Done submitting jobs!')
