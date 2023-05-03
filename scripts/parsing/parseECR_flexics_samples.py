'''
Created on 21 June 2020

@author: Arnold Hien
'''

from include_2 import *

# program parameters
methods = ["EFlexics", "GFlexics"]

npr = 30
output = "measure_ECR_flexics_1.tex"

taskTODO = "sample"
# qualityMeasure = ["frequency"] # it can be "uniform" or "purity" 
qualityMeasure = "frequency"

# F -> minFreq, L -> minLength, C -> Closed
# They can be combined : example -> F,C means closed 
# with a certain minimum frequency
constraintParameter = "F-C"

#error_tolerance = ["0.9", "0.5", "0.1"] # error tolerance
#error_tolerance = "0.5"
kappa = "0.9"
numberOfSample = "100"
timeout = "91800s"

fthresholds = {
               "BMS1.fimi" : ["0.0015", "0.0014", "0.0012"],
               "connect.fimi" : ["0.3", "0.18", "0.17", "0.15"],
               "hepatitis.fimi" : ["0.3", "0.2", "0.1"],
#               "hepatitis.fimi" : ["0.3", "0.2"],
               "mushroom.fimi" : ["0.05", "0.01", "0.008", "0.005"],
               "pumsb.fimi" : [ "0.4", "0.3", "0.2"],
#               "pumsb.fimi" : ["0.4", "0.3"],
               "retail.fimi" : [ "0.05", "0.01", "0.004"],
               "T10I4D100K.fimi" : [ "0.05", "0.01", "0.005" ],
               "chess.fimi" : ["0.4", "0.3", "0.2", "0.15", "0.1"],
               "heart-cleveland.fimi" : [ "0.2", "0.1", "0.08", "0.06"],
               "kr-vs-kp.fimi" : ["0.4", "0.3", "0.2", "0.1"],
               "splice1.fimi" : [ "0.1", "0.05"],
               "T40I10D100K.fimi" : [ "0.1", "0.08", "0.05", "0.03", "0.01" ]
               }

allSamples = {
               "BMS1.fimi" : ["609", "668", "823"],
               "connect.fimi" : ["18", "197", "272", "509"],
               "hepatitis.fimi" : ["12", "57", "2270"],
               "mushroom.fimi" : ["727", "12139", "15715", "27768"],
               "pumsb.fimi" : ["4", "15", "52"],
               "retail.fimi" : ["13", "111", "528"],
               "T10I4D100K.fimi" : ["11", "361", "617"],
               "chess.fimi" : ["5", "16", "96", "393", "4204"],
               "heart-cleveland.fimi" : ["81", "3496", "12842", "58240"],
               "kr-vs-kp.fimi" : ["5", "17", "96", "4120"],
               "splice1.fimi" : ["422", "8781"],
               "T40I10D100K.fimi" : ["75", "127", "288", "598", "7402"]
               }

samples = 10
trials = 100

res_subfolder = "Flexics"


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


def getNbrLignes(absolute_patterns_filename):
    nbLignes = sum(1 for line in open(absolute_patterns_filename, "r"))
    return nbLignes


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


def ParsePatternFileLine(line):
    coverage = []    
    blocks = re.findall('\[(.*?)\]', line)
    
    msg = "pattern's description and coverages are not synchronized!"
    assert len(blocks) == 2, msg
    
    if len(blocks[0].strip()) != 0:  # avoid loading empty set
        # we should start from index 0 instead of index 1 that is provided in the file
        coverage = []
        for t in blocks[1].strip().split(" "):
            coverage.append(int(t) - 1)
    
    return coverage


def load_patterns_samples(absolute_sol_file, nbPatterns):
    coverages = []
    save_samples_lines = []
    curr = 0
    
    borne_sup = max(100, nbPatterns)
    with open(absolute_sol_file, "r") as infile:
        for line in infile:
            # decide randomly if we should choose the sample
            rnd_index = random.randint(0, borne_sup)
            if rnd_index <= (borne_sup/2):
                coverage = ParsePatternFileLine(line)
                coverages.append(coverage)
                if len(coverages) == samples:
                    break
            else:
                # secure some lines to to complete the sample if random approach is no complete
                if curr <= samples:
                    save_samples_lines.append(line)
                    curr += 1
    
    # test if we have enough samples, if not load from saved lines
    curr = 0
    while len(coverages) < samples and curr < len(save_samples_lines):
        coverage = ParsePatternFileLine(save_samples_lines[curr])
        coverages.append(coverage)
        curr += 1
    # if we don't have enough sample from the file, then exit 
    if len(coverages) < samples:
        print("Not enough samples, the implemented ICD requires the same number of patterns")
        sys.exit(1)      
        
    return coverages

