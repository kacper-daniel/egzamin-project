'''
    Scraping INF.02 and INF.03 exam's questions data from online database to use it in the project
'''

#file which will store the data
f = open("egzamin.csv", mode='a', encoding='utf-8')

#necessary libs
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
action = ActionChains(driver)

# urls that data will be scraped from
urls_02 = ['https://www.praktycznyegzamin.pl/ee08/teoria/jedno/', 'https://www.praktycznyegzamin.pl/e12/teoria/jedno/', 'https://www.praktycznyegzamin.pl/e13/teoria/jedno/']
urls_03 = ['https://www.praktycznyegzamin.pl/inf03ee09e14/teoria/jedno/']

# how many questions to scrap
lengths_02 = [240, 918, 728]
lenghts_03 = [763]


# main scraping function
def scraping(urls, lengths):
    id = 0
    for i in range(len(urls)):

    # opening the website
        driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.CONTROL + 't') 
        time.sleep(1)
        driver.get(urls[i])
        driver.maximize_window()

        for j in range(lengths[i]):
            
    # clicking on 'A' to reveal correct answer
            driver.execute_script("scroll(0, 500)")
            button = WebDriverWait(driver, 1000).until(EC.presence_of_element_located((By.XPATH, '//*[@id="odpa"]')))
            action.move_to_element(button).click().perform()
            time.sleep(2)

            question = driver.find_element(By.CSS_SELECTOR, '#one-question > div > div.title').text

    # double try/except statement because there was an issue that some questions where skipped
    # finding element and clicking it after exception fixed this problem
            try:
                answer = driver.find_element(By.CLASS_NAME, 'correct').text
            except NoSuchElementException:
                time.sleep(2)
                button = WebDriverWait(driver, 1000).until(EC.presence_of_element_located((By.XPATH, '//*[@id="odpa"]')))
                action.move_to_element(button).click().perform()
                time.sleep(2)
                try:
                    answer = driver.find_element(By.CLASS_NAME, 'correct').text
                except NoSuchElementException:
                    continue

    # checking if question refers to image
            img_present = 1
            try:
                img = driver.find_element(By.CSS_SELECTOR, '#one-question > div > div.image')
            except NoSuchElementException:
                img_present = 0


    # dropping commas to prevent issues with csv
            question = question.replace(',', '')
            answer = answer.replace(',', '')

    # appending to scraped data to file
            f.write(str(id) + ',' + question + ',' + answer[0] + ',' + answer[3:] + ',' + str(img_present) + '\n')
            id += 1

    # next question
            next = WebDriverWait(driver, 1000).until(EC.presence_of_element_located((By.XPATH, '//*[@id="next"]')))
            action.move_to_element(next).click().perform()

        driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.CONTROL + 'w')

scraping(urls_03, lenghts_03)
driver.close()

scraping(urls_02, lengths_02)
driver.close()


