# Things3 and Notion Script

## Scripts

### `empty_things3_inbox_to_notion.py`
  - Takes a block id (i.e. `bf14e6e54b74464db2d2483e114455a6`) and takes all things3 inbox items with an empty title and copies them to that block (or page). You can get this link with `command + L` or from the end of the Notion URL.
  - Created because I write notes using Things3 quick capture and markdown support, and mark them as a note by having no name for the todo item.

## Setup

### Library installs

download `things`

```
$ pip3 install things.py
# or
$ git clone https://github.com/thingsapi/things.py && cd things.py && make install
```

download `dotenv`

```
pip3 install python-dotenv
```

download `notion_client`

```
pip3 install notion-client
```

### `.env` setup

Setup the `.env` file, then you can use the scripts.

- Get a [secret token](https://developers.notion.com/docs/authorization) from an [Notion integration](https://www.notion.so/help/create-integrations-with-the-notion-api).
- Set variable `NOTION_TOKEN` equal to your secret token.

## References

- [Things3 python library](https://github.com/thingsapi/things.py#documentation)
- [Notion API docs](https://developers.notion.com/docs/getting-started)
- [Notion python sdk](https://github.com/ramnes/notion-sdk-py)
  - often referenced `api_endpoints.py`
- `chmod a+x empty_things3_inbox_to_notion.command`
