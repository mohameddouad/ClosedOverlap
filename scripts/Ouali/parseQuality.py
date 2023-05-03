'''
Created on 25 mars 2020

@author: Abdelkader Ouali
'''

from include import *

# program parameters
allStrategies = ["MINCOV"]  # , "FIRSTWITCOV", "MINWITCOV"
methods = [["ClosedLCM"], ["ClosedDiversityNew", allStrategies]]  # 

npr = 30
output = "ips-ipd.tex"
jmax = "0.1"  # maximum jaccard-similarity threshold
threads = "0"  # number of threads used by the global constraint
historyAggregator = "MAX"
branchStrategy = "MINCOV"
timeout = "91800s"
fthresholds = {
               "BMS1.dat" : ["0.0015", "0.0014", "0.0012"],
#               "connect.dat" : ["0.3", "0.18", "0.17", "0.15"],
               "hepatitis.dat" : ["0.3", "0.2", "0.1"],
               "mushroom.dat" : ["0.05", "0.01", "0.008", "0.005"],
#               "pumsb.dat" : [ "0.4", "0.3", "0.2"],
               "retail.dat" : [ "0.05", "0.01", "0.004"],
               "T10I4D100K.dat" : [ "0.05", "0.01", "0.005" ],
#               "chess.dat" : ["0.4", "0.3", "0.2", "0.15"],
               "heart-cleveland.dat" : [ "0.2", "0.1", "0.08", "0.06"],
#               "kr-vs-kp.dat" : ["0.4", "0.3", "0.2"],
               "splice1.dat" : [ "0.1", "0.05", "0.02", "0.01" ],
               "T40I10D100K.dat" : [ "0.1", "0.08", "0.05", "0.03", "0.01"],
               'ijcai16.dat': ["0.3", "0.2", "0.1"]
               }

res_subfolder = "foxrex"


def loadDataset(absolute_input_dataset_file):
    with open(absolute_input_dataset_file, "r") as infile:
        db = []
        for line in infile:
            tmp = line.strip().split()
            if tmp :
                db.append(tmp)
        return db


def loadPatterns(absolute_patterns_filename, all_info=False):
    descriptions = []
    coverages = []
    witness = []
    ub_jac_lb = []
    with open(absolute_patterns_filename, "r") as infile:
        for line in infile:
            blocks = re.findall('\[(.*?)\]', line)
            if len(blocks) == 4:
                if len(blocks[1].strip()) != 0:  # avoid loading empty set
                    descriptions.append(blocks[1].strip().split(" "))
                    # we should start from index 0 instead of index 1 that is provided in the file
                    coverage = []
                    for t in blocks[2].strip().split(" "):
                        coverage.append(int(t) - 1)
                    coverages.append(coverage)
                    witness.append(int(blocks[0]))
                    ub_jac_lb.append(blocks[3].strip().split(" "))
            elif len(blocks) == 3:
                if len(blocks[0].strip()) != 0:  # avoid loading empty set
                    descriptions.append(blocks[0].strip().split(" "))
                    # we should start from index 0 instead of index 1 that is provided in the file
                    coverage = []
                    for t in blocks[1].strip().split(" "):
                        coverage.append(int(t))
                    coverages.append(coverage)     
            else:
                print("Error unknown *.res format")
                sys.exit(1)
                
    if all_info:
        return descriptions, coverages, witness, ub_jac_lb
    else:
        return descriptions, coverages


def jaccard(a, b):
    '''
    a and b are two lists
    '''
    sa = set(a)
    sb = set(b)
    cap = len(sa.intersection(sb))
    cup = len(sa.union(sb))
    if cup == 0:
        return 0
    else:
        return cap / cup

            
def jaccardBloc(queue, datasetAsList, coverages, cur_list, max_list):
    res = 0
    try:
        for comb in nestedCombLoop(cur_list, max_list):
            # IPS
            if len(comb) == 3:
                res += jaccard(datasetAsList[coverages[comb[0]][comb[1]]], datasetAsList[coverages[comb[0]][comb[2]]])
            # IPD
            elif len(comb) == 4:
                res += (1 - jaccard(datasetAsList[coverages[comb[0]][comb[1]]], datasetAsList[coverages[comb[2]][comb[3]]]))
    finally:
        queue.put([mp.current_process().name, res])


