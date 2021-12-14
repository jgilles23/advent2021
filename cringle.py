#Advent of code helper to download AOC input files and pre-interpret the data

from selenium import webdriver


# Using Chrome to access web
driver = webdriver.Chrome() 
# Open the website
driver.get('https://adventofcode.com/')