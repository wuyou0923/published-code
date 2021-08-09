from selenium import webdriver
from selenium.webdriver.common.by import By  # By.ID,By.CSS_SELECTOR
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
import time
import xlrd
import xlwt
from bs4 import BeautifulSoup
driver=webdriver.Chrome()
data = xlrd.open_workbook('sourceFile/31_Compounds_2.xlsx')
table = data.sheet_by_index(0)
pert_id = table.col_values(0)
i = 1
col_i=1
workbook = xlwt.Workbook(encoding='utf-8')
booksheet = workbook.add_sheet('Sheet 1', cell_overwrite_ok=True)
cas = None
name_div = None
timeStr=str(time.strftime('%m-%d %H-%M', time.localtime(time.time())))
while True:
    if(i>=len(pert_id)):
        break
    try:
        name_div=-2
        url='https://pubchem.ncbi.nlm.nih.gov/#query='
        urlTarget=url+str(pert_id[i])
        i += 1
        col_i+=1
        booksheet.write(col_i - 2, 0,i - 1)
        booksheet.write(col_i - 2, 1, pert_id[i-1])
        driver.get(urlTarget)
        print("No."+str(i-1))
        try:
            WebDriverWait(driver, 4).until(EC.presence_of_element_located((By.CLASS_NAME, "highlight")))
            driver.find_element_by_class_name("highlight").click()
        except:
            print("Not highlight")
            try:
                driver.find_elements_by_class_name("capitalized")[1].click()
            except:
                print("Not capitalized")
        WebDriverWait(driver, 4).until(EC.presence_of_element_located((By.CLASS_NAME, "p-sm-top")))

        MeSH = driver.find_element_by_id('MeSH-Entry-Terms').get_attribute("innerHTML")
        bs = BeautifulSoup(MeSH, "html.parser")

        columns=bs.find("div",class_="columns")
        for item in columns.find_all("p"):
            col_i+=1
            booksheet.write(col_i - 2, 2, item.get_text())
        workbook.save('resultFile/PubChemMeSH'+timeStr+'.xls')
        col_i+=1
    except:
        col_i+=1
        workbook.save('resultFile/PubChem'+timeStr+'.xls')
        print("Not find")
driver.close()
