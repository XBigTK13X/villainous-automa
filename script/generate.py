import os
import sys
import csv

disney_villains = []
with open('print-and-play/nandeck/disney.csv','r') as read_handle:
    csv_reader = csv.reader(read_handle, delimiter=',')
    count = 0
    for row in csv_reader:
        if count > 0:
            villain = {
                'name': row[0],
                'box': row[1],
                'special': row[2],
                'preference': row[3],
                'fate1': row[4],
                'fate2': row[5],
                'fate3': row[6],
                'brain_id': f'disney_{count}.jpg'
            }
            if villain['name'] in ['Captain Hook', 'Maleficent', 'Prince John', 'Ursula']:
                villain['name'] = f'{villain["name"]} ({"ItE" if "Intro" in villain["box"] else "TWTiA"})'
            disney_villains.append(villain)
        count += 1

marvel_villains = []
with open('print-and-play/nandeck/marvel.csv','r') as read_handle:
    csv_reader = csv.reader(read_handle, delimiter=',')
    count = 0
    for row in csv_reader:
        if count > 0:
            marvel_villains.append({
                'name': row[0],
                'box': row[1],
                'special': row[2],
                'preference': row[3],
                'fate1': row[4],
                'fate2': row[5],
                'fate3': row[6],
                'brain_id': f'marvel_{count:02d}.jpg'
            })
        count += 1
villains_content = 'window.villains_list = {'
villains_content += "\n\tdisney: ["
disney_villains = sorted(disney_villains, key=lambda x: x['name'])
for vv in disney_villains:
    villains_content += f'\n\t\t{{name: "{vv["name"]}", box: "{vv["box"]}", special: "{vv["special"]}", preference: "{vv["preference"]}", fate1: "{vv["fate1"]}", fate2: "{vv["fate2"]}", fate3: "{vv["fate3"]}", brainId: "{vv["brain_id"]}"}},'
villains_content += "\n\t],"
villains_content += "\n\tmarvel: ["
marvel_villains = sorted(marvel_villains, key=lambda x: x['name'])
for vv in marvel_villains:
    villains_content += f'\n\t\t{{name: "{vv["name"]}", box: "{vv["box"]}", special: "{vv["special"]}", preference: "{vv["preference"]}", fate1: "{vv["fate1"]}", fate2: "{vv["fate2"]}", fate3: "{vv["fate3"]}", brainId: "{vv["brain_id"]}"}},'
villains_content += "\n\t]"
villains_content += '\n}'

with open('docs/js/villains.js', 'w') as write_handle:
    write_handle.write(villains_content)