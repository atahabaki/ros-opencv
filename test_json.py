#!/usr/bin/env python
import json

def read_from_file(path):
    try:
        with open(path,"r") as file:
            return json.load(file)
    except:
        print("Could not convert \"{}\"...".format(path))
        return None

def main():
    resp=read_from_file("/home/atahabaki/Documents/mission_test_1.json")
    if resp != None:
        print(resp["waypoints"][0]["altitude"])
        print(resp["waypoints"][1]["altitude"])
        print(resp["waypoints"][2]["altitude"])

if __name__ == "__main__":
    main()
