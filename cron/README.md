# Crontab stuff

- `chmod 777 empty_things3_inbox_to_notion.py`
- `crontab -e`
- `*/1 * * * * cd /Users/averychan/Library/Application\ Support/Alfred/Alfred.alfredpreferences/workflows/things3notionscript && /usr/bin/python3 empty_things3_inbox_to_notion.py >> /Users/averychan/Library/Application\ Support/Alfred/Alfred.alfredpreferences/workflows/things3notionscript/cron/cron.txt 2>&1`
