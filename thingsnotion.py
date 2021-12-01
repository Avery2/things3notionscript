import things
import os
from dotenv import load_dotenv
from notion_client import Client
import time

load_dotenv()
my_key = os.getenv("DB_ID")
my_token = os.getenv("NOTION_TOKEN")
tokenv2 = os.getenv("TOKEN_V2")

def getProject(project_title: str):
        """Returns a project of the given name"""
        all_projects = things.projects()
        project = [p for p in all_projects if p["title"] == project_title][0]
        return project

def title_notes(project):
    todos = things.todos(project["uuid"])
    l = []
    for item in todos["items"]:
        title = item['title']
        notes = item['notes']
        if not notes:
            notes = ''
        if title:
            l.append((title, notes))
    return l

def getDatabase(client: Client, db_title: str):
    dbs = [db for db in client.databases.list()['results']]
    db = list(filter(lambda x: x['title'][0]['plain_text'] == db_title, dbs))[0]
    return db

def create_empty_page(client, parent_db, title=None):
    PARENT_DB = {
        "database_id": parent_db['id']
    }

    if not title:
        t = time.strftime("%H:%M:%S", time.localtime())
        title = f"Blank page created at {t}"

    PROPERTIES = {
        "title": [{"type": "text", "text": {"content": title}}],
    }

    created_page = client.pages.create(
        **{
            "parent": PARENT_DB,
            "properties": PROPERTIES
        }
    )

    return created_page


def create_heading(content, level=1):
    level = min(level, 3)
    return {
        "object": 'block',
        "type": f"heading_{level}",
        f"heading_{level}": {
            "text": [
              {
                  "type": 'text',
                  "text": {
                      "content": content,
                  },
              },
            ],
        },
    }

def create_paragraph(content):
    return {
        "object": 'block',
        "type": 'paragraph',
        "paragraph": {
            "text": [
              {
                  "type": 'text',
                  "text": {
                      "content": content,
                    #   "link": {
                    #       "url": 'https://en.wikipedia.org/wiki/Lacinato_kale',
                    #   },
                  },
              },
            ],
        },
    }

def parse_markdown_to_arr(md):
    return [x for x in md.split("\n") if x]

def parse_arr_to_obj(arr):
    btype = []
    for a in arr:
        if a[0] == "#":
            btype.append(f"h{a[:3].count('#')}")
        else:
            btype.append("p")
    
    obj_ = []
    for c, t in zip(arr, btype):
        if t[0] == "h":
            obj_.append(create_heading(c, int(t[1])))
        else:
            obj_.append(create_paragraph(c))
    return obj_

def obj_from_md(md):
    pmd = parse_markdown_to_arr(md)
    return parse_arr_to_obj(pmd)