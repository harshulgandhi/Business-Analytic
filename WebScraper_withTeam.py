from bs4 import BeautifulSoup
import re
import urllib
import os
import time


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
		#print link['href']
		if i == 25:
			break
	print "Fetching ",i," urls done\n"
	return links_list



##To get payer basic profile information in tabular form. This
##table is not in csv format!
def getPlayerBasicInformation(link):
	
	global home_url
	url = home_url+link.__str__()
	print "\nCompiled URL is ",url,"\n"
	html = urllib.urlopen(url).read();
	time.sleep(1)
	soup = BeautifulSoup(html)
	player_table = soup.find("table",{"class":"sortable stats_table" }) 	#reading the players table
	
	get_rows = player_table.find_all('tr')		#Getting individual rows
	get_rows_custom = []
	player_page_url=[]
	#print get_rows[0].__str__()

	##Getting only the rows where name is "<Strong>"
	needle_0= "<strong>"
	needle_1= '<a href="(/players/.*)">(.*)</a>'
	for i in range(len(get_rows)):
		if(re.search(needle_0,get_rows[i].__str__()) or i == 0):		#Looking for rows containing "strong" tag
			if i > 0:
				haystack = get_rows[i].__str__()
				result = re.search(needle_1,haystack)
				player_page_url.append(result.group(1))

				print "****Fetching information for player with page: ",result.group(1)				#This gives individual player url
				indvPlayerStats(result.group(1),result.group(2))			#Function call to read, parse and save individual player's data
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
	return all_data,link.__str__()						#All data corresponding to each player not in csv format


#Function to parse table into CSV format
def tableToCSV(all_data,link):
	print "Converting table to CSV...\n"
	path = '/basic profile'
	needle="/(.?)/"												#Getting alphabet for which tables is being converted
	result = re.search(needle,link)
	alphabet = result.group(1)
	if not os.path.exists(alphabet):
		os.makedirs(alphabet)
	print "Created forlder for alphaber : ",alphabet
	nameOfFile = os.path.join(alphabet,"basic_profile_for"+alphabet+".csv")
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
def indvPlayerStats(rel_link, player_name):
	
	particular_player_url = home_url+rel_link	
	needle_3='/players/(.?)/(.*).html'
	res = re.search(needle_3,rel_link)
	player_alphabet = res.group(1)
	#player_name=res.group(2)

	player_html = urllib.urlopen(particular_player_url).read();
	soup1 = BeautifulSoup(player_html)
	print "Reading page"
	get_stat_tables = soup1.find_all("div",{"class":"stw"})

	needle_2 = '<div class="stw" id="(all_.*)">'

	result = re.findall(needle_2,get_stat_tables.__str__())			#List of all tables on this page
	for i in range(len(result)):
		print "****Fetching table",result[i],"****"
		table_data=""
		stat_table_data=[]
		ind_table = soup1.find("div",{"id":result[i]})			#result[i] is the table name 'all_*'

		get_rows = ind_table.find_all('tr')
		'''
		Parsing data for each player and
		converting into csv format
		'''
		for each_row in get_rows:
			text = ''.join(each_row.find_all(text=True))
			stat_table_data.append(text)
		if not os.path.exists(player_alphabet+'/'+player_name):
			os.makedirs(player_alphabet+'/'+player_name)
		filename = os.path.join(player_alphabet+'/'+player_name,"Player_stat_"+player_name+'_'+result[i]+".csv")
		#filename= "player_stat_"+player_name+"_"+result[i]+".csv"
		csv_stat_output = open(filename,"w")
		tableSize = len(stat_table_data)
		for i in range(0,tableSize,1):
			row_len = len(stat_table_data[i])
			for j in range(1,row_len,1):
				try:
					if stat_table_data[i][j].__str__()!='\n':		##Encountered unicode character problem
						table_data = table_data + stat_table_data[i][j]
					else:
						table_data = table_data + ","
			
				except UnicodeEncodeError:
					table_data = "NonAsciiCharacter"

			csv_stat_output.write(table_data)	
			csv_stat_output.write("\n")
			table_data=""
		
	print "\n\n"		


##Function to read individual team
##page and parse team level stats
def indTeamStas(team_url):
	table_data=""
	team_html = urllib.urlopen(team_url).read();
	time.sleep(1)
	soup2 = BeautifulSoup(team_html)
	team_table_section = soup2.find("div",{"id":"div_active" })

	team_stat_table = []
	team_name = []
	#print team_table_section.__str__()
	team_table = team_table_section.find_all('tr',{"class":"full_table"})
	
	
	i = 0
	for each_entry in team_table:
		
		team_name.append(each_entry.find('a').contents[0])
		
		text = ''.join(each_entry.find_all(text=True))
		team_stat_table.append(text)
		if not os.path.exists('team/'+team_name[i].__str__()):
			print team_name[i]
			os.makedirs('team/'+team_name[i].__str__())
		filename = os.path.join('team/'+team_name[i],team_name[i]+".csv")
		csv_output = open(filename,"w")
		tableSize = len(team_stat_table)
		for i in range(0,tableSize,1):
			row_len = len(team_stat_table[i])
			for j in range(1,row_len,1):
				try:
					if team_stat_table[i][j].__str__()!='\n':		##Encountered unicode character problem
						table_data = table_data + team_stat_table[i][j]
					else:
						table_data = table_data + ","
			
				except UnicodeEncodeError:
					table_data = "NonAsciiCharacter"

			csv_output.write(table_data)	
			csv_output.write("\n")
			table_data=""


	



############# MAIN PROGRAM ################

home_url = "http://www.basketball-reference.com"
player_home_url = "http://www.basketball-reference.com/players/"
team_url = "http://www.basketball-reference.com/teams/"


links_list = getAlphabetLinks()
i = 0

for link in links_list:
	if(i==25):
		break
	print link['href']
	all_data,link1 = getPlayerBasicInformation(link['href'])
	tableToCSV(all_data,link1)
	i+=1

print "Players basic information saved!!"

#print "Now fetching individual player's information"
#indvPlayerStats("/players/m/machasc01.html")

print "Getting team level stats\n"
indTeamStas(team_url)



