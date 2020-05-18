#!/usr/bin/env python3
from AutoPilot.MultiWii import MultiWii
from dronekit import connect, VehicleMode, LocationGlobalRelative
import time
if __name__ == "__main__":
  port = "/dev/cu.usbmodem3672326532381"
  vehicle = MultiWii(serial_port=port)
#!/usr/bin/env python

"""show-attitude.py: Script to ask the MultiWii Board attitude and print it."""

__author__ = "Aldo Vargas"
__copyright__ = "Copyright 2017 Altax.net"

__license__ = "GPL"
__version__ = "1.1"
__maintainer__ = "Aldo Vargas"
__email__ = "alduxvm@gmail.com"
__status__ = "Development"

from AutoPilot.MultiWii import MultiWii
from sys import stdout
def scan_imu(board):
  try:
    while True:
      board.getData(MultiWii.RAW_IMU)
      #print (board.attitude) #uncomment for regular printing

      # Fancy printing (might not work on windows...)
      message = "ax = {:+.0f} \t ay = {:+.0f} \t az = {:+.0f} gx = {:+.0f} \t gy = {:+.0f} \t gz = {:+.0f} mx = {:+.0f} \t my = {:+.0f} \t mz = {:+.0f} \t elapsed = {:+.4f} \t" .format(float(board.rawIMU['ax']),float(board.rawIMU['ay']),float(board.rawIMU['az']),float(board.rawIMU['gx']),float(board.rawIMU['gy']),float(board.rawIMU['gz']),float(board.rawIMU['mx']),float(board.rawIMU['my']),float(board.rawIMU['mz']),float(board.attitude['elapsed']))
      stdout.write("\r%s" % message )
      stdout.flush()
      # End of fancy printing
  except Exception as error:
      print ("Error on Main: "+str(error))
if __name__ == "__main__":
    #board = MultiWii("/dev/ttyUSB0")
    serial_port = '/dev/cu.usbmodem3672326532381'
    board = MultiWii(serial_port=serial_port)
    scan_imu(board)

