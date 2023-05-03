'''
Created on 14 mai 2020

@author: ouali193
'''

from include import *
from parseQualityMeasures_with_samples import samples

# program parameters
allStrategies = ["MINCOV"]  # , "FIRSTWITCOV", "MINWITCOV"
methods = [["ClosedLCM"], ["ClosedDiversityNew", allStrategies]]  # 

npr = 30
output = "icd.tex"
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
samples = 100
trials = 50


def loadDataset(absolute_input_dataset_file):
    with open(absolute_input_dataset_file, "r") as infile:
        db = []
        for line in infile:
            tmp = line.strip().split()
            if tmp :
                db.append(tmp)
        return db
    
    
def getNbrLignes(absolute_patterns_filename):
    nbLignes = sum(1 for line in open(absolute_patterns_filename, "r"))
    return nbLignes


def ParsePatternFileLine(line):
    description = []
    coverage = []
    witness = 0
    ub_jac_lb = []
    blocks = re.findall('\[(.*?)\]', line)
    if len(blocks) == 4:
        if len(blocks[1].strip()) != 0:  # avoid loading empty set
            description = blocks[1].strip().split(" ")
            # we should start from index 0 instead of index 1 that is provided in the file
            coverage = []
            for t in blocks[2].strip().split(" "):
                coverage.append(int(t) - 1)
            witness = int(blocks[0])
            ub_jac_lb = blocks[3].strip().split(" ")
    elif len(blocks) == 3:
        if len(blocks[0].strip()) != 0:  # avoid loading empty set
            description = blocks[0].strip().split(" ")
            # we should start from index 0 instead of index 1 that is provided in the file
            coverage = []
            for t in blocks[1].strip().split(" "):
                coverage.append(int(t))  
    else:
        print("Error unknown *.res format")
        sys.exit(1)
    return description, coverage, witness, ub_jac_lb
    

def loadPatternsBySamples(absolute_patterns_filename, samples, all_info=False):
    descriptions = []
    coverages = []
    witnesses = []
    ub_jac_lbs = []
    save_samples_lines = []
    curr = 0
    with open(absolute_patterns_filename, "r") as infile:
        for line in infile:
            # decide randomly if we should choose the sample
            rnd_index = random.randint(0, 100)
            if rnd_index <= 50:
                description, coverage, witness, ub_jac_lb = ParsePatternFileLine(line)
                descriptions.append(description)
                coverages.append(coverage)
                witnesses.append(witness)
                ub_jac_lbs.append(ub_jac_lb)
            else:
                # secure some lines to to complete the sample if random approach is no complete
                if curr <= samples:
                    save_samples_lines.append(line)
                    curr += 1
    # test if we have enough samples, if not load from saved lines
    curr = 0
    while len(coverages) < samples and curr < len(save_samples_lines):
        description, coverage, witness, ub_jac_lb = ParsePatternFileLine(save_samples_lines[curr])
        descriptions.append(description)
        coverages.append(coverage)
        witnesses.append(witness)
        ub_jac_lbs.append(ub_jac_lb)
        curr += 1
    # if we don't have enough sample from the file, then exit 
    if len(coverages) < samples:
        print("Not enough samples, the implemented ICD requires the same number of patterns")
        sys.exit(1)      
        
    if all_info:
        return descriptions, coverages, witnesses, ub_jac_lbs
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


# inter-cluster dissimilarity
def computeICD(npr, datasetAsList, coverages):
    assert npr > 0, "you must at least specify one child process to compute ICD" 
    # balance task overload for each process
    sum = 0
    for cov in coverages:
        sum += len(cov)
    moy = int(sum / len(coverages))
    # launch
    n = 0
    procs = dict()
    queue = mp.Queue()
    c1 = 0
    tc1 = 0
    c2 = c1 + 1
    tc2 = 0
    while n < npr:
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
                        n += 1
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
        else :
            n = npr
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
            else:
                launched = True
    return res


# this function should be changed based on solver logs 
def readClosedLCM(content_param):
    '''
    content_param = [datasetAsList, data_name, absolute_dataset_res_dir, frequency]
    '''
    icd = "*"
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
                            icd = "-"
                            return icd
        if found:
            t = 0
            icd = 0
            for t in range(0, trials):
                random.seed(t)
                descriptions, coverages = loadPatternsBySamples(absolute_dataset_res_file, samples)
                icd += computeICD(npr, datasetAsList, coverages)
            icd = icd / trials
            icd = str(icd)
        print(icd)
        return icd


def readClosedDiversityNew(content_param):
    '''
    content_param = [datasetAsList, data_name, absolute_dataset_res_dir, freq_threshold, jmax, historyAggregator, branchStrategy, number_threads and timeout))
    '''
    icd = "*"
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
                            icd = "-"
                            return icd
        if found:
            t = 0
            icd = 0
            for t in range(0, trials):
                random.seed(t)
                descriptions, coverages = loadPatternsBySamples(absolute_dataset_res_file, samples)
                icd += computeICD(npr, datasetAsList, coverages)
            icd = icd / trials
            icd = str(icd)
        print(icd)
        return icd


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

    nbr_measures = 1
    for i in range(0, nbr_measures):  # ICD
        count, chaine = printTexHeadDynamicTool(['|r'])
        foutput.write(chaine)
    foutput.write('}\n')
    fcline = "2"
    lcline = str((count * nbr_measures) + 2)
    foutput.write('                \\hline\n')
    foutput.write('                {\\bf Dataset} & \\multirow{3}*{$\\theta$} & \\multicolumn{' + str(count) + '}{c}{ICD} \\\\\\cline{' + '3' + '-' + lcline + '} \n')
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
                        all_icd = []

                        for method in methods:
                            absolute_dataset_res_dir = os.path.abspath(os.path.join(project_res_dir, res_subfolder, method[0], data_name))
                            if len(method) == 1:
                                tmp = parsers[method[0]]([datasetLoaded, data_name, absolute_dataset_res_dir, threshold, jmax, historyAggregator, branchStrategy, threads, timeout])
                                if is_float(tmp):
                                    all_icd.append(float(tmp))
                                else:
                                    all_icd.append(-1)
                            elif len(method) > 1:
                                for strategy in method[1]:
                                    tmp = parsers[method[0]]([datasetLoaded, data_name, absolute_dataset_res_dir, threshold, jmax, historyAggregator, strategy, threads, timeout])
                                    if is_float(tmp):
                                        all_icd.append(float(tmp))
                                    else:
                                        all_icd.append(-1)
                        # ics
                        index, value = max(enumerate(all_icd), key=operator.itemgetter(1))
                        all_icd = ['*' if x == -1 else '{0:.2f}'.format(x) for x in all_icd]
                        for i in range(0, len(all_icd)):
                            if i == index:
                                resline += ' & \\bf{' + all_icd[i] + '}'
                            else:
                                resline += ' & ' + all_icd[i]
                        if count == len(fthresholds[dataset]):
                            resline += '\\\\\\hline\n'
                            foutput.write('                ' + resline)
                        else :
                            resline += '\\\\\\cline{' + str(fcline) + '-' + str(lcline) + '}\n'
                            foutput.write('                ' + resline)    
        printTexFoot(foutput)
