from bs4 import BeautifulSoup
import requests
import pandas as pd
import urllib.request

## Bug noted. if multiple positions then party incorrect
def getPics(soup):
	pics = soup.find_all(class_ = "result__thumbnail_parl")
	
	for p in pics:
		loc = "https://www.aph.gov.au/" + p.find_next("img")["src"]
		title = "pics/" + (p.find_next("img")["alt"]).strip("Photo of ") + ".jpeg"
		urllib.request.urlretrieve(loc,title)

def readHtml(url,fname):
	pollies = []
	r = requests.get(url)
	soup = BeautifulSoup(r.text,'html.parser')
	#with open("html-src/"+fname+".html",'w') as fr:
		#fr.write(r.text.encoding("utf-8"))
	
	return soup

def getinfo(soup):
	pollies = []
	res = soup.find_all(class_="medium-pull-2 medium-7 large-8 columns")
	for r in res:
		row = {}
		row["Name"] = r.find_next(class_="title").find_next("a").text
		row["Districts"] = r.find_next("dd").text
		n = r.find_next("dd").find_next("dt")
		if n.text.upper() == "POSITIONS":
			row["Positions"] = n.find_next("dd").text
			row["Party"] = n.find_next("dd").find_next("dd").text
		else:
			row["Positions"] = ""
			row["Positions"] =n.find_next("dd").text
		
		pollies.append(row)

	print("Counted: %i" % len(pollies))
	return pollies
	
def main():
	pollies=[]
	for i in range(1,2):
		if i == 1:
			url = "https://www.aph.gov.au/Senators_and_Members/Parliamentarian_Search_Results?q=&mem=1&par=-1&gen=0&ps=12&st=1"
		else:
			url = "https://www.aph.gov.au/Senators_and_Members/Parliamentarian_Search_Results?page=" +str(i)+ "&q=&mem=1&par=-1&gen=0&ps=12&st=1"

		soup = readHtml(url,str(i))

		pollies += getinfo(soup)
	df = pd.DataFrame(pollies)
	df.to_csv("pollies.csv")

if __name__ == "__main__":
	main()

