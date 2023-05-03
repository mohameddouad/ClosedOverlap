"""
Created on Fri Mar 13 17:10:07 2020

@author: hien
"""

from include import *

def loadPatterns(absolute_patterns_filename, all_info=False):
    descriptions = []
    coverages = []
    witness = []
    ub_jac_lb = []
    with open(absolute_patterns_filename, "r") as infile:
        for line in infile:
            blocks = re.findall('\[(.*?)\]', line)
            assert(len(blocks) == 4)
            if len(blocks[1].strip()) != 0:  # avoid loading empty set
                descriptions.append(blocks[1].strip().split(" "))
                # we should start from index 0 instead of index 1 that is provided in the file
                coverage = []
                for t in blocks[2].strip().split(" "):
                    coverage.append(str(int(t) - 1))
                coverages.append(coverage)
                witness.append(int(blocks[0]))
                ub_jac_lb.append(blocks[3].strip().split(" "))
    if all_info:
        return descriptions, coverages, witness, ub_jac_lb
    else:
        return descriptions, coverages

def jaccard(a, b):
    '''
    a and b are two lists
    '''
    # intersection
    cap = 0
    for e in a:
        if e in b:
            cap += 1
    # union
    cup = len(a)
    for e in b:
        if e not in a:
            cup += 1
    assert(cup != 0);
    return cap / cup;

# intra-cluster similarity
def ics(coverages):
    res = 0;
    for i in range(0, len(coverages)):
            j = i + 1
            while j < len(coverages):
                res += jaccard(coverages[i], coverages[j])
                j += 1
    return res/len(coverages)

def write_final_results(outputFile, quality):
    with open(outputFile, 'w') as f:
        f.write(quality+"\n")
        
    print("*** quality evaluation finished ***")

# inter-cluster dissimilarity
def icd(coverages):
    res = 0;
    for c1 in range(0, len(coverages)):
        for tc1 in coverages[c1]:
            c2 = c1 + 1
            while c2 < len(coverages):
                for tc2 in coverages[c2]:
                    res += (1 - jaccard(tc1, tc2));
                c2 += 1
    return res / ncr(len(coverages), 2)

if __name__ == '__main__':
    resultsFile = sys.argv[1]
    qualityFile = sys.argv[2]
    
    print("\n######################################################")
    print("########## New diversity quality evaluation ##########")
    
    val = "[ " + filename.split('.')[0] + " ] [ " + threshold + " " + jmax + " ] "        
    descriptions, coverages = loadPatterns(resultsFile)
    
    val_ics = ics(coverages)
    val_icd = icd(coverages)
    
    val += "[ " + str(val_ics) + " " + str(val_icd) + " ]"
    
    write_final_results(qualityFile, val)
    print("\n########## END ##########\n")
    
