# XRF

Steps to running the app:
1) Install Python, pip, etc.
2) clone repo
3) pip install -r requirements.txt
4) python app.py

To build the app on a Mac:
1) Make sure the build and dist folders are deleted (rm -rf build dist)
2) Install py2app using "pip install py2app"
3) In the XRF directory, run "python setup.py py2app"
4) The new app file should be in the dist folder
5) If planning on distributing and need to zip, use "zip --symlinks -r app.zip app.app/"
