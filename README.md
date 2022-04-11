# Things3 and Notion Script

## `.env` file setup

Set variable `NOTION_TOKEN` to your [secret token](https://developers.notion.com/docs/authorization).

## Scripts

- `empty_things3_inbox_to_notion.py`: takes a block id (i.e. `bf14e6e54b74464db2d2483e114455a6`) and takes all empty things3 inbox items and copies them to that block (or page). Created because I write notes using Things3 quick capture and markdown support, and mark them as a note by having no name for the todo item.

## References

- [Things3 python library](https://github.com/thingsapi/things.py#documentation)
- [Notion API docs](https://developers.notion.com/docs/getting-started)
- [Notion python sdk](https://github.com/ramnes/notion-sdk-py)
- also looking at `api_endpoints.py`
