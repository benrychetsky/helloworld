import os
import irsdk
import time
from datetime import datetime
from iRacingTelemetry import iRacing
import pandas as pd

n = 1

def dateCapture():
    rawDate = datetime.now()
    cleanDate = f"{rawDate.month}_{rawDate.day}_{rawDate.year}"
    return cleanDate

def ingestTelemetry(state):
    global n
    date = dateCapture()
    columns = list(state.iRacingVarDict().keys())
    telemetry_df = pd.DataFrame(columns=columns)
    if state.iRacingConnected:
        print("Capturing Telemetry Data... ")
    else:
        print("Error capturing telemetry.")

    while state.iRacingConnected:
        try:
            date = dateCapture()
            state.iRacingVars()
            data = state.iRacingVarDict()
            telemetry_df = telemetry_df._append(data, ignore_index=True)
            time.sleep(1/4)

        except KeyboardInterrupt:
            filename = f"telemetry_data_{date}_{n}.csv"
            if not os.path.exists(filename):
                telemetry_df.to_csv(filename, index=False)
                print(f"Telemetry file: {filename} has been created and stored.")
                break
            else:
                n+=1
            

if __name__ == '__main__':
    irsdk = irsdk.IRSDK()
    irsdk.startup()
    state = iRacing(irsdk)
    state.checkiRacing()
    ingestTelemetry(state)

