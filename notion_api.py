import requests
import os
import json

NOTION_TOKEN = os.getenv("NotionToken")
headers = {"Authorization": f"Bearer {NOTION_TOKEN}",
           "Content-Type": "application/json",
           "Notion-Version": "2021-05-13",
           }


def get_request_url(end_point):
    return f'https://api.notion.com/v1/{end_point}'


def get_page_urls(database_id):
    body = {
        "parent": {
            "database_id": database_id
            }
    }
    results = requests.request("POST",
                               url=get_request_url(f'databases/{database_id}/query'),
                               headers=headers,
                               data=json.dumps(body)).json()

    page_urls = list()
    if "results" in results:
        for result in results["results"]:
            page_urls.append(result["properties"]["URL"]["url"])

    return page_urls


def post_new_pages(database_id, title, url):
    body = {
        "parent": {
            "database_id": database_id
        },
        "properties": {
            "Name": {"title": [
                {"text": {"content": title}}
            ]},
            "URL": {
                "url": url
            }
        }
    }
    result = requests.request("POST", url=get_request_url(f'pages'), headers=headers,  data=json.dumps(body)).json()

    if result["object"] == "error":
        return False
    else:
        return True
