'''
Created on 12 janv. 2020

@author: Abdelkader Ouali
'''

from include import *

# program parameters
# methods = ["Closed", "ClosedDiversityNew"]
methods = ["ClosedDiversityMINCOV_estFreq_V2"]
# methods = ["ClosedDiversityMINCOV_JmaxV005_estFreq_V2"]

jmax = "0.1"  # maximum jaccard-similarity threshold
threads = "0"  # number of threads used by the global constraint
historyAggregator = "MAX"
branchStrategy = "MINCOV"
timeout = "91800s"
fthresholds = {
               "BMS1.dat" : ["0.0015", "0.0014", "0.0012"],
               "connect.dat" : ["0.4", "0.3", "0.18", "0.17", "0.15"],
               "hepatitis.dat" : ["0.3", "0.2", "0.1"],
               "mushroom.dat" : ["0.05", "0.01", "0.008", "0.005", "0.001"],
               "pumsb.dat" : [ "0.4", "0.3", "0.2", "0.15" ],
               "retail.dat" : [ "0.05", "0.01", "0.004" ],
               "T10I4D100K.dat" : [ "0.05", "0.01", "0.005" ],
               "chess.dat" : ["0.4", "0.3", "0.2", "0.15", "0.1"],
               "heart-cleveland.dat" : [ "0.2", "0.1", "0.08", "0.06"],
               "kr-vs-kp.dat" : ["0.4", "0.3", "0.2", "0.1"],
               "splice1.dat" : [ "0.1", "0.05", "0.02", "0.01" ],
               "T40I10D100K.dat" : [ "0.1", "0.08", "0.05", "0.03", "0.01" ]
               }


# this function should be changed based on solver logs 
def readResultClosed(absolute_dataset_res_file, absolute_dataset_ana_file, absolute_dataset_log_file):
    cputime = "*"
    nbr_pattern = "*"
    nbr_nodes = "*"
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
    return cputime, nbr_pattern, nbr_nodes


def readResultClosedDiversity(absolute_dataset_res_file, absolute_dataset_ana_file, absolute_dataset_log_file):
    cputime = "*"
    nbr_pattern = "*"
    nbr_nodes = "*"
    nbr_pattern_witness = "*"
    nbr_var_filtred_lb = "*"
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
    return cputime, nbr_pattern, nbr_nodes, nbr_pattern_witness, nbr_var_filtred_lb


# The functions below should be changed if readResult() has been changed, or we want a different tex output
def parseClosed(head_param, content_param):
    '''
    content_param = [data_name, absolute_dataset_res_dir, frequency]
    '''
    if head_param:
        head_param[0] += 3
        return ['|c|c|c', '& \\multicolumn{3}{c|} {Closed} ', '& CPU-Time & \\#Patterns & \\#Nodes'], head_param[0];
    elif content_param:
        data_name = content_param[0]
        absolute_dataset_res_dir = content_param[1]
        absolute_dataset_res_file = os.path.abspath(os.path.join(absolute_dataset_res_dir, data_name + "-" + content_param[2].replace(".", "v") + ".res"))
        absolute_dataset_ana_file = os.path.abspath(os.path.join(absolute_dataset_res_dir, data_name + "-" + content_param[2].replace(".", "v") + ".ana"))
        absolute_dataset_log_file = os.path.abspath(os.path.join(absolute_dataset_res_dir, data_name + "-" + content_param[2].replace(".", "v") + ".log"))
        cputime, nbr_pattern, nbr_nodes = readResultClosed(absolute_dataset_res_file, absolute_dataset_ana_file, absolute_dataset_log_file)
        return ' & ' + cputime + ' & ' + nbr_pattern + ' & ' + nbr_nodes


