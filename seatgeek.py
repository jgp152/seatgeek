# -*- coding: utf-8 -*-
"""
Created on Mon Apr  8 20:40:59 2019

@author: Jean-Gabriel
"""


import urllib # Website connections
import json
import pickle
import datetime
import os
import pandas as pd




# saving pickle
def save_pickle(variable, variable_name, data_folder, datestamp = True):
    today_str = ''
    if(datestamp):
        today_str = datetime.datetime.today().strftime('%Y%m%d')
    with open(os.path.join(data_folder,variable_name+'_'+today_str+'.dat'), 'wb') as handle:
        pickle.dump(variable, handle, protocol=pickle.HIGHEST_PROTOCOL) 
        
# defining variables
MYCLIENTID = 'ODA5ODAxM3wxNTU0NzcwMjc2LjUy'
MYCLIENTSECRET = '2ac32de7904b3d907b97f1583b1177bc9226997b67afcae2d27e8585601793e1'
performer = 'hamilton'
query ='https://api.seatgeek.com/2/events?performers.slug=' + performer + '&client_id=' + MYCLIENTID + '&client_secret=' + MYCLIENTSECRET + '&per_page=500&venue.state=NY'


# extracting data
req = urllib.request.Request(query, headers = {'User-Agent':'Mozilla/5.0'})
json_data = json.load(urllib.request.urlopen(req))

# saving data
save_pickle(json_data, 'seatgeek_hamilton', r'C:\Users\Jean-Gabriel\DATA')


results = pd.DataFrame()
for event in json_data['events']:
    
    results.loc[event['datetime_local'], 'price'] = event['stats']['lowest_price_good_deals']
    results.loc[event['datetime_local'], 'location'] = event['venue']['city'] + '_' + json_data['events'][0]['venue']['name']

cheapest_good_deal = results[results['location'] == 'New York_Richard Rodgers Theatre']['price']

cheapest_good_deal.plot(marker = 'o')


from datetime import datetime

cheapest_good_deal = cheapest_good_deal.to_frame('price')

for i in cheapest_good_deal.index:
    cheapest_good_deal.loc[i, 'date'] = datetime.strptime(i[:10], '%Y-%m-%d')
    cheapest_good_deal.loc[i, 'day'] = cheapest_good_deal.loc[i, 'date'].weekday() # Monday is 0 and Sunday is 6.
cheapest_good_deal = cheapest_good_deal.reset_index().set_index('date')


data_to_plot = pd.DataFrame()
data_to_plot['min'] = cheapest_good_deal.groupby('day').min()['price']
data_to_plot['median'] = cheapest_good_deal.groupby('day').median()['price']
data_to_plot['max'] = cheapest_good_deal.groupby('day').max()['price']
data_to_plot.plot(marker = 'o')


cheapest_good_deal[cheapest_good_deal['day'] == 3]['price'].plot(marker = 'o')




