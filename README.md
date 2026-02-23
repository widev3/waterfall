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

- `data`
- `lo`
- `tslice`
- `fslice`
- `frange`
- `trange`
- `show`
  - `waterfall`
  - `fslice`
  - `tslice`
    - `fft`
  - `ftot`
  - `ttot`
- `compute`
  - `tot`
  - `max`
  - `min`
  <!-- - `fft` -->
  - `fslice`
    - `tot`
    - `max`
    - `min`
    <!-- - `fft` -->
  - `tslice`
    - `tot`
    - `max`
    - `min`
    <!-- - `fft` -->
