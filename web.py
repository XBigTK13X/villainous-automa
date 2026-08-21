import os
import sys
import csv

print("Preparing web payloads")

disney_variants = {
    "Captain Hook": ["Worst", "Intro"],
    "Maleficent": ["Worst", "Intro", "Darkness"],
    "Prince John": ["Worst", "Intro"],
    "Ursula": ["Worst", "Intro", "Darkness"],
    "Evil Queen": ["Wicked", "Darkness"],
    "Sanderson Sisters": ["Fly", "Darkness"],
}

disney_villains = []
with open("print-and-play/disney/villains.csv", "r") as read_handle:
    csv_reader = csv.reader(read_handle, delimiter=",")
    count = 0
    for row in csv_reader:
        if count > 0:
            villain = {
                "enable": row[0],
                "name": row[1],
                "box": row[2],
                "special": row[3],
                "preference": row[4],
                "fate1": row[5],
                "fate2": row[6],
                "fate3": row[7],
                "brain_id": f"villains_{count}.jpg",
            }
            if villain["name"] in disney_variants:
                if (
                    "Worst" in disney_variants.get(villain["name"], "")
                    and "Worst" in villain["box"]
                ):
                    villain["name"] = f"{villain['name']} (TWTiA)"
                if (
                    "Intro" in disney_variants.get(villain["name"], "")
                    and "Intro" in villain["box"]
                ):
                    villain["name"] = f"{villain['name']} (ItE)"
                if (
                    "Darkness" in disney_variants.get(villain["name"], "")
                    and "Darkness" in villain["box"]
                ):
                    villain["name"] = f"{villain['name']} (DB)"
                if (
                    "Wicked" in disney_variants.get(villain["name"], "")
                    and "Wicked" in villain["box"]
                ):
                    villain["name"] = f"{villain['name']} (WttC)"
                if (
                    "Fly" in disney_variants.get(villain["name"], "")
                    and "Fly" in villain["box"]
                ):
                    villain["name"] = f"{villain['name']} (CWF)"
            disney_villains.append(villain)
        count += 1

marvel_villains = []
with open("print-and-play/marvel/villains.csv", "r") as read_handle:
    csv_reader = csv.reader(read_handle, delimiter=",")
    count = 0
    for row in csv_reader:
        if count > 0:
            marvel_villains.append(
                {
                    "name": row[0],
                    "box": row[1],
                    "special": row[2],
                    "preference": row[3],
                    "fate1": row[4],
                    "fate2": row[5],
                    "fate3": row[6],
                    "brain_id": f"marvel_{count:02d}.jpg",
                }
            )
        count += 1
villains_content = "window.villains_list = {"
villains_content += "\n\tdisney: ["
disney_villains = sorted(disney_villains, key=lambda x: x["name"])
for vv in disney_villains:
    villains_content += f'\n\t\t{{name: "{vv["name"]}", box: "{vv["box"]}", special: "{vv["special"]}", preference: "{vv["preference"]}", fate1: "{vv["fate1"]}", fate2: "{vv["fate2"]}", fate3: "{vv["fate3"]}", brainId: "{vv["brain_id"]}"}},'
villains_content += "\n\t],"
villains_content += "\n\tmarvel: ["
marvel_villains = sorted(marvel_villains, key=lambda x: x["name"])
for vv in marvel_villains:
    villains_content += f'\n\t\t{{name: "{vv["name"]}", box: "{vv["box"]}", special: "{vv["special"]}", preference: "{vv["preference"]}", fate1: "{vv["fate1"]}", fate2: "{vv["fate2"]}", fate3: "{vv["fate3"]}", brainId: "{vv["brain_id"]}"}},'
villains_content += "\n\t]"
villains_content += "\n}"

with open("docs/js/villains.js", "w") as write_handle:
    write_handle.write(villains_content)
