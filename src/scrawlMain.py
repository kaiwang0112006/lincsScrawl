# -*- coding: utf-8 -*-
import argparse
import csv
from subprocess import Popen, PIPE

##########################################
## Options and defaults
##########################################
def getOptions():
    parser = argparse.ArgumentParser(description='python *.py [option]"')
    requiredgroup = parser.add_argument_group('required arguments')
    requiredgroup.add_argument('--in', dest='input', help='input file', default='', required=True)
    requiredgroup.add_argument('--str', dest='str', help='all structure file to embide the smiles', default='', required=True)

    args = parser.parse_args()

    return args

##########################################
## Master function
##########################################           
def main():
    options = getOptions()
    structure = {}
    data = []
    with open(options.str) as fin:
        fcsv = csv.reader(fin)
        for eachline in fcsv:
            if fcsv.line_num == 1:
                continue
            structure[eachline[0]] = eachline[12] 
    
    with open(options.input) as fin:
        fcsv = csv.reader(fin)
        for eachline in fcsv:
            if fcsv.line_num == 1:
                continue
            link = eachline[-1]
            id = eachline[-1].split('/')[-2]

            cmd = "curl -H \"Accept: text/csv\" http://lincs.hms.harvard.edu/db/api/v1/datasetdata/%s/ > %s.csv" % (id,id)
            dataset = "%s.csv" % id
            
            p = Popen(cmd, stdout=PIPE, stderr=PIPE,shell=True)
            stdout, stderr = p.communicate()
            
            try:
                with open(dataset) as fdata:
                    datacsv = csv.reader(fdata,quotechar='"')
                    for eachline in datacsv:
                        if datacsv.line_num == 1:
                            title = eachline
                            continue
                        if eachline[5] == '200122':
                            smid = "%s-%s" % (eachline[9], eachline[8])
                            eachline.append(structure[smid])
                            data.append(eachline)
            except:
                print 'error read file %s' % dataset
    title.append('smiles')
    with open('result.csv', 'wb') as csvout:
        csvwriter = csv.writer(csvout, delimiter=',',quotechar='"', quoting=csv.QUOTE_MINIMAL)
        csvwriter.writerow(title)
        csvwriter.writerows(data)
                    
            
            
            
            
            
        
    
if __name__ == "__main__":
    main()