from collections import defaultdict
import os

def processScript(filename):
    filepath = os.path.join(datapath, filename)
    with open(filepath, mode='r') as f:
        lines = [line.strip().split(' ') for line in f]

    beginIdx = 0
    for i, line in enumerate(lines):
        if line[1].startswith('Key.'):
            line[1] = line[1].replace('Key.', '')
        line[0] = float(line[0])
        if line[1] == 'page_down' and line[2] == 'released' and beginIdx == 0:
            beginIdx = i+1
        if line[1] == 'esc' and line[2] == 'pressed':
            endIdx = i
            break
    lines = lines[beginIdx:endIdx]

    script_start_time = lines[0][0]
    keylist = [line for line in lines if line[2] == 'released']
    keyCounter = defaultdict(int)
    keyCounter.update({line[1]+'pressed': 1 for line in keylist})
    keylist.extend([line for line in lines if line[2] == 'pressed' and keyCounter[line[1]+line[2]] == 1])
    keyCounter.update({line[1]+line[2]: -1 for line in keylist if line[2] == 'released'})

    os.makedirs(os.path.join(datapath, 'Script'), exist_ok=True)
    filename = filename.replace('.log', '.script')
    filepath = os.path.join(datapath, 'Script', filename)
    with open(filepath, mode='w') as f:
        for line in keylist:
            line[0] -= script_start_time
            f.write(' '.join(str(elem) for elem in line)+'\n')


datapath = 'C:/ProgramData/Pmagic/Log/'
processScript('my_script.log')
