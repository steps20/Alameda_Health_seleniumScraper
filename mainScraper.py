import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from openpyxl import Workbook, load_workbook
import time
import xlsxwriter


#initilization of variables and web driver  
realUrl = "https://forms.alamedahealthsystem.org/salary/"
fileName = input("File save as: ")
keyword = input("Enter your search term: ")

options = Options()
options.headless = False

driver = webdriver.Chrome(options=options)
driver.get(realUrl)

driver.find_element(by=By.XPATH, 
	value="//*[@id='root']/div/div/div/div[1]/div/div/input"
	).send_keys(
    keyword, 
    Keys.ENTER
)

#excel workbook stuff
wb = xlsxwriter.Workbook(str(fileName)+".xlsx")
worksheet = wb.add_worksheet("firstSheet")
valueList = ['Job Title', 'Exempt', 'Union Code', 'Pay Grade', 'Effective Date', 'Range 1',
			'Range 2', 'Range 3', 'Range 4', 'Range 5', 'Range 6', 'Range 7', 'Range 8', 'Range 9', 
			'Range 10', 'Range 11', 'Range 12', 'Range 13', 'Range 14', 'Range 15', 'Range 16', 'Range 17',
			'Range 18', 'Range 19', 'Min', 'Mid', 'Max']

#Create the labels on the top row
for i in range (0 ,27):
	worksheet.write(0, i, str(valueList[i]))

#sleep is for load time
time.sleep(3)


mainCounter = 1

#main loop
while(True):
	mainCounter = mainCounter + 1
	try:
		caret =driver.find_element(by=By.XPATH,
			value="/html/body/div/div/div/div/div[2]/div/div["+str(mainCounter)+"]/div/div/div/div")
					
		caret.click()

	except:
		break

	#time to load + reseting variables
	time.sleep(1)
	pointer = 1
	hourlyList = []
	listofAll = []
	jobTitle = driver.find_element(by=By.XPATH,
		value="/html/body/div/div/div/div/div[2]/div/div["+str(mainCounter)+"]/div/div/div/div/strong").get_attribute("innerHTML")

	#puts hourly income into an array
	while(True):
		try:
			incomeHourly = driver.find_element(by=By.XPATH,
				value="/html/body/div/div/div/div/div[2]/div/div["+str(mainCounter)+"]/div/div[2]/div/div[2]/table/tbody/tr["+str(pointer)+"]/td[2]").get_attribute("innerHTML")
		
		except:
			break

		else:
			hourlyList.append(str(incomeHourly))
			pointer = pointer + 1

	#gets other job details html
	jobMData = driver.find_element(by=By.XPATH,
		value="/html/body/div/div/div/div/div[2]/div/div["+str(mainCounter)+"]/div/div[2]/div/div[1]").get_attribute("textContent")

	#splits the html into usable data
	dataList = jobMData.split(":")
	exemptData = dataList[1][1:len(dataList[1])-10]
	unionCode = dataList[2][1:len(dataList[1])-9]
	payGrade = dataList[3][1:len(dataList[3])-(14)]
	effectiveDate = dataList[4][2:]
	

	#writing data to excel
	worksheet.write((mainCounter-1), 0, str(jobTitle))
	worksheet.write((mainCounter-1), 1, str(exemptData))
	worksheet.write((mainCounter-1), 2, str(unionCode))
	worksheet.write((mainCounter-1), 3, str(payGrade))
	worksheet.write((mainCounter-1), 4, str(effectiveDate))
	p = 0
	#hourly pay
	if (len(hourlyList) == 3):
		worksheet.write((mainCounter-1), 24, str(hourlyList[0]))
		worksheet.write((mainCounter-1), 25, str(hourlyList[1]))
		worksheet.write((mainCounter-1), 26, str(hourlyList[2]))
	else:
		for i in range(len(hourlyList)):
			worksheet.write((mainCounter-1), i+5, str(hourlyList[i]))
	
	caret.click()
	time.sleep(1)

wb.close()
print("Done")
driver.quit()
