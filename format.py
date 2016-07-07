#!/usr/bin/env python
import sys
import os.path
import re

#asbasdas
def print_lines(n,y,data,outfile,base_year,categories):
	"""Add one section of numbers to .frmt file.

	Args:
		n: integer representing line in data file
		y: integer representing current year - base_year
		data: list of (string) lines in .out file
		outfile: .frmt file to write to
		base_year: integer first year simulation is run on
		categories: integer number of categories to consider
	"""

	frmt_data = []
	#get correct data/lines and remove extra characters
	for i in range(n,n+6):
		data[i] = data[i].replace('. ', '') 
		data[i] = data[i].replace('.\n','')
		#this is for CVD prevalence -- don't want 'x/y' just want rate
		data[i] = re.sub(r'[0-9]*./ \s*[0-9]*','',data[i])
		frmt_data += [s for s in data[i].split()]
	outfile.write(str(base_year + y))
	line = []
	#get data in correct order
	for i in range(categories*2):
		for j in range(6):
			line.append(frmt_data[i + (categories*2 + 1)*j + 1])
	into = '{:>12} ' + '{:>15} '*(12*categories-1) 
	outfile.write(into.format(*line) + "\n")


def setup(title,categories):
	"""Wrapper for creating .frmt file.

	Used for default formats -- two categories with
	Age/Sex and CHD incedence rate or one category
	which is Age/Sex Breakdown

	Args:
		title: label to look for e.g. "NEW CHD CASES"
		categories: integer number of categories to look for
	"""

	outfile.write(title + '\n')
	outfile.write('Year')
	into = '{:>12} ' + '{:>15} '*(12*categories-1)
	topline_f = []
	for i in range(categories):
		topline_f += topline
	outfile.write(into.format(*topline_f) + "\n")
	with open(sys.argv[1] + ".out", 'r') as myfile:
		data = myfile.readlines()
	i = 0
	years = 0
	base_year = int(data[9])
	for line in data:
		#find CORRECT title (e.g. not title + ' rate %' or 'Acute ' + title)
		if (line.find(title + "     ") != -1 or 
			line.find(title + "\n") != -1 and 
			line.find("Acute " + title) == -1): 
			#sections with >1 category have 7 lines before the numbers
			if categories != 1:  
				print_lines(i+7, years,data,outfile,base_year,categories)
			#sections with 1 category have 6 lines before numbers
			else:
				print_lines(i+6, years,data,outfile,base_year,categories)
			years += 1
		i+=1
	outfile.write("\n")


def setup2(title,categories,ctg_list,linesdown):
	"""Wrapper for creating .frmt file.

	Args:
		title: label to look for e.g. "NEW CHD CASES"
		categories: integer number of categories to look for
		ctg_list: list of string titles of categories (len(ctg_list)=categories)
		linesdown: integer number of lines below title to look for numbers
	"""
	outfile.write(title + '\n')
	topline_f = []
	into = '{:>12} ' + '{:>15} '*(12*categories-1)
	for i in range(categories):
		topline_f += topline
	line2 = '    {:>12}' + '{:>192}'*(categories-1)
	outfile.write(line2.format(*ctg_list) + "\n")
	outfile.write('Year')
	outfile.write(into.format(*topline_f) + "\n")
	with open(sys.argv[1] + ".out", 'r') as myfile:
		data = myfile.readlines()
	i = 0
	years = 0
	base_year = int(data[9])
	for line in data:
		#if we find CORRECT title (e.g. not title + ' rate %')
		if (line.find(title + "     ") != -1 or 
			line.find(title + "\n") != -1):
			print_lines(i+linesdown, years,data,outfile,base_year,categories)
			years += 1
		i+=1
	outfile.write("\n")


topline = ['M35-44',   'M45-54',   'M55-64',   'M65-74',   'M75-84',   'M85-94',   
			'F35-44',   'F45-54',   'F55-64',   'F65-74',   'F75-84',   'F85-94']

if not os.path.isfile(sys.argv[1] + ".out"):
	print("Invalid File Name")
	sys.exit()
fname = sys.argv[1] + ".frmt"
outfile = open(fname,'w')

setup("NEW CHD CASES",2)
setup2("CVD PREVALENCE - first of year",1,["Prevalence"],2)
setup("NEW INTERVENED CHD CASES",2)
setup2("NUMBER TREATED",2,["DE","DH"],4)
setup("CHD DEATHS",2)
setup("CHD Deaths (Bridge)",3)
setup("Acute CHD Death 11-17",3)
setup("Acute CHD Death 1-10",3)
setup2("Acute CHD Deaths (Bridge & DH)",3,["Arrest","MI","Revasc"],4)
setup2("Acute CHD Deaths (Bridge)",3,["MI","Arrest In-Hospital","Arrest Pre-Hospital"],4)
setup("Chronic CHD Death",3)
setup("Non-CVD Death",2)
setup("Non-CVD Death (DE)",3)
setup("DE Intervened Non-CVD Deaths", 3)
setup("Non-CVD Death (DH)",3)
setup("Total Pop (DE)",1)
setup("Total Pop (DH 11-17)",1)
setup("Total Pop (DH 1-10)",1)
setup("Total DE Diabetes Pop",1)
setup("NEW DIABETES CASES",2)
setup2("CVD EVENTS", 4, ["ANGINA", "ARREST", "MI", "STROKE"],17)
setup2("Revascularization Events",4,["AMI CABG","AMI PTCA","ISO CABG","ISO PTCA"],4)
setup2("CVD POPULATION DISTRIBUTION BY STATE",4,["ANGINA","REVSC","MI","TBD"],4)
setup2("CVD POPULATION DISTRIBUTION BY STATE",4,["REVSC + MI","TBD","TBD","TBD"],15)
setup2("CVD POPULATION DISTRIBUTION BY STATE",4,["TOT/ISC","MT+STROKE","BRIDGE MI","BRIDGE MI + ARR"],26)
setup2("CVD POPULATION DISTRIBUTION BY STATE",4,["BRIDGE ARREST","BRIDGE ANGINA","BRIDGE MI + REVSC","BRIDGE TOT STROKE"],37)
setup2("CVD POPULATION DISTRIBUTION BY STATE",1,["BRIDGE HEM STROKE"],48)
setup("Total MI",1)
setup("Bridge MI",1)
setup("DH First MI (1,2,14)",1)
setup("First MI",1)
setup("Total MI",1)
setup("DH 2nd MI (11,12,15, and dhxevt)",1)
setup("DH Re-MI (3-8,11-13,15)",1)
setup("DH MI Stroke (9,10,16,17)",1)
setup("TOTAL STROKE",2)
setup("BRIDGE STROKE",2)
setup("NEW INTERVENED STROKE CASES",2)
setup("First Stroke (DH ONLY)",2)
setup("STROKE DEATHS",2)
setup("TOTAL DEATHS",2)
setup2("NON-CVD Costs",1,["BACKGROUND HEALTHCARE COST"],5)
setup2("TOTAL CHD COSTS",1,["Age/Sex Breakdown($)"],12)
setup2("TOTAL PREVENTION COSTS",1,["Age/Sex Breakdown($)"],6)
setup2("TOTAL STROKE COSTS",1,["Age/Sex Breakdown($)"],5)
setup2("Total QALY",1,["Age/Sex Breakdown"],6)
setup2("Total DH QALY",1,["Age/Sex Breakdown"],6)