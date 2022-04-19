#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import os
import subprocess

# =============================================================================
# Top layer python script to set multiple jobs going on the cluster. 
# =============================================================================

filepath = '/beegfs/car/bsmart/MeerKAT/Mosaic_Planes/'

qsub_command = """qsub   -N idJob /beegfs/car/bsmart/MeerKAT/run_id.sh"""
print(qsub_command)
print('Submitting job')
exit_status = subprocess.call(qsub_command, shell=True)

if exit_status is 1:
	print('Job failed to submit')

print('Done submitting jobs!')
