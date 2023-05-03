'''
Created on 29 mars 2020

@author: Arnold Hien
'''

from include import *

# program parameters
allStrategies = ["MINCOV"]  # , "FIRSTWITCOV", "MINWITCOV"
#methods = [["ClosedLCM"], ["ClosedDiversityNew", allStrategies]]  # 
#methods = [["ClosedDiversityNew", allStrategies]]
methods = [["ClosedLCM"]]

npr = 100
output = "measure_new_CP_reste.tex"
jmax = "0.1"  # maximum jaccard-similarity threshold
threads = "0"  # number of threads used by the global constraint
historyAggregator = "MAX"
branchStrategy = "MINCOV"
timeout = "91800s"
fthresholds = {
#               "BMS1.dat" : ["0.0015", "0.0014", "0.0012"],
               "connect.dat" : ["0.3", "0.18", "0.17", "0.15"],
#               "german-credit.dat" : ["0.1", "0.01", "0.001", "0.025"],
#               "hepatitis.dat" : ["0.3", "0.2", "0.1"],
#               "mushroom.dat" : ["0.05", "0.01", "0.008", "0.005"],
#               "pumsb.dat" : [ "0.70", "0.4", "0.1"],
#               "retail.dat" : [ "0.05", "0.01", "0.004" ],
#               "T10I4D100K.dat" : [ "0.05", "0.01", "0.005" ],
#               "vote.dat" : ["0.1", "0.01", "0"],
               "chess.dat" : ["0.4", "0.3", "0.2", "0.15"],
#               "heart-cleveland.dat" : [ "0.2", "0.1", "0.08", "0.06"],
               "kr-vs-kp.dat" : ["0.4", "0.3", "0.2"]
#               "primary-tumor.dat" : [ "0.1", "0.01", "0"],
#               "splice1.dat" : [ "0.1", "0.05", "0.02", "0.01" ],
#               "T40I10D100K.dat" : [ "0.1", "0.08", "0.05", "0.03", "0.01" ],
#               "ijcai16.dat": ["0.3", "0.2", "0.1"]
               }
#               "BMS1.dat" : ["0.12"]
#               "connect.dat" : ["0.3"]
#               "hepatitis.dat" : ["0.3", "0.2", "0.1"],
#               "mushroom.dat" : ["0.05", "0.01"],
#               "pumsb.dat" : [ "0.4", "0.3", "0.2"],
#               "retail.dat" : [ "0.05", "0.01", "0.004"],
#               "T10I4D100K.dat" : [ "0.05", "0.01", "0.005" ],
#               "chess.dat" : ["0.4"],
#               "heart-cleveland.dat" : [ "0.2"],
#               "kr-vs-kp.dat" : ["0.4"]
#               "mushroom.dat" : ["0.05"]
#               "connect.dat" : ["0.3", "0.18"]
#               "splice1.dat" : [ "0.1" ]
#               "T40I10D100K.dat" : [ "0.1", "0.08"]
#               }

res_subfolder = "foxrex"
samples = 100
trials = 50


def loadDataset(absolute_input_dataset_file):
    with open(absolute_input_dataset_file, "r") as infile:
        db = []
        items = []
        for line in infile:
            tmp = line.strip().split()
            if tmp :
                db.append(tmp)
                for i in tmp:
                    if i not in items:
                        items.append(i)
        return db, items


def loadDatasetSamples(absolute_input_dataset_file, samples):
    all_indexes = []
    for s in range(0, samples):
        random.seed(s)
        rnd_index = random.randint(0, samples - 1)
        all_indexes.append(rnd_index)
    
    all_indexes.sort()
    nb_lignes = sum(1 for line in open(absolute_input_dataset_file, "r"))
    
    if nb_lignes < samples:
        return loadDataset(absolute_input_dataset_file)
    else:
        db = []
        items = []
        with open(absolute_input_dataset_file, "r") as infile:
            ind = 0
            for line in infile:
                if ind in all_indexes:
                    tmp = line.strip().split()
                    if tmp :
                        db.append(tmp)
                        for i in tmp:
                            if i not in items:
                                items.append(i)
                ind = ind+1
        return db, items


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


