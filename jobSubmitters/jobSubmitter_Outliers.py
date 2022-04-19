#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import glob
import subprocess
import sys

# =============================================================================
# Top layer python script to set multiple jobs going on the cluster. 
# =============================================================================

filepath = '/beegfs/car/bsmart/MeerKAT/Mosaic_Planes/'

f=sorted(glob.glob(filepath+'*'))
for im,filename in enumerate(f):

        if im == 0:
                print('Skipping first file')

        elif im % 2 == 1 and im != 55:
                
                print(f[im-1])
                print(filename)
                print(f[im+1])

                qsub_command = """qsub  -v FILE_ONE='{0}',FILE_TWO='{1}',FILE_THREE='{2}' -N {3}_job 
                /beegfs/car/bsmart/MeerKAT/run_outliers.sh""".format(f[im-1]+'/',filename+'/',f[im+1]+'/',im)
                print(qsub_command)
                print('Submitting job')
                exit_status = subprocess.call(qsub_command, shell=True)

                if exit_status is 1:
        
                        print('Job failed to submit')
        
        elif im == 55:
                print(f[im-1])
                print(filename)
                print(f[0])

                qsub_command = """qsub  -v FILE_ONE='{0}',FILE_TWO='{1}',FILE_THREE='{2}' -N {3}_job 
                /beegfs/car/bsmart/MeerKAT/run_outliers.sh""".format(f[im-1]+'/',filename+'/',f[0]+'/',im)
                print(qsub_command)
                print('Submitting job')
                exit_status = subprocess.call(qsub_command, shell=True)

                if exit_status is 1:
                        print('Job failed to submit')


print('Done submitting jobs!')
