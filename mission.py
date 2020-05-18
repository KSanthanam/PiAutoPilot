#!/usr/bin/env python3
from AutoPilot.MissionPlanner import MissionPlanner

if __name__ == "__main__":
    mission = MissionPlanner(serial_port="/dev/ttyAMA0")
    mission.start_mission()
