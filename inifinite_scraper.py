import sys
from PyQt5.QtWidgets import QApplication,QWidget,QPushButton,QLineEdit,QInputDialog,QColorDialog,QFrame,QSizePolicy,QLabel,QFontDialog,QComboBox
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
import time
import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
from selenium.webdriver.common.action_chains import ActionChains
from importlib import reload
m=0
df=pd.DataFrame({"project_name":[],
"area":[],
"latitude":[],
"longitude":[],
"type":[],
"price":[],
"sqft_price":[],
"sell_rent":[],
"furnished":[],
"contact_person":[],
"sqft":[],
"bedroom":[]
})
df1=pd.DataFrame({"project_name":[],
"area":[],
"latitude":[],
"longitude":[],
"type":[],
"price":[],
"sqft_price":[],
"sell_rent":[],
"contact_person":[],
"sqft":[],
"bedroom":[]
})


class example(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
    def initUI(self):
        self.btn=QPushButton('City',self)
        self.btn.move(20,20)
        self.btn.clicked.connect(self.showdialog)

        self.le=QLineEdit(self)
        self.le.move(250,22)

        self.btn1 = QPushButton('Locality', self)
        self.btn1.move(20, 50)

        self.btn1.clicked.connect(self.showdialog1)
        self.le1=QLineEdit(self)
        self.le1.move(250,52)

        self.lbl = QLabel('Output file type: ', self)
        self.lbl.move(20, 80)

        self.combo = QComboBox(self)
        self.combo.addItems(["Excel","JSON","CSV"])
        self.combo.move(250,82)
        
        self.combo1 = QComboBox(self)
        self.combo1.addItems(["Buy","Rent"])
        self.combo1.move(330,82)

        self.btn2 = QPushButton('Convert', self)
        self.btn2.setSizePolicy(QSizePolicy.Fixed,
            QSizePolicy.Fixed)
        self.btn2.setDisabled(True)

        self.btn2.move(300, 120)
        self.btn2.clicked.connect(self.showdialog2)

        self.btn3 = QPushButton('MagicBricks', self)
        self.btn3.setSizePolicy(QSizePolicy.Fixed,
            QSizePolicy.Fixed)

        self.btn3.move(20, 120)
        self.btn3.clicked.connect(self.processor1)

        self.btn4 = QPushButton('99Acres', self)
        self.btn4.setSizePolicy(QSizePolicy.Fixed,
            QSizePolicy.Fixed)

        self.btn4.move(150, 120)
        self.btn4.clicked.connect(self.processor2)

        self.lbl1 = QLabel('                                                           ', self)
        self.lbl1.move(220, 160)

        self.setGeometry(500,500,500,200)
        self.setWindowTitle('Data Scraper')
        self.show()
    def showdialog(self):
        text,ok=QInputDialog.getText(self,'City',"Which city's data are you looking for?" )
        if ok:
            self.le.setText(str(text))
    def showdialog1(self):
        text,ok=QInputDialog.getText(self,'DataFrame','Which locality?' )
        if ok:
            self.le1.setText(str(text))
    def showdialog2(self):

        text,ok=QInputDialog.getText(self,'address','Address of the output file with file name?' )
        if ok:
            if self.combo.currentIndex()==0:
                address=text+'.xls'
                if m==0:
                    df.to_excel(address)
                else:
                    df1.to_excel(address)
                self.lbl1.setText("saved as Excel file!")
            elif self.combo.currentIndex()==1:
                address=text+'.json'
                if m==0:
                    df.to_json(address)
                else:
                    df1.to_json(address)
                self.lbl1.setText("saved as JSON file!")
            else:
                address=text+'.csv'
                if m==0:
                    df.to_csv(address)
                else:
                    df1.to_csv(address)
                self.lbl1.setText("saved as CSV file!")
    def processor1(self):
        global df
        types=["Multistorey-Apartment","Builder-Floor-Apartment","Penthouse","Studio-Apartment","Residential-House","Villa"]
        driver=webdriver.Firefox()


        for typeh in types:
            if self.combo1.currentIndex()==1:
                driver.get("http://www.magicbricks.com/property-for-rent/residential-real-estate?proptype="+typeh+"&Locality="+(self.le1.text()).replace(" ","-")+"&cityName="+self.le.text())
            else:
                driver.get("http://www.magicbricks.com/property-for-sale/residential-real-estate?proptype="+typeh+"&Locality="+(self.le1.text()).replace(" ","-")+"&cityName="+self.le.text())
            end=0
            first=1
            lastHeight = driver.execute_script("return document.body.scrollHeight")
            while True:
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(2)
                newHeight = driver.execute_script("return document.body.scrollHeight")
                if newHeight == lastHeight:
                    break
                lastHeight = newHeight
                self.lbl1.setText("Scrolling")
            self.lbl1.setText("End of scroll")
            soup=BeautifulSoup(driver.page_source)
            if self.combo1.currentIndex()==1:
                samples = soup.find_all("div", "srpBlockListRow srpRentListRow srcShadow property-sticky-link animDef   ")
            else:    
                samples = soup.find_all("div", "SRCard")
            try:
                page=driver.find_element_by_class_name("pageNos").find_elements_by_tag_name("a")[-1]
                if page.get_attribute("class")=="toc":
                    page.click()
                    first=0
                    time.sleep(10)
                    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                else:
                    first=0
                    end=1
            except NoSuchElementException:
                    first=0
                    end=1

            for sample in samples:
                project=sample.find_all("input")[12]["value"]
                area=sample.find_all("span","localityFirst")[0].contents[0]
                if self.combo1.currentIndex()==0:
                    latitude=sample.find_all("div","iconMap")[0].a["data-link"]
                    no=latitude.find("lat")
                    latitude=latitude[no+4:no+13]
                    longitude=sample.find_all("div","iconMap")[0].a["data-link"]
                    no=longitude.find("longt")
                    longitude=longitude[no+6:no+15]
                else:
                     latitude=sample.find_all("a","Rent-SeeOnMapLink stop-propagation")[0]["data-link"]
                     no=latitude.find("lat")
                     latitude=latitude[no+4:no+13]
                     longitude=sample.find_all("a","Rent-SeeOnMapLink stop-propagation")[0]["data-link"]
                     no=longitude.find("longt")
                     longitude=longitude[no+6:no+15]
                    
                price=sample.find_all("span","proPriceField")[0].contents[0]
                bedroom=sample.find_all("a","property-sticky-link")[0].input["value"]
                try:
                    if self.combo1.currentIndex()==0:
                        sqft=sample.find_all("b","areaValue")[0].contents[0]
                    else:
                        sqft=sample.find_all("input")[18]["value"]
                        
                except IndexError:
                    sqft="not available"
                try:
                    sqft_price=sample.find_all("span","sqrPriceField")[0].contents[1]
                except IndexError:
                    sqft_price="not available"
                furnished=sample.find_all("input")[5]["value"]
                sell_rent=sample.find_all("input")[0]["value"]
                contact=sample.find_all("input")[13]["value"]
                if (df == np.array([area,bedroom,contact,furnished,latitude,longitude,price,project,sell_rent,sqft,sqft_price,typeh])).all(1).any():
                    self.lbl1.setText("rejected")
                else:
                    self.lbl1.setText("added row no "+str(len(df)))
                    df.loc[len(df)]=[area,bedroom,contact,furnished,latitude,longitude,price,project,sell_rent,sqft,sqft_price,typeh]
            try:
                page=driver.find_element_by_class_name("pageNos").find_elements_by_tag_name("a")[-1]
                time.sleep(10)
                while(end==0):
                    if first==1:
                        driver.find_element_by_class_name("pageNos").find_elements_by_tag_name("a")[-1].click()
                    time.sleep(10)
                    lastHeight = driver.execute_script("return document.body.scrollHeight")
                    while True:
                        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                        time.sleep(2)
                        newHeight = driver.execute_script("return document.body.scrollHeight")
                        if newHeight == lastHeight:
                            break
                        lastHeight = newHeight
                        self.lbl1.setText("Scrolling")
                    self.lbl1.setText("End of scroll")
                    soup=BeautifulSoup(driver.page_source)
                    if self.combo1.currentIndex()==1:
                        samples = soup.find_all("div", "srpBlockListRow srpRentListRow srcShadow property-sticky-link animDef   ")
                    else:    
                        samples = soup.find_all("div", "SRCard")
                    try:
                        page=driver.find_element_by_class_name("pageNos").find_elements_by_tag_name("a")[-1]
                        if page.get_attribute("class")=="toc":
                            page.click()
                            first=0
                            time.sleep(10)
                            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                        else:
                            first=0
                            end=1
                    except NoSuchElementException:
                        first=0
                        end=1


                    for sample in samples:
                        project=sample.find_all("input")[12]["value"]
                        area=sample.find_all("span","localityFirst")[0].contents[0]
                        if self.combo1.currentIndex()==0:
                            latitude=sample.find_all("div","iconMap")[0].a["data-link"]
                            no=latitude.find("lat")
                            latitude=latitude[no+4:no+13]
                            longitude=sample.find_all("div","iconMap")[0].a["data-link"]
                            no=longitude.find("longt")
                            longitude=longitude[no+6:no+15]
                        else:
                            latitude=sample.find_all("a","Rent-SeeOnMapLink stop-propagation")[0]["data-link"]
                            no=latitude.find("lat")
                            latitude=latitude[no+4:no+13]
                            longitude=sample.find_all("a","Rent-SeeOnMapLink stop-propagation")[0]["data-link"]
                            no=longitude.find("longt")
                            longitude=longitude[no+6:no+15]
                        price=sample.find_all("span","proPriceField")[0].contents[0]
                        bedroom=sample.find_all("a","property-sticky-link")[0].input["value"]
                        try:
                            if self.combo1.currentIndex()==0:
                                sqft=sample.find_all("b","areaValue")[0].contents[0]
                            else:
                                sqft=sample.find_all("input")[18]["value"]
                        except IndexError:
                            sqft="not available"
                        try:
                            sqft_price=sample.find_all("span","sqrPriceField")[0].contents[1]
                        except IndexError:
                            sqft_price="not available"
                        furnished=sample.find_all("input")[5]["value"]
                        sell_rent=sample.find_all("input")[0]["value"]
                        contact=sample.find_all("input")[13]["value"]
                        if (df == np.array([area,bedroom,contact,furnished,latitude,longitude,price,project,sell_rent,sqft,sqft_price,typeh])).all(1).any():
                            self.lbl1.setText("rejected")
                        else:
                            self.lbl1.setText("added row no "+str(len(df)))
                            df.loc[len(df)]=[area,bedroom,contact,furnished,latitude,longitude,price,project,sell_rent,sqft,sqft_price,typeh]



            except NoSuchElementException:
                continue
        self.btn2.setEnabled(True)
        self.lbl1.setText("Data is extracted!")
        global m
        m=0
        driver.quit()

    def processor2(self):
        global df1
        driver=webdriver.Firefox()
        actions = ActionChains(driver)
        driver.get("http://www.99acres.com/")
        if self.combo1.currentIndex()==1:
            driver.find_element_by_id("ResRentTab").click()
        end=0
        driver.find_element_by_id("keyword").clear()
        time.sleep(5)
        actions.send_keys(self.le1.text()+", "+self.le.text())
        actions.perform()
        time.sleep(5)
        driver.find_element_by_id("suggestions_custom").find_element_by_tag_name("a").click()
        driver.find_element_by_id("submit_query").click()
        time.sleep(10)
        soup=BeautifulSoup(driver.page_source)
        samples = soup.find_all("div", "srpWrap")    
                    
        try:
            page=driver.find_element_by_class_name("pgdiv").find_elements_by_tag_name("a")[-1]
            if page.get_attribute("class")=="pgselActive":
                page.click()
            else:
                end=1
        except NoSuchElementException:
                end=1
        
        for sample in samples:    
            project=sample.find_all("i","uline")[0]["data-bldname"]
            try:
                area=sample.find_all("meta",itemprop="addressLocality")[0]["content"]
            except IndexError:
                area="Malleshwaram"
            try:    
                typeh=sample.find_all("meta",itemprop="name")[0]["content"]
            except IndexError:
                typeh="unknown"
            latitude=sample.find_all("i","uline")[0]["data-maplatlngzm"]
            latitude=latitude[0:9]
            longitude=sample.find_all("i","uline")[0]["data-maplatlngzm"]
            longitude=longitude[24:34]
            price=str(sample.find_all("i","uline")[0]["data-price"])
            no=price.find(",")
            price=price[:no]
            bedroom=sample.find_all("i","uline")[0]["data-bedrm"]
            sqft=sample.find_all("i","uline")[0]["data-area"]
            no=sqft.find(",")
            no1=sqft[no+1:].find(",")
            sqft=sqft[no+1:no1+no+1]
            sqft_price=(str(sample.find_all("div","srpDataWrap")[0].span.contents[-1])).replace("<b>","").replace("</b>","")
            a=sample.find_all("div","srpDataWrap")[0].contents
            for b in a:
                if "Highlights" in str(b):
                    b=str(b)
                    no=b.find("</")
                    no1=(b[no+2:]).find("</")
                    sell_rent=b[no+14:no1+no+2]
                    sell_rent=sell_rent.replace(">","")
                    no=sell_rent.find("x")
                    sell_rent=sell_rent[:no]
                    
                
            contact=sample.find_all("a","srpBlue f13 mr10 lf cntClk")[0]["data-cl"]
            try:
                array=np.array([area,bedroom,contact,latitude,longitude,price,project,sell_rent,sqft,sqft_price,typeh])
            except ValueError:
                pass
            if (df1 == array ).all(1).any():
                self.lbl1.setText("rejected")
            else:
                self.lbl1.setText("added row no "+str(len(df)))    
                df1.loc[len(df1)]=[area,bedroom,contact,latitude,longitude,price,project,sell_rent,sqft,sqft_price,typeh]
                       
        try:
            while(end==0):
                time.sleep(10)
                soup=BeautifulSoup(driver.page_source)
                samples = soup.find_all("div", "srpWrap")
                try:
                    page=driver.find_element_by_class_name("pgdiv").find_elements_by_tag_name("a")[-1]
                    if page.get_attribute("class")=="pgselActive":
                        page.click()
                    else:
                        end=1
                except NoSuchElementException:
                    end=1
                
            
                for sample in samples:    
                    project=sample.find_all("i","uline")[0]["data-bldname"]
                    try:
                        area=sample.find_all("meta",itemprop="addressLocality")[0]["content"]
                    except IndexError:
                        area="Malleshwaram"
                    try:    
                        typeh=sample.find_all("meta",itemprop="name")[0]["content"]
                    except IndexError:
                        typeh="unknown"
                    latitude=sample.find_all("i","uline")[0]["data-maplatlngzm"]
                    latitude=latitude[0:9]
                    longitude=sample.find_all("i","uline")[0]["data-maplatlngzm"]
                    longitude=longitude[24:34]
                    price=str(sample.find_all("i","uline")[0]["data-price"])
                    no=price.find(",")
                    price=price[:no]
                    bedroom=sample.find_all("i","uline")[0]["data-bedrm"]
                    sqft=sample.find_all("i","uline")[0]["data-area"]
                    no=sqft.find(",")
                    no1=sqft[no+1:].find(",")
                    sqft=sqft[no+1:no1+no+1]
                    sqft_price=(str(sample.find_all("div","srpDataWrap")[0].span.contents[-1])).replace("<b>","").replace("</b>","")
                    a=sample.find_all("div","srpDataWrap")[0].contents
                    for b in a:
                        if "Highlights" in str(b):
                            b=str(b)
                            no=b.find("</")
                            no1=(b[no+2:]).find("</")
                            sell_rent=b[no+13:no1+no+2]
                            sell_rent=sell_rent.replace(">","")
                            no=sell_rent.find("x")
                            sell_rent=sell_rent[:no]
                        
                    contact=sample.find_all("a","srpBlue f13 mr10 lf cntClk")[0]["data-cl"]
                    try:
                        array=np.array([area,bedroom,contact,latitude,longitude,price,project,sell_rent,sqft,sqft_price,typeh])
                    except ValueError:
                        pass
                    if (df1 == array ).all(1).any():
                        self.lbl1.setText("rejected")
                    else:
                        self.lbl1.setText("added row no "+str(len(df)))    
                        df1.loc[len(df1)]=[area,bedroom,contact,latitude,longitude,price,project,sell_rent,sqft,sqft_price,typeh]    
                        
        except NoSuchElementException:
            pass
        self.btn2.setEnabled(True)
        self.lbl1.setText("Data is extracted!")
        global m
        m=1
        driver.quit()




app=QApplication(sys.argv)
e=example()
sys.exit(app.exec_())