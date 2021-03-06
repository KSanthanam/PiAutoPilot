#!/usr/bin/env python3

"""https://code.google.com/archive/p/multiwii/"""
"""MultiWii.py: Handles Multiwii Serial Protocol."""

import serial, time, struct, math
import numpy as np

class MultiWii(object):

    """Multiwii Serial Protocol message ID"""
    """updated for only modern Cleanflight codes"""


    IDENT = 100

    BOX = 113
    MISC = 114
    WP = 118
    BOXIDS = 119    
    RC_RAW_IMU = 121


    SET_RAW_GPS = 201
    SET_BOX = 203
    SET_MISC = 207

    SET_WP = 209
    IS_SERIAL = 211
    SET_MOTOR = 214

    DEBUG = 254

    VTX_CONFIG = 88
    VTX_SET_CONFIG = 89
    EEPROM_WRITE = 250
    REBOOT = 68


    STATUS = 101
    RAW_IMU = 102
    SERVO = 103
    MOTOR = 104
    RC = 105
    RAW_GPS = 106
    COMP_GPS = 107
    ATTITUDE = 108
    ALTITUDE = 109
    ANALOG = 110
    RC_TUNING = 111
    PID = 112
    MOTOR_PINS = 115
    BOXNAMES = 116
    PIDNAMES = 117
    BOXIDS = 119
    
    SET_RAW_RC = 200
    SET_PID = 202
    SET_RC_TUNING = 204
    ACC_CALIBRATION = 205
    MAG_CALIBRATION = 206
    RESET_CONF = 208
    SWITCH_RC_SERIAL = 210
    SET_MOTOR = 214
    DEBUG = 254

    AUX = [1000,1000,1000,1000]
    THROTTLE = 1100

    # !IMPORTANT! set to your min and max based on ESC mode in Cleanflight
    def convertThrottlePercentToRaw(self, percentOutOf100, THROTTLE_MIN = 1000, THROTTLE_MAX = 2000):
        value_range = THROTTLE_MAX - THROTTLE_MIN
        return math.floor(THROTTLE_MIN + (percentOutOf100/100)*value_range)

    def convertSignedPercentToRPYValue(self, signed_percent_out_of_100, rpy_min = 1000, rpy_max = 2000, rpy_neutral = 1500):
        if (signed_percent_out_of_100 < 0):
            value_range = rpy_neutral - rpy_min
            return math.floor(rpy_neutral + (signed_percent_out_of_100/100)*value_range)
        elif (signed_percent_out_of_100 >= 0):
            value_range = rpy_max - rpy_neutral
            return math.floor(rpy_neutral + (signed_percent_out_of_100/100)*value_range)

    def setRawRC(self, roll = 1500, pitch = 1500, yaw = 1500, throttle = 1100):
        self.THROTTLE = throttle
        data = [roll,pitch,throttle,yaw,self.AUX[0],self.AUX[1],self.AUX[2],self.AUX[3]]
        self.sendCMD(16,MultiWii.SET_RAW_RC,data)

    def setRCneutral(self, throttle = 1100):
        self.THROTTLE = throttle
        data = [1500,1500,throttle,1500,self.AUX[0],self.AUX[1],self.AUX[2],self.AUX[3]]
        self.sendCMD(16,MultiWii.SET_RAW_RC,data)

    def setAuxValue(self, aux1, aux2, aux3, aux4):
        self.AUX = [aux1, aux2, aux3, aux4]
        self.setRCneutral()

    def enableAuxMode(self, which_aux_indexed_at_0 = 0, enable_value = 1900):
        self.AUX[which_aux_indexed_at_0] = enable_value
        self.setRCneutral()

    """Class initialization"""
    def __init__(self, **kwargs):
      """Global variables of data"""
      super(MultiWii, self).__init__()
      self._serial_port = kwargs.get("serial_port",'/dev/ttyACM0')      

      self.PIDcoef = {'rp':0,'ri':0,'rd':0,'pp':0,'pi':0,'pd':0,'yp':0,'yi':0,'yd':0}
      self.rcChannels = {'roll':0,'pitch':0,'yaw':0,'throttle':0,'elapsed':0,'timestamp':0}
        ## IMU
        # Output Ports

        # stm

        # A reference to the stream. This output is merely a copy of the stm input. Providing this output makes it much easier to establish the execution order of Multiwii blocks in the diagram because Simulink generally executes daisy-chained blocks in sequence.

        # acc

        # A 3-vector value containing the raw accelerometer values in the x, y and z axes respectively. The units depend on the device.

        # gyr

        # A 3-vector value containing the raw gyroscope values in the x, y and z axes respectively. The units depend on the device.

        # mag

        # A 3-vector value containing the raw magnetometer values in the x, y and z axes respectively. The units depend on the device.

        # err

        # An int32 value indicating whether the data was read successfully. This value will be positive if data was read successfully. It will be zero if data could not be read immediately. If an error occurs then this value is a negative error code. See Error Codes for the different error codes and their values. Use the Compare to Error block rather than the error code itself to check for specific error codes. To check for errors in general use the Compare to Zero block to check whether the err output is less than zero.
      self.rawIMU = {'ax':0,'ay':0,'az':0,'gx':0,'gy':0,'gz':0,'mx':0,'my':0,'mz':0,'elapsed':0,'timestamp':0}

        ## GPS
        # Output Ports

        # stm

        # A reference to the stream. This output is merely a copy of the stm input. Providing this output makes it much easier to establish the execution order of Multiwii blocks in the diagram because Simulink generally executes daisy-chained blocks in sequence.

        # fix

        # A boolean value indicating whether a GPS fix has been obtained.

        # sat

        # A uint8 integer containing the number of satellites upon which the GPS measurements were made.

        # coord

        # A 2-vector containing the latitude and longitude coordinates respectively in radians.

        # alt

        # A scalar representing the altitude in metres.

        # speed

        # A scalar representing the speed in metres per second.

        # course

        # A scalar representing the ground course in radians.

        # err

        # An int32 value indicating whether the data was read successfully. This value will be positive if data was read successfully. It will be zero if data could not be read immediately. If an error occurs then this value is a negative error code. See Error Codes for the different error codes and their values. Use the Compare to Error block rather than the error code itself to check for specific error codes. To check for errors in general use the Compare to Zero block to check whether the err output is less than zero.
      self.rawGPS = {'fix':False,'sat':0,'coord_lat':0,'coord_lng':0,'alt':0,'speed':0,'course':0,'elapsed':0,'timestamp':0}

      
      self.motor = {'m1':0,'m2':0,'m3':0,'m4':0,'m5':0,'m6':0,'m7':0,'m8':0,'elapsed':0,'timestamp':0}
      self.attitude = {'angx':0,'angy':0,'heading':0,'elapsed':0,'timestamp':0}
      self.altitude = {'estalt':0,'vario':0,'elapsed':0,'timestamp':0}
      self.message = {'angx':0,'angy':0,'heading':0,'roll':0,'pitch':0,'yaw':0,'throttle':0,'elapsed':0,'timestamp':0}
      self.temp = ()
      self.temp2 = ()
      self.elapsed = 0
      self.PRINT = 1


      baud_rate = 115200
      self.ser = None # serial.Serial(self._serial_port, baudrate=baud_rate , timeout=None)
      """Time to wait until the board becomes operational"""
      wakeup = 2
      try:
          self.ser = serial.Serial(self._serial_port, baudrate=baud_rate , timeout=None)
          if self.PRINT:
              print("Waking up board on "+self._serial_port+"...")
          for i in range(1,wakeup):
              if self.PRINT:
                  print(wakeup-i)
                  time.sleep(1)
              else:
                  time.sleep(1)
      except Exception as error:
          print("\n\nError opening "+self._serial_port+" port.\n"+str(error)+"\n\n")
            
    """Function for sending a command to the board"""
    def sendCMD(self, data_length, code, data):
        checksum = 0
        total_data = [b'$', b'M', b'<', data_length, code] + data
        for i in struct.pack('<2B%dH' % len(data), *total_data[3:len(total_data)]):
            checksum = checksum ^ i #ord(i)
        total_data.append(checksum)
        b = None
        b = self.ser.write(struct.pack('<3c2B%dHB' % len(data), *total_data))
        return b

    def sendCMDreceiveATT(self, data_length, code, data):
        checksum = 0
        total_data = ['$', 'M', '<', data_length, code] + data
        for i in struct.pack('<2B%dH' % len(data), *total_data[3:len(total_data)]):
            checksum = checksum ^ ord(i)
        total_data.append(checksum)
        try:
            start = time.time()
            # b = None
            self.ser.write(struct.pack('<3c2B%dHB' % len(data), *total_data))
            while True:
                header = self.ser.read()
                if header == '$':
                    header = header+self.ser.read(2)
                    break
            datalength = struct.unpack('<b', self.ser.read())[0]
            code = struct.unpack('<b', self.ser.read())
            data = self.ser.read(datalength)
            temp = struct.unpack('<'+'h'*(datalength/2),data)
            self.ser.flushInput()
            self.ser.flushOutput()
            elapsed = time.time() - start
            self.attitude['angx']=float(temp[0]/10.0)
            self.attitude['angy']=float(temp[1]/10.0)
            self.attitude['heading']=float(temp[2])
            self.attitude['elapsed']=round(elapsed,3)
            self.attitude['timestamp']="%0.2f" % (time.time(),) 
            return self.attitude
        except Exception as error:
          if self.PRINT:
            print("\n\nError in sendCMDreceiveATT.")
            print ("("+str(error)+")\n\n")
          pass

    """Function to arm / disarm """
    """
    Modification required on Multiwii firmware to Protocol.cpp in evaluateCommand:
    case MSP_SET_RAW_RC:
      s_struct_w((uint8_t*)&rcSerial,16);
      rcSerialCount = 50; // 1s transition 
      s_struct((uint8_t*)&att,6);
      break;
    """
    def arm(self, MIN_THROTTLE = 1000):
        timer = 0
        start = time.time()
        while timer < 2.0:
            self.setRawRC(1500, 1500, 2000, MIN_THROTTLE)
            time.sleep(0.05)
            timer = timer + (time.time() - start)
            start =  time.time()

    def disarm(self, MIN_THROTTLE = 1000):
        timer = 0
        start = time.time()
        while timer < 1.0:
            self.setRawRC(1500, 1500, 1000, MIN_THROTTLE)
            time.sleep(0.05)
            timer = timer + (time.time() - start)
            start =  time.time()
    
    def autoLevelAtPercentThrottle(self, percentOutOf100 = 50):
        timer = 0
        start = time.time()
        while timer < 0.5:
            self.setRawRC(1500, 1500, 1500, self.convertThrottlePercentToRaw(percentOutOf100))
            time.sleep(0.05)
            timer = timer + (time.time() - start)
            start =  time.time()

    def setPID(self,pd):
        nd=[]
        for i in np.arange(1,len(pd),2):
            nd.append(pd[i]+pd[i+1]*256)
        data = pd
        print("PID sending:",data)
        self.sendCMD(30,MultiWii.SET_PID,data)
        self.sendCMD(0,self.EEPROM_WRITE,[])

    """Function to receive a data packet from the board"""
    def getData(self, cmd):
        try:
            start = time.time()
            self.sendCMD(0,cmd,[])
            while True:
                header = self.ser.read()
                if header == b'$':
                    header = header+self.ser.read(2)
                    break
            print("Got the header", header)
            datalength = struct.unpack('<b', self.ser.read())[0]
            struct.unpack('<b', self.ser.read())
            data = self.ser.read(datalength)
            length = int(datalength/2)
            fmt = '<' + ('h' * (int(length/len('h'))+1))[:length]
            temp = struct.unpack(fmt,data)
            self.ser.flushInput()
            self.ser.flushOutput()
            elapsed = time.time() - start
            if cmd == MultiWii.ATTITUDE:
                self.attitude['angx']=float(temp[0]/10.0)
                self.attitude['angy']=float(temp[1]/10.0)
                self.attitude['heading']=float(temp[2])
                self.attitude['elapsed']=round(elapsed,3)
                self.attitude['timestamp']="%0.2f" % (time.time(),) 
                return self.attitude
            elif cmd == MultiWii.ALTITUDE:
                self.altitude['estalt']=float(temp[0])
                self.altitude['vario']=float(temp[1])
                self.altitude['elapsed']=round(elapsed,3)
                self.altitude['timestamp']="%0.2f" % (time.time(),) 
                return self.altitude
            elif cmd == MultiWii.RC:
                self.rcChannels['roll']=temp[0]
                self.rcChannels['pitch']=temp[1]
                self.rcChannels['yaw']=temp[2]
                self.rcChannels['throttle']=temp[3]
                self.rcChannels['elapsed']=round(elapsed,3)
                self.rcChannels['timestamp']="%0.2f" % (time.time(),)
                return self.rcChannels
            elif cmd == MultiWii.RAW_IMU:
                self.rawIMU['ax']=float(temp[0])
                self.rawIMU['ay']=float(temp[1])
                self.rawIMU['az']=float(temp[2])
                self.rawIMU['gx']=float(temp[3])
                self.rawIMU['gy']=float(temp[4])
                self.rawIMU['gz']=float(temp[5])
                self.rawIMU['mx']=float(temp[6])
                self.rawIMU['my']=float(temp[7])
                self.rawIMU['mz']=float(temp[8])
                self.rawIMU['elapsed']=round(elapsed,3)
                self.rawIMU['timestamp']="%0.2f" % (time.time(),)
                return self.rawIMU
            elif cmd == MultiWii.MOTOR:
                self.motor['m1']=float(temp[0])
                self.motor['m2']=float(temp[1])
                self.motor['m3']=float(temp[2])
                self.motor['m4']=float(temp[3])
                self.motor['m5']=float(temp[4])
                self.motor['m6']=float(temp[5])
                self.motor['m7']=float(temp[6])
                self.motor['m8']=float(temp[7])
                self.motor['elapsed']="%0.3f" % (elapsed,)
                self.motor['timestamp']="%0.2f" % (time.time(),)
                return self.motor
            elif cmd == MultiWii.PID:
                dataPID=[]
                if len(temp)>1:
                    for t in temp:
                        dataPID.append(t%256)
                        dataPID.append(t/256)
                    for p in [0,3,6,9]:
                        dataPID[p]=dataPID[p]/10.0
                        dataPID[p+1]=dataPID[p+1]/1000.0
                    self.PIDcoef['rp']= dataPID=[0]
                    self.PIDcoef['ri']= dataPID=[1]
                    self.PIDcoef['rd']= dataPID=[2]
                    self.PIDcoef['pp']= dataPID=[3]
                    self.PIDcoef['pi']= dataPID=[4]
                    self.PIDcoef['pd']= dataPID=[5]
                    self.PIDcoef['yp']= dataPID=[6]
                    self.PIDcoef['yi']= dataPID=[7]
                    self.PIDcoef['yd']= dataPID=[8]
                return self.PIDcoef
            elif cmd == MultiWii.RAW_GPS:
                print(temp)
                self.rawGPS['fix']=bool(temp[0])
                self.rawGPS['sat']=int(temp[1])
                self.rawGPS['lat']=float(temp[2])
                self.rawGPS['lng']=float(temp[3])
                self.rawGPS['alt']=float(temp[4])
                self.rawGPS['speed']=float(temp[5])
                self.rawGPS['course']=float(temp[5])
                self.rawGPS['elapsed']=round(elapsed,3)
                self.rawGPS['timestamp']="%0.2f" % (time.time(),)
                return self.rawGPS
            else:
                return "No return error!"
        except Exception as error:
          if self.PRINT:
            print(error)
          pass

    """Function to receive a data packet from the board. Note: easier to use on threads"""
    def getDataInf(self, cmd):
        while True:
            try:
                start = time.clock()
                self.sendCMD(0,cmd,[])
                while True:
                    header = self.ser.read()
                    if header == '$':
                        header = header+self.ser.read(2)
                        break
                datalength = struct.unpack('<b', self.ser.read())[0]
                # code = struct.unpack('<b', self.ser.read())
                struct.unpack('<b', self.ser.read())
                data = self.ser.read(datalength)
                temp = struct.unpack('<'+'h'*(datalength/2),data)
                elapsed = time.clock() - start
                self.ser.flushInput()
                self.ser.flushOutput()
                if cmd == MultiWii.ATTITUDE:
                    self.attitude['angx']=float(temp[0]/10.0)
                    self.attitude['angy']=float(temp[1]/10.0)
                    self.attitude['heading']=float(temp[2])
                    self.attitude['elapsed']="%0.3f" % (elapsed,)
                    self.attitude['timestamp']="%0.2f" % (time.time(),)
                elif cmd == MultiWii.RC:
                    self.rcChannels['roll']=temp[0]
                    self.rcChannels['pitch']=temp[1]
                    self.rcChannels['yaw']=temp[2]
                    self.rcChannels['throttle']=temp[3]
                    self.rcChannels['elapsed']="%0.3f" % (elapsed,)
                    self.rcChannels['timestamp']="%0.2f" % (time.time(),)
                elif cmd == MultiWii.RAW_IMU:
                    self.rawIMU['ax']=float(temp[0])
                    self.rawIMU['ay']=float(temp[1])
                    self.rawIMU['az']=float(temp[2])
                    self.rawIMU['gx']=float(temp[3])
                    self.rawIMU['gy']=float(temp[4])
                    self.rawIMU['gz']=float(temp[5])
                    self.rawIMU['elapsed']="%0.3f" % (elapsed,)
                    self.rawIMU['timestamp']="%0.2f" % (time.time(),)
                elif cmd == MultiWii.RAW_GPS:
                    print(temp)
                    self.rawGPS['fix']=bool(temp[0])
                    self.rawGPS['sat']=int(temp[1])
                    self.rawGPS['lat']=float(temp[2])
                    self.rawGPS['lng']=float(temp[3])
                    self.rawGPS['alt']=float(temp[4])
                    self.rawGPS['speed']=float(temp[5])
                    self.rawGPS['course']=float(temp[5])
                    self.rawGPS['elapsed']=round(elapsed,3)
                    self.rawGPS['timestamp']="%0.2f" % (time.time(),)
                elif cmd == MultiWii.MOTOR:
                    self.motor['m1']=float(temp[0])
                    self.motor['m2']=float(temp[1])
                    self.motor['m3']=float(temp[2])
                    self.motor['m4']=float(temp[3])
                    self.motor['m5']=float(temp[4])
                    self.motor['m6']=float(temp[5])
                    self.motor['m7']=float(temp[6])
                    self.motor['m8']=float(temp[7])
                    self.motor['elapsed']="%0.3f" % (elapsed,)
                    self.motor['timestamp']="%0.2f" % (time.time(),)
            except Exception as error:
              if self.PRINT:
                print(error)
              pass

    """Function to ask for 2 fixed cmds, attitude and rc channels, and receive them. Note: is a bit slower than others"""
    def getData2cmd(self, cmd):
        try:
            start = time.time()
            self.sendCMD(0,self.ATTITUDE,[])
            while True:
                header = self.ser.read()
                if header == '$':
                    header = header+self.ser.read(2)
                    break
            datalength = struct.unpack('<b', self.ser.read())[0]
            # code = struct.unpack('<b', self.ser.read())
            struct.unpack('<b', self.ser.read())
            data = self.ser.read(datalength)
            temp = struct.unpack('<'+'h'*(datalength/2),data)
            self.ser.flushInput()
            self.ser.flushOutput()

            self.sendCMD(0,self.RC,[])
            while True:
                header = self.ser.read()
                if header == '$':
                    header = header+self.ser.read(2)
                    break
            datalength = struct.unpack('<b', self.ser.read())[0]
            # code = struct.unpack('<b', self.ser.read())
            struct.unpack('<b', self.ser.read())
            data = self.ser.read(datalength)
            temp2 = struct.unpack('<'+'h'*(datalength/2),data)
            elapsed = time.time() - start
            self.ser.flushInput()
            self.ser.flushOutput()

            if cmd == MultiWii.ATTITUDE:
                self.message['angx']=float(temp[0]/10.0)
                self.message['angy']=float(temp[1]/10.0)
                self.message['heading']=float(temp[2])
                self.message['roll']=temp2[0]
                self.message['pitch']=temp2[1]
                self.message['yaw']=temp2[2]
                self.message['throttle']=temp2[3]
                self.message['elapsed']=round(elapsed,3)
                self.message['timestamp']="%0.2f" % (time.time(),) 
                return self.message
            else:
                return "No return error!"
        except Exception as error:
            print(error)