import thingsnotion as tn
import things
from notion_client import Client
from dotenv import load_dotenv

load_dotenv()
import os
import re
import sys

# this toggles if this runs as a python script to be run from terminal manually or as an alfred workflow (so CLI only)
CLIonly = True


def addParagraphToBlock(block_id, paragraph_content):
    block = tn.create_paragraph(paragraph_content)
    notion.blocks.children.append(block_id, children=[block])


def addContentToBlock(
    block_id, content: list, *, padded=True, blank_header=False, as_callouts=False
):
    if as_callouts:
        content_ = [tn.create_callout_block(title="", children=content)]
    elif padded:
        content_ = [tn.create_paragraph("")] + content + [tn.create_paragraph("")]
        if blank_header and content and not tn.objIsHeader(content[0]):
            content_ = [tn.create_heading("")] + content
    notion.blocks.children.append(block_id, children=content_)


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


if __name__ == "__main__":
    # setup
    my_token = os.getenv("NOTION_TOKEN")
    notion = Client(auth=my_token)
    inbox = things.inbox()

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
            print(f"Invalid ID: \"{block_id}\"")

    tn.saveLastBlockID(block_id, CLIonly)

    migrate_empty_titles = promptYN("Migrate todo items with no title", True)
    # migrate_full_titles = promptYN("Migrate todo items with a title")
    migrate_full_titles = False
    migrate_date_titles = True

    def isDate(possibleDate: str):
        returnedMatches = re.match(r"(?i)((jan|feb|mar|apr|may|jun|jul|aug|sep|nov|dec)\s*\d+\,?\s*\s\d+\s\d+\:\d+\:\d+ (AM|PM))|((monday|tuesday|wednesday|thursday|friday|saturday|sunday)?\,?\s*(jan|feb|mar|apr|may|jun|jul|aug|sep|nov|dec)\s*\d+.{0,2}\,\s*\d{4}\s*(AM|PM)?(\d+\:\d+\s*\:?\d*\s?(AM|PM)?)?)$", possibleDate)
        if not returnedMatches:
            return False
        return True

    todo_item_ids = []
    # empty named todo items in Things3 inbox
    itemsToMigrate = [
        todo
        for todo in inbox
        if (
            (migrate_empty_titles and todo["title"] == "")
            or (migrate_full_titles and todo["title"] != "")
            or (migrate_date_titles and isDate(todo["title"]))
        )
    ]
    if migrate_full_titles:
        notes_raw = ["# " + obj["title"] + "\n" + obj["notes"] for obj in itemsToMigrate]
    else:
        notes_raw = []
        for obj in itemsToMigrate:
            note = ""
            if (obj["title"]):
                note += obj["title"] + "\n"
            note += obj["notes"]
            notes_raw.append(note)
    notes_dict = [tn.obj_from_md(o) for o in notes_raw]
    todo_item_ids = [o["uuid"] for o in itemsToMigrate]

    as_callouts = promptYN("Migrate as callout blocks?", True)
    add_empty_headers = False
    if not as_callouts:
        add_empty_headers = promptYN("Add empty headers when necessary?")

    num_written = 0
    # write to notion
    for note, note_id in zip(notes_dict, todo_item_ids):
        addContentToBlock(
            block_id, note, blank_header=add_empty_headers, as_callouts=as_callouts
        )
        num_written += 1
        tn.deleteTodoItemWithID(note_id)

    # tn.deleteBlankInboxItems()
    returnMessage = f"Wrote {num_written} objects. [{block_id=}]"
    print(returnMessage)
