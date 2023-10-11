import os
import pysteamcmd.steamcmd as pysteam
import time
import wget
import zipfile
import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
from urllib.parse import urlparse, parse_qs
import shutil

STEAMCMD_PATH = "./bin/steamcmd/"
STEAMCMD_FILENAME = "steamcmd.exe"
STEAMCMD_ARCHIVENAME = "steamcmd.zip"
GAME_EXECUTABLENAME= "SlayTheSpire.exe"
MOD_DIR = "./temp"

def checkIfFileExists(filePath):
  return os.path.isfile(filePath)

def checkIfDirectoryExists(dirPath):
  return os.path.isdir(dirPath)

def createDirectory(dirPath):
  os.makedirs(dirPath)

def downloadSteamCmd():
  if(checkIfDirectoryExists(STEAMCMD_PATH) == False):
    createDirectory(STEAMCMD_PATH)
  
  STEAMCMD_URL = "https://steamcdn-a.akamaihd.net/client/installer/steamcmd.zip"
  wget.download(STEAMCMD_URL, STEAMCMD_PATH+STEAMCMD_ARCHIVENAME)

  while(checkIfFileExists(STEAMCMD_PATH+STEAMCMD_ARCHIVENAME) == False):
    time.sleep(5)
  
  with zipfile.ZipFile(STEAMCMD_PATH+STEAMCMD_ARCHIVENAME, "r") as STEAM_ARCHIVE:
    STEAM_ARCHIVE.extractall(STEAMCMD_PATH)
  time.sleep(5)
  os.remove(STEAMCMD_PATH+STEAMCMD_ARCHIVENAME)

# steamcmd = pysteam.Steamcmd(STEAMCMD_PATH)
# steamcmd.install_workshopfiles(gameid=646570, workshop_id=2920075378 ,game_install_dir=MOD_DIR, user='anonymous', password=None)

#WINDOW

if not(checkIfFileExists(STEAMCMD_PATH+STEAMCMD_FILENAME)):
  downloadSteamCmd()

correct_path = False
game_path = ""
steamcmd = pysteam.Steamcmd(STEAMCMD_PATH)

statusModTheSpire = False
statusStSLib = False
statusBaseMod = False

def selectFile():
    
    global correct_path
    global game_path

    game_path = filedialog.askdirectory(title="Select Game Directory") + "/"
    if game_path:
      print("Selected path:", game_path)
      if (os.path.isfile(game_path + GAME_EXECUTABLENAME)):
        correct_path = True
        button.config(text="Game found ✔")
        checkIfRequiredLibsAreInstalled()
      else:
        requiredLibsLabel.config(text="")
        correct_path = False
        button.config(text="Game not found ✘")
      # Update the label to display the selected game_path
      label.config(text=game_path)
    

def isURLCorrect(URL):
  parsed_url = urlparse(URL)
  queries = parse_qs(parsed_url.query)
  if queries["id"] and len(queries["id"]) > 0:
    return True
  return False

def getQueries(URL):
  parsed_url = urlparse(URL)
  queries = parse_qs(parsed_url.query)

  return queries

def checkIfRequiredLibsAreInstalled():
  print("check")
  statusModTheSpire = os.path.isfile(game_path+"ModTheSpire.jar")
  statusBaseMod = os.path.isfile(game_path+"mods/BaseMod.jar")
  statusStSLib = os.path.isfile(game_path+"mods/StSLib.jar")

  requiredLibsLabel.config(text=f"\nModTheSpire: {statusModTheSpire}\nBaseMod: {statusBaseMod}\nStSLib: {statusStSLib}")

  return
  

def downloadModTheSpire():
  MOD_ID = 1605060445
  try:
    os.mkdir("./temp")
    steamcmd.install_workshopfiles(gameid=646570, workshop_id=MOD_ID ,game_install_dir=os.path.abspath(MOD_DIR), user='anonymous', password=None)
  except:
    statusModTheSpire = False
  else:
    try:
      shutil.copytree(f"{MOD_DIR}/steamapps/workshop/content/646570/{MOD_ID}/", game_path, dirs_exist_ok=True)
      print(f"Directory contents copied")
    except FileNotFoundError:
      print("Source directory not found.")
    except FileExistsError:
      print("Destination directory already exists. Remove or choose a different destination.")
    except PermissionError:
      print("Permission denied. Make sure you have the necessary permissions.")
    except Exception as e:
      print(f"An error occurred: {e}")
    statusModTheSpire = True
  finally:
    shutil.rmtree("./temp")
    return statusModTheSpire
    
