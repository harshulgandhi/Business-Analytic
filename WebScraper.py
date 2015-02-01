from bs4 import BeautifulSoup
import re
import urllib

output = open("testoutput.txt","w")
csv_output = open("csv_output.txt","w")
home_url = "http://www.basketball-reference.com"
player_home_url = "http://www.basketball-reference.com/players/"


##To get href for individual letters
def getAlphabetLinks():
	global player_home_url
	print "Getting link to individual letter..\n"
	home_html = urllib.urlopen(player_home_url).read();
	soup = BeautifulSoup(home_html)
	get_alphabet_section = soup.find("div",{"id":"page_content"})
	i = 0
	links_list = get_alphabet_section.find_all('a',href=True) 
	for link in links_list:
		i+=1
		print link['href']
		if i == 25:
			break
	#href_url = get_alphabet_section.find_all('a')
	#print href_url['href']
	#output1 = open("testoutput1.txt","w")
	#output1.write(get_alphabet_section['href'])
	#output1.write(get_alphabet_section.__str__())
	print "Fetching ",i," urls done\n"
	return links_list



##To get payer basic profile information in tabular form. This
##table is not in csv format!
def getPlayerBasicInformation(link):
	global home_url
	url = home_url+link.__str__()
	print "\nCompiled URL is ",url,"\n"
	html = urllib.urlopen(url).read();
	soup = BeautifulSoup(html)
	player_table = soup.find("table",{"class":"sortable stats_table" })
	#print player_table.__str__()
	#output.write(player_table.__str__())
	get_rows = player_table.find_all('tr')
	get_rows_custom = []
	#print get_rows[0].__str__()

	##Getting only the rows where name is "<Strong>"
	needle = "<strong>"
	for i in range(len(get_rows)):
		if(re.search(needle,get_rows[i].__str__()) or i == 0):
			get_rows_custom.append(get_rows[i])

	##
	'''
	print "get_rows_custom : "
	print get_rows_custom
	print "type(get_rows_custom) : " 
	print type(get_rows_custom)
	'''
	
	all_data = []
	all_text = []
	for each_row in get_rows_custom:
		text = ''.join(each_row.find_all(text=True))
		single_row = (each_row.find_all(text=True))
		all_data.append(text)
		
	#print all_rows[1]
	#output.write(all_data.__str__())
	#tableToCSV(all_data)
	return all_data,link.__str__()


#Function to parse table into CSV format
def tableToCSV(all_data,link):
	print "Converting table to CSV...\n"
	needle="/(.?)/"
	result = re.search(needle,link)
	alphabet = result.group(1)
	nameOfFile = "csv_output_for_"+alphabet+".txt"
	csv_output = open(nameOfFile,"w")
	table_data=""
	tableSize = len(all_data)
	for i in range(0,tableSize,1):
		row_len = len(all_data[i])
		for j in range(1,row_len,1):
			if all_data[i][j].__str__()!='\n':
				table_data = table_data + all_data[i][j]
			else:
				table_data = table_data + ","
				
		csv_output.write(table_data)	
		csv_output.write("\n")
		table_data=""

	print "CSV table for profile information of players whose name begin with '",alphabet,"'is ready\n"


############# MAIN PROGRAM ################
links_list = getAlphabetLinks()
i = 0
for link in links_list:
	if(i==25):
		break
	all_data,link1 = getPlayerBasicInformation(link['href'])
	tableToCSV(all_data,link1)
	i+=1

print "Players basic information saved!!"

