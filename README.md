# Coursera Crawler
Crawler for courser (still WIP)

**How to use:**

- You can simply run coursera_crawler.py
- If you prefer ipynb, you can use Coursera_crawling.ipynb
- Package requirements: bs4, langdetect, selenium, platform

# [Description]
This program is a crawler to scrape course information from : https://www.coursera.org/directory/courses
The current version take:

- Category 1
- Category 2 (sub category)
- Rating: overall rating
- Ratecount: # of rates
- Info (Some keyword about courses: '|' delimited
- Skills: 'Skills' tags of each courses: '|' delimited
- About: general explanation on each course
- Type: There are 2 different post types for courses - this field reveals which type does each course data takes
- Link: url for each course

# Output Sample Image:
<img width="1004" alt="Screen Shot 2021-04-01 at 3 33 56 AM" src="https://user-images.githubusercontent.com/43837843/113193686-37483f80-929b-11eb-8686-e8bffe95904e.png">

# [Some Useful features]
- If you use chrome, there's 'headless' option supports for faster crawling. **This takes about 2.5 sec/each courses**
- There are many courses with various language - with 'langdetect' setting, you can only scrape courses of your language

# [Some Limitations]
- There are some pages, which does not follow general rules - so there could be some missing values. For those cases, trying to detect and update
- Other info as Syllabus, is not included yet - tyring to update, to include more info
