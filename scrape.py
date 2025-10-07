from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
from bs4 import BeautifulSoup

def scrapeWebsite(website):
    print("Launching Chrome browser...")

    opts = Options()
    opts.add_argument("--headless")
    opts.add_argument("--no-sandbox")
    opts.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(options=opts)

    try:
        driver.get(website)  #use the driver which is automating the browser by using commands like .get()
        print("Web page loaded...")
        html = driver.page_source  #grab the page source code which is the html 
        time.sleep(10)
        return html  # then return the html
    
    finally:
        driver.quit()

def extract_body_content(html_content):
    soup = BeautifulSoup(html_content, "html.parser")
    body_content = soup.body
    if body_content:
        return str(body_content)
    return ""

def clean_body_content(body_content):
    soup = BeautifulSoup(body_content, "html.parser")
    
    for script_or_style in soup(["script", "style"]):
        script_or_style.extract() #removes script or style tags

    cleaned_content = soup.get_text(separator="\n") #get all of the text and separate with a new line
    cleaned_content = "\n".join(line.strip() for line in cleaned_content.splitlines() if line.strip) #If a \n is  not separating aything then remove it
    
    return cleaned_content

#function to seperate the txt into batches to feed the LLLM based on the token limit of characters it can take
def split_dom_content(dom_content, max_length=6000):
    return [
        dom_content[i: i + max_length] for i in range(0, len(dom_content), max_length) #take dom content from i=0 upt to i + maxLength which is 6000 then the for loop will
                                                                                    # take i at 6000 plus the next 6000 characters and continue on till it reaches length of dom_content
                                                                                    
    ]
