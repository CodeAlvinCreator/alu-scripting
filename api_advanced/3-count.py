#!/usr/bin/python3
"""Module to recursively count keywords in Reddit hot articles"""
import requests


def count_words(subreddit, word_list, counts={}, after=None):
    """Recursively queries Reddit API and prints sorted count of keywords"""

    # Initialize counts on first call
    if after is None and not counts:
        for word in word_list:
            word = word.lower()
            counts[word] = counts.get(word, 0)

    url = "https://www.reddit.com/r/{}/hot.json".format(subreddit)
    headers = {
        "User-Agent": "python:subreddit.count:v1.0 (by /u/CodeAlvinCreator)"
    }
    params = {"limit": 100, "after": after}

    response = requests.get(
        url,
        headers=headers,
        params=params,
        allow_redirects=False
    )

    if response.status_code != 200:
        return

    data = response.json()["data"]
    posts = data["children"]

    # Count keywords in each title
    for post in posts:
        title = post["data"]["title"].lower().split()
        for word in counts:
            counts[word] += title.count(word)

    after = data["after"]

    if after is None:
        # Print results sorted by count (desc) then alphabetically (asc)
        sorted_counts = sorted(counts.items(), key=lambda x: (-x[1], x[0]))
        for word, count in sorted_counts:
            if count > 0:
                print("{}: {}".format(word, count))
        return

    return count_words(subreddit, word_list, counts, after)
