from bs4 import BeautifulSoup
import re
import urllib


output = open("testoutput.txt","w")

url_a = "http://www.basketball-reference.com/players/a/"

html = urllib.urlopen(url_a).read();
soup = BeautifulSoup(html)

player_table = soup.findAll("table",{"class":"sortable stats_table" })
#print player_table

for each_row in player_table:
	row = each_row.find_all('tr')
	for each_element in row:
			cell = each_element.find_all('td')
			#output.write(cell)
			print cell[0].text+","


'''for er in each_row:
	tds = er.findAll('td')
	print (tds[0].text)+","+(tds[1],text)
'''