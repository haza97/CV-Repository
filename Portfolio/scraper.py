# Importing packages
from selenium import webdriver
from os import chdir
import pandas as pdlib
import csv
import re
import time
from selenium.common.exceptions import NoSuchElementException

# Importing the Kickstarter URLs into a list to iterate the scraper over
# insert filepath here: wd = filepath
reader = csv.reader(open(wd))
result = {}
for row in reader:
    key = int(row[0])
    if key in result:
        # implement your duplicate row handling here
        pass
    result[key] = row[1:]
# We get both urls from the dataset, but only need the first one, so we separate them after the ?
sep = '?'

# Creates a dictionary called result with a numbered key and the kickstarter project
for key in result:
    output = (
        re.search("(?P<url>https?://[^\s]+)", str(result[key])).group("url"))
    rest = output.split(sep, 1)[0]
    result[key] = str(rest)
    print(result[key])

# We now have a list of 133412 Kickstarter pages we can iterate the scraper over
print(len(result))

# Let's code ourselves a web scraper: the first one visits the website and counts the amount of pictures it finds
driver = webdriver.Chrome(
    'C:\\Users\\harol\\Desktop\\Thesis Scraper\\chromedriver')
imagecounter = []
videocounter = []
backercounter = []
for key in result:
    userlink = result[key].rpartition('/')
    driver.get(result[key])
    time.sleep(5)
    # Find all the images and print their source links into a list
    images = driver.find_elements_by_tag_name('img')
    imagelist = []
    for image in images:
        imagelist.append(image.get_attribute('src'))
    imagecounter.append(len(imagelist))
    # Now do the same thing for videos
    videos = driver.find_elements_by_tag_name('video')
    videolist = []
    for video in videos:
        videolist.append(video.get_attribute('src'))
    videocounter.append(len(videolist))
    # Now we get links to user profiles to check how many projects they've backed
    driver.get(userlink[0])
    # Check if the user page exists and find the backer count
    try:
        backercount = driver.find_element_by_class_name('backed').text
        count = re.findall(r'\d+', backercount)
        count = ''.join(count)
        backercounter.append(count)
    # If no user page exists, backer count defaults to 0
    except NoSuchElementException:
        backercount = 0
        backercounter.append(backercount)
print(imagecounter)
print(videocounter)
print(*backercounter, sep=', ')
