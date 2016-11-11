
# Made by Joo Yejin
# jinn0525@gmail.com
# 16.08.16

# Configuration:
# There must be in present directory: directory 'MOSS' and 'Static Analysis'.
# In 'MOSS': There are moss.pl, this(moss_auto.py)
# In 'Static Analysis': There are input files' category folder

# Notice: You need BeautifulSoup.
# Download Here https://www.crummy.com/software/BeautifulSoup/bs4/download/4.4/

import os, sys, csv, string, urllib
from bs4 import BeautifulSoup


def runmoss(path0, path1, wset0, wset1, category0, category1):
	sys.stdout.write(' >> MOSS is running')
	category0 = str(category0)
	category1 = str(category1)
	res_filename = 'result_moss_' + category0 + '_' + category1 + '_report.txt'
	res_filename = str(res_filename)
	for i in wset0:
		file0 = path0 + '\\' + i
		file0 = str(file0)
		for j in wset1:
			sys.stdout.write('.')
			file1 = path1 + '\\' + j
			file1 = str(file1)
			os.system('perl ./moss.pl -m 100000 ' + file0 + ' ' + file1 + '>> ' + res_filename)
	print 'Done.'
	
	return res_filename


def extract_url(res_filename):
	sys.stdout.write(' >> Extracting URL')
	moss_report_file = res_filename
	wfilename = 'extract_url_' + moss_report_file
	fw = open(wfilename, 'w')
	fr = open(moss_report_file, 'r')

	while True:
		line = fr.readline()
		if not line:
			break
		if (line.find('http://') != -1):
			sys.stdout.write('.')
			fw.write(line)

	fw.close()
	fr.close()
	print 'Done.'

	return wfilename


def count_line(wset1):
	fileset = wset1
	javafline = {}

	for member in fileset:
		member = str(member)
		count = 0
		fr = open(member, 'r')

		while True:
			line = fr.readline()
			count = count + 1
			if not line:
				break

		javafline[member] = count
		fr.close()

	return javafline


def make_csv(res_filename, wfilename, javafline):
	sys.stdout.write(' >> Making csv file')
	fr_url = open(wfilename, 'r')
	category = res_filename.split('_')

	del category[0]
	del category[0]
	category[0] = str(category[0])
	category[1] = str(category[1])
	# category[0] = first category
	# category[1] = second category

	while True:
		sys.stdout.write('.')
		url = fr_url.readline()
		if not url:
			break
		html = urllib.urlopen(url)
		soup = BeautifulSoup(html,"html.parser")
		data = soup.find_all("td", class_=None)
		csvlist = []

		for member in data:
			if data.index(member) > 1:
				break;
			index = data.index(member)
			member = str(member)
			tmp_list = member.split('\\'+ category[index] +'\\')
			tmp = tmp_list[1]
			tmp = str(tmp)
			tmp_list = tmp.split(' (', 1)
			tmp_list[0] = str(tmp_list[0])
			csvlist.append(tmp_list[0])
			csvlist.append(javafline[tmp_list[0]])
			tmp = tmp_list[1]
			tmp = str(tmp)
			tmp_list = tmp.split(')', 1)
			tmp_list[0] = str(tmp_list[0])
			csvlist.append(tmp_list[0])
			
		csvfilename = res_filename.split('.')
		csvfilename = csvfilename[0]
		csvfilename = str(csvfilename)
		csvfilename2 = csvfilename + '2'
		with open('./' + csvfilename + '.csv', 'a') as csvfile:
			writer = csv.writer(csvfile, delimiter = ',')
			writer.writerow(csvlist)
	wfilename = str(wfilename)
	os.remove(res_filename)
	os.remove(wfilename)

	print 'Done.'


def main():
	os.chdir('..')
	pwd = os.getcwd()
	os.chdir(pwd + '\\StaticAnalysis')
	pwd = os.getcwd()
	category = os.listdir(pwd)
	category_line = []

	for member in category:
		os.chdir(member)
		wset = os.listdir('./')
		category_line.append(count_line(wset))
		os.chdir('..')

	for member0 in category:
		for member1 in category:
			f = raw_input(' It will compare category ' + str(member0) + ' and ' + str(member1) + '. Continue?(Yes/No/eXit) ')
			if (f == 'Y' or f == 'y'):
				os.chdir(member0)
				path0 = os.getcwd()
				wset0 = os.listdir('./')
				os.chdir('..')
				os.chdir(member1)
				path1 = os.getcwd()
				wset1 = os.listdir('./')
				os.chdir('..')
				os.chdir('..')
				os.chdir('MOSS')
				pwd = os.getcwd()
				res_filename = runmoss(path0, path1, wset0, wset1, member0, member1)
				wfilename = extract_url(res_filename)
				make_csv(res_filename, wfilename, category_line[category.index(member1)])
				os.chdir('..')
				os.chdir('StaticAnalysis')
			elif (f == 'N' or f == 'n'): 
				break;
			else: 
				print "Invalid input."
		
		if (f == 'N' or f == 'n'):
			break;
		else:
			break;

	print "Good Bye."

if __name__ == '__main__':
	main()
	sys.exit(0)