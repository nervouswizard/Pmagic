from collections import defaultdict
import os

def processScript(logpath, script_path, filename):
    with open(os.path.join(logpath, filename), mode='r') as f:
        lines = [line.strip().split(' ') for line in f]

    beginIdx = 0
    endIdx = 0
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
    if lines == []:
        return

    script_start_time = lines[0][0]
    keylist = []
    keyCounter = defaultdict(int)
    for line in lines:
        line[0] = line[0] - script_start_time
        if line[2] == 'pressed' and keyCounter[line[1]+line[2]] == 0:
                keylist.append(line)
                keyCounter[line[1]+line[2]] += 1
        elif line[2] == 'released':
            keylist.append(line)
            keyCounter[line[1]+'pressed'] -= 1

    os.makedirs(os.path.join(script_path), exist_ok=True)
    filename = filename.replace('.log', '.script')
    with open(os.path.join(script_path, filename), mode='w') as f:
        for line in keylist:
            f.write(' '.join(str(elem) for elem in line)+'\n')

if __name__ == '__main__':
    datapath = 'C:/ProgramData/Pmagic_log/Log/'
    filelist = os.listdir(datapath)
    for idx, file in enumerate(filelist):
        if file.endswith('.log'):
            processScript(datapath, file)