# intra-cluster similarity
def computeIPS(npr, datasetAsList, coverages):
    assert npr > 0, "you must at least specify one child process to compute IPS"
    n = 0;
    procs = dict()
    queue = mp.Queue()
    k = 0
    i = 0
    keep = True
    # for each pattern
    printProgressBar(0, len(coverages), prefix='Progress:', suffix='Complete', length=50)
    while keep and k < len(coverages):
        # for each transaction t_i of pattern k
        i = 0
        while keep and i < len(coverages[k]) - 1:
            # for each transaction t_j of pattern k, we break the symmetry
            if n == npr:
                keep = False
                break
            # compute the jaccard distance between t_i and t_j
            proc = Process(target=jaccardBloc, args=(queue, datasetAsList, coverages, [k, i , i + 1], [k + 1, i + 1 , len(coverages[k])],))
            proc.start()
            procs[proc.name] = proc
            i += 1
            n += 1
        # keep index to continue the queue
        if keep:
            k += 1
            printProgressBar(k, len(coverages), prefix='Progress:', suffix='Complete', length=50)
    # queue
    res = 0
    while procs:
        # get results
        infos = queue.get()
        proc = procs[infos[0]]
        res += infos[1]
        proc.join()
        del procs[infos[0]]
        # continue launching
        launched = False
        while not launched:
            if k < len(coverages):
                # for each transaction t_i of pattern k
                if i < len(coverages[k]) - 1:
                    # compute the jaccard distance between t_i and t_j 
                    proc = Process(target=jaccardBloc, args=(queue, datasetAsList, coverages, [k, i , i + 1], [k + 1, i + 1 , len(coverages[k])],))
                    proc.start()
                    procs[proc.name] = proc
                    launched = True
                    i += 1
                else:
                    i = 0
                    k += 1
                    printProgressBar(k, len(coverages), prefix='Progress:', suffix='Complete', length=50)
            else:
                launched = True                   
    return res / len(coverages)


# inter-cluster dissimilarity
def computeIPD(npr, datasetAsList, coverages):
    assert npr > 0, "you must at least specify one child process to compute IPD"
    n = 0
    procs = dict()
    queue = mp.Queue()
    c1 = 0
    tc1 = 0
    c2 = 0
    tc2 = 0
    keep = True
    # balance task overload
    sum = 0
    for cov in coverages:
        sum += len(cov)
    moy = int(sum / len(coverages))

    # launch
    total_bar = len(coverages)
    printProgressBar(c1, total_bar, prefix='Progress:', suffix='Complete', length=50)
    while keep and c1 < len(coverages):
        tc1 = 0
        while keep and tc1 < len(coverages[c1]):
            c2 = c1 + 1
            while keep and c2 < len(coverages):
                while keep and tc2 < len(coverages[c2]):
                    # test to pass to the queue
                    if n == npr:
                        keep = False
                        break
                    if len(coverages[c2]) <= moy:
                        proc = Process(target=jaccardBloc, args=(queue, datasetAsList, coverages, [c1, tc1, c2 , 0], [c1 + 1, tc1 + 1, c2 + 1 , len(coverages[c2])],))
                        tc2 = len(coverages[c2])
                    else:
                        taille_max = tc2 + moy if tc2 + moy <= len(coverages[c2]) else len(coverages[c2])
                        proc = Process(target=jaccardBloc, args=(queue, datasetAsList, coverages, [c1, tc1, c2 , tc2], [c1 + 1, tc1 + 1, c2 + 1 , taille_max],))
                        tc2 += moy
                    proc.start()
                    procs[proc.name] = proc
                    n += 1
                if keep:
                    c2 += 1
                    tc2 = 0
            if keep:
                tc1 += 1
        if keep:
            c1 += 1
            printProgressBar(c1, total_bar, prefix='Progress:', suffix='Complete', length=50)
    # queue
    res = 0
    while procs:
        # get results
        infos = queue.get()
        proc = procs[infos[0]]
        res += infos[1]
        proc.join()
        del procs[infos[0]]
        # continue launching
        launched = False
        while not launched:
            if c1 < len(coverages):
                if tc1 < len(coverages[c1]):
                    if c2 < len(coverages):
                        if tc2 < len(coverages[c2]):
                            if len(coverages[c2]) <= moy:
                                proc = Process(target=jaccardBloc, args=(queue, datasetAsList, coverages, [c1, tc1, c2 , 0], [c1 + 1, tc1 + 1, c2 + 1 , len(coverages[c2])],))
                                tc2 = len(coverages[c2])
                            else:
                                taille_max = tc2 + moy if tc2 + moy <= len(coverages[c2]) else len(coverages[c2])
                                proc = Process(target=jaccardBloc, args=(queue, datasetAsList, coverages, [c1, tc1, c2 , tc2], [c1 + 1, tc1 + 1, c2 + 1 , taille_max],))
                                tc2 += moy
                            proc.start()
                            procs[proc.name] = proc
                            launched = True
                        else:
                            c2 += 1
                            tc2 = 0
                    else:
                        tc1 += 1
                        c2 = c1 + 1
                else:
                    c1 += 1
                    tc1 = 0
                    c2 = c1 + 1
                    printProgressBar(c1, total_bar, prefix='Progress:', suffix='Complete', length=50)
            else:
                launched = True
    return res / ncr(len(coverages), 2)


