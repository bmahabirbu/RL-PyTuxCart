# HOW TO RUN:
#first cd into your directory with your CA5 files
#python -m Runtime_to_csv
#Credit to Marcel edited his code from testcoding4.py
#Rename Runtime_template to Runtime_data to start saving data
import sys
import os
import subprocess
import pandas as pd
import numpy as np

dirname = os.path.dirname(__file__)
filename = os.path.join(dirname, r'Runtime_data.csv')

test_controller_or_planner = input("Test Controller or Planner (C or P): ")

while (test_controller_or_planner != "C") and (test_controller_or_planner != "P"):
    print(test_controller_or_planner)
    test_controller_or_planner = input("Please type valid answer, Test Controller or Planner (C or P): ")
    
if test_controller_or_planner == "P":
    planner_type = input("Name of planner: ")
else:
    planner_type = "Controller"

controller_type = input("Controller type AI or NO_AI: ")

while (controller_type != "AI") and (controller_type != "NO_AI"):
    print(test_controller_or_planner)
    controller_type = input("Please type valid answer, Controller type AI or NO_AI: ")

if controller_type == "AI":
    with open('utils.py', 'r') as file:
    # read a list of lines into data
        data = file.readlines()
        
    for count, line in enumerate(data):
        if line.strip() == 'config.players[0].controller = pystk.PlayerConfig.Controller.AI_CONTROL':
            print("Already AI controlled")
            break
        
        elif line.strip() == 'config.players[0].controller = pystk.PlayerConfig.Controller.PLAYER_CONTROL':
            print("Changing to AI controlled in utils")
            data[count] = '            config.players[0].controller = pystk.PlayerConfig.Controller.AI_CONTROL\n'
            # and write everything back
            with open('utils.py', 'w') as file:
                file.writelines( data )
        
        
            
elif controller_type == "NO_AI":
    with open('utils.py', 'r') as file:
    # read a list of lines into data
        data = file.readlines()
        
    for count, line in enumerate(data):
        if line.strip() == 'config.players[0].controller = pystk.PlayerConfig.Controller.PLAYER_CONTROL':
            print("Already Player controlled")
            break
        
        elif line.strip() == 'config.players[0].controller = pystk.PlayerConfig.Controller.AI_CONTROL':
            print("Changing to AI controlled in utils")
            data[count] = '            config.players[0].controller = pystk.PlayerConfig.Controller.PLAYER_CONTROL\n'
            # and write everything back
            with open('utils.py', 'w') as file:
                file.writelines( data )
    

df1 = pd.DataFrame([[planner_type, controller_type,"asd","asd","asd","asd","asd","asd","asd"]],
                   #columns=['Planner Type', 'Controller Type', 'Zengarden', 'lighthouse', 'hacienda',
                   #         'snowtuxpeak', 'cornfield_crossing', 'scotland', 'cocoa_temple'],
                   )

print(f'== Save Runtimes to CSV ==')
map_times = {
    'zengarden' : 50,
    'lighthouse' : 50,
    'hacienda' : 60,
    'snowtuxpeak' : 60,
    'cornfield_crossing' : 70,
    'scotland' : 70,
    'cocoa_temple': 70
}
#dictionary maps name of track to #column where its located
map_nums = {
    'zengarden' : 2,
    'lighthouse' : 3,
    'hacienda' : 4,
    'snowtuxpeak' : 5,
    'cornfield_crossing' : 6,
    'scotland' : 7,
    'cocoa_temple': 8
}

if planner_type == "Controller":
    cmd = "python -m controller " # change if error occurs (could have python as python3)
else:
    cmd = "python -m planner " # change if error occurs (could have python as python3)
    
print("Running command: "+cmd)

for key in map_times.keys():
    res = subprocess.check_output(f"{cmd} {key}", shell=True, universal_newlines=True)
    if float(res.split(' ')[0]) / 10 <= map_times[key]:
        print(f"[+] {key} passed with {float(res.split(' ')[0]) / 10}s")
        df1.at[0, map_nums.get(key)] = float(res.split(' ')[0]) / 10
    else:
        print(f"[+] {key} failed with {float(res.split(' ')[0]) / 10}s")
        df1.at[0, map_nums.get(key)] = float(res.split(' ')[0]) / 10

#print(df1)
df1.to_csv(filename,index=False,header=False,mode='a')