def load_nbPatterns(absolute_ana_file):
    nbPatterns = 0
    with open(absolute_ana_file, "r") as anafile:
        first_line = anafile.readline()
        resval = first_line.split(';')
        nbPatterns = resval[-5]
    return int(nbPatterns)-1


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
    msg = "pattern's descritpion and coverages are not synchronized!"
    assert len(descriptions) == len(coverages), msg
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
    printProgressBar(0, len(coverages), prefix='Progress:', suffix='Complete', length=50)
    for k in range(0, len(coverages)):
        tmp = set()
        for l in range(0, len(coverages)):
            if l != k:
                tmp = tmp.union(set(coverages[l]))
        union_cover.append(tmp)
        printProgressBar(k, len(coverages), prefix='Progress:', suffix='Complete', length=50)
    cap_cupcovother = []
    printProgressBar(0, len(coverages), prefix='Progress:', suffix='Complete', length=50)
    for k in range(0, len(coverages)):
        cap_cupcovother.append(list(set(coverages[k]).intersection(union_cover[k])))
        printProgressBar(k, len(coverages), prefix='Progress:', suffix='Complete', length=50)
    return cap_cupcovother


def properCoverRate(coverages, cap_cupcovother):
    msg = "pattern's descritpion and coverages are not synchronized!"
    assert len(cap_cupcovother) == len(coverages), msg
    res = 0
    printProgressBar(0, len(coverages), prefix='Progress:', suffix='Complete', length=50)
    for k in range(0, len(coverages)):
        sp = len(coverages[k])
        res += ((sp - len(cap_cupcovother[k])) / sp)
        printProgressBar(k, len(coverages), prefix='Progress:', suffix='Complete', length=50) 
    return res / len(coverages)


def readEFlexics(content_param, info=0):
    '''
    content_param = [datasetinfoblock, data_name, absolute_dataset_res_dir, frequency]
    '''
    val = "*"
    if content_param:
        absolute_dataset_res_dir = content_param[0]
        data_name = content_param[1]
        
        absolute_dataset_sol_file = os.path.abspath(os.path.join(absolute_dataset_res_dir, 
                data_name + "-" + content_param[2] + "-" + content_param[3] + "-" + content_param[4] + 
                "-" + content_param[6] + "-" + content_param[7] + "-" + content_param[8] + 
                "-" + content_param[9] + ".sol"))
        
        absolute_dataset_txt_file = os.path.abspath(os.path.join(absolute_dataset_res_dir, 
                data_name + "-" + content_param[2] + "-" + content_param[3] + "-" + content_param[4] + 
                "-" + content_param[6] + "-" + content_param[7] + "-" + content_param[8] + 
                "-" + content_param[9] + ".txt"))
        
#        print(absolute_dataset_sol_file)
        
        # compute
        found = False
        if (os.path.exists(absolute_dataset_sol_file)):
            found = True
        
        if found:
#            print(absolute_dataset_sol_file)
#            nbPAtterns = int(content_param[8])
            nbPAtterns = getNbrLignes(absolute_dataset_txt_file)
            if nbPAtterns < samples:
                val = "-"
            elif nbPAtterns == samples:
                coverages = load_patterns_samples(absolute_dataset_sol_file, nbPAtterns)
                cap_cupcovother = intersectionRest(coverages)
                val = properCoverRate(coverages, cap_cupcovother)
                val = str(val)
            else:
                pcr = 0.0
                for i in range(0, trials):
                    coverages = load_patterns_samples(absolute_dataset_sol_file, nbPAtterns)
                    cap_cupcovother = intersectionRest(coverages)
                    pcr = pcr + properCoverRate(coverages, cap_cupcovother)
                pcr = pcr/trials
                val = str(pcr)
            
        print(val)
        return val


def readGFlexics(content_param, info=0):
#    print("GFlexics")
    val = "*"
    if content_param:
        data_name = content_param[1]
        absolute_dataset_res_dir = content_param[0]
        
        absolute_dataset_sol_file = os.path.abspath(os.path.join(absolute_dataset_res_dir, 
                data_name + "-" + content_param[2] + "-" + content_param[3] + "-" + content_param[4] + 
                "-" + content_param[5] + "-" + content_param[6] + "-" + content_param[7] + 
                "-" + content_param[8] + "-" + content_param[9] + ".sol"))
        
        absolute_dataset_txt_file = os.path.abspath(os.path.join(absolute_dataset_res_dir, 
                data_name + "-" + content_param[2] + "-" + content_param[3] + "-" + content_param[4] + 
                "-" + content_param[5] + "-" + content_param[6] + "-" + content_param[7] + 
                "-" + content_param[8] + "-" + content_param[9] + ".txt"))
        
#        print(absolute_dataset_sol_file)
        
        # compute
        found = False
        if (os.path.exists(absolute_dataset_sol_file)):
            found = True
        
        if found:
