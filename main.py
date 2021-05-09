from bs4 import BeautifulSoup
import requests
import lxml
import csv


def get_coins():
    result=[]                                               #for storing the results
    obj=requests.get('https://coinmarketcap.com/').text     #collecting the website using requests
    main=BeautifulSoup(obj,'lxml')                          #creating a beautiful soups object 
    result.append(['Name','Symbol','Url'])

    body=main.body.tbody

    count=0                                                 

    #since all the data about the coins is stored in <tr> tags 
    #therefore iterating over each tr tag
    for row in body.find_all('tr'):
        #required data is stored in a anchor tag
        #creating a object for anchor tag
        obj=row.find('a',class_="cmc-link")
        #finding link       
        link=obj['href']
        base='https://coinmarketcap.com'                   #base url for each coin specific url
        #final url 
        url=base+link

        
        #because upto 10th coin data is stored as div and on later coins it is stored in a span
        if count<10:        
            name=obj.find('p',class_="sc-1eb5slv-0 iJjGCS").text    #found the class by inspecting  
            symbol=obj.find('p',class_="sc-1eb5slv-0 gGIpIK coin-item-symbol").text

        else:
            spanlist=obj.find_all('span')                 #a list for all span tag in the a tag
            name=spanlist[1].text                         #coin name is in 2nd span tag
            symbol=spanlist[2].text                       #coin symbol is in 3rd span tag

        
        result.append([name,symbol,url])

        count=count+1
        #print(name,symbol,url)
        if(count>49):
            break


    
    
    #writing the result in csv file
    with open('coins.csv', 'w') as csvfile: 
        # creating a csv writer object 
        csvwriter = csv.writer(csvfile)
        for values in result:
            csvwriter.writerow(values)
    


  
def get_coin_data(var):

    var=var.capitalize()
    basic=0
    with open('coins.csv','r') as csv_file:
        csv_reader=csv.reader(csv_file)
        
        for row in csv_reader:
            if row[0]==var:
                #print("ok")
                basic=row[2]
        csv_file.close()


    website=requests.get(basic).text
    html=BeautifulSoup(website,'lxml')
    
    heading=['Name','Symbol','Watchlist_count','Website_url','Supply','Price','volume','Market_domi.','Rank',
                'Market_cap','all_time_high_date','all_time_high_price','all_time_low_date','all_time_low_price']

    values=[]
    body=html.body

    #for 1st and 2nd task name and symbol
    for12=body.find('div',class_="sc-16r8icm-0 bbpCfl nameSection___3Hk6F")
    name=for12.find('h2').text
    values.append(name)


    symbol=for12.find('small').text
    values.append(symbol)

    #watchlist
    watchlists=for12.find_all('div',class_="namePill___3p_Ii")
    watchlist=watchlists[2].text
    watchlist=watchlist.split(' ')
    watchlist=watchlist[1]
    values.append(watchlist)

    #website_url
    for3=body.find('div',class_="sc-16r8icm-0 iiNgcJ linksSection___2uV91")
    website_url=for3.find('a',class_="button___2MvNi",target="_blank")
    website_url=website_url['href']
    values.append(website_url)

    #circulating supply
    for4=body.find('div',class_="statsSupplyBlock___ST_Wb")
    circulating_supply=for4.find('div',class_="supplyBlockPercentage___1g1SF").text
    values.append(circulating_supply)

    #for 5 to 13
    for5to13=body.find('div',class_="sc-16r8icm-0 frLsAa container___E9axz")
    divisons=for5to13.find_all('div',class_="sc-16r8icm-0 fIhwvd")
    #for 6 to 9
    div1=divisons[0]
    tablelist1=div1.find_all('tr')
    #price(6th task)
    price=tablelist1[0].text.split(' ')[1]
    values.append(price)
    #volume/market cpa(7th task)
    volume=tablelist1[4].text.split('p')[1]
    values.append(volume)
    #market dominance(8th task)
    market_dominance=tablelist1[5].span.text#text.split('e')[2]
    values.append(market_dominance)
    #market rank(9th task)
    market_rank=tablelist1[6].td.text#text.split('#')[1]
    values.append(market_rank)


    #for 10th task .market cap
    div2=divisons[1]
    market_cap=div2.find('span').text
    values.append(market_cap)

    #for 11 to 14
    
    #div3=divisons[2]           #no info to be retrived from 3rd divison
    
    div4=divisons[3]
    tablelist3=div4.find_all('tr')
    
    #11
    all_time_high_date=tablelist3[4].small.text
    values.append(all_time_high_date)
    #12
    all_time_high_price=tablelist3[4].span.text
    values.append(all_time_high_price)
    #13
    all_time_low_date=tablelist3[5].small.text
    values.append(all_time_low_date)
    #14
    all_time_low_price=tablelist3[5].span.text
    values.append(all_time_low_price)

    #15 to 17 task
    for1517=body.find('div',class_="sc-16r8icm-0 kXPxnI contentClosed___j-OB6 hasShadow___jrTed")
    info=for1517.find('div',class_="sc-1lt0cju-0 srvSa")


    #writing to csv file
    with open('coins.csv','a') as csv_file:
        csv_writer=csv.writer(csv_file)
        csv_writer.writerow(['DETAILS ABOUT THE REQUESTED COIN'])
        csv_writer.writerow(heading)
        csv_writer.writerow(values)
        csv_file.close()


#call the function by removing the comment 

#get_coins()
coinname="bitCoin"        #write your coin name here
#pass name as a string object
get_coin_data(coinname)

#first run the get_coins function .