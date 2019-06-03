import requests, re,csv,sys,html

class SCC:
	
	def __init__(self):
		
		self.caseURLs = "french_scc_links.csv" #local filepath of input file
		#self.queryURL = "https://www.canlii.org/en/ca/scc/doc/"
		
		#Web server root path where SCC decisions (html files) are stored. Change to your path.
		self.queryURL = "http://127.0.0.1:8082/html/SCC/ExportArchives/Documents/"

		self.outRows=[]

	def scrapeCanLII(self):
		
		outRows = self.outRows
		outRows.append(['Citation','Case','Date','filePath'])

		with open(self.caseURLs, newline='') as csvfile:#reading input file row by row
			readCSV = csv.reader(csvfile)
			
		
			for row in readCSV:
				date = (row[1])
				title = (row[0])
				fileName= (row[2])
				scc = self.queryURL+fileName
			
				print("processing title "+title)#logging line
					
				try:
					readHtml=requests.get(scc)
					print("read scc page")
					body = readHtml.content.decode('utf-8')
					body = body.replace('\r',' ')
					body = body.replace('\n',' ')
					
					#convert html entities
					body = html.unescape(body)
					
					
					#create local copies of the html pages as backup for later use if needed
					#with open(backup, 'w',encoding='utf8') as file:
						#file.write(body)
					
					#Grab 'authors cited' section of French cases
					print("trying to capture citation text now")
					matchCites = re.search(r"<B>Doctrine.et.autres(.*?)margin-bottom:24.0pt.*?>.*?POURVOI",body)

					if matchCites:
						authorsCited = matchCites.group(1)
						parseCites = re.compile(r'line-height:normal.*?>(.*?)</P>',re.I)#pattern for individual citation
						
						for match in parseCites.finditer(authorsCited):
							#NOW STRIP OUT RESIDUAL HTML BY LOOKING FOR "<.*?>" PATTERNS
							cleanCite = re.sub(r'<.*?.>','',match.group(1))
							outRows.append([cleanCite,title,date,fileName])
							
					else:
						outRows.append(["No Authors Cited section found",title,date,fileName])
					
				except requests.exceptions.RequestException as e:  #handle errors when scraping
					print (e)
					sys.exit(1)

						
				print("Moving to next case now.")
			
			self.outRows = outRows
			print("That's all. We're done processing rows.")
			
			self.writeCSV()

	
	def writeCSV(self):
		outRows = self.outRows
		escape_row = []
		print('Trying to write all rows to file now.')

		with open('scc_french_citations.csv', 'w', newline='',encoding='utf_8_sig') as output:#data found will write to this file
			writer = csv.writer(output)
						
			for row in outRows:
				try:
					writer.writerow(row)
				except:
					escape_row.extend((row[0],'',row[2]))
					print("Error writing this record to file: ",row[2])
					writer.writerow(escape_row)
					escape_row = []
					
		

		
getCites = SCC()
getCites.scrapeCanLII()

