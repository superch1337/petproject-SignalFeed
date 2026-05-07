import requests

BASE_URL = "https://hacker-news.firebaseio.com/v0"


def get_top_story_ids(limit=10):
    url = f"{BASE_URL}/topstories.json"
    response = requests.get(url)
    response.raise_for_status()
    return response.json()[:limit]


def get_item(item_id):
    url = f"{BASE_URL}/item/{item_id}.json"
    response = requests.get(url)
    response.raise_for_status()
    return response.json()


def get_top_posts(limit=10):
    ids = get_top_story_ids(limit)
    posts = []

    for item_id in ids:
        item = get_item(item_id)

        if item and item.get("type") == "story":
            posts.append({
                "title": item.get("title"),
                "author": item.get("by"),
                "score": item.get("score"),
                "url": item.get("url"),
                "comments": item.get("descendants", 0)
            })

    return posts