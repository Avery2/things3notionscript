# Things3 and Notion Script

A script I wrote that takes todo items in Things3 and writes them to a Notion database.

UPDATE: only `empty_things3_inbox_to_notion.py` is working, which take a block id and takes all empty things3 inbox items and copies them to that block (or page).

## Worked

https://github.com/thingsapi/things.py#documentation

https://developers.notion.com/docs/getting-started

This is the one that worked. It follows the official API so I think it's more reliable.
https://github.com/ramnes/notion-sdk-py

## Tried

https://github.com/jamalex/notion-py

## More (maybe) helpful links

- https://developers.notion.com/reference/block
- https://developers.notion.com/reference/patch-block-children
- https://developers.notion.com/docs/working-with-page-content#appending-blocks-to-a-page
- also looking at `api_endpoings`