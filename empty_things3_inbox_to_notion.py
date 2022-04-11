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

def addContentToBlock(block_id, content: list, padded=True):
    if padded:
        content = [tn.create_paragraph("")] + content + [tn.create_paragraph("")]
    notion.blocks.children.append(block_id, children=content)

if __name__ == '__main__':
    # setup
    my_key = os.getenv("DB_ID")
    my_token = os.getenv("NOTION_TOKEN")
    tokenv2 = os.getenv("TOKEN_V2")
    notion = Client(auth=my_token)
    inbox = things.inbox()

    block_id = ''
    # example id: ede03723649543a3a4cedc3065faaa8f
    while not block_id:
        print("Input block ID: ", end='')
        block_id = input().strip()
        block_id = re.match(r'[a-zA-Z\d]{32}', block_id)[0]
        if not block_id:
            print("Invalid ID")

    # empty named todo items in Things3 inbox
    blank_items = [todo for todo in inbox if todo['title'] == '']
    notes_raw = [obj['notes'] for obj in blank_items]
    notes_dict = [tn.obj_from_md(o) for o in notes_raw]

    write_to_notion = None
    while True:
        print("Write to notion? [y/n] ", end='')
        res = input().lower().strip()
        if res == 'y':
            write_to_notion = True
            break
        if res == 'n':
            write_to_notion = False
            break
        print("Invalid response. Type 'y' or 'n'")
        
    if write_to_notion:
        # write to notion
        for note in notes_dict:
            addContentToBlock(block_id, note)