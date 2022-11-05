import things
from dotenv import load_dotenv
from notion_client import Client
import os
from typing import Union, TypedDict, Optional

all_tasks = [t for t in things.tasks(status=None)]
load_dotenv()
# my_key = os.getenv("DB_ID")
NOTION_TOKEN = os.getenv("NOTION_TOKEN")
notion = Client(auth=NOTION_TOKEN)
NOTION_DB_ID = "a1fd716f1a6b4ae6b5fcd8e6817f9af3"

# get existing pages as python objects
notin_db_pages = notion.databases.query(NOTION_DB_ID)['results']
DB_PROPERTIES = notion.databases.retrieve(NOTION_DB_ID)['properties']

# update property in Notion DB

def updateNotionPage(page_id: str, property_id: str, value: Union[bool, str]):
    properties = {property_id: value}
    resonse = notion.pages.update(page_id, properties=properties)
    return resonse

# property = 'deleted'
# value_property = True
# notion_page_id = notin_db_pages[0]['id']
# notion_property_id = notion_properties[property]['id']
# updateNotionPage(notion_page_id, notion_property_id, value_property)

class MyNotionDBPage(TypedDict):
    status: bool
    deleted: Optional[bool]
    uuid: str
    title: str

def addNotionPage(notion_db_id:str, page_properties: MyNotionDBPage):
    properties = {
        DB_PROPERTIES['title']['id']: {
            DB_PROPERTIES['title']['id']: [
                {
                    "text": {
                        "content": page_properties['title']
                    }
                }
            ]
        },
        DB_PROPERTIES['status']['id']: {
            'checkbox': page_properties['status'] in ('completed')
        },
        DB_PROPERTIES['deleted']['id']: {
            'checkbox': False, # it's not deleted if I am adding it
        },
        DB_PROPERTIES['uuid']['id']: {
            "rich_text": [
                {
                    "type": "text",
                    "text": {
                    "content": page_properties['uuid']
                    }
                },
            ]
        },
    }
    parent = {'database_id': notion_db_id}
    return notion.pages.create(parent=parent, properties=properties)

# task = all_tasks[0]
# addNotionPage(NOTION_DB_ID, {
#     'status': task['status'],
#     'uuid': task['uuid'],
#     'title': task['title'],
# })
