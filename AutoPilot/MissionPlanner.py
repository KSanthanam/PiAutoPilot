#!/usr/bin/env python3

"""Plan the Trip"""
from . import MultiWii
from sys import stdout

class MissionPlanner(object):
  board = None
  PRINT = 1
  def __init__(self, **kwargs):
    self._serial_port = kwargs.get("serial_port",'/dev/ttyACM0')      
    self.board = MultiWii(serial_port="/dev/ttyACM0")
    # try:
    #   while True:
    #     self.board.getData(MultiWii.RAW_IMU)
    #     print (self.board.attitude) #uncomment for regular printing

    #     # Fancy printing (might not work on windows...)
    #     message = "ax = {:+.0f} \t ay = {:+.0f} \t az = {:+.0f} gx = {:+.0f} \t gy = {:+.0f} \t gz = {:+.0f} mx = {:+.0f} \t my = {:+.0f} \t mz = {:+.0f} \t elapsed = {:+.4f} \t" .format(float(self.board.rawIMU['ax']),float(self.board.rawIMU['ay']),float(self.board.rawIMU['az']),float(self.board.rawIMU['gx']),float(self.board.rawIMU['gy']),float(self.board.rawIMU['gz']),float(self.board.rawIMU['mx']),float(self.board.rawIMU['my']),float(self.board.rawIMU['mz']),float(self.board.attitude['elapsed']))
    #     stdout.write("\r%s" % message )
    #     stdout.flush()
    #     # End of fancy printing
    # except Exception as error:
    #   print ("Error on Main: "+str(error))

  def start_mission(self,start_lat=None,start_lng=None,end_lat=None,end_lng=None):
    if start_lat == None or start_lng == None or end_lat == None or end_lng == None:
      if self.PRINT:
        print("invalid coordinates givens (%f, %f),(%f,%f)", start_lat, start_lng, end_lat, end_lng)
      return False
    try:
      while True:
        self.board.getData(MultiWii.RAW_GPS)
        # Fancy printing (might not work on windows...)
        message = "lat = {:+.0f} \t lng = {:+.0f} \t elapsed = {:+.4f} \t" .format(float(self.board.rawGPS['lat']),float(self.board.rawGPS['lng']),float(self.board.attitude['elapsed']))
        stdout.write("\r%s" % message )
        stdout.flush()
        # End of fancy printing
    except Exception as error:
      print ("Error on Main: "+str(error))

    return True


