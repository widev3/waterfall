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

## Commands tree

- `data`      👍
- `lo`        👍
- `tslice`    👍
- `fslice`    👍
- `frange`    👍
- `trange`    👍
- `compute`
  - `tot`
  - `max`
  - `min`
  - `fslice`
    - `tot`
    - `max`
    - `min`
  - `tslice`
    - `tot`
    - `max`
    - `min`
- `export`
  - `tslice`
- `show`
  - `waterfall`
  - `tslice`
    - `fft`
  - `fslice`
  - `ftot`
  - `ttot`
