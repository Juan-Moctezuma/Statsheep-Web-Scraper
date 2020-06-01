from bs4 import BeautifulSoup
from datetime import datetime
from matplotlib import animation

import csv
import inflect
import matplotlib.pyplot as plt
import numpy as np
import requests

# Set up initial variables
data = []
date = str(datetime.date(datetime.now()))
url = "https://www.statsheep.com/p/Top-Video-Views?page="
csv_file = 'Top-Channels-by-views-' + date + '.csv'
p = inflect.engine()

# Loop through Statsheep.com to find 'Top-Video-Views'
for i in range(1, 11):
    text = requests.get(url + str(i)).text
    soup = BeautifulSoup(text, 'html.parser')

    table = soup.find('table', attrs={"data-table m-top-standard m-bottom-standard top-charts"})
    rows = table.find_all('tr')

    for row in rows:
        # A list containing dictionaries will be generated
        if row.find('img'):
            spans = row.find_all('span')
            extract = {'rank': spans[0].text,
                       'name': row.find('a').text,
                       'views': spans[1].text,
                       'profile_pic': row.find('img')['src']
                       }
            data.append(extract)

if __name__ == '__main__':
    #print(data)
    #print(len(data))

    # A CSV file gets generated
    try:
        keys = data[0].keys()
        with open(csv_file, 'w') as csvfile:
            writer = csv.DictWriter(csvfile, keys)
            writer.writeheader()
            writer.writerows(data)
    except IOError:
        print("CSV File can't be generated")

    # Set up bar chart using Matplotlib
    fig = plt.figure()
    position = np.arange(5) + .5
    plt.tick_params(axis='x', colors='#072b57')
    plt.tick_params(axis='y', colors='#072b57')

    # Values from dictionaries (within list) get extracted into lists
    #ranks = [sub['rank'] for sub in data]
    names = [sub['name'] for sub in data]
    views_tot = [sub['views'] for sub in data]
    #pics = [sub['profile_pic'] for sub in data]

    # Since we want the top 5 Youtube Channels, we need the fist 5 elements on views_list
    views_list = []
    for x in range(5):
        top5_views = views_tot[x].replace(',','')
        views_list.append(top5_views)
        #print(int(top5_views))

    views_list_int = [int(views_element) for views_element in views_list]
    #print(views_list_int)

    speeds = [.5, .5, .5, .5, .5]
    heights = views_list_int

    rects = plt.bar(position, np.zeros_like(heights), align='center',
                    color=['red', 'orange', 'blue', 'pink', 'green'])
    plt.xticks(position, (names[0], names[1], names[2], names[3], names[4]))
    upper_limit = round(views_list_int[0] + 50000000000, -11)
    number_in_words = p.number_to_words(upper_limit)

    plt.xlabel('Top 5 Channels', color='#072b57', fontweight="bold")
    plt.ylabel('Total Views', color='#072b57', fontweight="bold")
    plt.title('Number of Views per Channel\n(Upper Limit: ' + number_in_words +')', color='#072b57', fontweight="bold")

    plt.ylim((0, upper_limit))
    plt.xlim((0, 5))
    plt.grid(True)

    frames = 200
    min_speed = np.min(speeds)

    def init():
        return rects

    def animate(i):
        for h, r, s in zip(heights, rects, speeds):
            new_height = i / (frames - 1) * h * s / min_speed
            new_height = min(new_height, h)
            r.set_height(new_height)
        return rects

    anim = animation.FuncAnimation(fig, animate, init_func=init, frames=frames, interval=20, blit=True, repeat=False)

    plt.show()