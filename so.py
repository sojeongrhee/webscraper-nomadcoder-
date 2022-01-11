import requests
from bs4 import BeautifulSoup

LIMIT = 50
URL = f"https://stackoverflow.com/jobs?q=python"

def get_last_page():
  result = requests.get(URL)
  soup = BeautifulSoup(result.text, "html.parser")
  pages = soup.find("div", {"class" : "s-pagination"}).find_all("a")
  last_page = pages[-2].get_text(strip=True)
  return int(last_page)

def extract_job(html):
  #title
  title = html.find("h2", {"class" : "mb4"}).find("a")["title"]
  #company, location
  company, location = html.find("h3", {"class" : "fc-black-700"}).find_all("span", recursive = False)
  company = company.get_text(strip=True)
  location = location.get_text(strip=True)
  #apply link
  job_id = html['data-jobid']
  return{
    'title' : title, 
    'company' : company, 
    'location' : location, 
    'apply link' : f"https://stackoverflow.com/jobs/{job_id}"
  }

def extract_jobs(last_page):
  jobs = []
  for page in range(last_page):
    print(f"Scrapping S0 : Page : {page}")
    result = requests.get(f"{URL}&pg={page + 1}")
    #print(result.status_code)  //if status code = 200 -> properly working
    soup = BeautifulSoup(result.text, "html.parser")
    results = soup.find_all("div", {"class" : "-job"})
    for result in results:
      #print(result["data-jobid"])  //test code
      job = extract_job(result)
      jobs.append(job)
  return jobs
    
def get_jobs():
  last_page = get_last_page()
  jobs = extract_jobs(last_page)
  return jobs
