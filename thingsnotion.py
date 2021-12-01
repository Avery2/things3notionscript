import things
import os
from dotenv import load_dotenv
from notion_client import Client

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