def computeIPDBySamples(npr, datasetAsList, coverages):
    samples = 30
    trials = 10
    # launch
    if len(coverages) < samples:
        return computeIPD(npr, datasetAsList, coverages)       
    coverages_samples = []
    for t in range(0, trials):
        random.seed(t)
        tmp = []
        for s in range(0, samples):
            tmp.append(coverages[random.randint(0, len(coverages) - 1)])
        coverages_samples.append(tmp)
    coverages = []
    moy = 0
    for curr in coverages_samples:
        moy += computeIPD(npr, datasetAsList, curr)
    return moy / len(coverages_samples)


# this function should be changed based on solver logs 
def readClosedLCM(content_param, info=0):
    '''
    content_param = [datasetAsList, data_name, absolute_dataset_res_dir, frequency]
    '''
    ips = "*"
    ipd = "*"
    if content_param:
        # prepare the folder directories
        datasetAsList = content_param[0]
        data_name = content_param[1]
        absolute_dataset_res_dir = content_param[2]
        absolute_dataset_res_file = os.path.abspath(os.path.join(absolute_dataset_res_dir, data_name + "-" + content_param[3].replace(".", "v") + ".res"))
        absolute_dataset_ana_file = os.path.abspath(os.path.join(absolute_dataset_res_dir, data_name + "-" + content_param[3].replace(".", "v") + ".ana"))
        absolute_dataset_log_file = os.path.abspath(os.path.join(absolute_dataset_res_dir, data_name + "-" + content_param[3].replace(".", "v") + ".log")) 
        # compute
        found = False
        if (os.path.exists(absolute_dataset_log_file)):
            with open(absolute_dataset_log_file, 'r') as logfile:
                for line in logfile:
                    line_parse = re.findall(r'Exit status:[\s]+(\d+)', line)
                    if line_parse:
                        if line_parse[0] == '0':
                            found = True
                            break
                        elif line_parse[0] == '124':
                            ips = "-"
                            ipd = "-"
                            if info == 1:
                                return ips
                            elif info == 2:
                                return ipd
                            else:
                                return ips, ipd
        if found:
            descriptions, coverages = loadPatterns(absolute_dataset_res_file)
            if info == 1:
                ips = computeIPS(npr, datasetAsList, coverages)
                print(ips)
                return ips
            elif info == 2:
                ipd = computeIPDBySamples(npr, datasetAsList, coverages)
                print(ipd)
                return ipd
            else:
                ips = computeIPS(npr, datasetAsList, coverages)
                ipd = computeIPDBySamples(npr, datasetAsList, coverages)
                return ips, ipd
        else:
            if info == 1:
                print(ips)
                return ips
            elif info == 2:
                print(ipd)
                return ipd
            else:
                return ips, ipd


