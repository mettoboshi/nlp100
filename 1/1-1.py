# -*- coding: utf-8 -*-

DATA = "../data/address.txt"

def main():

  recNum = 0
  fin = open(DATA, "r")
  for row in fin:
    recNum = recNum + 1

  print("Record:" + str(recNum))


if __name__ == "__main__":
  main()

