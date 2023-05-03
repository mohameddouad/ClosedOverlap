'''
Created on 12 janv. 2020

@author: Abdelkader Ouali
'''

from include import *

# program parameters
allStrategies = ["MINCOV"]  # , "FIRSTWITCOV", "MINWITCOV"
methods = [["Closed"], ["ClosedDiversityNew", allStrategies]]

jmax = "0.1"  # maximum jaccard-similarity threshold
threads = "0"  # number of threads used by the global constraint
historyAggregator = "MAX"
branchStrategy = "MINCOV"
timeout = "91800s"
fthresholds = {
               "BMS1.dat" : ["0.0015", "0.0014", "0.0012"],
               "connect.dat" : ["0.3", "0.18", "0.17", "0.15"],
               "hepatitis.dat" : ["0.3", "0.2", "0.1"],
               "mushroom.dat" : ["0.05", "0.01", "0.008", "0.005"],
               "pumsb.dat" : [ "0.4", "0.3", "0.2"],
               "retail.dat" : [ "0.05", "0.01", "0.004"],
               "T10I4D100K.dat" : [ "0.05", "0.01", "0.005" ],
               "chess.dat" : ["0.4", "0.3", "0.2", "0.15"],
               "heart-cleveland.dat" : [ "0.2", "0.1", "0.08", "0.06"],
               "kr-vs-kp.dat" : ["0.4", "0.3", "0.2"],
               "splice1.dat" : [ "0.1", "0.05", "0.02", "0.01" ],
               "T40I10D100K.dat" : [ "0.1", "0.08", "0.05", "0.03", "0.01"],
               'ijcai16.dat': ["0.3", "0.2", "0.1"]
               }

res_subfolder = "foxrex"


# this function should be changed based on solver logs 
def readClosed(content_param, info=0):
    '''
    content_param = [data_name, absolute_dataset_res_dir, frequency]
    '''
    cputime = "*"
    nbr_pattern = "*"
    nbr_nodes = "*"
    if content_param:
        # prepare the folder directories
        data_name = content_param[0]
        absolute_dataset_res_dir = content_param[1]
        absolute_dataset_res_file = os.path.abspath(os.path.join(absolute_dataset_res_dir, data_name + "-" + content_param[2].replace(".", "v") + ".res"))
        absolute_dataset_ana_file = os.path.abspath(os.path.join(absolute_dataset_res_dir, data_name + "-" + content_param[2].replace(".", "v") + ".ana"))
        absolute_dataset_log_file = os.path.abspath(os.path.join(absolute_dataset_res_dir, data_name + "-" + content_param[2].replace(".", "v") + ".log")) 
        # extract
        if (os.path.exists(absolute_dataset_log_file)):
            with open(absolute_dataset_log_file, 'r') as logfile:
                for line in logfile:
                    line_parse = re.findall(r'Exit status:[\s]+(\d+)', line)
                    if line_parse:
                        if line_parse[0] == '0':
                            with open(absolute_dataset_ana_file, 'r') as anafile:
                                first_line = anafile.readline()
                                resval = first_line.split(';')
                                cputime = '{0:.2f}'.format(float(resval[-3]))
                                nbr_pattern = resval[-2]
                                nbr_nodes = resval[-1]  
                        elif line_parse[0] == '124':
                            cputime = "-"
                            nbr_pattern = "-"
                            nbr_nodes = "-"
    if info == 1:
        return nbr_pattern
    elif info == 2:
        return cputime
    elif info == 3:
        return nbr_nodes
    return cputime, nbr_pattern, nbr_nodes


