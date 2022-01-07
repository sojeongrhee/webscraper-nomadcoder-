import requests
from bs4 import BeautifulSoup

LIMIT = 50
URL = f"https://www.indeed.com/jobs?q=python&limit={LIMIT}"

def extract_indeed_pages():
  result = requests.get(URL)
  soup = BeautifulSoup(result.text, "html.parser")
  pagination = soup.find("div", {"class" : "pagination"})
  links = pagination.find_all('a')
  pages = []
  for link in links[:-1]:
    pages.append(int(link.string))
  max_page = pages[-1]
  return max_page

def extract_indeed_jobs(last_page):
  jobs = []
  for page in range(last_page):
    result = requests.get(f"{URL}&start={page*LIMIT}")
    soup = BeautifulSoup(result.text, "html.parser")
    results = soup.find_all("a", {"class" : "tapItem"})
    for result in results:
      title = result.find("h2", {"class" : "jobTitle"})
      title = str(title.find("span", title = True).string)
      title = title.strip()
      #title.find("span", title = True)는 Title이 있는 span을 찾으라는 의미임.
      company = result.find("span", {"class" : "companyName"})
      if company is not None:
        company = str(company.string)
      else:
        company = None
      company = company.strip()
      print(title)
      print(company)
  return jobs