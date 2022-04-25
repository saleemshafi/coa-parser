import pdfminer
import pdfminer.high_level
import os
import codecs


def textFromPDF(filename):
	text = pdfminer.high_level.extract_text(filename)
	return text


folder = './coa_scraper/downloads/full/'
files = os.listdir(folder)

for file in files:
	if "txt" in file:
		continue
	newFilename = folder+"txt3/"+file+".txt"
	if os.path.exists(newFilename):
		pass
	else:
		with codecs.open(newFilename, mode='w',encoding='utf8') as f:
			text = textFromPDF(folder+file)
			f.write(text)
