import irsdk
from datetime import timedelta
import time
import math

###REMOVE ROUNDING BECAUSE MORE DECIMAL PLACES ALLOWS MORE PRECISION
###TEST CASES SOON

class iRacing:

    def __init__(self, irsdk):
        
        #Class vars
        self.irsdk = irsdk
        self.iRacingConnected = False
        self.LastCarSetupTick = -1

        #Driver vars
        self.Throttle = 0
        self.Brake = 0
        self.Clutch = 0
        self.Speed = 0
        self.currentGear = 0
        self.rpm = 0
        self.SteeringWheelAngle = 0
        self.FuelLevelPct = 0

        #Tire vars

        # self.RFtempL = 0
        # self.RFtempM = 0
        # self.RFtempR = 0

        # self.LFtempL = 0
        # self.LFtempM = 0
        # self.LFtempR = 0

        # self.RFtempL = 0
        # self.RFtempM = 0
        # self.RFtempR = 0

        # self.RRtempL = 0
        # self.RRtempM = 0
        # self.RRtempR = 0


        self.LFtempCL = 0
        self.LFtempCR = 0
        self.LFtempCM = 0

        self.LRtempCL = 0
        self.LRtempCR = 0
        self.LRtempCM = 0

        self.RFtempCL = 0
        self.RFtempCR = 0
        self.RFtempCM = 0

        self.RRtempCL = 0
        self.RRtempCR = 0
        self.RRtempCM = 0

        self.LFwearL = 0
        self.LFwearM = 0
        self.LFwearR = 0

        self.LRwearL = 0
        self.LRwearM = 0
        self.LRwearR = 0

        self.RFwearL = 0
        self.RFwearM = 0
        self.RFwearR = 0

        self.RRwearL = 0
        self.RRwearM = 0
        self.RRwearR = 0

        self.TrackTemp = 0

        #Engine Vars
        self.OilTemp = 0
        self.WaterTemp = 0

        #Suspension vars
        self.RFshockDefl = 0
        self.RFshockVel = 0
        self.RFrideHeight = 0

        self.LFshockDefl = 0
        self.LFshockVel = 0
        self.LFrideHeight = 0

        self.RRshockDefl = 0
        self.RRshockVel = 0
        self.RRrideHeight = 0

        self.LRshockDefl = 0
        self.LRshockVel = 0

        self.RFrideHeight = 0
        self.RRrideHeight = 0

        self.LFrideHeight = 0
        self.LRrideHeight = 0

        self.RRspeed = 0
        self.RFspeed = 0

        self.LRspeed = 0
        self.LFspeed = 0

        #Aerodynamics vars
        self.AirDensity = 0
        self.AirPressure = 0
        self.AirTemp = 0
        self.WindDir = 0
        self.WindVel = 0


        #Vehicle dynamics vars
        self.CFrideHeight = 0
        self.CRrideHeight = 0
        self.LatAccel = 0
        self.LongAccel = 0
        self.VertAccel = 0
        self.Roll = 0
        self.RollRate = 0
        self.Yaw = 0
        self.YawRate = 0
        self.Pitch = 0
        self.PitchRate = 0
        self.gForces = 0

        #Session vars
        self.SessionFlags = None
        self.RaceFlag = None
        self.SessionFlag = None
        self.MyInfo = None
        self.WeekendInfo = None
        self.DriverInfo = None
        self.TrackName = None
        self.TrackType = None
        self.CarName = None
        self.RacePosition = 0
        self.Lap = 0
        self.PaceMode = None
        self.OnPitRoad = None
        self.LapPrct = 0
        self.LapDist = 0
        self.SessionTime = 0
        self.IsOnTrack = None
        self.LapBestLap = 0
        self.CurrentLapTime = 0
        self.LapCompleted = 0
        self.LapLastLapTime = 0
        self.LapBestLapTime = 0
        self.LapDeltaToBestLap = 0
        self.LapDeltaToBestLap_DD = 0

    def checkiRacing(self):
        if self.iRacingConnected and not (self.irsdk.is_initialized and self.irsdk.is_connected):
            self.iRacingConnected  = False
            self.LastCarSetupTick = -1
            self.irsdk.shutdown()
            return "iRacing not active"

        elif not self.iRacingConnected  and self.irsdk.startup() and self.irsdk.is_initialized and self.irsdk.is_connected:
            self.iRacingConnected = True
            return "iRacing active"

    def clutch_val(self, raw_clutch):
        clean_clutch = 1 - raw_clutch
        real_clutch = math.floor(clean_clutch * 100)
        return max(0, real_clutch)


    def gearDisplay(self, gear):
        if gear == 0:
            return "N"
        elif gear == -1:
            return "R"
        return gear

    def calcGForces(self, LatAccel, LongAccel, VertAccel):
        TotalAccel = math.sqrt(LatAccel ** 2 + LongAccel ** 2 + VertAccel ** 2)
        gForces = TotalAccel / 9.8
        return gForces

    def gForceConvert(self, accel):
        g_force = accel  * (1 / 9.81)
        return g_force

    def timeUpdater(self, seconds):
        minutes, seconds = divmod(seconds, 60)
        milliseconds = int((seconds - int(seconds)) * 1000)
        formatted_time = f"{int(minutes):02}:{int(seconds):02}.{milliseconds:06}"
        return formatted_time

    def celcius2farenheit(self, celcius):
        if celcius is None:
            return 0
        else:
            farenheit = math.floor((celcius * 9 / 5) + 32)
            return farenheit

    def val2Prct(self, val):
        if val == None:
            return "Null"
        else:
            real_val = math.floor(val * 100)
            return max(0, real_val)

    # def rad2degrees(self, steering_angle):
    #     steering_degrees = math.floor((steering_angle * 180) / math.pi)
    #     return steering_degrees\

    def rad2degrees(self, steering_angle):
        steering_degrees = math.degrees(steering_angle)
        return math.floor(-steering_degrees)

        
        # if steering_degrees <= 180:
        #     return math.floor(steering_degrees)

        # else:
        #     steering_var = steering_degrees - 360
        #     return math.floor(steering_var)
            

    def mps2mph(self, mps):
        if mps == None:
            return "Null"
        else:
            mph = round(mps * 2.23694, 2)
            return mph

    def meters2feet(self, meters):
        feet = meters * 3.28084
        return feet


    def densityConvert(self, kgm3):
        lbsPerCubicFt = round(kgm3 * 0.06242796, 2)
        return lbsPerCubicFt
    
    def pressureConvert(self, Pa):
        bar = round((Pa / 10**5), 2)
        return bar
    
    def radsPerSec2degPerSec(self, rads):
        degs = math.floor((rads / (2 * math.pi)) * 360)
        return degs

    def meters2milli(self, meters):
        if meters == None:
            return "Null"
        else:
            milli = meters * 1000
            return milli
    
    def paceMode(self, PaceMode):
        pacemode_dict = {
            0: "Single File Start",
            1: "Double File Start",
            2: "Single File Restart",
            3: "Double File Restart",
            4: "Not Pacing"
        }

        if PaceMode in pacemode_dict:
            return pacemode_dict[PaceMode]
    
    def absValSolver(self, value):
        return max(0, value)

    def flagDecrypt(self, RaceFlag):
        flags_mapping = {
            'irsdk_checkered': "Checkered Flag",
            'irsdk_white': "White Flag",
            'irsdk_green': "Green Flag",
            'irsdk_yellow': "Yellow Flag",
            'irsdk_red': "Red Flag",
            'irsdk_blue': "Blue Flag",
            'irsdk_caution': "Caution",
            'irsdk_black': "Black Flag",
            'irsdk_disqualify': "Disqualified",
            'irsdk_repair': "Repair Needed",
        }

        for flag in RaceFlag:
            if flag in flags_mapping:
                return flags_mapping[flag]
            else:
                return "Practice"




    def iRacingVars(self):
        #Function contains all variables coming from iRacing session while active

        flags_mapping = {
            'irsdk_checkered': 0x00000001,
            'irsdk_white': 0x00000002,
            'irsdk_green': 0x00000004,
            'irsdk_yellow': 0x00000008,
            'irsdk_red': 0x00000010,
            'irsdk_blue': 0x00000020,
            'irsdk_debris': 0x00000040,
            'irsdk_crossed': 0x00000080,
            'irsdk_yellowWaving': 0x00000100,
            'irsdk_oneLapToGreen': 0x00000200,
            'irsdk_greenHeld': 0x00000400,
            'irsdk_tenToGo': 0x00000800,
            'irsdk_fiveToGo': 0x00001000,
            'irsdk_randomWaving': 0x00002000,
            'irsdk_caution': 0x00004000,
            'irsdk_cautionWaving': 0x00008000,
            'irsdk_black': 0x00010000,
            'irsdk_disqualify': 0x00020000,
            'irsdk_servicible': 0x00040000,
            'irsdk_furled': 0x00080000,
            'irsdk_repair': 0x00100000,
            'irsdk_startHidden': 0x10000000,
            'irsdk_startReady': 0x20000000,
            'irsdk_startSet': 0x40000000,
        }

        #Driver vars 
        self.Speed = self.mps2mph(self.irsdk['Speed'])
        self.Brake = self.val2Prct(self.irsdk['Brake'])
        self.Throttle = self.val2Prct(self.irsdk['Throttle'])
        self.Clutch = self.clutch_val(self.irsdk['Clutch'])
        self.rpm = math.floor(self.irsdk['RPM'])
        self.currentGear = self.gearDisplay(self.irsdk['Gear'])
        self.SteeringWheelAngle = self.rad2degrees(self.irsdk['SteeringWheelAngle'])
        self.FuelLevelPct = self.val2Prct(self.irsdk['FuelLevelPct'])

        #Tire vars
        self.LFtempCL = self.celcius2farenheit(self.irsdk['LFtempCL'])
        self.LFtempCR = self.celcius2farenheit(self.irsdk['LFtempCR'])
        self.LFtempCM = self.celcius2farenheit(self.irsdk['LFtempCM'])

        self.LRtempCL = self.celcius2farenheit(self.irsdk['LRtempCL'])
        self.LRtempCR = self.celcius2farenheit(self.irsdk['LRtempCR'])
        self.LRtempCM = self.celcius2farenheit(self.irsdk['LRtempCM'])

        self.RFtempCL = self.celcius2farenheit(self.irsdk['RFtempCL'])
        self.RFtempCR = self.celcius2farenheit(self.irsdk['RFtempCR'])
        self.RFtempCM = self.celcius2farenheit(self.irsdk['RFtempCM'])

        self.RRtempCL = self.celcius2farenheit(self.irsdk['RRtempCL'])
        self.RRtempCR = self.celcius2farenheit(self.irsdk['RRtempCR'])
        self.RRtempCM = self.celcius2farenheit(self.irsdk['RRtempCM'])

        # self.RFtempL = self.celcius2farenheit(self.irsdk(['RFtempL']))
        # self.RFtempM = self.celcius2farenheit(self.irsdk(['RFtempM']))
        # self.RFtempR = self.celcius2farenheit(self.irsdk(['RFtempR']))
        # self.LFtempL = self.celcius2farenheit(self.irsdk(['LFtempL']))
        # self.LFtempM = self.celcius2farenheit(self.irsdk(['LFtempM']))
        # self.LFtempR = self.celcius2farenheit(self.irsdk(['LFtempR']))
        # self.RFtempL = self.celcius2farenheit(self.irsdk(['RFtempL']))
        # self.RFtempM = self.celcius2farenheit(self.irsdk(['RFtempM']))
        # self.RFtempR = self.celcius2farenheit(self.irsdk(['RFtempR']))
        # self.RRtempL = self.celcius2farenheit(self.irsdk(['RRtempL']))
        # self.RRtempM = self.celcius2farenheit(self.irsdk(['RRtempM']))
        # self.RRtempR = self.celcius2farenheit(self.irsdk(['RRtempR']))

        self.LFwearL = self.val2Prct(self.irsdk['LFwearL'])
        self.LFwearM = self.val2Prct(self.irsdk['LFwearM'])
        self.LFwearR = self.val2Prct(self.irsdk['LFwearR'])

        self.LRwearL = self.val2Prct(self.irsdk['LRwearL'])
        self.LRwearM = self.val2Prct(self.irsdk['LRwearM'])
        self.LRwearR = self.val2Prct(self.irsdk['LRwearR'])

        self.RFwearL = self.val2Prct(self.irsdk['RFwearL'])
        self.RFwearM = self.val2Prct(self.irsdk['RFwearM'])
        self.RFwearR = self.val2Prct(self.irsdk['RFwearR'])

        self.RRwearL = self.val2Prct(self.irsdk['RRwearL'])
        self.RRwearM = self.val2Prct(self.irsdk['RRwearM'])
        self.RRwearR = self.val2Prct(self.irsdk['RRwearR'])

        self.TrackTemp = self.celcius2farenheit(self.irsdk['TrackTemp'])

        # #Suspension vars                                                                  Removing due to illegitimate data ingested
        self.RFshockDefl = self.meters2milli(self.irsdk['RFshockDefl'])
        self.RFshockVel = self.mps2mph(self.irsdk['RFshockVel'])

        self.LFshockDefl = self.meters2milli(self.irsdk['LFshockDefl'])
        self.LFshockVel = self.mps2mph(self.irsdk['LFshockVel'])

        self.RRshockDefl = self.meters2milli(self.irsdk['RRshockDefl'])
        self.RRshockVel = self.mps2mph(self.irsdk['RRshockVel'])

        self.LRshockDefl = self.meters2milli(self.irsdk['LRshockDefl'])
        self.LRshockVel = self.mps2mph(self.irsdk['LRshockVel'])
        self.RFrideHeight = self.meters2milli(self.irsdk['RFrideHeight'])
        self.RRrideHeight = self.meters2milli(self.irsdk['RRrideHeight'])
        self.LFrideHeight = self.meters2milli(self.irsdk['LFrideHeight'])
        self.LRrideHeight = self.meters2milli(self.irsdk['LRrideHeight'])
        self.RRspeed = self.mps2mph(self.irsdk['RRspeed'])
        self.RFspeed = self.mps2mph(self.irsdk['RFspeed'])
        self.LRspeed = self.mps2mph(self.irsdk['LRspeed'])
        self.LFspeed = self.mps2mph(self.irsdk['LFspeed'])


        #Engine vars
        self.OilTemp = self.celcius2farenheit(self.irsdk['OilTemp'])
        self.WaterTemp = self.celcius2farenheit(self.irsdk['WaterTemp'])

        #Aerodynamics vars
        self.AirDensity = self.densityConvert(self.irsdk['AirDensity'])
        self.AirPressure = self.pressureConvert(self.irsdk['AirPressure'])
        self.AirTemp = self.celcius2farenheit(self.irsdk['AirTemp'])
        self.WindDir = self.rad2degrees(self.irsdk['WindDir'])
        self.WindVel = self.mps2mph(int(self.irsdk['WindVel']))

        #Vehicle dynamics vars
        self.LatAccel = self.gForceConvert(self.irsdk['LatAccel'])
        self.LongAccel = self.gForceConvert(self.irsdk['LongAccel'])
        self.VertAccel = self.gForceConvert(self.irsdk['VertAccel'])
        self.Roll = self.rad2degrees(self.irsdk['Roll'])
        self.RollRate = self.radsPerSec2degPerSec(self.irsdk['RollRate'])
        self.Yaw = self.rad2degrees(self.irsdk['Yaw'])
        self.YawRate = self.radsPerSec2degPerSec(self.irsdk['YawRate'])
        self.Pitch = self.rad2degrees(self.irsdk['Pitch'])
        self.PitchRate = self.radsPerSec2degPerSec(self.irsdk['PitchRate'])
        self.gForces = self.calcGForces(self.LatAccel, self.LongAccel, self.VertAccel)
        
        #Session vars
        self.SessionFlags = self.irsdk['SessionFlags']
        self.WeekendInfo = dict(self.irsdk['WeekendInfo'])
        self.DriverInfo = dict(self.irsdk['DriverInfo'])
        self.MyInfo = next((driver for driver in self.DriverInfo['Drivers'] if driver['UserName'] == 'Ben Rychetsky'), None)
        self.RaceFlag = [flag for flag, value in flags_mapping.items() if self.SessionFlags & value == value]
        self.SessionFlag = self.flagDecrypt(self.RaceFlag),
        #sessionflag var that decrypts the raceflag var and returns the valuable session flag/'s
        self.TrackName = self.WeekendInfo.get('TrackDisplayName')
        self.TrackType = self.WeekendInfo.get('TrackConfigName')
        self.RacePosition = self.irsdk['PlayerCarPosition']
        self.CarName = self.MyInfo.get('CarScreenName')
        self.RaceLaps = self.irsdk['RaceLaps']
        self.PaceMode = self.paceMode(self.irsdk['PaceMode'])
        self.OnPitRoad = self.irsdk['OnPitRoad']
        self.LapPrct = self.val2Prct(self.irsdk['LapDistPct'])
        self.SessionTime = self.timeUpdater(self.irsdk['SessionTime'])
        self.IsOnTrack = self.irsdk['IsOnTrack']
        self.Lap = self.irsdk['Lap']
        self.LapLastLapTime = round(self.irsdk['LapLastLapTime'], 3)
        self.LapDist = self.meters2feet(self.irsdk['LapDist'])
        self.LapBestLap = round(self.absValSolver(self.irsdk['LapBestLap']), 3)
        self.LapCompleted = self.absValSolver(self.irsdk['LapCompleted'])
        self.CurrentLapTime = self.timeUpdater(self.irsdk['LapCurrentLapTime'])
        self.LapBestLapTime = round(self.irsdk['LapBestLapTime'], 3)
        self.LapDeltaToBestLap = self.timeUpdater(self.irsdk['LapDeltaToBestLap'])
        self.LapDeltaToBestLap_DD = self.irsdk['LapDeltaToBestLap_DD']

    def iRacingVarDict(self):
        iRacingDict = {
            #Session vars
            "TrackName": self.TrackName,
            "TrackType": self.TrackType,
            "SessionFlag": self.SessionFlag,
            "CarName": self.CarName,
            "RacePosition": self.RacePosition,
            "Lap Nbr": self.Lap,
            "PaceMode": self.PaceMode,
            "OnPitRoad": self.OnPitRoad,
            "LpDistance": self.LapDist,
            "LapDistPrct %": self.LapPrct,
            "SessionTime": self.SessionTime,
            "IsOnTrack": self.IsOnTrack,
            "PreviousLap": self.LapLastLapTime,
            "LapBestLap": self.LapBestLap,
            "LapCompleted": self.LapCompleted,
            "CurrentLapTime": self.CurrentLapTime,
            "LapBestLapTime": self.LapBestLapTime,
            "LapDeltaToBestLap": self.LapDeltaToBestLap,
            "LapDeltaToBestLap_DD": self.LapDeltaToBestLap_DD,

            #Driver vars
            "Throttle %": self.Throttle,
            "Brake %": self.Brake,
            "Clutch %": self.Clutch,
            "Speed (MPH)": self.Speed,
            "currentGear": self.currentGear,
            "RPM": self.rpm,
            "SteeringWheelAngle (deg)": self.SteeringWheelAngle,
            "FuelLevelPct": self.FuelLevelPct,

            #Tire vars
            # "RFtempL": self.RFtempL,
            # "RFtempM": self.RFtempM,
            # "RFtempR": self.RFtempR,

            # "LFtempL": self.LFtempL,
            # "LFtempM": self.LFtempM,
            # "LFtempR": self.LFtempR,

            # "RFtempL": self.RFtempL,
            # "RFtempM": self.RFtempM,
            # "RFtempR": self.RFtempR,

            # "RRtempL": self.RRtempL,
            # "RRtempM": self.RRtempM,
            # "RRtempR": self.RRtempR,


            "LFtempCL (F)": self.LFtempCL,
            "LFtempCR (F)": self.LFtempCR,
            "LFtempCM (F)": self.LFtempCM,

            "LRtempCL (F)": self.LRtempCL,
            "LRtempCR (F)": self.LRtempCR,
            "LRtempCM (F)": self.LRtempCM,

            "RFtempCL (F)": self.RFtempCL,
            "RFtempCR (F)": self.RFtempCR,
            "RFtempCM (F)": self.RFtempCM,

            "RRtempCL (F)": self.RRtempCL,
            "RRtempCR (F)": self.RRtempCR,
            "RRtempCM (F)": self.RRtempCM,

            "LFwearL %": self.LFwearL,
            "LFwearM %": self.LFwearM,
            "LFwearR %": self.LFwearR,

            "LRwearL %": self.LRwearL,
            "LRwearM %": self.LRwearM,
            "LRwearR %": self.LRwearR,

            "RFwearL %": self.RFwearL,
            "RFwearM %": self.RFwearM,
            "RFwearR %": self.RFwearR,

            "RRwearL %": self.RRwearL,
            "RRwearM %": self.RRwearM,
            "RRwearR %": self.RRwearR,
            
            "TrackTemp (F)": self.TrackTemp,

            #Engine Vars
            "OilTemp (F)": self.OilTemp,
            "WaterTemp (F)": self.WaterTemp,

            #Suspension vars
            # "RFshockDefl (m/s)": self.RFshockDefl,
            # "RFshockVel (MPH)": self.RFshockVel,

            # "LFshockDefl (m/s)": self.LFshockDefl,
            # "LFshockVel (MPH)": self.LFshockVel,

            # "RRshockDefl (m/s)": self.RRshockDefl,
            # "RRshockVel (MPH)": self.RRshockVel,

            # "LRshockDefl (m/s)": self.LRshockDefl,
            # "LRshockVel (MPH)": self.LRshockVel,
            # "RF Ride Height (mm)": self.RFrideHeight,
            # "RR Ride Height (mm)": self.RRrideHeight,
            # "LF Ride Height (mm)": self.LFrideHeight,
            # "LR Ride Height (mm)": self.LRrideHeight,
            # "RR Speed (mm)": self.RRspeed,
            # "RF Speed (mm)": self.RFspeed,
            # "LR Speed (mm)": self.LRspeed,
            # "LF Speed (mm)": self.LFspeed,
            # "CF Ride Height (mm)": self.CFRideHeight,
            # "CR Ride Height (mm)": self.CRrideHeight,

            #Aerodynamics vars
            "AirDensity (lbs/ft^3)": self.AirDensity,
            "AirPressure (bar)": self.AirPressure,
            "AirTemp (F)": self.AirTemp,
            "WindDir (deg)": self.WindDir,
            "WindVel (MPH)": self.WindVel,
            

            #Vehicle dynamics vars
            "LatAccel (m/s)": self.LatAccel,
            "LongAccel (m/s)": self.LongAccel,
            "VertAccel (m/s)": self.VertAccel,
            "Roll (deg)": self.Roll,
            "RollRate (deg/s)": self.RollRate,
            "Yaw (deg)": self.Yaw,
            "YawRate (deg/s)": self.YawRate,
            "Pitch (deg)": self.Pitch,
            "PitchRate (deg/s)": self.PitchRate,
            "gForces": self.gForces
        }
        return iRacingDict



