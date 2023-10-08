from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import time
import pandas as pd



def get_jobs(keyword, num_jobs, verbose, path, slp_time):
    '''Gathers jobs as a dataframe, scraped from Glassdoor'''

    # Initializing the webdriver
    options = webdriver.ChromeOptions()

    # Uncomment the line below if you'd like to scrape without a new Chrome window every time.
    # options.add_argument('headless')
    service = Service(path)
    # Change the path to where chromedriver is in your home folder.
    driver = webdriver.Chrome(service=service, options=options)
    driver.set_window_size(1120, 1000)

    url = "https://www.glassdoor.com/Job/jobs.htm?suggestCount=0&suggestChosen=false&clickSource=searchBtn&typedKeyword=" + keyword + "&sc.keyword=" + keyword + "&locT=&locId=&jobType="
    # url = 'https://www.glassdoor.com/Job/jobs.htm?sc.keyword="' + keyword + '"&locT=C&locId=1147401&locKeyword=San%20Francisco,%20CA&jobType=all&fromAge=-1&minSalary=0&includeNoSalaryJobs=true&radius=100&cityId=-1&minRating=0.0&industryId=-1&sgocId=-1&seniorityType=all&companyId=-1&employerSizes=0&applicationType=0&remoteWorkType=0'
    driver.get(url)
    jobs = []

    time.sleep(slp_time)

    # Try to send email and password on the glassdoor
    try:
        # Click to accept cookies and sign in with username password

        driver.find_element(By.ID, 'onetrust-accept-btn-handler').click()
        driver.find_element(By.ID, 'SignInButton').click()
        time.sleep(2)
        driver.find_element(By.ID, "fishbowlCoRegEmail").send_keys("giannakis_@hotmail.com")
        time.sleep(2)
        driver.find_element(By.CLASS_NAME, "emailButton").click()
        time.sleep(2)
        driver.find_element(By.ID, "fishbowlCoRegPassword").send_keys("skatopsixos")
        time.sleep(2)
        driver.find_element(By.NAME, "submit").click()
        time.sleep(12)
        driver.find_element(By.CSS_SELECTOR, '[alt="Close"]').click()
        time.sleep(2)
    except NoSuchElementException:
        pass


    while len(jobs) < num_jobs:  # If true, should be still looking for new jobs.

        # Let the page load. Change this number based on your internet speed.
        # Or, wait until the webpage is loaded, instead of hardcoding it.
        time.sleep(slp_time)

        # Going through each job in this page
        job_buttons = driver.find_elements(By.CLASS_NAME, "JobsList_jobListItem__JBBUV")  # jl for Job Listing. These are the buttons we're going to click.
        for job_button in job_buttons:
            print(len(job_buttons))


            print("Progress: {}".format("" + str(len(jobs)) + "/" + str(num_jobs)))
            if len(jobs) >= num_jobs:
                break

            job_button.click()  # You might
            time.sleep(1)
            collected_successfully = False

            while not collected_successfully:
                try:
                    company_data = job_button.text
                    collected_successfully = True
                except:
                    time.sleep(5)

            # try:
            #     salary_estimate = driver.find_element(By.XPATH,'.//span[@class="gray salary"]').text
            # except NoSuchElementException:
            #     salary_estimate = -1  # You need to set a "not found value. It's important."

            # try:
            #     rating = driver.find_element(By.XPATH,'.//span[@class="rating"]').text
            # except NoSuchElementException:
            #     rating = -1  # You need to set a "not found value. It's important."

            # Printing for debugging
            if verbose:
                print("Company Data: {}".format(company_data))



            jobs.append({"Company Data:": company_data
                         })
            # add job to jobs

        # Clicking on the "next page" button
        try:
            driver.find_element(By.CLASS_NAME, 'button_Button__meEg5').click()
        except NoSuchElementException:
            print("Scraping terminated before reaching target number of jobs. Needed {}, got {}.".format(num_jobs,
                                                                                                         len(jobs)))
            break

    return pd.DataFrame(jobs)  # This line converts the dictionary object into a pandas DataFrame.