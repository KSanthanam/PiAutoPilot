#!/usr/bin/env python3
# from dronekit import connect, VehicleMode, LocationGlobalRelative
import time
from AutoPilot.MultiWii import MultiWii
from sys import stdout
import argparse
def scan_imu(board):
  try:
    while True:
      board.getData(MultiWii.RAW_IMU)
      print (board.attitude) #uncomment for regular printing

      # Fancy printing (might not work on windows...)
      message = "ax = {:+.0f} \t ay = {:+.0f} \t az = {:+.0f} gx = {:+.0f} \t gy = {:+.0f} \t gz = {:+.0f} mx = {:+.0f} \t my = {:+.0f} \t mz = {:+.0f} \t elapsed = {:+.4f} \t" .format(float(board.rawIMU['ax']),float(board.rawIMU['ay']),float(board.rawIMU['az']),float(board.rawIMU['gx']),float(board.rawIMU['gy']),float(board.rawIMU['gz']),float(board.rawIMU['mx']),float(board.rawIMU['my']),float(board.rawIMU['mz']),float(board.attitude['elapsed']))
      stdout.write("\r%s" % message )
      stdout.flush()
      # End of fancy printing
  except Exception as error:
      print ("Error on Main: "+str(error))
if __name__ == "__main__":
  parser = argparse.ArgumentParser(description='commands')
  parser.add_argument('--connect')
  args = parser.parse_args()
    # serial_port = '/dev/cu.usbmodem3672326532381'
  connect_string = args.connect
  if connect_string != None:
    board = MultiWii(serial_port=connect_string)
    scan_imu(board)
  else:
    print("No connection string supplied")

