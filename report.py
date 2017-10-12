import pandas as pd
import numpy as np
from states import states
import json
import time
import math
from reportlab.pdfgen import canvas

# Creates a report as pdf file

c = canvas.Canvas("report.pdf")
c.setFont('Helvetica', 14)
c.setFillColorRGB(0,0,255)
c.drawString(90,800,"Basic insights drawn from two datasets source1.csv and source2.csv")


df1 = pd.read_csv('source1.csv')
df2 = pd.read_csv('source2.csv')

####################     Question 1     ##########################
# 1. what was the total spent against people with purple hair?

start = time.time()

c.setFont('Helvetica',12)
c.setFillColorRGB(0,0,0)
c.drawString(30,750,'1. What was the total spent against people with purple hair?')

c_start = time.time()

hair_color = 'purple'
campaign_ids = df1[df1['audience'].str.contains(hair_color)]['campaign_id']
total_spent = sum(df2[df2['campaign_id'].isin(campaign_ids)]['spend'])

c_end = time.time()

c.drawString(30,735,'Ans: Total spent against people with ' + hair_color + ' is ' + str(total_spent))
c.drawString(30,720,'Runtime: took ' + str(round(c_end-c_start,4)) + ' time')

####################     Question 2     ##########################
# 2. how many campaigns spent on more than 4 days?

c.drawString(30,690,'2. How many campaigns spent on more than 4 days?')

c_start = time.time()

mt_4 = sum(list(df2.groupby(['campaign_id']).count()['date'] > 4))

c_end = time.time()

c.drawString(30,675,'Ans: Campaigns that spent more than 4 days are ' + str(mt_4))
c.drawString(30,660,'Runtime: took ' + str(round(c_end-c_start,4)) + ' time')


####################     Question 3     ##########################
# 3. how many times did source H report on clicks?

c.drawString(30,630,'3. How many times did source H report on clicks?')

c_start = time.time()

total_reports = 0
total_clicks = 0

selected_idxs =  list(df2['actions'].str.contains('H'))

for row in df2.iloc[selected_idxs]['actions']:
	for obj in json.loads(row):
		if ('H' in obj) and obj['action'] == 'clicks':
			total_clicks += obj['H']
			total_reports += 1

c_end = time.time()

c.drawString(30,615,'Ans: Source H reported ' + str(total_reports) + ' times and a total of ' + str(total_clicks) + ' clicks' )
c.drawString(30,600,'Runtime: took ' + str(round(c_end-c_start,4)) + ' time')

####################     Question 4     ##########################
# 4. which sources reported more "junk" than "noise"?

c.drawString(30,570,'4. Which sources reported more "junk" than "noise"?')

c_start = time.time()

doc = {}

actions_list = ['junk', 'noise']
list_of_actions =  df2[df2['actions'].str.contains(actions_list[0]+"|"+actions_list[1])]['actions']

for row in list_of_actions:
	for obj in json.loads(row):
		if obj['action'] in actions_list:
			if not obj['action'] in doc:
				doc[obj['action']] = {}
			for key in obj.keys():
				if key == 'action':
					continue
				if not key in doc[obj['action']]:
					doc[obj['action']][key] = obj[key]
				else:
					doc[obj['action']][key] = doc[obj['action']][key] + obj[key]

df = pd.DataFrame.from_dict(doc)
df = df[df.junk > df.noise]
sources =  "Sources " + ','.join(df.index.values) + " reported more junk than noise."

c_end = time.time()

c.drawString(30,555,'Ans: Sources ' + sources + 'reported more junk than noise.')
c.drawString(30,540,'Runtime: took ' + str(round(c_end-c_start,4)) + ' time')

####################     Question 5     ##########################
# 5. what was the total cost per view for all video ads, truncated to two decimal places?

c.drawString(30,510,'5. What was the total cost per view for all video ads, truncated to two decimal places?')

c_start = time.time()

video_df = df2[df2['ad_type'].str.contains("video")]
value_spent = video_df['spend'].sum()
list_of_actions = video_df[video_df['actions'].str.contains('views')]['actions']

no_of_views = 0

for row in list_of_actions:
	for obj in json.loads(row):
		if obj['action'] == 'views':
			for val in obj.values():
				if val != 'views':
					no_of_views += val

cost_per_view = str(round(float(value_spent) / no_of_views ,2)) + '$ Spent on each view for video ads'

c_end = time.time()

c.drawString(30,495,'Ans: ' + cost_per_view)
c.drawString(30,480,'Runtime: took ' + str(round(c_end-c_start,4)) + ' time')

####################     Question 6     ##########################
# 6. how many source B conversions were there for campaigns targeting NY?

c.drawString(30,450,'6. How many source B conversions were there for campaigns targeting NY?')

c_start = time.time()

NY_campaign_ids = df1[df1['audience'].str.contains("NY")]['campaign_id']
NY_actions = df2[df2['campaign_id'].isin(NY_campaign_ids)]['actions']

total_conversions_in_NY = 0
for row in NY_actions:
	for obj in json.loads(row):
		if ('B' in obj) and (obj['action'] == 'conversions'):
			total_conversions_in_NY += obj['B']

c_end = time.time()

c.drawString(30,435,'Ans: There were ' + str(total_conversions_in_NY) +' source B conversions for campaigns targeting NY')
c.drawString(30,420,'Runtime: took ' + str(round(c_end-c_start,4)) + ' time')


####################     Question 7     ##########################
# 7. what combination of state and hair color had the best CPM?

c.drawString(30,390,'7. What combination of state and hair color had the best CPM?')

c_start = time.time()

pattern = '([A-Z]+\_[a-z]+)'
grouped = df1.groupby([df1['audience'].str.extract(pattern, expand=False)])

min_cpm = float('nan')
audience_name = '' 

for name, group in grouped:
	impressions = sum(group['impressions'])
	spend = sum(df2[df2['campaign_id'].isin(group['campaign_id'])]['spend'])
	cpm = round(float(spend) / (impressions) * 1000 , 4)
	if math.isnan(min_cpm) or (cpm < min_cpm):
		min_cpm = cpm
		audience_name = name

color = audience_name.split('_')[1]
state = audience_name.split('_')[0]

c_end = time.time()

c.drawString(30,375,'Answer: ' + states[state] + ' with ' + color +' hair color combination has the best CPM of ' + str(round(min_cpm,4)) + '$')
c.drawString(30,360,'Runtime: took ' + str(round(c_end-c_start,4)) + ' time')

c.drawString(160, 320,'---------------------------- O ----------------------------')

end = time.time()

c.drawString(30,290,'Took ' + str(round(end-start,4)) + 'sec\'s to generate the report')

c.save()