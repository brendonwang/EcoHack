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
