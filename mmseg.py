#!/bin/env python

import sys
import os

lexpath = os.path.join(os.path.dirname(os.path.realpath(__file__)),'lexicon_cn')
cjkc = 0
ncjk = 0
cjkword = 0
lexicon = []

def load_lexicon():
	for i in range(2,9):
		fin = open("%s/chr%d.lex"%(lexpath,i))
		lexicon.append({'head':[],'body':[]})
		for line in fin:
			line = line.strip()
			lexicon[-1]['head'].append(line[:3])
			lexicon[-1]['body'].append([])
			for j in range(3,len(line),i*3-3):
				lexicon[-1]['body'][-1].append(line[j:j+i*3-3])
		fin.close()

def segment(chunk):
	global cjkword
	i = 0
	segs = []
	len_chunk = len(chunk);
	while i*3 < len_chunk:
		if len_chunk/3-i < 8:
			l = len_chunk/3 - i
		else:
			l = 8
		longest = 0
		if l>1:
			for j in range(l,1,-1):
				head = chunk[i*3:i*3+3]
				#print("j=%d try %s as head"%(j,head))
				if head in lexicon[j-2]['head']:
					idx = lexicon[j-2]['head'].index(head)
					body = chunk[i*3+3:i*3+j*3]
					#print("test %s as body"%(body))
					if body in lexicon[j-2]['body'][idx]:
						longest = j
						break
			if longest:
				#print("---- Found longest=%d"%longest)
				segs.append(chunk[i*3:i*3+longest*3])
				i += longest
			else:
				segs.append(chunk[i*3:i*3+3])
				i += 1
		else:
			segs.append(chunk[i*3:i*3+3])
			i += 1
		cjkword += 1

	return segs

def chunk_and_segment(file,line):
	global cjkc, ncjk
	i = 0
	lenl = len(line)
	chunk = ""
	has_chunk = False;
	while i<lenl:
		if line[i] >= '\xe4' and line[i] <= '\xe9':
			cjkc += 1
			chunk = "%s%s"%(chunk,line[i:i+3])
			has_chunk = True
			i += 3
		else:
			ncjk += 1
			if line[i] < '\x80':
				buf = line[i]
				i += 1
			elif line[i] < '\xc0':
				print("Oops: this's not a UTF8 file, bail!")
				sys.exit()
			elif line[i] < '\xe0':
				buf = line[i:i+2]
				i += 2
			else:
				buf = line[i:i+3]
				i += 3
			if chunk:
				file.write(" %s "%" ".join(segment(chunk)))
			file.write(buf)
			chunk = ''
	if chunk:
		file.write(" %s "%" ".join(segment(chunk)))

	
if __name__ == '__main__':
	if len(sys.argv) != 3:
		print "mmseg.py input output"
		sys.exit()

	load_lexicon()
	fin = open(sys.argv[1])
	fout = open(sys.argv[2],'w')
	for line in fin:
		line=line.strip()
		chunk_and_segment(fout,line)
		fout.write('\n')
	fin.close()
	fout.close()

	print("cjk characters = %d"%cjkc)
	print("non-cjk characters = %d"%ncjk)
	print("cjk words = %d"%cjkword)
	if cjkword:
		print("Average cjk word length = %f"%(cjkc/float(cjkword)))

