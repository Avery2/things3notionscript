import thingsnotion as tn
import things
from notion_client import Client
from dotenv import load_dotenv
from enum import Enum

load_dotenv()
import os
import re
import sys

# this toggles if this runs as a python script to be run from terminal manually or as an alfred workflow (so CLI only)
CLIonly = True

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

def promptYN(prompt, overrideAsTrue):
    if overrideAsTrue or CLIonly:
        return overrideAsTrue
    response = False
    while True:
        print(f"{prompt} [y/n] ", end="")
        res = input().lower().strip()
        if res == "y":
            response = True
            break
        if res == "n":
            response = False
            break
        print("Invalid response. Type 'y' or 'n'")
    return response


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
        if CLIonly and query:
            block_id = query.strip().split("-")[-1]
        if not CLIonly:
            print("Input block ID or URL: ", end="")
            block_id = input().strip().split("-")[-1]
        if not block_id:
            block_id = tn.getLastBlockID(CLIonly)
        block_id = re.match(r"[a-zA-Z\d]{32}", block_id)[0]
        if not block_id:
            print(f'Invalid ID: "{block_id}"')

    tn.saveLastBlockID(block_id, CLIonly)

    migrate_empty_titles = promptYN("Migrate todo items with no title", True)
    migrate_full_titles = False
    migrate_date_titles = True

    def isDate(possibleDate: str, allowBlank=True):
        returnedMatches = re.match(
            r"(?i)((jan|feb|mar|apr|may|jun|jul|aug|sep|nov|dec)\s*\d+\,?\s*\s\d+\s\d+\:\d+\:\d+ (AM|PM))|((monday|tuesday|wednesday|thursday|friday|saturday|sunday)?\,?\s*(jan|feb|mar|apr|may|jun|jul|aug|sep|nov|dec)\s*\d+.{0,2}\,\s*\d{4}\s*(AM|PM)?(\d+\:\d+\s*\:?\d*\s?(AM|PM)?)?)$",
            possibleDate.strip(),
        )
        if allowBlank:
            if possibleDate.strip() == "":
                return True
        if not returnedMatches:
            return False
        return True

    todo_item_ids = []
    # empty named todo items in Things3 inbox
    # EXAMPLE ITEM {'uuid': 'E9LkoqBLAiJHdKWvPkCSk8', 'type': 'to-do', 'title': '', 'status': 'incomplete', 'notes': 'skdljaskldjdlakjlk', 'tags': ['add as resource'], 'start': 'Inbox', 'start_date': None, 'deadline': None, 'stop_date': None, 'created': '2023-01-22 22:38:30', 'modified': '2023-01-22 22:38:36', 'index': -33736, 'today_index': 0}
    TABS_TO_MIGRATE = set(['migrate to notion'])
    itemsToMigrate = [
        todo
        for todo in inbox
        if (
            (migrate_empty_titles and todo["title"] == "")
            or (migrate_full_titles and todo["title"] != "")
            or (migrate_date_titles and isDate(todo["title"]))
            or ('tags' in todo and len(list(set(todo['tags']) & TABS_TO_MIGRATE)) > 0)
        )
    ]
    export_locations = list([2 if isDate(todo["title"], allowBlank=False) else 1 for todo in itemsToMigrate])
    project_tasks = list(filter(lambda x: migrate_date_titles and isDate(x['title']), getProjectTasks(amplitude_projects_uuids)))
    area_tasks = list(filter(lambda x: migrate_date_titles and isDate(x['title']), getAreaTasks(amplitude_areas_uuids)))
    itemsToMigrate += project_tasks
    print(f"{export_locations=}")
    export_locations += [3 for t in project_tasks]
    itemsToMigrate += area_tasks
    export_locations += [3 for t in area_tasks]

    print(f"{export_locations=}")

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

    as_callouts = promptYN("Migrate as callout blocks?", True)
    add_empty_headers = False
    if not as_callouts:
        add_empty_headers = promptYN("Add empty headers when necessary?")

    num_written = 0
    # write to notion
    for i, (note_content, note_id, export_location) in enumerate(zip(
        notes_dict, todo_item_ids, export_locations
    )):
        if export_location == 3:
            writeToBlockId = MOMENT_PAGE_WORK_ID
        elif export_location == 2:
            writeToBlockId = MOMENT_PAGE_CAPTURE_ID
            as_callouts = False
        else:
            writeToBlockId = block_id

        block_type = tn.BlockTypes.CALLOUT if as_callouts else tn.BlockTypes.TOGGLE

        # hack: this is fragile way to parse the title from the content, need to refactor to get this -- ideally parse from the raw markdown
        bad_title_parsing = note_content[0]['paragraph']['rich_text'][0]['text']['content']

        if addContentToBlock(
            writeToBlockId,
            note_content,
            title=str(bad_title_parsing),
            padded=False,
            blank_header=add_empty_headers,
            as_type=block_type
        ):
            num_written += 1
            tn.deleteTodoItemWithID(note_id, area_names=amplitude_area_names, project_names=amplitude_project_names)
        print(f"{i=} {export_location=} {writeToBlockId=}")
        if i % 10:
            print(f"processing items... [{i=}]")

    # tn.deleteBlankInboxItems()
    returnMessage = f"Wrote {num_written} objects. [{block_id=}]"
    print(returnMessage)
