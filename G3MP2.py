#!/usr/bin/env python

import os
import subprocess

cwd = os.getcwd()
pref = cwd.split('/')[-1]
gaslogN = pref + '.M062X_6-31pGd_opt.log'
watlogN = pref + '.M062X_6-31pGd_opt_water.log'
gaslogA = pref + '_a1.M062X_6-31pGd_opt.log'
watlogA = pref + '_a1.M062X_6-31pGd_opt_water.log'

MP2Sn = f'qmin {gaslogN} -c 0 -t MP2 '
subprocess.call(MP2Sn, shell=True)
MP2Ln = f'qmin {gaslogN} -c 0 -t MP2 -b GTMP2LARGE'
subprocess.call(MP2Ln, shell=True)
CCSDTn = f'qmin {gaslogN} -c 0 -t CCSD-T -p qchem'
subprocess.call(CCSDTn, shell=True)
MP2Sa = f'qmin {gaslogA} -c -1 -t MP2 '
subprocess.call(MP2Sa, shell=True)
MP2La = f'qmin {gaslogA} -c -1 -t MP2 -b GTMP2LARGE'
subprocess.call(MP2La, shell=True)
CCSDTa = f'qmin {gaslogA} -c -1 -t CCSD-T -p qchem'
subprocess.call(CCSDTa, shell=True)
subprocess.call('pysub *MP2* -ncpus 4', shell=True)
subprocess.call('pysub *.in', shell=True)


