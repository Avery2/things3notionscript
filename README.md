### Notes

- What is this?
    - Part of my workflow using Things3 and Notion. I write all my notes in Things3's [quick capture](https://culturedcode.com/things/support/articles/2249437/) feature and later use this script to migrate those notes to Notion.
- migrates todos in inbox with the `migrate to notion` tag
- migrates todos with no name in inbox

### Scripts

- `empty_things3_inbox_to_notion.py`
    - Description
        - Takes a block id (i.e. `bf14e6e54b74464db2d2483e114455a6`) and takes all things3 inbox items with an empty title and copies them to that block (or page). You can get this link with `command + L` or from the end of the Notion URL.
        - Created because I write notes using Things3 quick capture and markdown support and mark them as a note by having no name for the to-do item.
    - Instructions
        - Setup the `.env` file (see `[.env` setup](notion://www.notion.so/avery2/c6efe5c895d64a779d0a60cc9023aa50?v=0b5002f4c2094a64b019534003e045c2&p=e67fc39e8ee34c59b891a037f723dc57&pm=s#env-setup))
        - Use this to enable permissions for the script
            - `chmod a+x empty_things3_inbox_to_notion.py`
        - Run the script with `python3 empty_things3_inbox_to_notion.py`

### Setup

- Library installs
    - download `things`
        - `pip3 install things.py`
    - download `dotenv`
        - `pip3 install python-dotenv`
    - download `notion_client`
        - `pip3 install notion-clien`
    - download library to call applescript:
        - `pip3 install pyobjc`
- `.env` setup
    - Setup the `.env` file, then you can use the scripts.
        - Get a [secret token](https://developers.notion.com/docs/authorization) from an [Notion integration](https://www.notion.so/help/create-integrations-with-the-notion-api).
        - Set variable `NOTION_TOKEN` equal to your secret token.

### References

- [Things3 python library](https://github.com/thingsapi/things.py#documentation)
- [Notion API docs](https://developers.notion.com/docs/getting-started)
- [Notion python sdk](https://github.com/ramnes/notion-sdk-py) (most used in `api_endpoints.py`)
- Why I like [quick capture](https://culturedcode.com/things/support/articles/2249437/): to [Close open loops](https://notes.andymatuschak.org/z8d4eJNaKrVDGTFpqRnQUPRkexB7K6XbcffAV)
- Setup ChronTab: https://betterprogramming.pub/how-to-execute-a-cron-job-on-mac-with-crontab-b2decf2968eb which means to make script run on regular basis
- I leverage [Things3's Applescript Support](https://culturedcode.com/things/support/articles/2803572/)
