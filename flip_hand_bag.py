#!/usr/bin/env python 

# -*- coding: latin-1 -*-
# -*- coding: iso-8859-15 -*-
# -*- coding: ascii -*-
# -*- coding: utf-8 -*-

import proxy_module
import firebug_proxy
import time
from bs4 import BeautifulSoup 
import csv
import proxy_module
from Queue import Queue
from threading import Thread
import threading
import sys
import logging



logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s (%(threadName)-2s) %(message)s',
                    )

num_fetch_threads = 15
enclosure_queue = Queue()

class parse(object):
    def __init__(self, link):
        self.link = link
        self.page, self.driver = firebug_proxy.main(self.link)


    def scroll(self):
        for i in range(0,25):
	    self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)
        
        loop =  True
     
        while loop is True:
            try:
                elem = self.driver.execute_script("window.scrollBy(0,-450)", "");
                time.sleep(1)
                elem = self.driver.find_element_by_id("show-more-results")
                elem.click()   
                time.sleep(2)  
                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(1)
            except:
                loop = False

        self.page = self.driver.page_source
        self.driver.close()

        return self.page 


    def collect_frame(self, page):
        self.page = page
        soup = BeautifulSoup(page)
        self.visual = soup.find_all("div", attrs={"class":"pu-visual-section"})
   
       
        self.data = soup.find_all("div", attrs={"class":"pu-details lastUnit"})
        #print len(self.visual)
        #print len(self.data )

        condition = threading.Condition()

        # Set up some threads to fetch the enclosures
        for i in range(num_fetch_threads):
            worker = Thread(target=self.collect_data, args=(i, enclosure_queue,))
            #worker.setDaemon(True)
            worker.start()
            logging.debug(worker)

        for visual, data in zip(self.visual, self.data):         
            enclosure_queue.put([visual, data])


    def collect_data(self,i,q):
        #visual_n_data = q.get()
        #print visual_n_data 
            
        while True:
            visual_n_data = q.get()

            visual = visual_n_data[0]
            data = visual_n_data[1]

            visual_image = visual.a.img.get("src")

            title_n_link = data.find_all("div", attrs={"class":"pu-title fk-font-13"}) 
            title = title_n_link[0].get_text()
            title_link = title_n_link[0].a.get("href")
            title_link = "http://www.flipkart.com"+str(title_link)

            page = proxy_module.main(title_link)
            soup = BeautifulSoup(page)
            page.close()
            seller_dtata = soup.find_all("a", attrs={"class":"pp-seller-badge-name fk-bold"})
            seller_name = seller_dtata[0].get_text().strip()

        
            try:
                discount = data.find_all("div", attrs={"class":"pu-discount fk-font-11"})
                discount = discount[0].get_text()
            except:
                discount = "no discount"

            final_price = data.find_all("div", attrs={"class":"pu-final"})
            final_price = final_price[0].get_text()

            colour_image_link = data.find_all("div", attrs={"class":"pu-swatch cp-item"})
            colo_image_link_list = []

            if colour_image_link:

                for  l in colour_image_link: 
                    try:
                        image_link = l.a.img.get("src")
                    except:
                        image_link = "not available"                    
                    colo_image_link_list.append(image_link)
            
                colour_image_link = ' and '.join(colo_image_link_list)

            else:
                colour_image_link = "not found"
                
            colour = data.find_all("div",attrs={"class":"fk-hidden cp-sizes"})
            clrs = []

            if colour:
                for  l in colour:     
                    clrs.append(l.div.get_text())

                clr = ' and '.join(clrs).replace(",",' and ')

            else:
                clr = "None"


            self.csv_list = [title.strip(), title_link.strip(), visual_image.strip(), discount.strip(),final_price.strip(), colour_image_link.strip(),clr.strip(), seller_name]
            logging.debug(self.csv_list)
            self.csv_fun()
            

    def csv_fun(self):
        with open('hand_bag2.csv', 'ab+') as csvfile:
            spamwriter = csv.writer(csvfile)
            spamwriter.writerow(self.csv_list)
        csvfile.close()
        

            
            
if __name__=="__main__":

    with open('hand_bag2.csv', 'ab+') as csvfile:
        spamwriter = csv.writer(csvfile)
        spamwriter.writerow( ["title", "title_link", "visual_image", "discount", "final_price", "colour_image_link", "clr", "seller_name"])
    csvfile.close()

    link = "http://www.flipkart.com/bags-wallets-belts/bags/hand-bags/pr?sid=reh%2Cihu%2Cm08"

    obj = parse(link)
    page = obj.scroll()

    f = open("sourse_code2.html","w+")
    html = page.encode("ascii", "ignore")
    print >>f, html
    f.close()
     
    
    '''f = open("sourse_code2.html")
    html = f.read().encode("ascii", "ignore")
    f.close()'''

    page = page.encode("ascii", "ignore")
    obj.collect_frame(page)