def loadPatternsSamples(samples, debut_interv, fin_interv, absolute_patterns_filename, all_info=False):
    nb_lignes = sum(1 for line in open(absolute_patterns_filename, "r"))
    
    if nb_lignes < samples:
        return loadPatterns(absolute_patterns_filename, all_info)
    else:
        all_indexes = []
        
        for s in range(debut_interv, fin_interv):
            random.seed(s)
            rnd_index = random.randint(0, nb_lignes)
            all_indexes.append(rnd_index)
        all_indexes.sort()
        
        # print("nb_lignes=", nb_lignes, "\n", all_indexes, "\n")
        
        descriptions = []
        coverages = []
        witness = []
        ub_jac_lb = []
        
        with open(absolute_patterns_filename, "r") as infile:
            ind = 0
            for line in infile:
                if ind in all_indexes:
                    
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
                ind = ind+1
        if all_info:
            return descriptions, coverages, witness, ub_jac_lb
        else:
            # print("taille description et couvertures ===> ", len(coverages))
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


def compressionRate(dataset, items_list, descriptions, coverages):
    assert len(descriptions) == len(coverages), "pattern's descritpion and coverages are not synchronized!"
    res = 0  
    for k in range(0, len(descriptions)):
        freq = len(coverages[k])
        size = len(descriptions[k])
        # local
        p = freq * (len(items_list) - size) + size
        # remains
        sum_not_t = 0
        for t in range(0, len(dataset)):
            if t not in coverages[k]:
                sum_not_t += 1
        res += p + (sum_not_t * len(items_list))
    return res / len(descriptions)


def intersectionRest(coverages):
    union_cover = []
    printProgressBar(0, len(coverages), prefix='Intersect cover --> Progress:', suffix='Complete', length=50)
    for k in range(0, len(coverages)):
        tmp = set()
        for l in range(0, len(coverages)):
            if l != k:
                tmp = tmp.union(set(coverages[l]))
        union_cover.append(tmp)
        printProgressBar(k, len(coverages), prefix='Intersect cover --> Progress:', suffix='Complete', length=50)
    cap_cupcovother = []
    printProgressBar(0, len(coverages), prefix='Intersect cover --> Progress:', suffix='Complete', length=50)
    for k in range(0, len(coverages)):
        cap_cupcovother.append(list(set(coverages[k]).intersection(union_cover[k])))
        printProgressBar(k, len(coverages), prefix='Intersect cover --> Progress:', suffix='Complete', length=50)
    return cap_cupcovother


def properCoverRate(coverages, cap_cupcovother):
    assert len(cap_cupcovother) == len(coverages), "pattern's descritpion and coverages are not synchronized!"
    res = 0
    printProgressBar(0, len(coverages), prefix='ProperCover evaluation --> Progress:', suffix='Complete', length=50)
    for k in range(0, len(coverages)):
        sp = len(coverages[k])
        res += ((sp - len(cap_cupcovother[k])) / sp)
        printProgressBar(k, len(coverages), prefix='ProperCover evaluation --> Progress:', suffix='Complete', length=50) 
    return res / len(coverages)


def covP(queue, coverages, cap_cupcovother, allCovP, ind):
    queue.put(mp.current_process().name)
    
    sp = len(coverages[ind])
    res = ((sp - len(cap_cupcovother[ind])) / sp)
    printProgressBar(ind, len(coverages), prefix='Progress:', suffix='Complete', length=50) 
    allCovP[str(ind)] = res


def properCoverRateParallele(coverages, cap_cupcovother):
    assert len(cap_cupcovother) == len(coverages), "pattern's descritpion and coverages are not synchronized!"
    res = 0
    
    manager = mp.Manager()
    allCovP = manager.dict()
    procs = dict()
    queue = mp.Queue()
    
    printProgressBar(0, len(coverages), prefix='Progress:', suffix='Complete', length=50)
    
    curr = 0
    for iterPar in range(0, npr):
        if curr < len(coverages):
            allCovP[str(curr)] = 0.0
            proc = mp.Process(target=covP, args=(queue, coverages, cap_cupcovother, allCovP, curr,))
            proc.start()
            procs[proc.name] = proc
            curr += 1
    
    # using the queue, launch a new process whenever
    # an old process finishes its workload
    while procs:
        name = queue.get()
        proc = procs[name]
        proc.join()
        del procs[name]
        if curr < len(coverages):
            allCovP[str(curr)] = 0.0
            proc = mp.Process(target=covP, args=(queue, coverages, cap_cupcovother, allCovP, curr,))
            proc.start()
            procs[proc.name] = proc
            curr += 1
            
    return sum(allCovP.values()) / len(coverages)


