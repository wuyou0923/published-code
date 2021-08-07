# -*- coding: utf-8 -*-

import time

import requests
import xlrd
import xlwt
from bs4 import BeautifulSoup
import math

headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36'}

#baseUrl : the website
baseUrl="https://pubmed.ncbi.nlm.nih.gov/?term="
#Compound list : please make sure it was stored in this directory
data = xlrd.open_workbook('sourceFile/2 Compounds.xlsx')
resultFileName="resultFile/Pubmed"
table = data.sheet_by_index(0)
compd_name = table.col_values(0)
i = 1
workbook = xlwt.Workbook(encoding='utf-8')
booksheet = workbook.add_sheet('Sheet 1', cell_overwrite_ok=True)

timeStr=str(time.strftime('%m-%d %H-%M', time.localtime(time.time())))
subtitles=["influenza","antiviral"]
currentb=0 # 0: influenza，1: antiviral

booksheet.write(0, 0, "No.")
booksheet.write(0, 1, "Name")
booksheet.write(0, 2, "The number of entries")
booksheet.write(0, 3, "Title")
booksheet.write(0, 4, "Abstract")
a = 1

while True:
    print("Working......................................................................................No."+str(i))
    if(i>=len(compd_name)):
        break
    # resp: returned result
    try:
        # a += 1
        currentName=compd_name[i]+"+"+subtitles[currentb]
        print(str(currentName))
        resp=requests.get(baseUrl+"("+compd_name[i]+"[Title/Abstract])+AND+("+subtitles[currentb]+"[Title/Abstract])",headers=headers)
        resp.encoding='utf-8'  #Setting utf-8
        bs=BeautifulSoup(resp.text,"html.parser")
        booksheet.write(a, 0, i)
        booksheet.write(a, 1, currentName)


        currenti = i
        i += 1

        # try:
        #     em = bs.find("em", class_="altered-search-explanation query-error-message").get_text()
        #     print(em)
        #     booksheet.write(a, 2, "No Result")
        # except:
        #     print("Normal")
        try:


            title = bs.find("h1", class_="heading-title").get_text().replace("\n", "").replace("\r", "").replace(
                "                          ", "")
            print(str(currentName)+"the only one")
            booksheet.write(a, 2, 1)
            booksheet.write(a, 3, title)

            print(title)
            Abstract = bs.find("div", class_="abstract-content selected").get_text().replace("\n", "").replace("\r",
                                                                                                                  "")
            print(Abstract)

            booksheet.write(a, 4, Abstract)


        except:
            print(str(currentName)+" more than 1")

        titleList = bs.find("div",class_="search-results-chunks")
        amountPapers=bs.find("div", class_="results-amount").get_text().strip().replace("results", "").replace("\n", "").replace("\r", "").replace(" ", "").replace(",", "")

        print(str(currentName) +" find " + str(amountPapers) )
        booksheet.write(a, 2, amountPapers)
        amountPages=math.ceil(int(amountPapers) / 10)

        print("In total："+str(amountPages)+" pages")

        amountPages = 10 if amountPages > 10 else amountPages
        for y in range(1, amountPages + 1):
            if (y > 1):
                print(str(baseUrl + pert_id[currenti] + subtitles[currentb] + "&page=" + str(y)))
                resp = requests.get(
                    baseUrl + "(" + pert_id[currenti] + "[Title/Abstract])+AND+(" + subtitles[currentb] + "[Title/Abstract])"+ "&page=" + str(y),
                    headers=headers)
                #resp = requests.get(baseUrl + pert_id[currenti] + subtitles[currentb] + "&page=" + str(y), headers=headers)
                resp.encoding = 'utf-8'
                bs = BeautifulSoup(resp.text, "html.parser")
                titleList = bs.find("div", class_="search-results-chunks")
            try:
                p = 1 + (y - 1) * 10
                for full_docsum in titleList.find_all("article", class_="full-docsum"):
                    try:
                        print("Finding：" + str(currentName) + " No." + str(p) + " article")
                        currentp=p
                        currenta = a
                        a += 1
                        p += 1
                        href = full_docsum.find("a", class_="docsum-title").get("href")
                        respnew = requests.get("https://pubmed.ncbi.nlm.nih.gov" + href, headers=headers)
                        bsnew = BeautifulSoup(respnew.text, "html.parser")
                        # WebDriverWait(driver, 4).until(EC.presence_of_element_located((By.CLASS_NAME, "heading-title")))
                        title = bsnew.find("h1", class_="heading-title").get_text().replace("\n", "").replace("\r",
                                                                                                              "").replace(
                            "                          ", "")
                        booksheet.write(currenta, 3, title)


                        print(title)
                        Abstract = bsnew.find("div", class_="abstract-content selected").get_text().replace("\n",
                                                                                                            "").replace(
                            "\r", "")
                        print(Abstract)

                        booksheet.write(currenta, 4, Abstract)

                        workbook.save(resultFileName + timeStr + '.xls')


                    except:
                        workbook.save(resultFileName + timeStr + '.xls')
                        print(str(currentName) + " No." + str(currentp) + "without abstract")
            except:
                workbook.save(resultFileName + timeStr + '.xls')
                print("No." + str(i) + "  " + str(currentName) + ": Not found")


    except :

        workbook.save(resultFileName + timeStr + '.xls')
        a+=1
        print("No."+str(i)+"  "+str(currentName)+ ":ERROR")


workbook.save(resultFileName + timeStr + '.xls')
