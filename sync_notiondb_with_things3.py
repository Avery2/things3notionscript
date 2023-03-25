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
load_dotenv()
# my_key = os.getenv("DB_ID")
NOTION_TOKEN = os.getenv("NOTION_TOKEN")
notion = Client(auth=NOTION_TOKEN)
NOTION_DB_ID = "a1fd716f1a6b4ae6b5fcd8e6817f9af3"

# these vars are manually updated from notion_properties = notion.databases.retrieve(notion_db_id)['properties']
STATUS_PROPERTY_ID = "PBVs"
UUID_PROPERTY_ID = "wrMk"
TITLE_PROPERTY_ID = "title"


def getExistingDBPages():
    """get existing pages as python objects"""
    return notion.databases.query(NOTION_DB_ID)["results"]


# # ! warning delete all
# pages = getExistingDBPages()
# while len(pages) > 0:
#     delete_ids = [p["id"] for p in pages]
#     for _id in delete_ids:
#         print(f"delete block: {_id}")
#         notion.blocks.delete(block_id=_id)
#     pages = getExistingDBPages()

# exit(1)
# # ! warning delete all end

numUpdatedProps = 0
numAddedPages = 0


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


def uuidInNotion(uuid: str) -> bool:
    return len(getPagesWithUUID(uuid)) > 0


# other ways to query uuid from notion page object
#         myKey = p["properties"]["uuid"]["plain_text"]
#         myKey = p["properties"]["uuid"]["rich_text"][0]["plain_text"]
#         myKey = p["properties"]["uuid"]["rich_text"][0]["text"]["content"]
def getPagesWithUUID(uuid: str):
    filterProp = {
        "and": [
            {"property": UUID_PROPERTY_ID, "rich_text": {"contains": uuid}},
        ]
    }
    matches = notion.databases.query(database_id=NOTION_DB_ID, filter=filterProp)[
        "results"
    ]
    return matches


DB_PROPERTIES = getExistingDBProperties()

tasks_by_uuid = {t["uuid"]: t for t in all_tasks}


for i, task in enumerate(all_tasks):
    if i % 100 == 0:
        print(
            f"Syncing existing things3 task {i} of {len(all_tasks)} [{numUpdatedProps=} {numAddedPages=}]"
        )
    things3_status = task["status"]
    things3_uuid = task["uuid"]
    things3_title = task["title"]
    if not things3_title and SKIP_NO_TITLE_THINGS3:
        continue

    isTaskInNotion = uuidInNotion(things3_uuid)

    if isTaskInNotion:
        page_id = getPagesWithUUID(things3_uuid)[0]["id"]
        notion_status = getPagesWithUUID(things3_uuid)[0]["properties"]["status"][
            "checkbox"
        ]
        notion_title = getPagesWithUUID(things3_uuid)[0]["properties"]["title"][
            "title"
        ][0]["text"]["content"]

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
    elif things3_status in ("incomplete"):  # only add incomplete todo items
        # add page
        addNotionPage(
            NOTION_DB_ID,
            {"status": things3_status, "uuid": things3_uuid, "title": things3_title},
        )
f"Finished syncing {len(all_tasks)} tasks [{numUpdatedProps=} {numAddedPages=}]"

# todo: go through existing DB items and delete stale Pages (that have since been deleted in Things3)
# for i, (nuuid, npage) in enumerate(pages_by_uuid.items()):
#     print(f"Syncing existing notion pages")

#     isPageInThings3 = nuuid in tasks_by_uuid.keys()
#     if not isPageInThings3:
#         # delete page
#         to_delete_id = npage["id"]
#         print(f"delete block: {to_delete_id}")
#         notion.blocks.delete(block_id=to_delete_id)
