from bs4 import BeautifulSoup
import re
import urllib
import os
import time

#output = open("testoutput.txt","w")
#csv_output = open("csv_output.txt","w")
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
	player_table = soup.find("table",{"class":"sortable stats_table" }) 	#reading the players table
	#print player_table.__str__()
	#output.write(player_table.__str__())
	get_rows = player_table.find_all('tr')		#Getting individual rows
	get_rows_custom = []
	player_page_url=[]
	#print get_rows[0].__str__()

	##Getting only the rows where name is "<Strong>"
	needle_0= "<strong>"
	needle_1= '<a href="(/players/.*)">'
	for i in range(len(get_rows)):
		if(re.search(needle_0,get_rows[i].__str__()) or i == 0):		#Looking for rows containing "strong" tag
			if i > 0:
				haystack = get_rows[i].__str__()
				result = re.search(needle_1,haystack)
				player_page_url.append(result.group(1))
				print "****Fetching information for player with page: ",result.group(1)				#This gives individual player url
				indvPlayerStats(result.group(1))			#Function call to read, parse and save individual player's data
			get_rows_custom.append(get_rows[i])
			#output.write(get_rows_custom.__str__())

	all_data = []
	all_text = []
	for each_row in get_rows_custom:
		text = ''.join(each_row.find_all(text=True))
		#print player_url[0]
		single_row = (each_row.find_all(text=True))
		all_data.append(text)
		
	#print all_rows[1]
	#output.write(all_data.__str__())
	#tableToCSV(all_data)
	return all_data,link.__str__()


#Function to parse table into CSV format
def tableToCSV(all_data,link):
	print "Converting table to CSV...\n"
	path = '/basic profile'
	needle="/(.?)/"												#Getting alphabet for which tables is being converted
	result = re.search(needle,link)
	alphabet = result.group(1)
	nameOfFile = os.path.join("basic profile/","csv_output_for_"+alphabet+".txt")
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





##### Reading individual player's page and saving all stats#####
def indvPlayerStats(rel_link):
	
	particular_player_url = home_url+rel_link	
	needle_3='/players/(.?)/(.*).html'
	res = re.search(needle_3,rel_link)
	player_name=res.group(2)
	#particular_player_url="http://www.basketball-reference.com/players/m/machasc01.html"

	#player_name="acyqu01"
	#particular_player_url = "http://www.basketball-reference.com/players/a/acyqu01.html"

	player_html = urllib.urlopen(particular_player_url).read();
	soup1 = BeautifulSoup(player_html)
	print "Reading page"
	get_stat_tables = soup1.find_all("div",{"class":"stw"})

	#testoutput2 = open("testoutput2.txt","w")
	#testoutput2.write(get_stat_tables.__str__())
	needle_2 = '<div class="stw" id="(all_.*)">'

	#testoutput3 = open("testoutput3.txt","w")
	#csv_output1=open("stat_csv_table.txt","w")

	result = re.findall(needle_2,get_stat_tables.__str__())			#List of all tables on this page
	for i in range(len(result)):
		print "****Fetching table",result[i],"****"
		table_data=""
		stat_table_data=[]
		ind_table = soup1.find("div",{"id":result[i]})			#result[i] is the table name 'all_*'
		#testoutput3.write(ind_table.__str__())
		get_rows = ind_table.find_all('tr')
		for each_row in get_rows:
			text = ''.join(each_row.find_all(text=True))
			stat_table_data.append(text)
		filename= "player_stat_"+player_name+"_"+result[i]+".txt"
		csv_stat_output = open(filename,"w")
		tableSize = len(stat_table_data)
		for i in range(0,tableSize,1):
			row_len = len(stat_table_data[i])
			for j in range(1,row_len,1):
				if stat_table_data[i][j].__str__()!='\n':
					table_data = table_data + stat_table_data[i][j]
				else:
					table_data = table_data + ","
			

			csv_stat_output.write(table_data)	
			csv_stat_output.write("\n")
			table_data=""



############# MAIN PROGRAM ################
links_list = getAlphabetLinks()
i = 0
for link in links_list:
	if(i==2):
		break
	print link['href']
	all_data,link1 = getPlayerBasicInformation(link['href'])
	tableToCSV(all_data,link1)
	i+=1

print "Players basic information saved!!"

#print "Now fetching individual player's information"
#indvPlayerStats("/players/m/machasc01.html")



