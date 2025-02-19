# -*- coding: utf-8 -*-
"""
Created on Sun Sep  1 23:09:18 2024

@author: carri
"""

import pandas as pd
from inline_sql import sql

#%% Unfollowers List ==========================================================

def imp_followers (followers_file):
    followers = pd.read_json(followers_file)
    followers = followers.string_list_data
    for i in range(len(followers)):
        followers[i] = followers[i][0]['value']
    return followers

def imp_following (following_file):
    following = pd.read_json(following_file)
    following = following.relationships_following
    for i in range(len(following)):
        following[i] = following[i]['string_list_data'][0]['value']
    return following

def unfollowers (followers_file, following_file):
    followers = imp_followers(followers_file)
    following = imp_following(following_file)
    unfollowers = sorted(following[~following.isin(followers)])
    return pd.DataFrame(unfollowers)

#%% Followers & Following Counting ============================================

def count_fwers_fwing (followers, following):
    
    file = open('./fwers_fwing.txt', 'r')
    fwers_fwing = file.read()
    file.close()
    
    fwers_fwing = fwers_fwing.split(' ')
    fwers_fwing = [int(x) for x in fwers_fwing]
    
    old_fwers = fwers_fwing[0]
    old_fwing = fwers_fwing[1]
    
    new_fwers = len(imp_followers(followers))
    new_fwing = len(imp_following(following))

    print(f"(*) Followers: {new_fwers} ({new_fwers-old_fwers})")
    print(f"(*) Following: {new_fwing} ({new_fwing-old_fwing})")
    
    file = open('./fwers_fwing.txt', 'w')
    file.write(f"{new_fwers} {new_fwing}")
    
#%% Main ====================================================================== 
    
followers = './connections/followers_and_following/followers_1.json'
following = './connections/followers_and_following/following.json'
unfollow = './unfollowers.csv'

old_unfollowers = pd.read_csv(unfollow)
new_unfollowers = unfollowers(followers, following)

sql_query = """
            SELECT DISTINCT *
            FROM new_unfollowers AS nu
            EXCEPT
            SELECT DISTINCT *
            FROM old_unfollowers AS ou
            """

count_fwers_fwing(followers, following)
print(sql^ sql_query)
new_unfollowers.to_csv('unfollowers.csv', index = False)