def readClosedDiversityNew(content_param, info=0):
    '''
    content_param = [filename, absolute_dataset_res_dir, freq_threshold, jmax, historyAggregator, branchStrategy, number_threads and timeout))
    '''
    cputime = "*"
    nbr_pattern = "*"
    nbr_nodes = "*"
    nbr_pattern_witness = "*"
    nbr_var_filtred_lb = "*"
    if content_param:
        data_name = content_param[0]
        absolute_dataset_res_dir = content_param[1]
        absolute_dataset_res_file = os.path.abspath(os.path.join(absolute_dataset_res_dir, data_name + "-" + content_param[2].replace(".", "v") + "-" + content_param[3].replace(".", "v") + "-" + content_param[4] + "-" + content_param[5] + "-" + content_param[6] + "-" + content_param[7] + ".res"))
        absolute_dataset_ana_file = os.path.abspath(os.path.join(absolute_dataset_res_dir, data_name + "-" + content_param[2].replace(".", "v") + "-" + content_param[3].replace(".", "v") + "-" + content_param[4] + "-" + content_param[5] + "-" + content_param[6] + "-" + content_param[7] + ".ana"))
        absolute_dataset_log_file = os.path.abspath(os.path.join(absolute_dataset_res_dir, data_name + "-" + content_param[2].replace(".", "v") + "-" + content_param[3].replace(".", "v") + "-" + content_param[4] + "-" + content_param[5] + "-" + content_param[6] + "-" + content_param[7] + ".log"))
        # prepare the folder directories
        if (os.path.exists(absolute_dataset_log_file)):
            with open(absolute_dataset_log_file, 'r') as logfile:
                for line in logfile:
                    line_parse = re.findall(r'Exit status:[\s]+(\d+)', line)
                    if line_parse:
                        if line_parse[0] == '0':
                            with open(absolute_dataset_ana_file, 'r') as anafile:
                                first_line = anafile.readline()
                                resval = first_line.split(';')
                                cputime = '{0:.2f}'.format(float(resval[-6]))
                                nbr_pattern = resval[-5]
                                nbr_pattern_witness = resval[-3]
                                nbr_nodes = resval[-4]  
                                nbr_var_filtred_lb = resval[-2]
                        elif line_parse[0] == '124':
                            cputime = "-"
                            nbr_pattern = "-"
                            nbr_nodes = "-"
                            nbr_pattern_witness = "-"
                            nbr_var_filtred_lb = "-"
    if info == 1:
        return nbr_pattern + ' (' + nbr_pattern_witness + ')'
    elif info == 2:
        return cputime
    elif info == 3:
        return nbr_nodes + ' (' + nbr_var_filtred_lb + ')'
    return cputime, nbr_pattern, nbr_nodes, nbr_pattern_witness, nbr_var_filtred_lb


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
    for method in methods:
        if len(method) == 1:
            count += 1
            if len(m) == 1:
                print(m[0], end="")
            elif len(m) > 1:
                print(m[0] + method[0] + m[1], end="")
        elif len(method) > 1:
            for strategy in method[1]:
                count += 1
                if len(m) == 1:
                    print(m[0], end="")
                elif len(m) > 1:
                    print(m[0] + strategy + m[1], end="")
    return count


def printTexHeadDynamic(methods, parsers):
    print('\\begin{table}[htbp]')
    print('    \\centering')
    print('        \\scalebox{.7}{')
    print('\\begin{tabular}[h]{c|c', end="")

    for i in range(0, 3):  # Patterns, # Time, # Node 
        count = printTexHeadDynamicTool(['|r'])
     
    print('}')
    fcline = "2"
    lcline = str((count * 3) + 2)
    print('                \\hline')
    print('                {\\bf Dataset} & \\multirow{3}*{$\\theta$} & \\multicolumn{' + str(count) + '}{c||}{\\#Patterns} &')
    print('                \\multicolumn{', count, '}{c||}{Time (s)} & \\multicolumn{' + str(count) + '}{c}{\\#Nodes (\\#Fil. Var.)} \\\\\\cline{' + '3' + '-' + lcline + '} ')
    print('                $|\\items| \\times |\\bdd|  $ &  ', end="")
    for i in range(0, 3):  # Patterns, # Time, # Node 
        printTexHeadDynamicTool([' & \\multirow{2}*{', '}'])
    print('\\\\')
    print('                $\\rho(\\%)$ ', end="")
    for i in range(0, 3):  # Patterns, # Time, # Node 
        printTexHeadDynamicTool([' & '])
    
    print('\\\\\\hline')
    print('%....................................................................%')
    return fcline, lcline


def printTexFoot():
    print('            %-------------------------------------------------------------------%')
    print('        \\end{tabular}')
    print('    }')
    print('\\caption{*: not yet launched, or in the worst case an error has occured. -: timeout reached. For the \\#Patterns, the value in bold reduces more than 20\% of the total \\# of patterns}') 
    print('\\end{table}')


