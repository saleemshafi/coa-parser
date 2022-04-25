import PyPDF2
import re
import os

def textBetween(before, after, text):
	splits = re.split(before, text)[:2] if before != None else [text]
	found = splits[-1]
	
	splits = re.split(after, found)[:2] if after != None else [found]
	found = splits[0]

	return found


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

def rezonings(minutes):
	# Extract the Public Hearings section
	pubHearingsExtract = textBetween(r'\s+[A-Z]\.\s+P\n?U\n?B\n?L\n?I\n?C\s+H\n?E\n?A\n?R\n?I\n?N\n?G\n?S\s*\n',
									 r'\n\s+[A-Z]\.\s+[A-Z ]+\s*\n',
									 minutes)

	namedSections = list()
	# Identify all of the numbered headings
	hNum = 1
	heading = None
	remainingText = pubHearingsExtract
	m = re.search('\s'+str(hNum)+'\.?\s+([a-zA-Z \-]+)(?::|\s*\n)', remainingText)
	while m != None:
		if heading != None:
			section = remainingText[:m.start()]
			namedSections.append(tuple((heading,section)))
		heading = m.groups()[0]
		print str(hNum)+":"+	heading
		remainingText = remainingText[m.end():]
		hNum = hNum + 1
		m = re.search('\s'+str(hNum)+'\.?\s+([a-zA-Z \-]+)(?::|\s*\n)', remainingText)
	if heading != None:
		namedSections.append(tuple((heading,remainingText)))

	# Select only the "Rezoning" sections
	return [x for x in namedSections if x[0] == 'Rezoning']


def extractRezoningData(filename, section):
	sectionText = section[1].encode('utf-8')
	parts = re.split(r'\n\s+\n', sectionText)
	parts = [x.replace('\n','') for x in parts]
	meta = parts[0]
	# Notes might not have everything as it's not always double spaced
	notes = "\n".join(parts[1:])

	# get ID
	caseNumber = re.findall(r'([\w-]+)', meta.split(' - ')[0])[0]

	district = textBetween(r'District\s+', '(?!\d+)\s', meta)

	# get address / watershed / NP area
	addressText = textBetween('Location:', 'Owner/Applicant', meta).strip()
	pieces = re.split('[,;]', addressText)
	npArea = None
	watershed = None
	for p in pieces[:]:
		if "NP Area" in p:
			npArea = p.strip()
			pieces.remove(p)
		if "Watershed" in p:
			watershed = p.strip()
			pieces.remove(p)
	address = ','.join(pieces)

 	# get owner / applicant
	ownerText = textBetween('Owner/Applicant:', 'Agent', meta).strip()


 	# get agent / agent firm
	agentText = textBetween('Agent:', 'Request', meta)
	agentFirm = textBetween(None, r'\(', agentText).strip()
	agent = textBetween(r'\(', r'\)', agentText).strip()

 	# get request
 	# try to pick this apart (from/to)
	requestText = textBetween('Request:', 'Staff Rec', meta)
	fromText = textBetween(None, r'[tT]o', requestText)
	fromText = textBetween(r'[fF]rom', None, fromText).strip()
	toText = textBetween(r'[tT]o', None, requestText).strip()

 	# get staff recommendation
	staffRecText = textBetween(r'Staff Rec\.?:', 'Staff', meta).strip()

 	# get staff info
	staffText = textBetween('Staff:', None, meta)
	staffName = staffText.split(',')[0].strip()

	if re.search(r'Department\s{2}', staffText):
		misplacedNotes = textBetween(r'Department\s{2}', None, staffText)
		staffText = staffText[:staffText.find(misplacedNotes)]
		notes = misplacedNotes + ' ' + notes

 	# try to pick out resolution from notes
 		# approved staff recommendation
 		# approved staff recommendation with conditions
 		# postponed
 	result = None
 	if re.search(r'postpone.*approved', notes):
 		result = 'Postponed'
 	if re.search(r'recommendation.*approved', notes):
 		result = 'Approved staff recommendation'
 	if re.search(r'recommendation.*approved.*with conditions', notes):
 		result = 'Approved staff recommendation with conditions'

 	return {
	 	"caseNumber": caseNumber,
	 	"district":	district,
	 	"fullAddressText": addressText, 
	 	"address":address, 
	 	"watershed":watershed,
	 	"npArea": npArea, 
	 	"fullOwnerText": ownerText, 
	 	"fullAgentText": agentText,
	 	"agentFirm": agentFirm,
	 	"agent": agent, 
	 	"fullRequestText": requestText, 
	 	"from": fromText,
	 	"to": toText,
	 	"staffRec": staffRecText, 
	 	"staff": staffText,
	 	"staffName": staffName, 
	 	"result": result,
	 	"notes": notes
 	}



DEBUG = 'Case Number: {}\n' \
	'Hearing Date: {}\n' \
	'Full Address Text: {}\n' \
	'Address: {}\n' \
	'District: {}\n' \
	'Watershed: {}\n' \
	'NP Area: {}\n' \
	'Owner: {}\n' \
	'Agent Text: {}\n' \
	'Agent Firm: {}\n' \
	'Agent: {}\n' \
	'Full Request Text: {}\n' \
	'From: {}\n' \
	'To: {}\n' \
	'Staff Recommendation: {}\n' \
	'Full Staff Text: {}\n' \
	'Staff: {}\n' \
	'Result: {}\n' \
	'\n' \
	'Notes:\n' \
	'{}\n'

csv = '"{}","{}","{}","{}","{}","{}","{}","{}","{}","{}","{}","{}","{}","{}","{}","{}"'
csvError = '"{}","{}"'

files = os.listdir('./minutes')
#files = ['document_D5D26F4D-BDCD-7E3E-4991993167E6872E.pdf']
files = ['document_D67C1715-0EDB-6250-35D8FAD253BCF779.pdf']

print '"File","Status","Date","Case Number","Address","District","Watershed","NP Area","Owner/Applicant","Agent Firm","Agent","From","To","Staff","Staff Recommendation","Result"'
for minutesFile in files:
#	try:
		minutes = textFromPDF('./minutes/'+minutesFile)

		date = textBetween('MINUTES', '(?!\s*\w+\s*\d{1,2}\s*,\s*\d{4}\s*)[a-zA-Z]', minutes).replace('\n', '').strip()
		rezoningSections = rezonings(minutes)
		if len(rezoningSections) == 0:
			print csvError.format(minutesFile, 'No Rezonings')
		else:
			for section in rezoningSections:
				try:
					data = extractRezoningData(minutesFile, section)
				except Exception as e:
					print csvError.format(minutesFile, 'Error')
				else:
				 	print csv.format(
				 		minutesFile,
				 		'Success',
					 	date,
					 	data["caseNumber"],
					 	data["address"], 
					 	data["district"],
					 	data["watershed"],
					 	data["npArea"], 
					 	data["fullOwnerText"], 
					 	data["agentFirm"],
					 	data["agent"], 
					 	data["from"],
					 	data["to"],
					 	data["staffName"], 
					 	data["staffRec"], 
					 	data["result"]
					)
#	except Exception as e:
#		print "Error in file: "+minutesFile
#		print e
