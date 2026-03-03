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

## Commands

|command|arg1|arg2|arg3|
|-|-|-|-|
|`load`|filename: str|[object_name: str]||
|`lo`|value: float|[object_name: str]||
|`tslice`|value: float|[object_name: str]||
|`fslice`|value: float|[object_name: str]||
|`frange`|start_value: float|stop_value: float|[object_name: str]|
|`trange`|start_value: float|stop_value: float|[object_name: str]|
|`compute`||||
|├──`tot`||||
|├──`max`||||
|├──`min`||||
|├──`fslice`||||
|│&emsp;&emsp;├──`tot`||||
|│&emsp;&emsp;├──`max`||||
|│&emsp;&emsp;└──`min`||||
|└──`tslice`||||
|&emsp;&emsp;├──`tot`||||
|&emsp;&emsp;├──`max`||||
|&emsp;&emsp;└──`min`||||
|`show`||||
|├──`waterfall`||||
|├──`tslice`||||
|│&emsp;&emsp;└──`fft`||||
|├──`fslice`||||
|├──`ftot`||||
|└──`ttot`||||

`object_name` is `.` by default. Hence, when not specified, command operate on the same object.
