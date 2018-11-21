from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from string import ascii_lowercase
import sys
driver = webdriver.Firefox()

textfile = file('elite_list.txt','a') # Saves all names to file

s1_start = int(sys.argv[1]) # 3 integer arguments required to specify start point of nested loops (zero indexed)
s2_start = int(sys.argv[2]) # Eg to start at 'dac', use 3 0 2
s3_start = int(sys.argv[3])

for s1 in ascii_lowercase[s1_start:]:
    driver.quit()   # Good to restart web browser every once in a while to clear cache, cookies, etc
    driver = webdriver.Firefox()
    for s2 in ascii_lowercase[s2_start:]:
        for s3 in ascii_lowercase[s3_start:]:
            driver.get("https://www.manchesterroadrace.com/registration/RegistrationQuery.aspx")
            elem = driver.find_element_by_id("txtLastName")
            elem.clear()
            elem.send_keys(s1 + s2 + s3)
            elem.send_keys(Keys.RETURN)

            try:
                element = WebDriverWait(driver, 4).until( # Waits up to 4 seconds for element before throwing a TimeoutException
                    EC.presence_of_element_located((By.ID, "tblRegistrants"))
                )
            except TimeoutException:
                print ("Exception thrown, skipping letter combo")
                continue
            finally:
                try:
                    table = driver.find_element_by_id("tblRegistrants")
                    rows = table.find_elements_by_tag_name("tr")
                    for x in range(1, len(rows)):
                        row = rows[x]
                        td_array = row.find_elements_by_tag_name("td")
                        seed = td_array[10]
                        if seed.text == "Elite":
                            first_name = td_array[1]
                            last_name = td_array[3]
                            print (first_name.text) # Prints elite runner's name if found
                            print (last_name.text)
                            textfile.write(first_name.text + " " + last_name.text + "\n")
                except NoSuchElementException as e:
                    print str(e)
        s3_start = 0
    s2_start = 0
textfile.close()
