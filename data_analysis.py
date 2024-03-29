import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objs as go
import datetime


schema = {
    "TrackName": str,
    "TrackType": str,
    "SessionFlag": str,
    "CarName": str,
    "RacePosition": int,
    "Lap Nbr": int,
    "PaceMode": str,
    "OnPitRoad": str,
    "LapDistPrct %": int,
    "SessionTime": str,
    "IsOnTrack": str,
    "PreviousLap": str,
    "LapBestLap": str,
    "LapCompleted": str,
    "CurrentLapTime": str,
    "LapBestLapTime": str,
    "LapDeltaToBestLap": str,
    "LapDeltaToBestLap_DD": str,
    "Throttle %": int,
    "Brake %": int,
    "Clutch %": int,
    "Speed (MPH)": int,
    "currentGear": str,
    "RPM": int,
    "SteeringWheelAngle (deg)": int,
    "FuelLevelPct": int,
    "LFtempCL (F)": int,
    "LFtempCR (F)": int,
    "LFtempCM (F)": int,
    "LRtempCL (F)": int,
    "LRtempCR (F)": int,
    "LRtempCM (F)": int,
    "RFtempCL (F)": int,
    "RFtempCR (F)": int,
    "RFtempCM (F)": int,
    "RRtempCL (F)": int,
    "RRtempCR (F)": int,
    "RRtempCM (F)": int,
    "LFwearL %": int,
    "LFwearM %": int,
    "LFwearR %": int,
    "LRwearL %": int,
    "LRwearM %": int,
    "LRwearR %": int,
    "RFwearL %": int,
    "RFwearM %": int,
    "RFwearR %": int,
    "RRwearL %": int,
    "RRwearM %": int,
    "RRwearR %": int,
    "TrackTemp (F)": int,
    "OilTemp (F)": int,
    "WaterTemp (F)": int,
    "AirDensity (lbs/ft^3)": float,
    "AirPressure (bar)": float,
    "AirTemp (F)": int,
    "WindDir (deg)": float,
    "WindVel (MPH)": int,
    "LatAccel (m/s)": float,
    "LongAccel (m/s)": float,
    "VertAccel (m/s)": float,
    "Roll (deg)": float,
    "RollRate (deg/s)": float,
    "Yaw (deg)": float,
    "YawRate (deg/s)": float,
    "Pitch (deg)": float,
    "PitchRate (deg/s)": float,
    "gForces": float
}



df1 = pd.read_csv(r'C:\Users\jedin\projects\helloworld\telemetry_data_3_28_2024_1.csv')




def custom_time_parser(time_str):

    parsed_time = pd.to_datetime(time_str, format='%M:%S.%f')

    return pd.Timestamp("1900-01-01") + (parsed_time - pd.Timestamp("1900-01-01"))

df1['Session_Time'] = df1['SessionTime'].apply(custom_time_parser)
# df1['PrevLap_'] = df1['PreviousLap'].apply(lambda x: '00:' + x)
# df1['PrevLap'] = df1['PrevLap_'].apply(custom_time_parser)


df1['Session_Time'] = df1['Session_Time'].dt.strftime('%M:%S.%f')
# df1['steering_angle'] = df1['SteeringWheelAngle (deg)'].apply(lambda x: -x)
# df1['yaw'] = df1['Yaw (deg)'].apply(lambda x: -x)
# df1['yawRate'] = df1['YawRate (deg/s)'].apply(lambda x: -x)
# df1['pitch'] = df1['Pitch (deg)'].apply(lambda x: -x)
# df1['pitchRate'] = df1['PitchRate (deg/s)'].apply(lambda x: -x)
# df1['roll'] = df1['Roll (deg)'].apply(lambda x: -x)
# df1['rollRate'] = df1['RollRate (deg/s)'].apply(lambda x: -x)

