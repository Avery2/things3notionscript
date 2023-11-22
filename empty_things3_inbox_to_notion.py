#!/usr/bin/python3
import thingsnotion as tn
import things
from notion_client import Client
from dotenv import load_dotenv
from enum import Enum

load_dotenv()
import os
import re
import sys

# just for me, I have a diff page I like to put the "date" notes into
MOMENT_PAGE_CAPTURE_ID = os.getenv("MOMENT_PAGE_CAPTURE_ID")
MOMENT_PAGE_WORK_ID = os.getenv("MOMENT_PAGE_WORK_ID")
class ExportLocation(Enum):
    THINGS_3_DUMP = 1
    CAPTURE = 2
    WORK = 3

def addParagraphToBlock(block_id, paragraph_content):
    block = tn.create_paragraph(paragraph_content)
    notion.blocks.children.append(block_id, children=[block])

def addContentToBlock(
    block_id, content: list, *, title="", padded=True, blank_header=False, as_type: tn.BlockTypes=None
):
    if as_type == tn.BlockTypes.CALLOUT:
        content_ = [tn.create_callout_block(title=title, children=content)]
    elif as_type == tn.BlockTypes.TOGGLE:
        content_ = [tn.create_toggle_block(title=title, children=content)]
    elif as_type:
        content_ = [tn.create_block(title=title, children=content, type=type)]
    elif padded:
        content_ = [tn.create_paragraph("")] + content + [tn.create_paragraph("")]
        if blank_header and content and not tn.objIsHeader(content[0]):
            content_ = [tn.create_heading("")] + content
    try:
        notion.blocks.children.append(block_id, children=content_)
    except Exception as e:
        print(f"failed call to addContentToBlock() where {block_id=} {content_=} because {e=}")
        return False
    return True

def getProjectTasks(amplitude_projects_uuids):
    for uuid in amplitude_projects_uuids:
        for task in things.projects(uuid)['items']:
            yield task

def getAreaTasks(amplitude_areas_uuids):
    for uuid in amplitude_areas_uuids:
        for task in things.areas(uuid, include_items=True)['items']:
            yield task

if __name__ == "__main__":
    # setup
    my_token = os.getenv("NOTION_TOKEN")
    notion = Client(auth=my_token)
    inbox = things.inbox()

    # just for me
    amplitude_projects = [(p['uuid'], p['title'].lower(), p['title']) for p in things.projects()]
    amplitude_areas = [(a['uuid'], a['title'].lower(), a['title']) for a in things.areas()]

    amplitude_projects=list(filter(lambda x: x[1].find("amplitude") != -1, amplitude_projects))
    amplitude_areas=list(filter(lambda x: x[1].find("amplitude") != -1, amplitude_areas))
    amplitude_projects_uuids=[e[0] for e in amplitude_projects]
    amplitude_areas_uuids=[e[0] for e in amplitude_areas]

    amplitude_project_names = [e[2] for e in amplitude_projects]
    amplitude_area_names = [e[2] for e in amplitude_areas]

    query = None
    if len(sys.argv) > 1:
        query = sys.argv[1]
    block_id = ""
    # example id: ede03723649543a3a4cedc3065faaa8f
    while not block_id:
        if query:
            block_id = query.strip().split("-")[-1]
        if not block_id:
            block_id = tn.getLastBlockID()
        block_id = re.match(r"[a-zA-Z\d]{32}", block_id)[0]
        if not block_id:
            print(f'Invalid ID: "{block_id}"')

    tn.saveLastBlockID(block_id)

    migrate_empty_titles = True
    migrate_full_titles = False
    migrate_date_titles = True

    todo_item_ids = []
    # empty named todo items in Things3 inbox
    # EXAMPLE ITEM {'uuid': 'E9LkoqBLAiJHdKWvPkCSk8', 'type': 'to-do', 'title': '', 'status': 'incomplete', 'notes': 'skdljaskldjdlakjlk', 'tags': ['add as resource'], 'start': 'Inbox', 'start_date': None, 'deadline': None, 'stop_date': None, 'created': '2023-01-22 22:38:30', 'modified': '2023-01-22 22:38:36', 'index': -33736, 'today_index': 0}
    TABGS_TO_MIGRATE = set(['migrate to notion'])
    itemsToMigrate = [
        todo
        for todo in inbox
        if (
            (migrate_empty_titles and todo["title"] == "")
            or (migrate_full_titles and todo["title"] != "")
            or ('tags' in todo and len(list(set(todo['tags']) & TABGS_TO_MIGRATE)) > 0)
        )
    ]

    if migrate_full_titles:
        notes_raw = [
            "# " + obj["title"] + "\n" + obj["notes"] for obj in itemsToMigrate
        ]
    else:
        notes_raw = []
        for obj in itemsToMigrate:
            note_content = ""
            if obj["title"]:
                note_content += obj["title"] + "\n"
            note_content += obj["notes"]
            notes_raw.append(note_content)
    notes_dict = [tn.obj_from_md(o) for o in notes_raw]
    todo_item_ids = [o["uuid"] for o in itemsToMigrate]

    as_callouts = False
    add_empty_headers = False

    num_written = 0
    # write to notion
    for i, (note_content, note_id) in enumerate(zip(
        notes_dict, todo_item_ids
    )):
        block_type = tn.BlockTypes.CALLOUT if as_callouts else tn.BlockTypes.TOGGLE

        # hack: this is fragile way to parse the title from the content, need to refactor to get this -- ideally parse from the raw markdown
        try:
            bad_title_parsing = note_content[0]['paragraph']['rich_text'][0]['text']['content']
        except (IndexError, KeyError):
            bad_title_parsing = ""

        if addContentToBlock(
            block_id,
            note_content[1:] if bad_title_parsing else note_content,
            title=str(bad_title_parsing),
            padded=False,
            blank_header=add_empty_headers,
            as_type=block_type
        ):
            num_written += 1
            tn.deleteTodoItemWithID(note_id, area_names=amplitude_area_names, project_names=amplitude_project_names)
        print(f"{i=} {block_id=}")
        if i % 10:
            print(f"processing items... [{i=}]")

    returnMessage = f"Wrote {num_written} objects. [{block_id=}]"
    print(returnMessage)