def parseClosedDiversityMINCOV_estFreq_V2(head_param, content_param):
    '''
    content_param = [filename, absolute_dataset_res_dir, freq_threshold, jmax, historyAggregator, branchStrategy, number_threads and timeout))
    '''
    if head_param:
        head_param[0] += 4
        return ['|c|c|c|c', '& \\multicolumn{4}{c|} {Closed Diversity} ', '& Jmax & CPU-Time & \\#Patterns (\\#Witness) & \\#Nodes (\\#Fil. Var.)'], head_param[0];
    elif content_param:
        data_name = content_param[0]
        absolute_dataset_res_dir = content_param[1]
        absolute_dataset_res_file = os.path.abspath(os.path.join(absolute_dataset_res_dir, data_name + "-" + content_param[2].replace(".", "v") + "-" + content_param[3].replace(".", "v") + "-" + content_param[4] + "-" + content_param[5] + "-" + content_param[6] + "-" + content_param[7] + ".res"))
        absolute_dataset_ana_file = os.path.abspath(os.path.join(absolute_dataset_res_dir, data_name + "-" + content_param[2].replace(".", "v") + "-" + content_param[3].replace(".", "v") + "-" + content_param[4] + "-" + content_param[5] + "-" + content_param[6] + "-" + content_param[7] + ".ana"))
        absolute_dataset_log_file = os.path.abspath(os.path.join(absolute_dataset_res_dir, data_name + "-" + content_param[2].replace(".", "v") + "-" + content_param[3].replace(".", "v") + "-" + content_param[4] + "-" + content_param[5] + "-" + content_param[6] + "-" + content_param[7] + ".log"))
        cputime, nbr_pattern, nbr_nodes, nbr_pattern_witness, nbr_var_filtred_lb = readResultClosedDiversity(absolute_dataset_res_file, absolute_dataset_ana_file, absolute_dataset_log_file)
        return ' & ' + content_param[3] + ' & ' + cputime + ' & ' + nbr_pattern + ' (' + nbr_pattern_witness + ')' + ' & ' + nbr_nodes + ' (' + nbr_var_filtred_lb + ')'


def mapParsersDynamic(methods): 
    parsers = {}
    for method in methods:
        method_name = 'parse' + method
        possibles = globals().copy()
        possibles.update(locals())
        parse_method = possibles.get(method_name)
        if not parse_method:
            raise NotImplementedError("Method %s not implemented" % method_name)
        parsers[method] = parse_method
    return parsers


def printTexHeadDynamic(methods, parsers): 
    
    # prepare table headline based on available methods
    print('\\begin{table}')
    print('    \\scriptsize')
    print('    \\raggedleft \\scalebox{.82}{')
    
    columns_line = '        \\begin{tabular}[h]{|L{2cm}|c' 
    head_line1 = '\\multirow{2}{1cm}{Datasets} & \\multirow{2}{0.5cm}{Min Freq.}'
    head_line2 = ' & '
    
    fcline = 2
    lcline = fcline
    for method in methods:
        parse_res, lcline = parsers[method]([lcline], [])
        columns_line += parse_res[0]
        head_line1 += parse_res[1]
        head_line2 += parse_res[2]
    
    columns_line += "|} \\hline"
    head_line1 += '  \\\\\\cline{' + str(fcline + 1) + '-' + str(lcline) + '}'
    head_line2 += "  \\\\\\hline"
    
    print(columns_line)
    print(head_line1)
    print(head_line2)
    print('            %-------------------------------------------------------------------%')
    return fcline, lcline


def printTexFoot():
    print('            %-------------------------------------------------------------------%')
    print('        \\end{tabular}')
    print('    }')
    print('\\caption{*: not yet launched, or in the worst case an error has occured. -: timeout reached. }') 
    print('\\end{table}')


# now parsing the results of the available methods, this method should be modified, unless a new method is added
if __name__ == '__main__':
    parsers = mapParsersDynamic(methods)
    fcline, lcline = printTexHeadDynamic(methods, parsers)
    for dataset in os.listdir(project_data_dir):
        if dataset.endswith(".dat"):
            first = True
            data_name = dataset.split('.')[0]
            if dataset in fthresholds:
                print('\\hline')
                count = 0
                for threshold in fthresholds[dataset]:
                    count += 1
                    if first:
                        resline = data_name + ' & ' + threshold + ' '
                        first = False
                    else:
                        resline = ' & ' + threshold + ' '
                    for method in methods:
                        absolute_dataset_res_dir = os.path.abspath(os.path.join(project_res_dir, method, data_name))
                        resline += parsers[method]([], [data_name, absolute_dataset_res_dir, threshold, jmax, historyAggregator, branchStrategy, threads, timeout])
                    if count == len(fthresholds[dataset]):
                        print(resline, '\\\\\\hline')
                    else :
                        print(resline, '\\\\\\cline{' + str(fcline) + '-' + str(lcline) + '}')
                    
    printTexFoot()
