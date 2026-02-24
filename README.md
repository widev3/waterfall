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

`data`  
`lo`  
`tslice`  
`fslice`  
`frange`  
`trange`  
`compute`  
├──`tot`  
├──`max`  
├──`min`  
├──`fslice`  
│&emsp;&emsp;├──`tot`  
│&emsp;&emsp;├──`max`  
│&emsp;&emsp;└──`min`  
└──`tslice`  
&emsp;&emsp;├──`tot`  
&emsp;&emsp;├──`max`  
&emsp;&emsp;└──`min`  
`export`  
└──`tslice`  
`show`  
├──`waterfall`  
├──`tslice`  
│&emsp;&emsp;└──`fft`  
├──`fslice`  
├──`ftot`  
└──`ttot`  
