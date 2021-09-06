# EcoHack

## prebuild release 
[Mac](https://www.dropbox.com/s/vbibrl4j87q08xv/EcoHack?dl=0) | [Windows](https://www.dropbox.com/s/i51nn670mq5ymxh/EcoHack.exe?dl=0)

## pre requisite
```
conda install pygame
```

## run the game
```
python main.py
```

## release the game
 * install pyinstaller
```
conda install pyinstaller
```
 * release
 mac/linux
 ```
 pyinstaller --onefile -n EcoHack  --add-data "asset/*.*:./asset"  main.py
 ```
 windows
 ```
 pyinstaller --onefile -n EcoHack  --add-data "asset/*.*;./asset"  main.py
 ```
