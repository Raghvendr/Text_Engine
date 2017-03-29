import urllib2
from bs4 import BeautifulSoup
icicipl="https://www.icicibank.com/Personal-Banking/loans/personal-loan/index.page"
HDFCPL = "http://www.hdfcbank.com/personal/products/loans/personal-loan"
SBIPL= "https://www.sbi.co.in/portal/web/personal-banking/personal-loans"

page = urllib2.urlopen(icicipl)
soup = BeautifulSoup(page)
print soup.prettify()
soup.title
soup.title.string
soup.a
all_links = soup.find_all("a")
for link in all_links:
    print link.get("href")
for link in all_links:
    print link.get("class")
