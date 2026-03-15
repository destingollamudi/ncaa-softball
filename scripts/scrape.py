# import required libraries
import requests
import argparse
import os
import json 
import re
from bs4 import BeautifulSoup
from schools import SCHOOLS


"""
job of this file:

1) will scrape from player desired or all players based on roster desired
2) based on input we will parse by year or total career stats cumulated year by year 
3) will take raw data and put into /data/raw as raw json
 
e.x. 
python scripts/scrape.py [college] [player_firstname-player_lastname] --[year]
where arg 1 and 2 are required
year. is optional. if not used then we will get career stats for that player
"""

parser = argparse.ArgumentParser()
parser.add_argument("school", help="School which you would like to parse data from")
parser.add_argument("player", help="firstname-lastname. Player which you would like to get stats from")
parser.add_argument("-y", "--year", help="the year in which you would like the stats from (if blank then will grab cumulative stats)", type=int)
parser.add_argument("-d", "--download", action="store_true", help="save raw json to data/raw")
args = parser.parse_args()

school = args.school
player = args.player
year = args.year
base_url = SCHOOLS[school]
scrape_url = base_url + "/sports/softball/roster/" # hardcode for softball
download = args.download

# must find player ID
res = requests.get(scrape_url)
page = BeautifulSoup(res.text, "html.parser")
link = page.find("a", href=re.compile(player))
player_url =  base_url + link["href"] # now go here to get endpoint for data 
current_rpid = player_url.split("/")[-1]

if (not year):
    base_endpoint = base_url + f"/services/responsive-roster-bio.ashx?type=career-stats&rp_id={current_rpid}&path=baseball"
else:
    res = requests.get(player_url)
    page = BeautifulSoup(res.text, "html.parser")
    tag = page.find("a", {"aria-label": f"Load {year} Season Stats"})
    rpid = json.loads(tag["data-params"])["rp_id"]
    player_id = json.loads(tag["data-params"])["player_id"]
    base_endpoint = base_url + f"/services/responsive-roster-bio.ashx?type=stats&rp_id={rpid}&path=softball&year={year}&player_id={player_id}"

# now we have endpoint that grabs data. Career data is a nice clean json 
# however for specific year it returns html table. further cleaning is required but now we can save json
headers = {
"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
"Referer": player_url
}
data = requests.get(base_endpoint, headers=headers)
data_json = data.json()
if (download):
    if (year):
        filename = f"{player}_{school}_{year}.json"
    else:
        filename = f"{player}_{school}.json"
    filepath = os.path.join("../","data", "raw", filename)
    
    with open(filepath, "w") as f:
        json.dump(data_json, f)
else:
    # so we can pipe to clean.py if we want
    print(json.dumps(data_json))