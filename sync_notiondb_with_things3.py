import things
from dotenv import load_dotenv
from notion_client import Client
import os
from typing import Union, TypedDict, Optional

SKIP_COMPLETED = False
SKIP_NO_TITLE_THINGS3 = True
SKIP_BEFORE_DATE = "2022-07"
if SKIP_COMPLETED:
    all_tasks = [t for t in things.tasks()]
else:
    all_tasks = [t for t in things.tasks(status=None)]

all_tasks = list(
    filter(
        lambda t: t["created"][0 : len(SKIP_BEFORE_DATE)] > SKIP_BEFORE_DATE, all_tasks
    )
)
print(f"{len(all_tasks)=}")
load_dotenv()
# my_key = os.getenv("DB_ID")
NOTION_TOKEN = os.getenv("NOTION_TOKEN")
notion = Client(auth=NOTION_TOKEN)
NOTION_DB_ID = "a1fd716f1a6b4ae6b5fcd8e6817f9af3"

#
def getExistingDBPages():
    """get existing pages as python objects"""
    return notion.databases.query(NOTION_DB_ID)["results"]


def getExistingDBProperties():
    return notion.databases.retrieve(NOTION_DB_ID)["properties"]


# update property in Notion DB


def updateNotionPageProperty(page_id: str, property_id: str, value: Union[bool, str]):
    properties = {property_id: value}
    resonse = notion.pages.update(page_id, properties=properties)
    return resonse


class MyNotionDBPage(TypedDict):
    status: bool
    uuid: str
    title: str


def addNotionPage(notion_db_id: str, page_properties: MyNotionDBPage):
    properties = {
        DB_PROPERTIES["title"]["id"]: {
            DB_PROPERTIES["title"]["id"]: [
                {"text": {"content": page_properties["title"]}}
            ]
        },
        DB_PROPERTIES["status"]["id"]: {
            "checkbox": page_properties["status"] in ("completed")
        },
        DB_PROPERTIES["uuid"]["id"]: {
            "rich_text": [
                {"type": "text", "text": {"content": page_properties["uuid"]}},
            ]
        },
    }
    parent = {"database_id": notion_db_id}
    return notion.pages.create(parent=parent, properties=properties)


# task = all_tasks[0]
# addNotionPage(NOTION_DB_ID, {
#     'status': task['status'],
#     'uuid': task['uuid'],
#     'title': task['title'],
# })

# these vars are manually updated from notion_properties = notion.databases.retrieve(notion_db_id)['properties']
STATUS_PROPERTY_ID = "PBVs"
UUID_PROPERTY_ID = "wrMk"
TITLE_PROPERTY_ID = "title"

# ! FIXME: this is broken bc it gets rate limited to only 100 values
existing_notion_pages = getExistingDBPages()
DB_PROPERTIES = getExistingDBProperties()

pages_by_uuid = {}
for p in existing_notion_pages:
    try:
        myKey = p["properties"]["uuid"]["plain_text"]
    except:
        myKey = p["properties"]["uuid"]["rich_text"][0]["plain_text"]
    finally:
        myKey = p["properties"]["uuid"]["rich_text"][0]["text"]["content"]
    pages_by_uuid[myKey] = p

tasks_by_uuid = {t["uuid"]: t for t in all_tasks}

pages_by_uuid_set = set(list(pages_by_uuid.keys()))

for i, task in enumerate(all_tasks):
    if i % 100 == 0:
        print(f"Syncing existing things3 task {i} of {len(all_tasks)}")
    things3_status = task["status"]
    things3_uuid = task["uuid"]
    things3_title = task["title"]
    if not things3_title and SKIP_NO_TITLE_THINGS3:
        continue

    isTaskInNotion = things3_uuid in pages_by_uuid_set
    if not isTaskInNotion:
        # print(f"{things3_uuid=} {isTaskInNotion=} {pages_by_uuid_set=}")
        print(f"{things3_uuid=} {isTaskInNotion=} {len(pages_by_uuid_set)=}")

    if isTaskInNotion:
        page_id = pages_by_uuid[things3_uuid]["id"]
        notion_status = pages_by_uuid[things3_uuid]["properties"]["status"]["checkbox"]
        notion_title = pages_by_uuid[things3_uuid]["properties"]["title"]["title"][0][
            "text"
        ]["content"]

        # update page
        if notion_status != things3_status:
            updateNotionPageProperty(
                page_id=page_id,
                property_id=STATUS_PROPERTY_ID,
                value=things3_status in ("completed"),
            )
        if notion_title != things3_title:
            updateNotionPageProperty(
                page_id=page_id, property_id=UUID_PROPERTY_ID, value=things3_title
            )
    else:
        # add page
        addNotionPage(
            NOTION_DB_ID,
            {"status": things3_status, "uuid": things3_uuid, "title": things3_title},
        )

for i, (nuuid, npage) in enumerate(pages_by_uuid.items()):
    print(f"{i=} {nuuid=} npage=[not shown]")
    if i % 100 == 0:
        print(f"Syncing existing notion page {i} of {len(pages_by_uuid)}")

    isPageInThings3 = nuuid in tasks_by_uuid.keys()
    if not isPageInThings3:
        # delete page
        notion.blocks.delete(block_id=npage["id"])
