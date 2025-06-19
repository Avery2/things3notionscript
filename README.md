### Description

Things3 to Notion workflow to migrate Things3 "notes" (items in the inbox with no title) to Notion. It will migrate notes in the inbox with no title or notes with the `migrate to notion` tag.

### Setup

#### Library installs
- `pip3 install things.py`
- `pip3 install python-dotenv`
- `pip3 install notion-client`
- `pip3 install pyobjc`
#### `.env` setup
- Setup the `.env` file, then you can use the scripts.
    - Get a [secret token](https://developers.notion.com/docs/authorization) from an [Notion integration](https://www.notion.so/help/create-integrations-with-the-notion-api) [here](https://www.notion.so/profile/integrations).
    - Set variable `NOTION_TOKEN` equal to your secret token.

You can use this template

```
DB_ID=""
NOTION_TOKEN=""
ALFRED_FILEPATH=""
MOMENT_PAGE_CAPTURE_ID=""
MOMENT_PAGE_WORK_ID=""
```

### Scripts

`empty_things3_inbox_to_notion.py`: Takes a block id (i.e. `bf14e6e54b74464db2d2483e114455a6`) and migrates the things3 inbox items to that block (or page). You can get this link with `command + L` or from the end of the Notion URL.
- Setup Instructions
    - Enable permissions for the script: `chmod a+x empty_things3_inbox_to_notion.py`
    - Run the script: `python3 empty_things3_inbox_to_notion.py [block ID]`
        - If no `block ID` given, it will try to infer from last used block ID

### Debug
- Make sure your Things3 is up to date. This broke the Things3 python library for me before

### References

- [Things3 python library](https://github.com/thingsapi/things.py#documentation)
- [Notion API docs](https://developers.notion.com/docs/getting-started)
- [Notion python sdk](https://github.com/ramnes/notion-sdk-py)
- Why I like [quick capture](https://culturedcode.com/things/support/articles/2249437/): to [Close open loops](https://notes.andymatuschak.org/z8d4eJNaKrVDGTFpqRnQUPRkexB7K6XbcffAV)
- [Things3's Applescript Support](https://culturedcode.com/things/support/articles/2803572/)
