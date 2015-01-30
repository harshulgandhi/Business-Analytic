from bs4 import BeautifulSoup
import re
import urllib


output = open("testoutput.txt","w")
csv_output = open("csv_output.txt","w")


url_a = "http://www.basketball-reference.com/players/a/"

html = urllib.urlopen(url_a).read();
soup = BeautifulSoup(html)

player_table = soup.find("table",{"class":"sortable stats_table" })
#print player_table.__str__()
#output.write(player_table.__str__())

get_rows = player_table.find_all('tr')
all_rows = []
all_data = []
all_text = []
for each_row in get_rows:
	text = ''.join(each_row.find_all(text=True))
	single_row = (each_row.find_all(text=True))
	all_rows.append(single_row)
	all_data.append(text)
	
#print all_rows[1]
output.write(all_data.__str__())


print all_data[1].__str__()
print all_data[2].__str__()
print len(all_data)

if all_data[1][68].__str__() == '\n\n':
	print "It matches!!"

#Function to parse table into CSV format

def tableToCSV():
	print "Converting table to CSV..."
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


tableToCSV()