#!/usr/bin/env python3
from AutoPilot.MissionPlanner import MissionPlanner
import argparse
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--port", help="echo the string you use here")
    args = parser.parse_args()
    print(args.port)
    if args.port != None:

        exit(-1)
    mission = MissionPlanner(serial_port=args.port)
    mission.start_mission(corner1=(55,65), corner2=(65,55))