def computeproperCoverRateBySamples(coverages, cap_cupcovother):
    samples = 50
    trials = 20
    # launch
    if len(coverages) < samples:
        return properCoverRate(coverages, cap_cupcovother)       
    coverages_samples = []     
    cap_cupcovother_samples = []
    for s1 in range(0, trials):
        tmp1 = []
        tmp2 = []
        for s in range(0, samples):
            random.seed(s)
            rnd_index = random.randint(0, len(coverages) - 1)
            tmp1.append(coverages[rnd_index])
            tmp2.append(cap_cupcovother[rnd_index])
        coverages_samples.append(tmp1)
        cap_cupcovother_samples.append(tmp2)
    coverages = []
    moy = 0
#    ij = 0
    print("taille = ", len(coverages_samples), "\n")
    for curr in range(0, samples):
#        if ij == 0:
#            print(curr)
#            print(curr, "-", cap_cupcovother_samples[curr])
#        ij = ij+1
        moy += properCoverRate(coverages_samples[curr], cap_cupcovother_samples[curr])
    return moy / len(coverages_samples)


# this function should be changed based on solver logs 
def readClosedLCM(content_param, info=0):
    '''
    content_param = [datasetinfoblock, data_name, absolute_dataset_res_dir, frequency]
    '''
    val = "*"
    if content_param:
        # prepare the folder directories
        # datasetAsList = content_param[0][0]
        # items_list = content_param[0][1]
        data_name = content_param[0]
        absolute_dataset_res_dir = content_param[1]
        absolute_dataset_res_file = os.path.abspath(os.path.join(absolute_dataset_res_dir, data_name + "-" + content_param[2].replace(".", "v") + ".res"))
        absolute_dataset_log_file = os.path.abspath(os.path.join(absolute_dataset_res_dir, data_name + "-" + content_param[2].replace(".", "v") + ".log")) 
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
                            val = "-"
                            return val
        if found:
            """
            descriptions, coverages = loadPatterns(absolute_dataset_res_file)
            cap_cupcovother = intersectionRest(coverages)
            val = properCoverRate(coverages, cap_cupcovother)
            print(val)
            return val
            """
            
            moy_val = 0
            debut = 0
            fin = samples
            for co in range(0, trials):
                descriptions, coverages = loadPatternsSamples(
                    samples, debut, fin, absolute_dataset_res_file)
                cap_cupcovother = intersectionRest(coverages)
                print("\n")
                val = properCoverRate(coverages, cap_cupcovother)
                # print(val)
                # print("trial", co, ":", val)
                print("\n\n")
                moy_val += val
                
                debut = fin + 1
                fin = fin+samples
                
            # print(moy_val / trials)
            print("\n", data_name, "--> ClosedPattern PCR:", moy_val / trials, 
                  "\n\n\n-------------------------------------", 
                  "\n-------------------------------------\n\n")
            return moy_val / trials
        else:
            print(val)
            return val


