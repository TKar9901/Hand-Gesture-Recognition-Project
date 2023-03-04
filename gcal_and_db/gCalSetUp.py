from google_auth_oauthlib.flow import InstalledAppFlow
import pickle

scopes = ["https://www.googleapis.com/auth/calendar"]

flow = InstalledAppFlow.from_client_secrets_file("client_secret.json", scopes=scopes)
credentials = flow.run_console()

pickle.dump(credentials, open("token.pkl", "wb"))
print(dir(flow))


# automatic localhost + receiver.
# flow.run_local_server()


# # launch localhost chrome browser (secure)
# import os
# os.chdir("C:\\Program Files\\Google\\Chrome\\Application")
# os.system("""cmd /c chrome.exe --remote-debugging-port=9222 --user-data-dir="C:\\Users\\RhysGray\\.wdm\\drivers\\chromedriver\\win32\\104.0.5112\\localhost" """)


# # web interaction
# import time
# from selenium import webdriver
# from webdriver_manager.chrome import ChromeDriverManager
# from selenium.webdriver.chrome.service import Service as ChromeService
# from selenium.webdriver.common.by import By
# from selenium.webdriver.common.keys import Keys
# from selenium.webdriver.support.relative_locator import locate_with

# option = webdriver.ChromeOptions()
# option.add_experimental_option("debuggerAddress", "localhost:9222")
# serv = ChromeService(executable_path="C:\\Users\\RhysGray\\.wdm\\drivers\\chromedriver\\win32\\104.0.5112\\chromedriver.exe")
# driver = webdriver.Chrome(service=serv, options=option)

# url = flow.authorization_url()[0]
# url = url[:144] + "redirect_uri=urn%3Aietf%3Awg%3Aoauth%3A2.0%3Aoob&" + url[144:]
# driver.get(url)


# # key retreival
# accounts = driver.find_elements(By.TAG_NAME, "li")
# accounts[0].click()
# time.sleep(2)
# cont = driver.find_element(locate_with(By.TAG_NAME, "button").to_left_of({By.TAG_NAME: "button"})).click()
# time.sleep(2)
# buttons = driver.find_elements(By.TAG_NAME, "button")
# buttons[2].click()
# time.sleep(2)
# # key = driver.find_element(locate_with(By.CLASS_NAME, "fD1Pid").to_left_of({By.TAG_NAME: "button"})).text
# # time.sleep(2)
# # print(key)
# driver.close()