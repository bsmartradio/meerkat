#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import os
import subprocess

# =============================================================================
# Top layer python script to set multiple jobs going on the cluster. 
# =============================================================================

filepath = '/beegfs/car/bsmart/MeerKAT/Mosaic_Planes/'

f=os.listdir (filepath)

for filename in f:

	folder=filepath+filename+'/'

	qsub_command = """qsub  -v FILENAME='{0}' -N photJob /beegfs/car/bsmart/MeerKAT/run_phot.sh""".format(folder)
	print(qsub_command)
	print('Submitting job')
	exit_status = subprocess.call(qsub_command, shell=True)

	if exit_status is 1:
		print('Job failed to submit')

print('Done submitting jobs!')
