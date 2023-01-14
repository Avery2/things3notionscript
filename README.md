# Things3 to Notion migration script

Part of my workflow using Things3 and Notion. I write all my notes in Things3's [quick capture](https://culturedcode.com/things/support/articles/2249437/) feature and later use this script to migrate those notes to Notion. See [Scripts](#scripts) to learn how to run a specific script.

<details><summary>Screenshots to illustrate user journey [click to expand]</summary>

<div align="center">
<img width="1840" alt="image" src="https://user-images.githubusercontent.com/53503018/194209594-50fc1ac6-993c-4f3f-94cd-2204f794c07c.png">
<p>Original inbox where I mark notes that I want to migrate to Notion by not titling them.</p>
</div>

<div align="center">
<img width="1840" alt="image" src="https://user-images.githubusercontent.com/53503018/194209675-8ae09dc6-21ee-4500-9cde-35365c9aefe4.png">
  <p>Create new Notion page and copy link with <code>command + L</code></p>
</div>

<div align="center">
<img width="690" alt="image" src="https://user-images.githubusercontent.com/53503018/194209712-57165b79-262e-4c66-907f-21a771fb3f90.png">
  <p>Strip the ID from the link using Things3's <a href="https://culturedcode.com/things/support/articles/2249437/">quick capture</a> as a place to edit text. This is also how I wrote all the notes.</p>
</div>

<div align="center">
<img width="1840" alt="image" src="https://user-images.githubusercontent.com/53503018/194209916-b5c20ba8-a708-4ced-95fd-43e145a4edab.png">
<p>Run script.</p>
</div>

<div align="center">
<img width="1840" alt="image" src="https://user-images.githubusercontent.com/53503018/194210014-95f91c71-4b05-483d-84fd-7c39077ca6f6.png">
<p>Result in Notion.</p>
</div>

<div align="center">
<img width="1840" alt="image" src="https://user-images.githubusercontent.com/53503018/194210114-0e3b1e03-e05f-4f86-81f9-601a46e929f9.png">
<p>Manually delete empty items.</p>
</div>

</details>

## Scripts

### `empty_things3_inbox_to_notion.py`

#### Description
  - Takes a block id (i.e. `bf14e6e54b74464db2d2483e114455a6`) and takes all things3 inbox items with an empty title and copies them to that block (or page). You can get this link with `command + L` or from the end of the Notion URL.
  - Created because I write notes using Things3 quick capture and markdown support and mark them as a note by having no name for the to-do item.

#### Instructions
  - Setup the `.env` file (see [`.env` setup](#env-setup))
  - Use this to enable permissions for the script (I run it as a `.command` file so I can double click it. See [this](https://superuser.com/questions/966946/how-to-run-python-script-in-a-terminal-window-by-double-clicking-it).)
    - `chmod a+x empty_things3_inbox_to_notion.py`
  - Run the script with `python3 empty_things3_inbox_to_notion.py`

### `sync_notiondb_with_things3.py`

#### Description

One-way sync from things3 to a specified notion database. So that you can have context and notes in Notion, but track progress metadata in Things3.

<details><summary>Screenshot of resulting Notion database [click to expand]</summary>
  <img width="1840" alt="image" src="https://user-images.githubusercontent.com/53503018/200147235-30ffb84a-621e-4f44-829a-a6789b52bb1e.png">
</details>


# Instructions

todo

## Setup

### Library installs

download `things`

```
pip3 install things.py
# or
git clone https://github.com/thingsapi/things.py && cd things.py && make install
```

download `dotenv`

```
pip3 install python-dotenv
```

download `notion_client`

```
pip3 install notion-client
```

download library to call applescript:

```
pip3 install pyobjc
```

### `.env` setup

Setup the `.env` file, then you can use the scripts.

- Get a [secret token](https://developers.notion.com/docs/authorization) from an [Notion integration](https://www.notion.so/help/create-integrations-with-the-notion-api).
- Set variable `NOTION_TOKEN` equal to your secret token.

### Alfred workflow

Assumes a local version of this repository is in `~/Library/Application Support/Alfred/Alfred.alfredpreferences/workflows/things3notionscript`. You may have to run `chmod a+x *.py` to enable the script.

Double click `Things3NotionScript.alfredworkflow` to import into Alfred (assuming [alfred](https://www.alfredapp.com/) is installed)

- this repo must be named `things3notionscript`
- gotta have env setup
- you can debug the workflow with this:
- ![CleanShot 2023-01-13 at 21 26 55@2x](https://user-images.githubusercontent.com/53503018/212457477-6748f80b-49d9-4b85-aab2-2d1e57006ab9.png)


## References

- `crontab -l` list all chron
- [Things3 python library](https://github.com/thingsapi/things.py#documentation)
- [Notion API docs](https://developers.notion.com/docs/getting-started)
- [Notion python sdk](https://github.com/ramnes/notion-sdk-py) (most used in `api_endpoints.py`)
- Why I like [quick capture](https://culturedcode.com/things/support/articles/2249437/): to [Close open loops](https://notes.andymatuschak.org/z8d4eJNaKrVDGTFpqRnQUPRkexB7K6XbcffAV)
- Setup ChronTab: https://towardsdatascience.com/how-to-schedule-python-scripts-with-cron-the-only-guide-youll-ever-need-deea2df63b4e which means to make script run on regular basis
