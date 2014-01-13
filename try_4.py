#!/usr/bin/env python 

# -*- coding: latin-1 -*-
# -*- coding: iso-8859-15 -*-
# -*- coding: ascii -*-
# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup 
import proxy_module
import csv


def in_file(data):
    with open('eggs.csv', 'ab+') as csvfile:
        spamwriter = csv.writer(csvfile, dialect='excel', delimiter=' ',quotechar='|', quoting=csv.QUOTE_MINIMAL)
        spamwriter.writerow(data)
    csvfile.close()  


def main2(num):
    num = str(num)
 
    main_link ="http://www.flipkart.com/bags-wallets-belts/bags/hand-bags/pr?p[]=facets.ideal_for%255B%255D%3DWomen&p[]=sort%3Dpopularity&sid=reh%2Cihu%2Cm08&facetOrder[]=ideal_for&otracker=nmenu_sub_women_0_Handbags"
   
    link = "http://www.flipkart.com/bags-wallets-belts/bags/hand-bags/pr?p[]=facets.ideal_for%255B%255D%3DWomen&p[]=sort%3Dpopularity&sid=reh%2Cihu%2Cm08&start="+num+"&ajax=true"
    page = proxy_module.main(link)
    st = page.read()
    st = st.replace("&lt;","<")
    st = st.replace("&gt;",">")
    st = st.replace("&quot;",'"')
    soup = BeautifulSoup(st)
    details = soup.find_all("div",attrs={"class":"pu-details lastUnit"})  
    if details:
        for l in details:  
            link = str(l.div.a.get("href"))
            link = "http://www.flipkart.com"+link
            title = str(l.div.a.get("title"))          
            discount = l.find("div", attrs={"class":"pu-discount fk-font-11"})
            if discount:
                dis = discount.span.get_text()
            else:
                dis = "None"              
            final_price = l.find("div",attrs={"class":"pu-final"})
            final_price = final_price.span.get_text()
            colour = l.find_all("div",attrs={"class":"fk-hidden cp-sizes"})
            clrs = []
            if colour:
                for  l in colour:
                    clr = l.div.get_text()
                    clrs.append(clr)
            else:
                clr = "None"
            clr = ','.join(clrs)
                   
        collection = [main_link, title,link, dis,final_price,clr]
        in_file(collection)
         



def  main():
   
    collection =["main_link", "title","sub_link", "actual_price","final_price","colours"]
    in_file(collection)
    link ="http://www.flipkart.com/bags-wallets-belts/bags/hand-bags/pr?p[]=facets.ideal_for%255B%255D%3DWomen&p[]=sort%3Dpopularity&sid=reh%2Cihu%2Cm08&facetOrder[]=ideal_for&otracker=nmenu_sub_women_0_Handbags"
    page = proxy_module.main(link)
    soup = BeautifulSoup(page)
    data = soup.find_all("span",attrs={"class":"items"})
    number  = data[0].get_text()
    number = number.strip()
    number = int(number)
    for  num in range(1,number,15):
        main2(num)


if __name__=="__main__":
    main()
    
    
