import re, time, json, os, argparse, requests
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
parser.add_argument(
    "-y",
    "--year", 
    help="the year(s) in which you would like the stats from (if blank then will grab cumulative stats)", 
    type=int,
    nargs="*"
)
parser.add_argument("-d", "--download", action="store_true", help="save raw json to data/raw")
args = parser.parse_args()

school = args.school
player = args.player
years = args.year
base_url = SCHOOLS[school]
scrape_url = base_url + "/sports/softball/roster/" # hardcode for softball
download = args.download

# must find player ID
res = requests.get(scrape_url)
page = BeautifulSoup(res.text, "html.parser")
link = page.find("a", href=re.compile(player))
player_url =  base_url + link["href"] # now go here to get endpoint for data 
current_rpid = player_url.split("/")[-1]
headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Referer": player_url
}

if (not years):
    base_endpoint = base_url + f"/services/responsive-roster-bio.ashx?type=career-stats&rp_id={current_rpid}&path=baseball"
else:
    endpoints = []
    for y in years:
        res = requests.get(player_url, headers=headers)
        page = BeautifulSoup(res.text, "html.parser")
        tag = page.find("a", {"aria-label": f"Load {y} Season Stats"})
        rpid = json.loads(tag["data-params"])["rp_id"]
        player_id = json.loads(tag["data-params"])["player_id"]
        base_endpoint = base_url + f"/services/responsive-roster-bio.ashx?type=stats&rp_id={rpid}&path=softball&year={y}&player_id={player_id}"
        endpoints.append(base_endpoint)

# now we have endpoint that grabs data. Career data is a nice clean json 
# however for specific year it returns html table. further cleaning is required but now we can save json
if years:
    items = zip(years, endpoints)
else:
    items = [(None, base_endpoint)]

for y, end in items:
    data = requests.get(end, headers=headers)
    data_json = data.json()
    if download:
        filename = f"{school}_{player}_{y}_raw.json" if y else f"{school}_{player}_career_raw.json"
        filepath = os.path.join("..", "data", "raw", filename)
        with open(filepath, "w") as f:
            json.dump(data_json, f)
    else:
        print(json.dumps(data_json))
    if years:
        time.sleep(5)