def readClosedDiversityNew(content_param, info=0):
    '''
    content_param = [datasetAsList, data_name, absolute_dataset_res_dir, freq_threshold, jmax, historyAggregator, branchStrategy, number_threads and timeout))
    '''
    ips = "*"
    ipd = "*"
    if content_param:
        datasetAsList = content_param[0]
        data_name = content_param[1]
        absolute_dataset_res_dir = content_param[2]
        absolute_dataset_res_file = os.path.abspath(os.path.join(absolute_dataset_res_dir, data_name + "-" + content_param[3].replace(".", "v") + "-" + content_param[4].replace(".", "v") + "-" + content_param[5] + "-" + content_param[6] + "-" + content_param[7] + "-" + content_param[8] + ".res"))
        absolute_dataset_ana_file = os.path.abspath(os.path.join(absolute_dataset_res_dir, data_name + "-" + content_param[3].replace(".", "v") + "-" + content_param[4].replace(".", "v") + "-" + content_param[5] + "-" + content_param[6] + "-" + content_param[7] + "-" + content_param[8] + ".ana"))
        absolute_dataset_log_file = os.path.abspath(os.path.join(absolute_dataset_res_dir, data_name + "-" + content_param[3].replace(".", "v") + "-" + content_param[4].replace(".", "v") + "-" + content_param[5] + "-" + content_param[6] + "-" + content_param[7] + "-" + content_param[8] + ".log"))
        # compute
        found = False
        if (os.path.exists(absolute_dataset_log_file)):
            with open(absolute_dataset_log_file, 'r') as logfile:
                for line in logfile:
                    line_parse = re.findall(r'Exit status:[\s]+(\d+)', line)
                    if line_parse:
                        if line_parse[0] == '0':
                            found = True
                            break                            
                        elif line_parse[0] == '124':
                            ips = "-"
                            ipd = "-"
                            if info == 1:
                                return ips
                            elif info == 2:
                                return ipd
                            else:
                                return ips, ipd
        if found:
            descriptions, coverages = loadPatterns(absolute_dataset_res_file)
            if info == 1:
                ips = computeIPS(npr, datasetAsList, coverages)
                print(ips) 
                return ips
            elif info == 2:
                ipd = computeIPDBySamples(npr, datasetAsList, coverages)
                print(ipd)
                return ipd
            else:
                ips = computeIPS(npr, datasetAsList, coverages)
                ipd = computeIPDBySamples(npr, datasetAsList, coverages)
                return ips, ipd
        else:
            if info == 1:
                print(ips)
                return ips
            elif info == 2:
                print(ipd)
                return ipd
            else:
                return ips, ipd


def mapParsersDynamic(methods): 
    parsers = {}
    for method in methods:
        method_name = 'read' + method[0]
        possibles = globals().copy()
        possibles.update(locals())
        parse_method = possibles.get(method_name)
        if not parse_method:
            raise NotImplementedError("Method %s not implemented" % method_name) 
        parsers[method[0]] = parse_method
    return parsers


def printTexHeadDynamicTool(m):
    count = 0
    chaine = ""
    for method in methods:
        if len(method) == 1:
            count += 1
            if len(m) == 1:
                chaine += m[0]
            elif len(m) > 1:
                chaine += m[0] + method[0] + m[1]
        elif len(method) > 1:
            for strategy in method[1]:
                count += 1
                if len(m) == 1:
                    chaine += m[0]
                elif len(m) > 1:
                    chaine += m[0] + strategy + m[1]
    return count, chaine


def printTexHeadDynamic(methods, parsers, foutput):
    foutput.write('\\begin{table}[htbp]\n')
    foutput.write('    \\centering\n')
    foutput.write('        \\scalebox{.7}{\n')
    foutput.write('            \\begin{tabular}[h]{c|c')

    nbr_measures = 2
    for i in range(0, nbr_measures):  # IPS, IPD
        count, chaine = printTexHeadDynamicTool(['|r'])
        foutput.write(chaine)
    foutput.write('}\n')
    fcline = "2"
    lcline = str((count * nbr_measures) + 2)
    foutput.write('                \\hline\n')
    foutput.write('                {\\bf Dataset} & \\multirow{3}*{$\\theta$} & \\multicolumn{' + str(count) + '}{c||}{IPS} &\n')
    foutput.write('                \\multicolumn{' + str(count) + '}{c}{IPD} \\\\\\cline{' + '3' + '-' + lcline + '} \n')
    foutput.write('                $|\\items| \\times |\\bdd|  $ &  ')
    for i in range(0, nbr_measures):  # Patterns, # Time, # Node 
        count, chaine = printTexHeadDynamicTool([' & \\multirow{2}*{', '}'])
        foutput.write(chaine)
    foutput.write('\\\\\n')
    foutput.write('                $\\rho(\\%)$ ')
    for i in range(0, nbr_measures):  # Patterns, # Time, # Node 
        count, chaine = printTexHeadDynamicTool([' & '])
        foutput.write(chaine)
    foutput.write('\\\\\\hline\n')
    foutput.write('                %....................................................................%\n')
    return fcline, lcline


def printTexFoot(foutput):
    foutput.write('                %-------------------------------------------------------------------%\n')
    foutput.write('            \\end{tabular}\n')
    foutput.write('        }\n')
    foutput.write('    \\caption{*: not yet launched, or in the worst case an error has occured. -: timeout reached. For the \\#Patterns, the value in bold reduces more than 20\% of the total \\# of patterns}\n') 
    foutput.write('\\end{table}\n')
    

