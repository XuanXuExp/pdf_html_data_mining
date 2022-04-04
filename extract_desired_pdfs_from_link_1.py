##example getting all links from a url

from bs4 import BeautifulSoup
# from BeautifulSoup import BeautifulSoup
#import urllib2  ## instead : from urllib.request import urlopen
from urllib.request import urlopen
import re

import requests
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

# html_page = urllib2.urlopen("https://arstechnica.com")  # instead: html_page = urllib2.urlopen("https://arstechnica.com")


##########  download_link_content  ################################################

def download_link_content(file_name, response):
    with open(file_name, 'wb') as f:
        f.write(response.content)


##########  find_link ##############################################################

def find_and_parse_link(url):
    html_page = urlopen(url)
    soup = BeautifulSoup(html_page, 'lxml')
    return soup

########################################################################################
# def clickLinkByHref (driver,href):
#     anchors = driver.find_element(By.tagName("a"))
#     i = anchors.iterator()
#
#     while(i.hasNext()):
#         anchor = i.next()
#         if(anchor.getAttribute("href").contains(href)):
#             anchor.click()
#             break
#######################################################################################
def get_desired_pdf_of_inks(year_href, driver,save_file_directory):

    ### the href in links corresponding to each year (I think they represents months)
    valid_link_text = {'01/', '02/', '03/', '04/', '05/', '06/', '07/', '08/', '09/', '10/', '11/', '12/'}

    continue_link = driver.find_element_by_link_text(year_href).click()
    current_link = driver.current_url

    html_page = urlopen(current_link)
    soup = BeautifulSoup(html_page, 'lxml')
    tag_a_list = soup.findAll('a')

    for tag in tag_a_list:
        if tag.text in valid_link_text:
            tag_text = tag.text

            continue_link1 = driver.find_element_by_link_text(tag_text).click()
            current_link1 = driver.current_url
            html_page1 = urlopen(current_link1)
            soup1 = BeautifulSoup(html_page1, 'lxml')

            # all_desired_pdfs = soup1.findAll('a', attrs={'href': re.compile("^MRK(.*?)pdf$")})
            # other_cases =[]
            # other_cases.extend(soup1.findAll('a', attrs={'href': re.compile("^mRK(.*?)pdf$")}))
            # other_cases.extend(soup1.findAll('a', attrs={'href': re.compile("^MrK(.*?)pdf$")}))
            # other_cases.extend(soup1.findAll('a', attrs={'href': re.compile("^MRk(.*?)pdf$")}))
            # other_cases.extend(soup1.findAll('a', attrs={'href': re.compile("^mrK(.*?)pdf$")}))
            # other_cases.extend(soup1.findAll('a', attrs={'href': re.compile("^mRk(.*?)pdf$")}))
            # other_cases.extend(soup1.findAll('a', attrs={'href': re.compile("^Mrk(.*?)pdf$")}))
            # other_cases.extend(soup1.findAll('a', attrs={'href': re.compile("^mrk(.*?)pdf$")}))
            # all_desired_pdfs.extend(other_cases)


            all_desired_pdfs = soup1.findAll('a', attrs={'href': re.compile("^M.{0,2}R.{0,2}K(.*?)pdf$")})
            other_cases =[]
            other_cases.extend(soup1.findAll('a', attrs={'href': re.compile("^m.{0,2}R.{0,2}K(.*?)pdf$")}))
            other_cases.extend(soup1.findAll('a', attrs={'href': re.compile("^M.{0,2}r.{0,2}K(.*?)pdf$")}))
            other_cases.extend(soup1.findAll('a', attrs={'href': re.compile("^M.{0,2}R.{0,2}k(.*?)pdf$")}))
            other_cases.extend(soup1.findAll('a', attrs={'href': re.compile("^m.{0,2}r.{0,2}K(.*?)pdf$")}))
            other_cases.extend(soup1.findAll('a', attrs={'href': re.compile("^m.{0,2}R.{0,2}k(.*?)pdf$")}))
            other_cases.extend(soup1.findAll('a', attrs={'href': re.compile("^M.{0,2}r.{0,2}k(.*?)pdf$")}))
            other_cases.extend(soup1.findAll('a', attrs={'href': re.compile("^m.{0,2}r.{0,2}k(.*?)pdf$")}))
            all_desired_pdfs.extend(other_cases)


            if len(all_desired_pdfs):
                i = 1

                for link in all_desired_pdfs:
                    print(link.get('href'))
                    #print(link)

                    h = link.get('href')
                    link1 =  current_link1 + h
                    driver.get(link1)

                    response = requests.get(link1)
                    file_name = year_href.strip('/') + '_' +tag_text.strip('/')+'_' +str(i)+'_'+h
                    i += 1
                    # download_link_content(file_name, response)
                    ###
                    save_pdf_path = save_file_directory + '/' +file_name
                    download_link_content(save_pdf_path, response)
                    ###

                driver.get(current_link)
                #driver.back()
            else:
                driver.back()
##########............main...............################################################

def extract_desired_pdfs_from_link(save_file_directory):

    url = "https://www.charm.com/wp-content/uploads/"
    #html_page = urlopen(url)

    driver = webdriver.Chrome('chromedriver.exe')
    driver.get(url)

    html_page1 = urlopen(url)
    soup2 = BeautifulSoup(html_page1, 'lxml')
    tag_a_list2 = soup2.findAll('a')

    for tag in tag_a_list2:
        print(tag)
        pattern = '(?P<year>\d{4})'
        year = re.search(pattern, tag.text)
        if year and int(year.group('year')) >= 2018:
            get_desired_pdf_of_inks(tag.text, driver, save_file_directory)
        driver.get(url)


    # for tag in tag_a_list2:
    #     print(tag)
    #
    #     try:
    #         # h = int(tag.text.strip('/'))
    #         # if isinstance(h, int):
    #         year = int(tag.text.strip('/'))
    #         if year >= 2019:
    #             get_desired_pdf_of_inks(tag.text)
    #
    #     except:
    #         continue





    # continue_link = driver.find_element_by_link_text(year_href).click()
    # current_link = driver.current_url

####
# if __name__ == '__main__':
#     main()

############# main
save_file_directory= "D:\_GRA projects\extracted_pdfs_from_charm_link"
extract_desired_pdfs_from_link(save_file_directory)