best_lap = df1['LapBestLap'].iloc[-1]
flt_df = df1[df1['Lap Nbr'] == best_lap]
lap_time = flt_df['Session_Time']
y_speed = flt_df['Speed (MPH)']
y_throttle = flt_df['Throttle %']
y_brake = flt_df['Brake %']
y_latAccel = flt_df['LatAccel (m/s)'] * (1 / 9.81)
y_longAccel = flt_df['LongAccel (m/s)'] * (1 / 9.81)
y_vertAccel = flt_df['VertAccel (m/s)'] * (1 / 9.81)
y_gforce = flt_df['gForces']
y_yaw = flt_df['Yaw (deg)']
y_yawRate = flt_df['YawRate (deg/s)']
y_pitch = flt_df['Pitch (deg)']
y_pitchRate = flt_df['PitchRate (deg/s)']
y_roll = flt_df['Roll (deg)']
y_rollRate = flt_df['RollRate (deg/s)']
y_steering = flt_df['SteeringWheelAngle (deg)']
# prevlap = df1['PreviousLap'].unique()
# y_prevlap = prevlap[1:]

df_laps = df1[df1['OnPitRoad'] != True]

df_laps = df_laps[['OnPitRoad', 'LapCompleted', 'PreviousLap']]
df_laps = df_laps[df_laps['LapCompleted'] > 0]
df_laps = df_laps.drop_duplicates(subset='LapCompleted', keep='first')

x_laps = df_laps['LapCompleted']
x_laps = x_laps[1:]
x_laps = x_laps - 1
y_time = df_laps['PreviousLap']
y_time = y_time[1:]




fig_speed = px.line(flt_df, x=lap_time, y=y_speed, title=f'Speed Trace Lap {best_lap}', line_shape='spline')
fig_speed.update_layout(xaxis=dict(tickmode='array', tickvals=[]))

fig_throttle = px.line(flt_df, x=lap_time, y=y_throttle, title=f'Throttle Trace Lap {best_lap}', line_shape='spline')
fig_throttle.update_layout(xaxis=dict(tickmode='array', tickvals=[]))

fig_brake = px.line(flt_df, x=lap_time, y=y_brake, title=f'Brake Trace Lap {best_lap}', line_shape='spline')
fig_brake.update_layout(xaxis=dict(tickmode='array', tickvals=[]))

fig_latAccel = px.line(flt_df, x=lap_time, y=y_latAccel, title=f'LatAccel Trace Lap {best_lap}', line_shape='spline')
fig_latAccel.update_layout(xaxis=dict(tickmode='array', tickvals=[]))

fig_longAccel = px.line(flt_df, x=lap_time, y=y_longAccel, title=f'LongAccel Trace Lap {best_lap}', line_shape='spline')
fig_longAccel.update_layout(xaxis=dict(tickmode='array', tickvals=[]))

fig_vertAccel = px.line(flt_df, x=lap_time, y=y_vertAccel, title=f'VertAccel Trace Lap {best_lap}', line_shape='spline')
fig_vertAccel.update_layout(xaxis=dict(tickmode='array', tickvals=[]))

fig_yaw = px.line(flt_df, x=lap_time, y=y_yawRate, title=f'Yaw Trace Lap {best_lap}', line_shape='spline')
fig_yaw.update_layout(xaxis=dict(tickmode='array', tickvals=[]))

fig_pitch = px.line(flt_df, x=lap_time, y=y_pitchRate, title=f'Pitch Trace Lap {best_lap}', line_shape='spline')
fig_pitch.update_layout(xaxis=dict(tickmode='array', tickvals=[]))

fig_roll = px.line(flt_df, x=lap_time, y=y_rollRate, title=f'Roll Trace Lap {best_lap}', line_shape='spline')
fig_roll.update_layout(xaxis=dict(tickmode='array', tickvals=[]))

fig_gForces = px.line(flt_df, x=lap_time, y=y_gforce, title=f'gForces Trace Lap {best_lap}', line_shape='spline')
fig_gForces.update_layout(xaxis=dict(tickmode='array', tickvals=[]))

fig_steering = px.line(flt_df, x=lap_time, y=y_steering, title=f'Steering Trace Lap {best_lap}', line_shape='spline')
fig_steering.update_layout(xaxis=dict(tickmode='array', tickvals=[]))

fig_laps = px.line(flt_df, x=x_laps, y=y_time, title='Laps', markers=True)






            