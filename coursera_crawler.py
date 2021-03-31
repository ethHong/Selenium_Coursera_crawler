from bs4 import BeautifulSoup
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
import os
from fake_useragent import UserAgent
from tqdm.notebook import trange
import time
import platform
from langdetect import detect
import json

options = webdriver.ChromeOptions()
# options.add_argument('headless')
options.add_experimental_option("excludeSwitches", ["enable-automation"])

# Just for in cast when we need fake-UA (when request blocked)
def mock_user_agent():
    ua = UserAgent()

    working = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.1 Safari/605.1.15"
    working_tail = "(" + working.split("(")[-1]
    random_head = ua.random.split("(")[0] + "(" + ua.random.split("(")[1]
    return random_head + working_tail


# Choose right chromedriver of your OS
if platform.system() == "Windows":
    driverpath = os.getcwd() + "/chromedriver.exe"
else:
    driverpath = os.getcwd() + "/chromedriver"


def get_links(page, lang=True):

    url = "https://www.coursera.org/directory/courses?page=" + str(page)
    driver.get(url)
    soup = BeautifulSoup(driver.page_source, "lxml")
    links = soup.findAll("a", {"class": "c-directory-link"}, href=True)

    course_name = []
    course_links = []
    for i in links:
        if detect(i.text) == "en":
            course_name.append(i.text)
            course_links.append("https://coursera.org" + i["href"])

    collected = {}
    for i in range(0, len(course_name)):
        collected[course_name[i]] = course_links[i]
    return collected


def crawl(url):
    driver.get(url)
    soup = BeautifulSoup(driver.page_source, "lxml")

    # Category
    category1 = soup.findAll("div", {"class": "_1ruggxy"})[1].text
    category2 = soup.findAll("div", {"class": "_1ruggxy"})[2].text

    # Rating, if exists
    ratingContainer = soup.findAll(
        "span",
        {"class": "_16ni8zai m-b-0 rating-text number-rating number-rating-expertise"},
    ) + soup.findAll(
        "span", {"class": "_16ni8zai m-b-0 rating-text number-rating m-l-1s m-r-1"}
    )
    if ratingContainer != [] and ratingContainer != None:
        rating = float(re.sub("[^0-9.]+", "", ratingContainer[0].text))
    else:
        rating = "None"

    # Number of Ratings
    ratecountContainer = soup.findAll(
        "div", {"class": "_wmgtrl9 color-white ratings-count-expertise-style"}
    ) + soup.findAll("div", {"class": "_wmgtrl9 m-r-1s"})
    if ratecountContainer != [] and ratecountContainer != None:
        ratecount = int(re.sub("[^0-9.]+", "", ratecountContainer[0].text))
    else:
        ratecount = "None"

    skills = "|".join([i.text for i in soup.findAll("span", {"class": "_1q9sh65"})])

    try:
        if (
            soup.findAll("div", {"class": "contents_inner"})
            + soup.findAll("p", {"class": "_g61i7y"})
            == []
        ):
            driver.find_element(By.CLASS_NAME, "overlay").click()
            # time.sleep(1)
            soup = BeautifulSoup(driver.page_source, "lxml")

        about = " ".join(
            [
                i.text
                for i in soup.findAll("div", {"class": "contents_inner"})
                + soup.findAll("p", {"class": "_g61i7y"})
            ]
        )
    except:
        about = "None"

    # There are two templates - one includes extra info-tag
    infos1 = soup.findAll("div", {"class": "_16ni8zai m-b-0"})
    infos2 = soup.findAll("div", {"class": "_16ni8zai m-b-0 m-t-1s"})
    infos = list(set([i.text for i in infos1 + infos2]))

    # Type1
    if infos != [] and infos != None:
        infos = infos
        type_of_doc = "type1"

    # Type2
    else:
        infos = soup.findAll("span", {"class": "_1rcyblj"}) + soup.findAll(
            "span", {"class": "_1ounhrgz"}
        )
        infos = list(set([i.text for i in infos]))
        type_of_doc = "type2"

    infos = "|".join(infos)
    return {
        "Category1": category1,
        "Category2": category2,
        "Rating": rating,
        "Ratecount": ratecount,
        "Info": infos,
        "skills": skills,
        "about": about,
        "type": type_of_doc,
    }


driver = webdriver.Chrome(driverpath, chrome_options=options)
data = {}

page = input("How many pages to cralw? (Max 194): ")

for i in range(1, page):
    links = get_links(i, lang=True)  # Detect language, and if not English, skip
    names = list(links.keys())
    for c in trange(0, len(names)):
        course = names[c]
        link = links[course]
        data[course] = crawl(link)


# Save as json file
import json

with open("coursera.json", "w") as json_file:
    json.dump(data, json_file)