import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
import selenium
import requests
import math
import time
import base64

# Selenium Imports
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys


# Selenium initialization
def initializeSelenium():
    chrome_options = Options()
    chrome_options.add_argument("window-size=1200x600")
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--headless')
    driver = Chrome(executable_path="/Users/marcoscarlata/Desktop/Projects/Scraper_Project/chromedriver",
                    options=chrome_options)
    return driver


# Helper function to accessSite
def accessSite(driver, link):
    driver.get(link)


def getTable():
    # Obtain the number of rows in body
    rows = 1 + len(driver.find_elements_by_xpath(
        "/html/body/section/div[1]/div[1]/div[1]/div[1]/div[1]/div[2]/div[3]/table/tbody/tr"))

    # Obtain the number of columns in table
    cols = len(driver.find_elements_by_xpath(
        "/html/body/section/div[1]/div[1]/div[1]/div[1]/div[1]/div[2]/div[3]/table/tbody/tr[1]/td"))
    table = []
    for r in range(2, rows + 1):
        row = []
        for p in range(1, cols + 1):
            # obtaining the text from each column of the table
            try:
                value = driver.find_element_by_xpath(
                    "/html/body/section/div[1]/div[1]/div[1]/div[1]/div[1]/div[2]/div[3]/table/tbody/tr[" + str(
                        r) + "]/td[" + str(p) + "]").text
                row.append(value)
            except NoSuchElementException:
                break
        table.append(row)
    table = [val[1:] for val in table]
    years = ['(2012)', '(2017)', '(2018)', '(2019)', '(2020)', '(2021)']
    table = [val for val in table if len(val) > 0]
    for val in table:
        number = val[-1]
        for year in years:
            if year in number:
                number = number.replace(' ' + year, '')
        if ' +' in number:
            number = number.replace(' +', '')
        if '+' in number:
            number = number.replace('+', '')
        if ',' in number:
            number = number.replace(',', '')
        if '-' in number:
            val[-1] = [int(i) for i in number.split("-")][-1]
        else:
            val[-1] = int(number)
    return sorted(table, key=lambda x: x[2], reverse=True)
st.write("""
# Web Scraper App

Welcome to the web scraping app!

""")

directory_option = st.selectbox(
    'Scrape the follow points of data:',
    ('Top OPT Companies', 'Other')
)

# Upon "GO" button submission
if st.button("GO"):
    # Checks if it says "Other"
    if directory_option == 'Other':
        st.error("Invalid directory, please re-enter a correct value")
    else:
        with st.spinner("Scraping Top OPT Listings"):
            driver = initializeSelenium()
            driver.implicitly_wait(3)
            link = "https://unitedopt.com/Home/blogdetail/top-companies-offering-opt-jobs-to-international-students-in-2021"
            accessSite(driver, link)
            table = getTable()
            df_table = pd.DataFrame(table, columns=['Company Name', 'Sector', 'Employee Number'])
            st.table(df_table)

        st.success("Initialization complete!")
        directory_option = st.selectbox(
            'Scrape the follow points of data:',
            set(df_table['Company Name'])
        )
        #TODO: Scrap company specific site for mission statement, perks, payments etc (keyvalue, lever, the company site etc)

        #
        # with st.spinner("Scraping directory"):
        #     scrap_prog = st.progress(0)
        #
        #     scrap_prog.progress(100)
        #
        # st.success("Directory has been scraped!")
        st.balloons()

        # df_text = pd.DataFrame(scrap_text)
        # #Workaround to Streamlit file exports
        # csv = df_text.to_csv(index=False)
        # b64 = base64.b64encode(csv.encode()).decode()
        # filename = f"{directory_option}_Scraped_Text"
        # href = f'<h3>Click here to download the scraped directory: <a href="data:file/csv;base64,{b64}" download="{filename}.csv">Here</a></h3>'
        # st.markdown(href, unsafe_allow_html=True)
        #
        # st.write("""
        #         ## Here is a sample of the scraped text:
        # """)
        # text_slot = st.empty()
        # text_slot.write(f"{scrap_text[0]}")
