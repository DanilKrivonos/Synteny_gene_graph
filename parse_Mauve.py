import pandas as pd
import argparse
import sys
import numpy as np
import os
from os.path import splitext 
from os.path import split
from pyteomics.fasta import read

parser = argparse.ArgumentParser(description='Parsing of Mauve')
parser.add_argument('-backbone', 
    type=str, 
    help='backbonefile', 
    required=True
    )
parser.add_argument('-save_way', 
    type=str, 
    help='Saveway', 
    required=True
    )
parser.add_argument('-orgs', 
    type=str, 
    help='Strain path', 
    default=None
    )
parser.add_argument('-out', 
    type=str, 
    help='Output file of Mauve', 
    default=None
    )
parser.add_argument('-data_type', 
    type=str, 
    help='If fold or file', 
    default='file'
    )
args = parser.parse_args()


if args.data_type == 'file':
    A = np.array(pd.read_csv(args.backbone, sep='\t'))

    S=[]
    for i in range(0, A.shape[1], 2):
        S.append(A[:,i:i+2].tolist())
    S = np.array(S, dtype=np.float64)

    S[S==0] = np.inf
    S = np.abs(S)
    S = S.tolist()

    for org in S:
        for ind in range(len(org)):
            org[ind] += [ind]

    for i in S:
        i.sort()
    
    NS = np.array(S)
    OrgMax = []
    for org in NS:
        sliceS = org[:,:2]
        sliceS[sliceS == np.inf] = 0
        lens = sliceS[:, 1] - sliceS[:, 0]
        maxlen = int(np.abs(np.max(lens)))
        OrgMax.append(maxlen)
    maxlen = max(OrgMax)

    node = []
    edges = ''
    if args.out != None:  
        current_org = 0
    else:
        current_org = 1

    #list of strains
    if args.out != None:  
        strains = []
        path = open(args.out)
        for line in path:
            if line[: 9] != 'terminate':
                if line[: 3] == '../':
                    strains.append(split(splitext(splitext(line)[0])[0])[1])
            else:
                break

    print('Making file ...')
    for org in S:
        print('Analyzing of microorganism ...')
        for n in range(len(org)-1):
            if org[n][0] == float('inf') or org[n+1][0] == float('inf'):
                continue
            startnode = int(org[n][2])
            endnode = int(org[n+1][2])
            len1 = int(abs(org[n][1] - org[n][0]))
            len2 = int(abs(org[n+1][1] - org[n+1][0]))
            
            if org[n][0] < 0:
                strand = '-'
            else:
                strand = '+'
            if not len1 == 0 or len2 == 0:
                if args.out != None:
                    edges += 'sb{}\tsb{}\t{}\t{}\t{}\t{}\n'.format(
                        startnode, 
                        endnode, 
                        strains[current_org], 
                        int(org[n][0]), 
                        int(org[n][1]), 
                        maxlen
                        )
                else:
                    edges += 'sb{}\tsb{}\tg{}\t{}\t{}\t{}\n'.format(
                        startnode, 
                        endnode, 
                        current_org, 
                        int(org[n][0]), 
                        int(org[n][1]), 
                        maxlen 
                        )

        current_org += 1
        
    savefile = open(args.save_way + '.txt', 'w')
    savefile.write('Strat_LCB\tNext_LCB\tStrain\tStart_coordinate\tEnd_coordinate\tLength_of_the_largest_LCB\n')
    savefile.write(edges)
    savefile.close()
    print('Finish!')
elif args.data_type == 'fold':
    path = os.listdir(args.backbone)
    for microorganism in path:
        #Change path if you have enother
        if '_result' in microorganism:
            A = np.array(pd.read_csv(args.backbone + microorganism + '/' + microorganism[: -8] +'_backbone' , sep='\t'))

            S=[]
            for i in range(0, A.shape[1], 2):
                S.append(A[:,i:i+2].tolist())
            S = np.array(S, dtype=np.float64)

            S[S==0] = np.inf
            S = np.abs(S)
            S = S.tolist()

            for org in S:
                for ind in range(len(org)):
                    org[ind] += [ind]

            for i in S:
                i.sort()
            
            NS = np.array(S)
            OrgMax = []
            for org in NS:
                sliceS = org[:,:2]
                sliceS[sliceS == np.inf] = 0
                lens = sliceS[:, 1] - sliceS[:, 0]
                maxlen = int(np.abs(np.max(lens)))
                OrgMax.append(maxlen)
            maxlen = max(OrgMax)

            node = []
            edges = ''
            if args.out != None:  
                current_org = 0
            else:
                current_org = 1

            #list of strains
            if args.out != None:  
                strains = []
                #Change path if you have enother
                path = open(args.out + microorganism + '/' + microorganism[: -8] +'.out')
                for line in path:
                    if line[: 9] != 'terminate':
                        if line[: 3] == '../':
                            strains.append(split(splitext(splitext(line)[0])[0])[1][: -8])
                    else:
                        break
            
            orgs = os.listdir(args.orgs)
            for org in orgs:
                if org in microorganism:
                    way = args.orgs + org + '/All/'
                    stars = os.listdir(way)

            print('Making file ...')
            print('Analyzing of {} ...'.format(microorganism[: -8]))

            strand = ''
            for org in S:
                print('Analyzing of {} ...'.format(strains[current_org]))
                for n in range(len(org)-1):
                    if org[n][0] == float('inf') or org[n+1][0] == float('inf'):
                        continue
                    startnode = int(org[n][2])
                    endnode = int(org[n+1][2])
                    len1 = int(abs(org[n][1] - org[n][0]))
                    len2 = int(abs(org[n+1][1] - org[n+1][0]))
                    if org[n][0] < 0:
                        strand = '-'
                    else:
                        strand = '+'
                    if not len1 == 0 or len2 == 0:
                        if args.out != None:
                            edges += 'sb{}\tsb{}\t{}\t{}\t{}\t{}\n'.format(
                                startnode, 
                                endnode, 
                                strains[current_org], 
                                int(org[n][0]), 
                                int(org[n][1]), 
                                maxlen
                                )
                        else:
                            edges += 'sb{}\tsb{}\tg{}\t{}\t{}\t{}\n'.format(
                                startnode,
                                endnode, 
                                current_org, 
                                int(org[n][0]), 
                                int(org[n][1]), 
                                maxlen
                                )
                current_org += 1

            print('{} was done!'.format(microorganism[: -8]))        
            savefile = open(args.save_way + microorganism + '/' + microorganism[: -8] + '.txt', 'w')
            savefile.write('Strat_LCB\tNext_LCB\tStrain\tStart_coordinate\tEnd_coordinate\tLength_of_the_largest_LCB\n')
            savefile.write(edges)
            savefile.close()
else:
    print('Unsupportable format :(')

print('Done!')