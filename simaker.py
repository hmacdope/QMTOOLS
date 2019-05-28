import os
import subprocess
flist = os.listdir()
logs = [f for f in flist if '.log' in f]
with open('loglist') as f:
    for log in logs:
        pref = log.split('.log')[0]
        f.write(f' {pref}\n')
