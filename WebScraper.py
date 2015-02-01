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
get_rows_custom = []
print get_rows[0].__str__()

##Getting only the rows where name is "<Strong>"
needle = "<strong>"
for i in range(len(get_rows)):
	if(re.search(needle,get_rows[i].__str__()) or i == 0):
		get_rows_custom.append(get_rows[i])

##

print "get_rows_custom : "
print get_rows_custom
print "type(get_rows_custom) : " 
print type(get_rows_custom)

all_rows = []
all_data = []
all_text = []
for each_row in get_rows_custom:
	#text = ''.join(each_row.find_all(text=True and 'strong'))
	text = ''.join(each_row.find_all(text=True))
	#print text
	single_row = (each_row.find_all(text=True))
	all_rows.append(single_row)
	all_data.append(text)
	
#print all_rows[1]
output.write(all_data.__str__())


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



##Getting href for individual letters
print "\n\n\n*****************"
home_url = "http://www.basketball-reference.com/players/"
home_html = urllib.urlopen(home_url).read();
soup = BeautifulSoup(home_html)
get_alphabet_section = soup.find_all("div",{"id":"page_content"})
output1 = open("testoutput1.txt","w")
output1.write(get_alphabet_section.__str__())
'''
for url in soup.find_all('a',href=True):
	print "Following URLs found :", url['href'],"\n"
'''



