#!/usr/bin/python3
"""Module to recursively query Reddit API for all hot articles"""
import requests


def recurse(subreddit, hot_list=[], after=None):
    """Returns a list of titles of all hot articles for a given subreddit"""
    url = "https://www.reddit.com/r/{}/hot.json".format(subreddit)
    headers = {
        "User-Agent": "python:subreddit.recurse:v1.0 (by /u/CodeAlvinCreator)"
    }
    params = {"limit": 100, "after": after}

    response = requests.get(
        url,
        headers=headers,
        params=params,
        allow_redirects=False
    )

    if response.status_code != 200:
        return None

    data = response.json()["data"]
    posts = data["children"]

    if len(posts) == 0:
        return hot_list if hot_list else None

    for post in posts:
        hot_list.append(post["data"]["title"])

    after = data["after"]

    if after is None:
        return hot_list

    return recurse(subreddit, hot_list, after)
