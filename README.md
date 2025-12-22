# Waterfall

## Build bash

```bash
pyinstaller main.py \
    --workpath=./build \
    --specpath=./ \
    --distpath=./dist \
    --noconfirm \
    --log-level=TRACE \
    --onedir \
    --name=`basename "$PWD"` \
    --add-data=despyner/icons/:despyner/icons/ \
    --add-data=wide3.ico:. \
    --optimize=2
```