# now parsing the results of the available methods, this method should be modified, unless a new method is added
if __name__ == '__main__':
    parsers = mapParsersDynamic(methods)
    fcline, lcline = printTexHeadDynamic(methods, parsers)
    
    if not branchStrategy in allStrategies:
        print("ERROR, you must respect the syntax for the branch strategy : \"MINCOV\", \"FIRSTWITCOV\" or \"MINWITCOV\" \n")
        sys.exit(1)
        
    for dataset in os.listdir(project_data_dir):
        if dataset.endswith(".dat"):
            nline = 1
            data_name = dataset.split('.')[0]
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
                print('\\hline')
                count = 0
                for threshold in fthresholds[dataset]:
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
                    all_p = []
                    all_reduced = []
                    all_t = []
                    all_tfloat = []
                    all_n = []
                    best_p = 0
                    best_t = 0
                    for info in range(1, 4):
                        for method in methods:
                            absolute_dataset_res_dir = os.path.abspath(os.path.join(project_res_dir, res_subfolder, method[0], data_name))
                            if len(method) == 1:
                                if info == 1:
                                    all_p.append(parsers[method[0]]([data_name, absolute_dataset_res_dir, threshold, jmax, historyAggregator, branchStrategy, threads, timeout], info))
                                    if len(all_reduced) == 0:
                                        all_reduced.append(0)
                                    else:
                                        if is_float(all_p[-1].split(' ')[0]) and is_float(all_p[0]):
                                            all_reduced.append(100 - ((float(all_p[-1].split(' ')[0]) * 100) / float(all_p[0])))
                                        else:
                                            all_reduced.append(0)
                                elif info == 2:
                                    all_t.append(parsers[method[0]]([data_name, absolute_dataset_res_dir, threshold, jmax, historyAggregator, branchStrategy, threads, timeout], info))
                                    if is_float(all_t[-1]):
                                        all_tfloat.append(float(all_t[-1]))
                                    else:
                                        all_tfloat.append(sys.float_info.max)
                                else:
                                    all_n.append(parsers[method[0]]([data_name, absolute_dataset_res_dir, threshold, jmax, historyAggregator, branchStrategy, threads, timeout], info))
                            elif len(method) > 1:
                                for strategy in method[1]:
                                    if info == 1:
                                        all_p.append(parsers[method[0]]([data_name, absolute_dataset_res_dir, threshold, jmax, historyAggregator, strategy, threads, timeout], info))
                                        if len(all_reduced) == 0:
                                            all_reduced.append(0)
                                        else:
                                            if is_float(all_p[-1].split(' ')[0]) and is_float(all_p[0]):
                                                all_reduced.append(100 - ((float(all_p[-1].split(' ')[0]) * 100) / float(all_p[0])))
                                            else:
                                                all_reduced.append(0)
                                    elif info == 2:
                                        all_t.append(parsers[method[0]]([data_name, absolute_dataset_res_dir, threshold, jmax, historyAggregator, strategy, threads, timeout], info))
                                        if is_float(all_t[-1]):
                                            all_tfloat.append(float(all_t[-1]))
                                        else:
                                            all_tfloat.append(sys.float_info.max)
                                    else:
                                        all_n.append(parsers[method[0]]([data_name, absolute_dataset_res_dir, threshold, jmax, historyAggregator, strategy, threads, timeout], info)) 
                    # patterns
                    index, value = max(enumerate(all_reduced), key=operator.itemgetter(1))
                    for i in range(0, len(all_p)):
                        if i == index and  value >= 20:
                            resline += ' & \\bf{' + all_p[i] + '}'
                        else:
                            resline += ' & ' + all_p[i]
                    index, value = min(enumerate(all_tfloat), key=operator.itemgetter(1))
                    # time             
                    for i in range(0, len(all_t)):
                        if i == index:
                            resline += ' & \\bf{' + all_t[i] + '}'
                        else:
                            resline += ' & ' + all_t[i]
                    # nodes
                    for i in range(0, len(all_n)):
                            resline += ' & ' + all_n[i]
                        
                    if count == len(fthresholds[dataset]):
                        print(resline, '\\\\\\hline')
                    else :
                        print(resline, '\\\\\\cline{' + str(fcline) + '-' + str(lcline) + '}')    
    printTexFoot()
