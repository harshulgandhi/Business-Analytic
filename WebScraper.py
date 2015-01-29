from bs4 import BeautifulSoup
import re
import urllib

url_a = "http://www.basketball-reference.com/players/a/"

html = urllib.urlopen(url_a).read();
soup = BeautifulSoup(html)

player_table = soup.findAll("table",{"class":"sortable stats_table" })
print player_table

#each_row = player_table.find_all('tr')
'''
for er in each_row:
	tds = er.findAll('td')
	print (tds[0].text)+","+(tds[1],text)
'''