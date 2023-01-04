#/usr/bin/env python3

import shaarli_client.client as c
import json
import os
import sys
import subprocess
import apprise
from datetime import datetime

shaarli_url = os.environ.get('SHAARLI_URL')
shaarli_token = os.environ.get('SHAARLI_TOKEN')
shaarli_tag = os.environ.get('SHAARLI_TAG')
archive_url = os.environ.get('ARCHIVE_URL')

pushover_user = os.environ.get('PUSHOVER_USER')
pushover_token = os.environ.get('PUSHOVER_TOKEN')

now = datetime.now()
archive_date = now.strftime("%Y%m%d_%H%M%S")
archive_date_readable = now.strftime("%Y-%m-%d %H:%M:%S")

# Connect to your instance
response = c.ShaarliV1Client(shaarli_url, shaarli_token)

# Find the links with the dedicated tag
answer = response.get_links({'searchtags': shaarli_tag, 'limit': 'all'})

j = answer.text
x = json.loads(j)

if x == []:
    print(archive_date_readable + " - Nothing to process...")
else:
    for i in x:
        bookmark_id=i['id']
        bookmark_url=i['url']
        bookmark_title=i['title']
        bookmark_description=i['description']
        bookmark_private=i['private']
        bookmark_tags=i['tags']

        output_file = str(bookmark_id) + "_" + archive_date + ".html"

        print(archive_date_readable + " - Archiving bookmark ID " + str(i['id']) + " " + i['url'] + " at " + archive_url + "/" + str(bookmark_id) + "_" + archive_date + ".html")

        try:
            process = subprocess.run(['/usr/local/bin/single-file','--browser-executable-path','/usr/bin/chromium-browser','--output-directory','/archives/','--filename-template',output_file,'--browser-args','["--no-sandbox"]', bookmark_url], stdout=subprocess.PIPE, universal_newlines=True)

            # update description with the archive link
            params = {
                "description": bookmark_description + "\n\n---\n\n[Archived on " + archive_date_readable + "](" + archive_url + '/' + str(bookmark_id) + "_" + archive_date + ".html)",
                "private": bookmark_private,
                "tags": bookmark_tags + ['shaarli-archiver'],
                "title": bookmark_title,
                "url": bookmark_url
            }

            print("Updating bookmark with link to archive")
            response.put_link(bookmark_id, params)

            if pushover_user:
                apobj = apprise.Apprise()
                apobj.add('pover://' + pushover_user + '@' + pushover_token)

                apobj.notify(
                    body='URL ' + bookmark_url + ' has been processed',
                    title='Shaarli Archiver',
                )
        except:
            sys.exit("Something failed...")

    # Delete the tag when all links have been processed
    print("Deleting tag " + shaarli_tag)
    response.delete_tag(shaarli_tag, params=False)