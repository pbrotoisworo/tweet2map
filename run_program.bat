@echo off
rem [PYTHON INTERPRETER] [python file]
rem First script is the Tweet2Map.py file which runs under Python 3
rem Second script is the ArcPy script which needs ArcPy and Python 2
"C:\ProgramData\Anaconda3\python.exe" "C:\Users\Panji\Documents\Python Scripts\Non-Jupyter Py Scripts\MMDA Tweet2Map\Tweet2Map.py"
"C:\Python27\ArcGIS10.6\python.exe" "C:\Users\Panji\Documents\Python Scripts\Non-Jupyter Py Scripts\MMDA Tweet2Map\arcpy_Spatial_Join_City.py"
