'''
Created on 12 avril 2020

@author: Arnold Hien

'''

from include import *
from datetime import date, datetime

def add(n):
    return n+1

def formatSolutions(absolute_dataset_temp_res_file, absolute_dataset_final_res_file):
    try:
        if (not os.path.exists(absolute_dataset_temp_res_file)):
            print("Error: needed results files for launching are missing!")
            sys.exit(1)
        
        all_solutions = ""
        
        with open(absolute_dataset_temp_res_file, "r") as lines:
            for line in lines:
                line = line.replace("\n", "")
                tab = line.split(";")
                
                pattern = tab[0]
                number = tab[1]
                
                if pattern == "":
                    all_solutions += "[  ] [ " + number + " ]\n"
                else:
                    # all_solutions += "[ " + ' '.join(map(str, sorted(set(map(add, map(int, set(pattern.split("+")))))))) + " ] [ " + number + " ]\n"
                    all_solutions += "[ " + pattern.replace("+", " ") + " ] [ " + number + " ]\n"
                
                #all_solutions += "[ " + ' '.join(map(str, sorted(set(map(add, map(int, set(pattern.split("+")))))))) + " ] [ " + number + " ]\n"
                # all_solutions += "[ " + line.replace("+", " ").replace(";", " ] [ ").replace(",", ".").replace("\n", "") + " ]\n"
            
        final_file = open(absolute_dataset_final_res_file,"w")
        final_file.write(all_solutions)
        final_file.close()
        
        print("***** final results written *****")
        
    finally:
        print("~~~~~ end ~~~~~")
    
if __name__ == '__main__':
    print("\nDate =", date.today(), "- Time =", datetime.now())
    absolute_dataset_temp_res_file = sys.argv[1]
    absolute_dataset_final_res_file = sys.argv[2]
    
    print("\n***********************************\n***********************************\n\n***** begin post processing *****\n")
    
    formatSolutions(absolute_dataset_temp_res_file, absolute_dataset_final_res_file)
    
    print("\n***** end of post processing *****\n")
    
