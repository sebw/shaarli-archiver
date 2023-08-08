# Shaarli Archiver

[Shaarli](https://github.com/shaarli/Shaarli) doesn't have native local archiving possibilities.

[SingleFile](https://github.com/gildas-lormeau/SingleFile) provides an easy way to archive web pages in a single HTML file (embedding pictures!).

This container image combines the power of both!

## How does it work?

- this container will query your Shaarli instance every hour
- it searches your Shaarli for links with a specific tag that you define (e.g. `to_archive`)
- if bookmarks are found with that tag, SingleFile processes the links and saves the single HTML under `/archives` on the container filesystem (mount the folder!)
- when processed bookmarks are edited
  - description is updated with a link to the archive (e.g.: `file:///home/user/archives/1234_20200101_120000.html` or `https://archive.example.com/1234_20200101_120000.html`)
  - tag `shaarli-archiver` is added, making it easy to find archived bookmarks
- an (optional) notification is sent to Pushover (it uses the [apprise](https://github.com/caronc/apprise) library)
- when all links are processed, the dedicated and unique tag is deleted

## How a bookmark looks before processing

![](https://raw.githubusercontent.com/sebw/shaarli-archiver/master/screenshots/before.png)

## How it looks after processing

![](https://raw.githubusercontent.com/sebw/shaarli-archiver/master/screenshots/after.png)

The "Archived on..." is clickable and goes to `ARCHIVE_URL`/linkID_archivalDate.html

## Run the container

`SHAARLI_TAG` is the dedicated and unique tag that triggers the archiving.

`SHAARLI_TOKEN` is the token that can be found in your Shaarli under Tools > Configure your Shaarli > REST API secret

`ARCHIVE_URL` is where you will expose your archives (e.g. `file:///home/user/archives/`, `https://archive.example.com` or `https://archive.example.com/subfolder`)

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
    ghcr.io/sebw/shaarli-archiver:0.4
```

## Exposing your archives

If you want to expose your archives, you can use the `nginx` container image mounted to the same local folder:

```bash
docker run -d --restart unless-stopped --name shaarli-archiver-site -p 80:80 -v /some/local/folder/archives:/usr/share/nginx/html:ro -d nginx
```

## Build the container yourself

```bash
git clone https://github.com/sebw/shaarli-archiver
cd shaarli-archiver
docker build . -t shaarli-archiver:0.4
```

## Troubleshooting

### Checking the logs

```bash
docker exec -it shaarli-archiver tail -f /var/log/shaarli-archiver.log
```

### Execute manually

```bash
docker exec -it shaarli-archiver sh
/usr/bin/python3 /opt/check.py
```
