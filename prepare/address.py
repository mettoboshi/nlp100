import requests
import csv
import zipfile
import os
import codecs

ZIP_CODE_URL = "http://www.post.japanpost.jp/zipcode/dl/kogaki/zip/ken_all.zip"
DIR_PATH = "../data/"
FILE_NAME = "address.txt"

def main():
  zipFileName = os.path.basename(ZIP_CODE_URL)
#  getData(zipFileName)
  files = unZip(zipFileName)
  datasets = getDatasets(files[0]) 
  writeFile(datasets)

def getData(zipFileName):
  req = requests.get(ZIP_CODE_URL)
  with open(DIR_PATH + zipFileName, "wb") as f:
    f.write(req.content)

def unZip(zipFileName):
  path = DIR_PATH + zipFileName

  files = []
  with zipfile.ZipFile(path, "r") as zdir:
    for zf in zdir.namelist():
      wpath = DIR_PATH + str(zf)
      files.append(zf)
      with open(wpath, "wb") as unziped:
        unziped.write(zdir.read(zf))

  return files    

def getDatasets(filename):
  
  PREFECTURE = 6
  CITY = 7
  TOWN = 8

  address_set=set()
  with codecs.open(DIR_PATH + filename, "r", "shift_jis") as fin:
    rows = csv.reader(fin, delimiter=",")
    for row in rows:
      address = "".join([row[PREFECTURE], row[CITY]])
      town = row[TOWN]
      if town == "以下に掲載がない場合":
        continue
      else:
        sections = town.split("、") 
        for s in sections:
          house_number_index_en = s.find("(")
          house_number_index_em = s.find("（")
          if house_number_index_en > -1:
            s = s[:house_number_index_en]
          elif house_number_index_em > -1:
            s = s[:house_number_index_em]
          address_set.add((address, s))
      
  datasets = []
  for add1, add2 in address_set:
    datasets.append((add1, add2))

  return datasets

def writeFile(datasets):
  separator = "\t"
  opath = DIR_PATH + FILE_NAME

  with open(opath, "wb") as of:
    for dataset in datasets:
      if isinstance(dataset, list) or isinstance(dataset, tuple):
        line = ""
        line = separator.join(dataset) + "\n"
        print(line)
      of.write(line.encode("utf-8"))
  return

if __name__ == "__main__":
  main()
