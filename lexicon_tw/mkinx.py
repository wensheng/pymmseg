#!/bin/env python

for i in range(2,9):
    fin = open("chr%d.lex"%i)
    fout = open("chr%d.inx"%i,'w')
    while 1:
        offset = fin.tell()
        line = fin.readline()
        if not line:
           break
        line = line.strip()
        length = len(line)
        counter = (length - 3) / (i*3-3)
        fout.write("%s%6d%3d\n"%(line[:3],offset,counter))
    fin.close()
    fout.close()
