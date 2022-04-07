#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import os
import subprocess

# =============================================================================
# Top layer python script to set multiple jobs going on the cluster. 
# =============================================================================

filepath = '/beegfs/car/bsmart/MeerKAT/Mosaic_Planes/'

#f = open(filepath+'folder_list_cluster.text', "r")

qsub_command = """qsub   -N catalogJob /beegfs/car/bsmart/MeerKAT/run_catalog.sh"""
	#qsub_command = """qsub run_bane.sh""".format(filename)
print(qsub_command)
print('Submitting job')
exit_status = subprocess.call(qsub_command, shell=True)
	#exit_status = subprocess.call('qsub run_bane.sh', shell=True)

if exit_status is 1:
	print('Job failed to submit')

print('Done submitting jobs!')
