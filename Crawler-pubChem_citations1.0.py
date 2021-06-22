from selenium import webdriver  # 用来驱动浏览器的
from selenium.webdriver.common.by import By  # 按照什么方式查找，By.ID,By.CSS_SELECTOR
from selenium.webdriver.support import expected_conditions as EC  # 和下面WebDriverWait一起用的
from selenium.webdriver.support.wait import WebDriverWait  # 等待页面加载某些元素
import time
import xlrd
# import xlwt
import requests
driver=webdriver.Chrome()
data = xlrd.open_workbook('sourceFile/待补充的5个化合物.xlsx')
table = data.sheet_by_index(0)
pert_id = table.col_values(0)
pert_id_name = table.col_values(1)
i = 1
#workbook = xlwt.Workbook(encoding='utf-8')
#booksheet = workbook.add_sheet('Sheet 1', cell_overwrite_ok=True)
cas = None
name_div = None
timeStr=str(time.strftime('%m-%d %H-%M', time.localtime(time.time())))
while True:

    if(i>=len(pert_id)):
        break

    try:

        cas=-2
        name_div=-2
        url='https://pubchem.ncbi.nlm.nih.gov/#query='
        urlTarget=url+str(pert_id_name[i])
        i += 1
        #booksheet.write(i - 2, 0, pert_id[i-1])
        driver.get(urlTarget)
        print("No."+str(i-1)+str(pert_id[i]))
        try:
            WebDriverWait(driver, 4).until(EC.presence_of_element_located((By.CLASS_NAME, "highlight")))
            driver.find_element_by_class_name("highlight").click()
        except:
            print("Not highlight")
            try:
                driver.find_elements_by_class_name("capitalized")[1].click()

            except:
                print("Not capitalized")

        #currrntUrl=driver.current_url
        #time.sleep(1)
        #driver.get(currrntUrl+"#section=CAS")
        current_url=driver.current_url#获取当前页面的网址
        time.sleep(2)
        #WebDriverWait(driver, 4).until(EC.presence_of_element_located((By.CLASS_NAME, "p-sm-top")))
        #name_div = driver.find_element_by_class_name("p-sm-top").get_attribute("textContent")
        print(name_div)
        #booksheet.write(i-2, 2, name_div)
        try:
            cas = driver.find_element_by_xpath('//*[@id="CAS"]/div[2]/div[1]/p').get_attribute("textContent")
        except:
            print("CAS没有找到")
            cas=""
        #booksheet.write(i - 2, 1, cas)
        #driver.get(current_url+"#section=Depositor-Provided-PubMed-Citations")
        driver.get(current_url+"#section=Depositor-Supplied-Patent-Identifiers")

        time.sleep(3)
        driver.find_element_by_id('Depositor-Supplied-Patent-Identifiers').find_element_by_id("Download").click()
        #WebDriverWait(driver, 4).until(EC.presence_of_element_located((By.CLASS_NAME, "button.with-padding-small.with-border")))
        time.sleep(1)
        filehref=driver.find_element_by_class_name("button.with-padding-small.with-border").get_attribute("href")
        file=requests.get(filehref).content
        print(filehref)
        print(pert_id[i-1])
        #with open("patent/" +pert_id[i-1]+"_"+cas+"_"+pert_id_name[i-1]+".csv", "wb") as f:
        with open("result_patent/" + pert_id[i - 1] + "_" + cas + "_" + pert_id_name[i - 1] + ".csv", "wb") as f:
            f.write(file)
       # workbook.save('resultFile/PubChem'+timeStr+'.xlsx')



    except:

        # booksheet.write(i - 2, 2, name_div)
        # booksheet.write(i - 2, 1, cas)

       # workbook.save('resultFile/PubChem'+timeStr+'.xlsx')
        print("Not find")

driver.close()