# now parsing the results of the available methods, this method should be modified, unless a new method is added
if __name__ == '__main__':
    with open(output, "w") as foutput:
        nbr_measures = 2
        parsers = mapParsersDynamic(methods)
        fcline, lcline = printTexHeadDynamic(methods, parsers, foutput)
        
        if not branchStrategy in allStrategies:
            print("ERROR, you must respect the syntax for the branch strategy : \"MINCOV\", \"FIRSTWITCOV\" or \"MINWITCOV\" \n")
            sys.exit(1)
    
        for dataset in os.listdir(project_data_dir):
            if dataset.endswith(".dat"):
                nline = 1
                data_name = dataset.split('.')[0]
                absolute_dataset_file = os.path.abspath(os.path.join(project_data_dir, data_name + '.dat'))
                datasetLoaded = loadDataset(absolute_dataset_file)
                if dataset in fthresholds:
                    items = ""
                    trans = "" 
                    density = ""
                    absolute_dataset_desc_dir = os.path.abspath(os.path.join(project_data_dir, data_name + '.desc'))
                    with open(absolute_dataset_desc_dir, 'r') as fdesc:
                        first_line = fdesc.readline().strip().split(' ')
                        trans = first_line[0]
                        items = first_line[1]
                        density = first_line[2]
                    foutput.write('                \\hline\n')
                    foutput.flush();
                    count = 0
                    for threshold in fthresholds[dataset]:
                        print(dataset, threshold)
                        # prepare the dataset description
                        count += 1
                        if nline == 1:
                            resline = '{' + data_name + '} & ' + threshold    
                            nline = 2
                        elif nline == 2:
                            resline = '{' + items + ' $\\times$ ' + trans + '}  & ' + threshold
                            nline = 3
                        elif nline == 3:
                            resline = '{' + density + '\\%} & ' + threshold
                            nline = 4
                        else:
                            resline = ' & ' + threshold + ' '
                        # print the resutls for each method+strategy
                        all_ips = []
                        all_ipd = []
                        for info in range(1, nbr_measures + 1):
                            for method in methods:
                                absolute_dataset_res_dir = os.path.abspath(os.path.join(project_res_dir, res_subfolder, method[0], data_name))
                                if len(method) == 1:
                                    if info == 1:
                                        tmp = "*"  # parsers[method[0]]([datasetLoaded, data_name, absolute_dataset_res_dir, threshold, jmax, historyAggregator, branchStrategy, threads, timeout], info)
                                        if is_float(tmp):
                                            all_ips.append(float(tmp))
                                        else:
                                            all_ips.append(sys.float_info.max)
                                    elif info == 2:
                                        tmp = parsers[method[0]]([datasetLoaded, data_name, absolute_dataset_res_dir, threshold, jmax, historyAggregator, branchStrategy, threads, timeout], info)
                                        if is_float(tmp):
                                            all_ipd.append(float(tmp))
                                        else:
                                            all_ipd.append(-1)
                                elif len(method) > 1:
                                    for strategy in method[1]:
                                        if info == 1:
                                            tmp = "*"  # parsers[method[0]]([datasetLoaded, data_name, absolute_dataset_res_dir, threshold, jmax, historyAggregator, strategy, threads, timeout], info)
                                            if is_float(tmp):
                                                all_ips.append(float(tmp))
                                            else:
                                                all_ips.append(sys.float_info.max)
                                        elif info == 2:
                                            tmp = parsers[method[0]]([datasetLoaded, data_name, absolute_dataset_res_dir, threshold, jmax, historyAggregator, strategy, threads, timeout], info)
                                            if is_float(tmp):
                                                all_ipd.append(float(tmp))
                                            else:
                                                all_ipd.append(-1)
                        # ips
                        index, value = min(enumerate(all_ips), key=operator.itemgetter(1))
                        all_ips = ['*' if x == sys.float_info.max else '{0:.2f}'.format(x) for x in all_ips]
                        for i in range(0, len(all_ips)):
                            if i == index:
                                resline += ' & \\bf{' + str(all_ips[i]) + '}'
                            else:
                                resline += ' & ' + str(all_ips[i])
                        index, value = max(enumerate(all_ipd), key=operator.itemgetter(1))
                        all_ipd = ['*' if x == -1 else '{0:.2f}'.format(x) for x in all_ipd]
                        # ipd
                        for i in range(0, len(all_ipd)):
                            if i == index:
                                resline += ' & \\bf{' + all_ipd[i] + '}'
                            else:
                                resline += ' & ' + all_ipd[i]
                        if count == len(fthresholds[dataset]):
                            resline += '\\\\\\hline\n'
                            foutput.write('                ' + resline)
                        else :
                            resline += '\\\\\\cline{' + str(fcline) + '-' + str(lcline) + '}\n'
                            foutput.write('                ' + resline)    
        printTexFoot(foutput)
