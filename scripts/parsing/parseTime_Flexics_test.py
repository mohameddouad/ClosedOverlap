'''
Created on 12 janv. 2020

@author: Abdelkader Ouali
'''

from include import *

# program parameters
methods = ["EFlexics", "GFlexics"]
threads = "0"  # number of threads used by the global constraint

oracle = "gflexics"
qualityMeasure = "frequency" # it can be "uniform" or "purity" 

constraintParameter = "F-C" # F -> minFreq, L -> minLength, C -> Closed -- They can be combined : example -> F,C means closed with a certain minimum frequency

taskTODO = "sample"

error_tolerance = ["0.9", "0.5", "0.1"] # error tolerance
timeout = "91800s"

fthresholds = {
               "BMS1.fimi" : ["0.0015", "0.0014", "0.0012"],
               "connect.fimi" : ["0.3", "0.18", "0.17", "0.15"],
               "hepatitis.fimi" : ["0.3", "0.2", "0.1"],
               "mushroom.fimi" : ["0.05", "0.01", "0.008", "0.005"],
               "pumsb.fimi" : ["0.4", "0.3", "0.2"],
               "retail.fimi" : ["0.05", "0.01", "0.004"],
               "T10I4D100K.fimi" : ["0.05", "0.01", "0.005" ],
               "chess.fimi" : ["0.4", "0.3", "0.2", "0.15", "0.1"],
               "heart-cleveland.fimi" : ["0.2", "0.1", "0.08", "0.06"],
               "kr-vs-kp.fimi" : ["0.4", "0.3", "0.2", "0.1"],
               "splice1.fimi" : ["0.1", "0.05"],
               "T40I10D100K.fimi" : ["0.1", "0.08", "0.05", "0.03", "0.01"]
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


def readResultFlexics(absolute_dataset_log_file, absolute_dataset_time_file):
    cputime = "*"
    ok = False
    
    # print("", absolute_dataset_log_file, "\n", absolute_dataset_time_file, "\n")
    
    # extract
    if (os.path.exists(absolute_dataset_log_file)):
        with open(absolute_dataset_log_file, 'r') as timefile:
            for line in timefile:
                line_parse = re.findall(r'Exit status:[\s]+(\d+)', line)
                if line_parse:
                    if line_parse[0] == '0':
                        ok = True
                        break
                    elif line_parse[0] == '1':
                        cputime = "!"
                        break
                    elif line_parse[0] == '124':
                        cputime = "-"
                        break
        
        if ok:
            with open(absolute_dataset_time_file, 'r') as timefile:
                for line in timefile:
                    temps_splt = line.split(" or m:ss): ")
                    if len(temps_splt) > 1:
                        
#                        if aff:
#                            print("\n", line, "\n")
                        
                        tab = temps_splt[1].split(":")
                        temps = 0.0
                        if len(tab) == 3:
                            temps = temps + (3600*int(tab[0])) + (60*int(tab[1])) + float(tab[2])
                        elif len(tab) == 2:
                            temps = temps + (60*int(tab[0])) + float(tab[1])
                        
                        cputime = str('{0:.2f}'.format(temps))
        
    return cputime


def parseEFlexics(head_param, content_param):
    '''
    content_param = [filename, absolute_dataset_res_dir, freq_threshold, jmax, historyAggregator, branchStrategy, number_threads and timeout))
    '''
    if head_param:
        head_param[0] += 3
        return ['|c|c|c', '& \\multicolumn{3}{c|} {EFlexics} ', ' & Kappa=0.9 & Kappa=0.5 & Kappa=0.1 '], head_param[0];
    elif content_param:
        data_name = content_param[0]
        # absolute_dataset_gflexics_res_dir = os.path.abspath(os.path.join(content_param[1], "Flexics", "EFlexics"))
        absolute_dataset_gflexics_res_dir = content_param[1]
        # absolute_dataset_res_file = os.path.abspath(os.path.join(absolute_dataset_res_dir, data_name + "-" + content_param[2].replace(".", "v") + "-" + content_param[3].replace(".", "v") + "-" + content_param[4] + "-" + content_param[6] + "-" + content_param[7] + ".res"))
        # absolute_dataset_ana_file = os.path.abspath(os.path.join(absolute_dataset_res_dir, data_name + "-" + content_param[2].replace(".", "v") + "-" + content_param[3].replace(".", "v") + "-" + content_param[4] + "-" + content_param[6] + "-" + content_param[7] + ".ana"))
        absolute_dataset_log_file = os.path.abspath(os.path.join(absolute_dataset_gflexics_res_dir, data_name + "-" + content_param[2] + "-" + content_param[3] + "-" + content_param[4] + "-" + content_param[6] + "-" + content_param[7] + "-" + content_param[8] + "-" + content_param[9] + ".log"))
        absolute_dataset_time_file = os.path.abspath(os.path.join(absolute_dataset_gflexics_res_dir, data_name + "-" + content_param[2] + "-" + content_param[3] + "-" + content_param[4] + "-" + content_param[6] + "-" + content_param[7] + "-" + content_param[8] + "-" + content_param[9] + ".time"))
        
#        print("", absolute_dataset_log_file, "\n", absolute_dataset_time_file, "\n")
        
        cputime = readResultFlexics(absolute_dataset_log_file, absolute_dataset_time_file)
        return ' & ' + cputime + ''


def parseGFlexics(head_param, content_param):
    '''
    content_param = [filename, absolute_dataset_res_dir, freq_threshold, jmax, historyAggregator, branchStrategy, number_threads and timeout))
    '''
    if head_param:
        head_param[0] += 3
        return ['|c|c|c', '& \\multicolumn{3}{c|} {GFlexics} ', ' & Kappa=0.9 & Kappa=0.5 & Kappa=0.1 '], head_param[0];
    elif content_param:
        data_name = content_param[0]
        # absolute_dataset_gflexics_res_dir = os.path.abspath(os.path.join(content_param[1], "Flexics", "GFlexics")))
        absolute_dataset_gflexics_res_dir = content_param[1]
        # absolute_dataset_res_file = os.path.abspath(os.path.join(absolute_dataset_res_dir, data_name + "-" + content_param[2].replace(".", "v") + "-" + content_param[3].replace(".", "v") + "-" + content_param[4] + "-" + content_param[6] + "-" + content_param[7] + ".res"))
        # absolute_dataset_ana_file = os.path.abspath(os.path.join(absolute_dataset_res_dir, data_name + "-" + content_param[2].replace(".", "v") + "-" + content_param[3].replace(".", "v") + "-" + content_param[4] + "-" + content_param[6] + "-" + content_param[7] + ".ana"))
        absolute_dataset_log_file = os.path.abspath(os.path.join(absolute_dataset_gflexics_res_dir, data_name + "-" + content_param[2] + "-" + content_param[3] + "-" + content_param[4] + "-" + content_param[5] + "-" + content_param[6] + "-" + content_param[7] + "-" + content_param[8] + "-" + content_param[9] + ".log"))
        absolute_dataset_time_file = os.path.abspath(os.path.join(absolute_dataset_gflexics_res_dir, data_name + "-" + content_param[2] + "-" + content_param[3] + "-" + content_param[4] + "-" + content_param[5] + "-" + content_param[6] + "-" + content_param[7] + "-" + content_param[8] + "-" + content_param[9] + ".time"))
        
        cputime = readResultFlexics(absolute_dataset_log_file, absolute_dataset_time_file)
        return ' & ' + cputime + ''


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
    print('\\begin{table}[t]')
    print('    \\scriptsize')
    print('    \\centering \\scalebox{.82}{')
    
    columns_line = '        \\begin{tabular}[h]{|L{2cm}|c' 
    head_line1 = '\\multirow{2}{1cm}{Datasets} & \\multirow{2}{0.5cm}{Min Freq.} & \\multirow{2}{0.82cm}{#Samples}'
    head_line2 = ' & & '
    
    fcline = 3
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
    print('\\caption{*: not yet launched, or in the worst case an error has occured. -: timeout reached. !: error }') 
    print('\\end{table}')


# now parsing the results of the available methods, this method should be modified, unless a new method is added
if __name__ == '__main__':

    parsers = mapParsersDynamic(methods)
    fcline, lcline = printTexHeadDynamic(methods, parsers)
    for dataset in os.listdir(project_flexics_data_dir):
        if dataset.endswith(".fimi"):
            first = True
            data_name = dataset.split('.')[0]
            if dataset in fthresholds:
                print('\\hline')
                count = 0
                for i in range(0, len(fthresholds[dataset])):
                    # absolute_threshold = int(math.ceil(float(fthresholds[filename][i]) * nbrTrans(absolute_dataset_file)))
                    count += 1
                    if first:
                        resline = data_name + ' & ' + fthresholds[dataset][i] + ' & ' + allSamples[dataset][i] + ' '
                        first = False
                    else:
                        resline = ' & ' + fthresholds[dataset][i] + ' & ' + allSamples[dataset][i] + ' '
                    for method in methods:
                        for j in range(0, len(error_tolerance)):
                            kappa = error_tolerance[j]
                            absolute_dataset_res_dir = os.path.abspath(os.path.join(project_res_dir, "Flexics", method, data_name))
                            
                            # resline += parsers[method]([], [data_name, absolute_dataset_res_dir, taskTODO, oracle, fthresholds[dataset][i].replace(".", "v"), constraintParameter, qualityMeasure, kappa.replace(".", "v"), allSamples[dataset][i], timeout])
                            resline += parsers[method]([], [data_name, absolute_dataset_res_dir, taskTODO, method.lower(), fthresholds[dataset][i].replace(".", "v"), constraintParameter, qualityMeasure, kappa.replace(".", "v"), allSamples[dataset][i], timeout])
                            
#                            print("\n")
                    
#                    print("\n\n")
                            
                    if count == len(fthresholds[dataset]):
                        print(resline, '\\\\\\hline')
                    else :
                        print(resline, '\\\\\\cline{' + str(fcline) + '-' + str(lcline) + '}')
                    
    printTexFoot()
