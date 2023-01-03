# Shaarli Archiver

[Shaarli](https://github.com/shaarli/Shaarli) doesn't have native local archiving possibilities.

[SingleFile](https://github.com/gildas-lormeau/SingleFile) provides an easy way to archive web pages in a single HTML file.

This container image combines the power of both!

## How it works

- this container will query your Shaarli instance every hour
- it searchs for bookmarks with a dedicated and unique tag (e.g. `to_archive`)
- if a bookmark is found with that tag, SingleFile processes the link and saves the HTML under `/archives`
- when processed, the description of the bookmark is updated with a link to archive (that can be `file:///home/user/archives` or `https://archive.example.com`)
- an (optional) notification is sent to Pushover (it uses the [apprise](https://github.com/caronc/apprise) library)
- the dedicated and unique tag is deleted

## How a bookmark looks before processing

![](https://raw.githubusercontent.com/sebw/shaarli-archiver/master/screenshots/before.png)

## How it looks after processing

![](https://raw.githubusercontent.com/sebw/shaarli-archiver/master/screenshots/after.png)

The "Archived on..." is clickable and goes to `ARCHIVE_URL`

## Run the container

`SHAARLI_TAG` is the dedicated and unique tag that triggers the archiving.

`SHAARLI_TOKEN` is the token that can be found in your Shaarli under Tools > Configure your Shaarli > REST API secret

`ARCHIVE_URL` is the address where the archives will be available (e.g. `file:///home/user/archives/` or `https://archive.example.com`)

`PUSHOVER_USER` (optional) is your Pushover user token, if you want to get notified when a link is processed

`PUSHOVER_TOKEN` (optional) is your Pushover application token, if you want to get notified when a link is processed

```bash
sudo docker run -d \
    --name=shaarli-archiver \
    -e SHAARLI_URL=https://shaarli.example.com \
    -e SHAARLI_TOKEN=abcdef \
    -e SHAARLI_TAG=to_archive \
    -e ARCHIVE_URL=https://archive.example.com \
    -e PUSHOVER_USER=abc \
    -e PUSHOVER_TOKEN=xyz \
    -v /some/local/folder/archives:/archives \
    ghcr.io/sebw/shaarli-archiver:0.3
```

## Or build the container yourself

```bash
git clone https://github.com/sebw/shaarli-archiver
cd shaarli-archiver
docker build . -t shaarli-archiver:0.3
```

## Troubleshooting

### Checking the logs

```bash
docker exec -it shaarli-archiver tail -f /var/log/shaarli-archiver.log
```

### Execute manually

```bash
docker exec -it shaarli-archiver sh
/usr/bin/python3 /usr/src/app/check.py
```