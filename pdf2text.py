import PyPDF2
import re
import os
import codecs


def textFromPDF(filename):
	pdfFile = open(filename,'rb')
	pdfReader = PyPDF2.PdfFileReader(pdfFile)
	numPages = pdfReader.numPages
	output = ""

	for i in range(numPages):
		page = pdfReader.getPage(i)
		output += page.extractText()
	output = output.replace('\u2122', '\'')
	return output





folder = './coa_scraper/downloads/full/'
files = os.listdir(folder)

for file in files:
	if "txt" in file:
		continue
	newFilename = folder+file+".txt"
	if os.path.exists(newFilename):
		pass
	else:
		with codecs.open(newFilename, mode='w',encoding='utf8') as f:
			text = textFromPDF(folder+file)
			f.write(text)
