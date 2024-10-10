set "embree3=.\embree3"

if not exist "%embree3%" (
    curl -L -o embree3.zip https://github.com/RenderKit/embree/releases/download/v3.13.5/embree-3.13.5.x64.vc14.windows.zip
    tar -xf .\embree3.zip
    del .\embree3.zip
    move .\embree-3.13.5.x64.vc14.windows embree3
)
