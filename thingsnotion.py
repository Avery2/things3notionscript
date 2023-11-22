import things
import os
from dotenv import load_dotenv
from notion_client import Client
import time
from Foundation import NSAppleScript
from enum import Enum

load_dotenv()
my_key = os.getenv("DB_ID")
my_token = os.getenv("NOTION_TOKEN")
last_url_filename = '.lastblockid'
# alfred_filepath_extension = "../things3notionscript/"
# filepath to "things3notionscript" folder
alfred_filepath_extension = os.getenv("ALFRED_FILEPATH")
if (alfred_filepath_extension[-1] != '/'):
    alfred_filepath_extension += '/'

# Block types which support children are “paragraph”, “bulleted_list_item”, “numbered_list_item”, “toggle”, “to_do”, “quote”, “callout”, “synced_block”, “template”, “column”, “child_page”, “child_database”, and “table”. All heading blocks (“heading_1”, “heading_2”, and “heading_3”) support children when the is_toggleable property is true.
class BlockTypes(Enum):
    PARAGRAPH="paragraph"
    BULLETED_LIST_ITEM="bulleted_list_item"
    NUMBERED_LIST_ITEM="numbered_list_item"
    TOGGLE="toggle"
    TO_DO="to_do"
    QUOTE="quote"
    CALLOUT="callout"
    SYNCED_BLOCK="synced_block"
    TEMPLATE="template"
    COLUMN="column"
    CHILD_PAGE="child_page"
    CHILD_DATABASE="child_database"
    TABLE="table"

def create_heading(content, level=1):
    level = min(level, 3)
    return {
        "object": 'block',
        "type": f"heading_{level}",
        f"heading_{level}": {
            "rich_text": [
              {
                  "type": 'text',
                  "text": {
                      "content": content,
                  },
              },
            ],
        },
    }

def create_callout_block(title='', children=[]):
    emoji = '👉'
    return {
        "object": 'block',
        "type": 'callout',
        "has_children": True,
        "callout": {
            "rich_text": [{
                "type": "text",
                "text": {
                    "content": title,
                },
                }],
                "icon": {
                "emoji": emoji
            },
            "color": "default",
            "children": children
        },
    }

def create_toggle_block(title='', children=[]):
    return {
        "object": 'block',
        "type": 'toggle',
        "has_children": True,
        "toggle": {
            "rich_text": [{
                "type": "text",
                "text": {
                    "content": title,
                },
            }],
            "color": "default",
            "children": children
        },
    }

def create_paragraph(content):
    return {
        "object": 'block',
        "type": 'paragraph',
        "paragraph": {
            "rich_text": [
              {
                  "type": 'text',
                  "text": {
                      "content": content,
                      "link": None
                  },
              },
            ],
        },
    }

def parse_markdown_to_arr(md):
    return [x for x in md.split("\n") if x]

def stringIsHeader(a):
    if a:
        return a[0] == "#"
    return False

def objIsHeader(obj):
    if 'type' in obj:
        return "heading" in obj['type']
    return False

def parse_arr_to_obj(arr):
    btype = []
    for a in arr:
        if stringIsHeader(a):
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

def saveLastBlockID(blockID):
    url = alfred_filepath_extension + last_url_filename
    with open(url, 'w') as f:
        f.write(blockID)

def getLastBlockID():
    url = alfred_filepath_extension + last_url_filename
    with open(url, 'r') as f:
        return f.read()

def obj_from_md(md):
    pmd = parse_markdown_to_arr(md)
    return parse_arr_to_obj(pmd)

def deleteTodoItemWithID(id: str, area_names=[], project_names=[]):
    """deletes an item in the inbox that has the given id, using applescript"""

    foo = ['list \"Inbox\"'] + [f'area \"{a}\"' for a in area_names] + [f'project \"{p}\"' for p in project_names]

    for bar in foo:
        s = NSAppleScript.alloc().initWithSource_(f"""tell application "Things3"
            set inboxToDos to to dos of {bar}
            repeat with inboxToDo in inboxToDos
                if id of inboxToDo equals "{id}"
                    move inboxToDo to list "Trash"
                end if
            end repeat
        end tell""")
        print(f"error(s): {s.executeAndReturnError_(None)}")

def deleteBlankInboxItems():
    """Deletes all inbox items without a name, using applescripts"""
    s = NSAppleScript.alloc().initWithSource_("""tell application "Things3"
        set inboxToDos to to dos of list "Inbox"
        repeat with inboxToDo in inboxToDos
            if name of inboxToDo equals ""
                move inboxToDo to list "Trash"
            end if
        end repeat
    end tell""")
    print(f"error(s): {s.executeAndReturnError_(None)}")

def createNewTodo(name="New to do [made by script]"):
    """Create a new todo of name `name`, using applescripts"""
    s = NSAppleScript.alloc().initWithSource_(f"""tell application "Things3"
        set newToDo to make new to do with properties \{name:"{name}"\}
    end tell""")
    print(f"error(s): {s.executeAndReturnError_(None)}")
