import thingsnotion as tn
import things
from notion_client import Client
from dotenv import load_dotenv
load_dotenv()
import os
import re

def addParagraphToBlock(block_id, paragraph_content):
    block = tn.create_paragraph(paragraph_content)
    notion.blocks.children.append(block_id, children=[block])

def addContentToBlock(block_id, content: list, *, padded=True, blank_header=False, as_callouts=False):
    if as_callouts:
        content_ = [tn.create_callout_block(title="", children=content)]
    elif padded:
        content_ = [tn.create_paragraph("")] + content + [tn.create_paragraph("")]
        if blank_header and content and not tn.objIsHeader(content[0]):
            content_ = [tn.create_heading("")] + content
    notion.blocks.children.append(block_id, children=content_)

def promptYN(prompt):
    response = False
    while True:
        print(f"{prompt} [y/n] ", end='')
        res = input().lower().strip()
        if res == 'y':
            response = True
            break
        if res == 'n':
            response = False
            break
        print("Invalid response. Type 'y' or 'n'")
    return response

if __name__ == '__main__':
    # setup
    my_token = os.getenv("NOTION_TOKEN")
    notion = Client(auth=my_token)
    inbox = things.inbox()

    block_id = ''
    # example id: ede03723649543a3a4cedc3065faaa8f
    while not block_id:
        print("Input block ID or URL: ", end='')
        block_id = input().strip().split("-")[-1]
        block_id = re.match(r'[a-zA-Z\d]{32}', block_id)[0]
        if not block_id:
            print("Invalid ID")

    migrate_empty_titles = promptYN("Migrate todo items with no title")
    migrate_full_titles = promptYN("Migrate todo items with a title")

    # empty named todo items in Things3 inbox
    blank_items = [todo for todo in inbox if ((migrate_empty_titles and todo['title'] == '') or (migrate_full_titles and todo['title'] != ''))]
    if migrate_full_titles:
        notes_raw = ['# ' + obj['title'] + '\n' + obj['notes'] for obj in blank_items]
    else:
        notes_raw = [obj['notes'] for obj in blank_items]
    notes_dict = [tn.obj_from_md(o) for o in notes_raw]

    as_callouts = promptYN("Migrate as callout blocks?")
    add_empty_headers = False
    if not as_callouts:
        add_empty_headers = promptYN("Add empty headers when necessary?")

    num_written = 0
    # write to notion
    for note in notes_dict:
        addContentToBlock(block_id, note, blank_header=add_empty_headers, as_callouts=as_callouts)
        num_written += 1

    print(f"Wrote {num_written} objects.")
