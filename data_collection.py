import glassdoor_scraper as gs
import pandas as pd

path = "F:/New_Python_staff/ds_salaries/chromedriver.exe"

df = gs.get_jobs('data scientist',5, False, path, 15)

df.to_csv('glassdoor_jobs_scrapped.csv', index = False)