def readClosedDiversityNew(content_param, info=0):
    '''
    content_param = [datasetinfoblock, data_name, absolute_dataset_res_dir, freq_threshold, jmax, historyAggregator, branchStrategy, number_threads and timeout))
    '''
    val = "*"
    if content_param:
        # datasetAsList = content_param[0][0]
        # items_list = content_param[0][1]
        data_name = content_param[0]
        absolute_dataset_res_dir = content_param[1]
        absolute_dataset_res_file = os.path.abspath(os.path.join(absolute_dataset_res_dir, data_name + "-" + content_param[2].replace(".", "v") + "-" + content_param[3].replace(".", "v") + "-" + content_param[4] + "-" + content_param[5] + "-" + content_param[6] + "-" + content_param[7] + ".res"))
        absolute_dataset_log_file = os.path.abspath(os.path.join(absolute_dataset_res_dir, data_name + "-" + content_param[2].replace(".", "v") + "-" + content_param[3].replace(".", "v") + "-" + content_param[4] + "-" + content_param[5] + "-" + content_param[6] + "-" + content_param[7] + ".log"))
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
                            val = "-"
                            return val
        if found:
            """
            descriptions, coverages = loadPatterns(absolute_dataset_res_file)
            cap_cupcovother = intersectionRest(coverages)
            val = properCoverRate(coverages, cap_cupcovother)
            print(val)
            return val
            """
            
            moy_val = 0
            debut = 0
            fin = samples
            for co in range(0, trials):
                descriptions, coverages = loadPatternsSamples(
                    samples, debut, fin, absolute_dataset_res_file)
                cap_cupcovother = intersectionRest(coverages)
                print("\n")
                val = properCoverRate(coverages, cap_cupcovother)
                # print("trial", co, ":", val, "\n\n")
                print("\n")
                moy_val += val
                
                debut = fin + 1
                fin = fin + samples
                
            print("\n", data_name, "--> ClosedDiversity PCR:", moy_val / trials, 
                  "\n\n\n-------------------------------------", 
                  "\n-------------------------------------\n\n")
            return moy_val / trials
        
        else:
            print(val)
            return val


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
    for i in range(0, nbr_measures):  # IPS, IPD
        count, chaine = printTexHeadDynamicTool(['|r'])
        foutput.write(chaine)
    foutput.write('}\n')
    fcline = "2"
    lcline = str((count * nbr_measures) + 2)
    foutput.write('                \\hline\n')
    foutput.write('                {\\bf Dataset} & \\multirow{3}*{$\\theta$} & \\multicolumn{' + str(count) + '}{c||}{Compression Rate} \n')
    foutput.write('                \\\\\\cline{' + '3' + '-' + lcline + '} \n')
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
        nbr_measures = 1
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
                
                # datasetLoaded, items_list = loadDataset(absolute_dataset_file)
                # datasetSampleLoaded, items_sample_list = loadDatasetSamples(absolute_dataset_file, samples) 
                
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
                        all_comp = []
                        for info in range(1, nbr_measures + 1):
                            for method in methods:
                                absolute_dataset_res_dir = os.path.abspath(os.path.join(project_res_dir, res_subfolder, method[0], data_name))
                                if len(method) == 1:
                                        # tmp = parsers[method[0]]([[datasetLoaded, items_list], data_name, absolute_dataset_res_dir, threshold, jmax, historyAggregator, branchStrategy, threads, timeout], info)
                                        # tmp = parsers[method[0]]([[datasetSampleLoaded, items_sample_list], data_name, absolute_dataset_res_dir, threshold, jmax, historyAggregator, branchStrategy, threads, timeout], info)
                                        tmp = parsers[method[0]]([data_name, absolute_dataset_res_dir, threshold, jmax, historyAggregator, branchStrategy, threads, timeout], info)

                                        if is_float(tmp):
                                            all_comp.append(float(tmp))
                                        else:
                                            all_comp.append(-1)
                                elif len(method) > 1:
                                    for strategy in method[1]:
                                        # tmp = parsers[method[0]]([[datasetLoaded, items_list], data_name, absolute_dataset_res_dir, threshold, jmax, historyAggregator, strategy, threads, timeout], info)
                                        # tmp = parsers[method[0]]([[datasetSampleLoaded, items_sample_list], data_name, absolute_dataset_res_dir, threshold, jmax, historyAggregator, strategy, threads, timeout], info)
                                        tmp = parsers[method[0]]([data_name, absolute_dataset_res_dir, threshold, jmax, historyAggregator, strategy, threads, timeout], info)
                                        if is_float(tmp):
                                            all_comp.append(float(tmp))
                                        else:
                                            all_comp.append(-1)

                        # compression
                        index, value = max(enumerate(all_comp), key=operator.itemgetter(1))
                        all_comp = ['*' if x == -1 else '{0:.2f}'.format(x) for x in all_comp]
                        for i in range(0, len(all_comp)):
                            if i == index:
                                resline += ' & \\bf{' + str(all_comp[i]) + '}'
                            else:
                                resline += ' & ' + str(all_comp[i])
                                
                        if count == len(fthresholds[dataset]):
                            resline += '\\\\\\hline\n'
                            foutput.write('                ' + resline)
                        else :
                            resline += '\\\\\\cline{' + str(fcline) + '-' + str(lcline) + '}\n'
                            foutput.write('                ' + resline)
                        foutput.flush();    
        printTexFoot(foutput)
