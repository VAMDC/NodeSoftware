def append_base_path(depth):
  import sys
  import os
  mypath=os.path.abspath(__file__)
  for i in range(0,depth):
    mypath=os.path.dirname(mypath)
  sys.path.append(mypath)
  print(mypath)
  return mypath