#            print(absolute_dataset_sol_file)
#            nbPAtterns = int(content_param[8])
            nbPAtterns = getNbrLignes(absolute_dataset_txt_file)
            if nbPAtterns < samples:
                val = "-"
            elif nbPAtterns == samples:
                coverages = load_patterns_samples(absolute_dataset_sol_file, nbPAtterns)
                cap_cupcovother = intersectionRest(coverages)
                val = properCoverRate(coverages, cap_cupcovother)
                val = str(val)
            else:
                pcr = 0.0
                for i in range(0, trials):
                    coverages = load_patterns_samples(absolute_dataset_sol_file, nbPAtterns)
                    cap_cupcovother = intersectionRest(coverages)
                    pcr = pcr + properCoverRate(coverages, cap_cupcovother)
                pcr = pcr/trials
                val = str(pcr)
            
        print(val)
        return val

def mapParsersDynamic(methods): 
    parsers = {}
    for method in methods:
        method_name = 'read' + method
        possibles = globals().copy()
        possibles.update(locals())
        parse_method = possibles.get(method_name)
        if not parse_method:
            raise NotImplementedError("Method %s not implemented" % method_name) 
        parsers[method] = parse_method
    return parsers


def printTexHeadDynamicTool(m):
    count = 0
    chaine = ""
    for method in methods:
        count += 1
        if len(m) == 1:
            chaine += m[0]
        elif len(m) > 1:
            chaine += m[0] + method + m[1]
        
#        if len(method) == 1:
#            count += 1
#            if len(m) == 1:
#                chaine += m[0]
#            elif len(m) > 1:
#                chaine += m[0] + method + m[1]
#        elif len(method) > 1:
#            for strategy in method[1]:
#                count += 1
#                if len(m) == 1:
#                    chaine += m[0]
#                elif len(m) > 1:
#                    chaine += m[0] + strategy + m[1]
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
    foutput.write('                {\\bf Dataset} & \\multirow{3}*{$\\theta$} & \\multicolumn{' + 
                  str(count) + '}{c||}{Compression Rate} \n')
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
    foutput.write('                ' + 
                  '%....................................................................%\n')
    return fcline, lcline


def printTexFoot(foutput):
    foutput.write('                ' + 
                  '%-------------------------------------------------------------------%\n')
    foutput.write('            \\end{tabular}\n')
    foutput.write('        }\n')
    foutput.write('    \\caption{*: not yet launched, or in the worst case an error ' + 
                                 'has occured. -: timeout reached. For the \\#Patterns, ' + 
                                 'the value in bold reduces more than 20\% of the total \\# ' + 
                                 'of patterns}\n') 
    foutput.write('\\end{table}\n')
    

# now parsing the results of the available methods, 
# this method should be modified, unless a new method is added
if __name__ == '__main__':
    with open(output, "w") as foutput:
        nbr_measures = 1
        parsers = mapParsersDynamic(methods)
        fcline, lcline = printTexHeadDynamic(methods, parsers, foutput)
        
        for dataset in os.listdir(project_flexics_data_dir):
            if dataset.endswith(".fimi"):
                nline = 1
                data_name = dataset.split('.')[0]
                absolute_dataset_file = os.path.abspath(os.path.join(project_data_dir, 
                                                                     data_name + '.dat'))
#                datasetLoaded, items_list = loadDataset(absolute_dataset_file)
                if dataset in fthresholds:
                    items = ""
                    trans = "" 
                    density = ""
                    absolute_dataset_desc_dir = os.path.abspath(os.path.join(project_data_dir, 
                                                                             data_name + '.desc'))
                    with open(absolute_dataset_desc_dir, 'r') as fdesc:
                        first_line = fdesc.readline().strip().split(' ')
                        trans = first_line[0]
                        items = first_line[1]
                        density = first_line[2]
                    foutput.write('                \\hline\n')
                    foutput.flush();
                    count = 0
#                    for threshold in fthresholds[dataset]:
                    for k in range(0, len(fthresholds[dataset])):
                        threshold = fthresholds[dataset][k]
                        nbSamples = allSamples[dataset][k]
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
                                print(method)
                                absolute_dataset_res_dir = os.path.abspath(os.path.join(
                                        project_res_dir, res_subfolder, method, data_name))
                                
                                tmp = parsers[method]([absolute_dataset_res_dir, data_name, taskTODO, method.lower(), threshold.replace(".", "v"), constraintParameter, qualityMeasure, kappa.replace(".", "v"), nbSamples, timeout])
                                
                                if is_float(tmp):
                                    all_comp.append(float(tmp))
                                else:
                                    all_comp.append(-1)
                                
                                print()
                        print("\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n")

                        # compression
                        index, value = max(enumerate(all_comp), key=operator.itemgetter(1))
                        all_comp = ['*' if x == -1 else '{0:.4f}'.format(x) for x in all_comp]
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