def downloadBaseMod():
  MOD_ID = 1605833019
  if not os.path.isdir(game_path+"mods"):
    os.mkdir(game_path+"mods")
  try:
    os.mkdir("./temp")
    steamcmd.install_workshopfiles(gameid=646570, workshop_id=MOD_ID ,game_install_dir=os.path.abspath(MOD_DIR), user='anonymous', password=None)
  except:
    statusBaseMod = False
  else:
    try:
      shutil.copytree(f"{MOD_DIR}/steamapps/workshop/content/646570/{MOD_ID}/", f"{game_path}/mods", dirs_exist_ok=True)
      print(f"Directory contents copied")
    except FileNotFoundError:
      print("Source directory not found.")
    except FileExistsError:
      print("Destination directory already exists. Remove or choose a different destination.")
    except PermissionError:
      print("Permission denied. Make sure you have the necessary permissions.")
    except Exception as e:
      print(f"An error occurred: {e}")
    statusBaseMod = True
  finally:
    shutil.rmtree("./temp")
    return statusBaseMod
  
def downloadStSLib():
  MOD_ID = 1609158507
  if not os.path.isdir(game_path+"mods"):
    os.mkdir(game_path+"mods")
  try:
    os.mkdir("./temp")
    steamcmd.install_workshopfiles(gameid=646570, workshop_id=MOD_ID ,game_install_dir=os.path.abspath(MOD_DIR), user='anonymous', password=None)
  except:
    statusStSLib = False
  else:
    try:
      shutil.copytree(f"{MOD_DIR}/steamapps/workshop/content/646570/{MOD_ID}/", f"{game_path}/mods", dirs_exist_ok=True)
      print(f"Directory contents copied")
    except FileNotFoundError:
      print("Source directory not found.")
    except FileExistsError:
      print("Destination directory already exists. Remove or choose a different destination.")
    except PermissionError:
      print("Permission denied. Make sure you have the necessary permissions.")
    except Exception as e:
      print(f"An error occurred: {e}")
    statusStSLib = True
  finally:
    shutil.rmtree("./temp")
    return statusStSLib

def downloadRequiredLibs():
  if not correct_path:
    statusLabel.config(text="Status: invalid game path")
    return
  downloadModTheSpire()
  downloadBaseMod()
  downloadStSLib()
  checkIfRequiredLibsAreInstalled()
  statusLabel.config(text="Required mods have been downloaded successfully")

def downloadWorkshopFile():
  if not correct_path:
    statusLabel.config(text="Status: invalid game path")
    return
  
  URL = input.get()

  if not isURLCorrect(URL):
    statusLabel.config(text="Workshop url is incorrect")
  
  workshopID = getQueries(URL)["id"][0]

  if not os.path.isdir(game_path+"mods"):
    os.mkdir(game_path+"mods")
  try:
    os.mkdir("./temp")
    steamcmd.install_workshopfiles(gameid=646570, workshop_id=int(workshopID) ,game_install_dir=os.path.abspath(MOD_DIR), user='anonymous', password=None)
  except:
    print("ERROR STEAMCMD")
    return
  else:
    statusLabel.config(text="Succesfully downloaded " + workshopID)
    try:
      shutil.copytree(f"{MOD_DIR}/steamapps/workshop/content/646570/{workshopID}/", f"{game_path}/mods", dirs_exist_ok=True)
      print(f"Directory contents copied")
    except FileNotFoundError:
      print("Source directory not found.")
    except FileExistsError:
      print("Destination directory already exists. Remove or choose a different destination.")
    except PermissionError:
      print("Permission denied. Make sure you have the necessary permissions.")
    except Exception as e:
      print(f"An error occurred: {e}")
  finally:
    shutil.rmtree("./temp")


window = tk.Tk()
window.title("Better Spire Modding")
window.geometry("800x300")

label = ttk.Label(master=window, text=game_path)
label.pack()

button = ttk.Button(master=window, text="Find game", command=selectFile)
button.pack()


inputLabel = ttk.Label(master=window, text="Workshop url:")
inputLabel.pack()
input  = ttk.Entry(master=window, width=80)
input.pack()

downloadButton = ttk.Button(master=window, text="Download mod", command=downloadWorkshopFile)
downloadButton.pack()

statusLabel = ttk.Label(master=window, text="Status: -")
statusLabel.pack() 

requiredLibsLabel = ttk.Label(master=window, text="")
requiredLibsLabel.pack()

requiredLibsButton = ttk.Button(master=window, text="Redownload Required Mods", command=downloadRequiredLibs)
requiredLibsButton.pack()

window.mainloop()