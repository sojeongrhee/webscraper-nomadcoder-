import requests
from bs4 import BeautifulSoup

LIMIT = 50
URL = f"https://www.indeed.com/jobs?q=python&limit={LIMIT}"

def extract_indeed_pages():
  result = requests.get(URL)
  soup = BeautifulSoup(result.text, "html.parser")
  pagination = soup.find("ul", {"class" : "pagination-list"})
  links = pagination.find_all('a')
  pages = []
  for link in links[0:-1]:
    pages.append(int(link.string))
  max_page = pages[-1]
  return max_page

def extract_job(html):
  #title
  title = html.find("h2", {"class" : "jobTitle"})
  title = str(title.find("span", title = True).string)
  title = title.strip()
    #title.find("span", title = True)는 Title이 있는 span을 찾으라는 의미임.
  #company
  company = html.find("span", {"class" : "companyName"})
  if company is not None:
    company = str(company.string)  
  else:
    company = None
  company = company.strip()
  #location
  location = str(html.find("div", {"class" : "companyLocation"}).string)
  location = location.strip()
  #id
  job_id = html["data-jk"]

  return {'title' : title, 'company' : company, 'location' : location, 'link' : f"https://www.indeed.com/viewjob?jk={job_id}&from=serp&vjs=3"}

def extract_indeed_jobs(last_page):
  jobs = []
  for page in range(last_page):
    print(f"Scrapping page {page}")
    result = requests.get(f"{URL}&start={page*LIMIT}")
    soup = BeautifulSoup(result.text, "html.parser")
    results = soup.find_all("a", {"class" : "tapItem"})
    for result in results:
      job = extract_job(result)
      jobs.append(job)
  return jobs

