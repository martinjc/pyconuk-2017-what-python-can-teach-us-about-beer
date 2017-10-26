"""
Wapper for Untappd data.
"""


import datetime
import json
import os


DROPBOX_DATA_DIR = "/Users/martin/Dropbox/Coding/tap/cache/data"


#
#
# Helpers
#

def as_datetime(date_str):
    # Sun, 12 May 2013 20:50:23 +0000
    date_str = date_str.split(', ')[1]
    date_str, offset = date_str.split(' +')
    assert offset == "0000"
    dt = datetime.datetime.strptime(date_str, '%d %b %Y %H:%M:%S')
    return dt


#
#
# Untappd data loaders
#

def load_beers():
    """
    As bid2beer: int -> dict.
    130MB+ on disk.
    """
    fp = os.path.join(DROPBOX_DATA_DIR, 'beers.json')
    with open(fp) as f:
        dat = json.load(f)
    bid2beer = {}
    for bid, beer in dat.items():
        bid2beer[int(bid)] = beer
    return bid2beer


def load_users():
    """
    As uid2user: int -> dict.
    250MB+ on disk.
    """
    fp = os.path.join(DROPBOX_DATA_DIR, 'users.json')
    with open(fp) as f:
        dat = json.load(f)
    uid2user = {}
    for uid, user in dat.items():
        uid2user[int(uid)] = user
    return uid2user


def load_venues():
    """
    As vid2venue: int -> dict.
    250MB+.
    """
    fp = os.path.join(DROPBOX_DATA_DIR, 'venues.json')
    with open(fp) as f:
        dat = json.load(f)
    vid2venue = {}
    for vid, venue in dat.items():
        vid2venue[int(vid)] = venue
    return vid2venue

def load_breweries():
    """
    As bid2brewery: int -> dict.
    250MB+.
    """
    fp = os.path.join(DROPBOX_DATA_DIR, 'breweries.json')
    with open(fp) as f:
        dat = json.load(f)
    bid2brewery = {}
    for bid, brewery in dat.items():
        bid2brewery[int(bid)] = brewery
    return bid2brewery


def list_collection_cities():
    """
    List of collection cities.
    """
    cities = []
    for fname in os.listdir(os.path.join(DROPBOX_DATA_DIR, 'checkins')):
        if fname.startswith('checkins') and fname.endswith('.json'):
            city = fname.replace('checkins_', '').replace('.json', '')
            cities.append(city)
    cities = sorted(cities)
    return tuple(cities)




def load_city_checkins(city, min_dt=datetime.datetime.min,
                       max_dt=datetime.datetime.max):
    """
    Return checkins for city `city`. If specified, `min_dt` and/or `max_dt`
    will filter checkins to within given date range (half-open interval,
    min <= dt < max).

    Checkins that are malformed or invalid in some way are omitted.
    """
    fp = os.path.join(DROPBOX_DATA_DIR, 'checkins', 'checkins_%s.json' % city)
    checkins = {}
    c_data = []
    with open(fp, 'r') as f:
        for ln in f.readlines():
            c = json.loads(ln)
            c_data.append(c)
    for row in c_data:
        checkins[row['checkin_id']] = row  # filter dupes by checkin_id

    checkins = checkins.values()

    # for c in checkins:
    #     c['created_at'] = as_datetime(c['created_at'])
    #     for f in ['media', 'comments', 'toasts', 'checkin_comment']:
    #         if f in c:
    #             del c[f]
    #
    # # filter
    # def is_int(val):
    #     try:
    #         int(val)
    #         return True
    #     except TypeError:
    #         return False
    #
    # def is_keeper(c):
    #     return ((min_dt <= c['created_at'] < max_dt)
    #             and is_int(c['venue'])
    #             and is_int(c['beer']))
    #
    # checkins = filter(is_keeper, checkins)
    return checkins
