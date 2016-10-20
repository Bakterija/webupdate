# webupdate
My system for updating kivy apps from zip files on a apache webserver.    
Tested in **Ubuntu 16.x**.

**build_updater.py** increases version number in a text file by one and puts a zip archive of current folder (bin/ and .buildozer/ excluded) in a target folder (should be a webserver folder for apache_updater.py to read)

**apache_updater.py** reads the target webaddress with requests module and looks for 'href="apd_ver'+vernumber+".zip", appends all the found links to a list and checks for higher version numbers. If an update is found, the newest .zip archive is downloaded and extracted in app folder

## How to use
**Updating:**    
Put web_updater in application folder
```python
## import it in application
from web_updater.apache_updater import ApacheUpdater
## Instantiate
app_updater =  ApacheUpdater()
## Set version path
app_updater.version_path = sys.path[4]+'/web_updater/version.txt'  #place where updater finds its own version number
## Set update path
app_updater.update_path = sys.path[4]+'/'  #Place where update files will be extracted
## Set http path
app_updater.http_path = 'http://localhost/'  #Web address from which .zip file updates will be downloaded

## Run update
app_updater.check_update_thread()  #In a different thread
app_updater.check_update()  #In main thread
```
**Making new web builds:**    
Make changes to application    
Open terminal in application folder
Make new zipfile and move it to webserver folder with below commands
```Bash
#Zip app folder contents
python web_updater/build_updater.py
##Set folder where to move zipfile
python web_updater/build_updater.py --webpath /var/www/html/myfolder/
#Run "buildozer android debug" and zip .buildozer/android/app/*
python web_updater/build_updater.py --buildozer-android  
#Run "buildozer android debug new" and zips .buildozer/android/app/*
python web_updater/build_updater.py --buildozer-android_new   .buildozer/android/app/*
```
