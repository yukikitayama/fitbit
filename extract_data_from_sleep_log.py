import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import json
import pprint
pd.set_option('display.max_columns', None)
pd.set_option('expand_frame_repr', False)


DATE = '2021-11-28'
DATA = f'data/sleep_log_{DATE}.json'
IMAGE = f'image/sleep_level_time_series_{DATE}.png'


def main():

    # Read data
    with open(DATA, 'r') as outfile:
        data = json.load(outfile)
    print(f'type: {type(data)}')
    pprint.pprint(data)
    print()

    # Extract simple data
    sleep = data['sleep'][0]
    summary = data['summary']
    total_minutes = summary['totalMinutesAsleep']
    hour, minute = divmod(total_minutes, 60)
    stages = summary['stages']
    # Type str
    start_time = sleep['startTime']
    end_time = sleep['endTime']

    print(f'Sleep duration: {hour} hours and {minute} minutes on {DATE}')
    print(f'Sleep detail: Awake: {stages["wake"]} min, REM: {stages["rem"]} min, '
          f'Light: {stages["light"]} min, Deep: {stages["deep"]} min')
    print(f'Sleep started at {start_time} and ended at {end_time}')

    # Make time series dataframe
    df_level = pd.DataFrame(sleep['levels']['data'])
    df_level['index'] = pd.to_datetime(df_level['dateTime'])
    df_level = df_level.set_index('index')

    index = pd.date_range(min(df_level.index), max(df_level.index), freq='30S')
    df = pd.DataFrame(data=np.repeat(None, len(index)), index=index, columns=['tmp'])
    df['level'] = df_level['level']
    df['level'] = df['level'].fillna(method='ffill')

    levels = ['deep', 'light', 'rem', 'wake']
    for i, level in enumerate(levels):
        df.loc[df['level'] == level, 'level_integer'] = i
    df['level_integer'] = df['level_integer'].astype(int)

    df = df.drop(columns=['tmp'])
    print(df.shape)
    print(df.dtypes)
    print(df.head())
    print(df.tail())

    # Visualize data
    plt.plot(df['level_integer'])
    plt.title(f'Sleep level time series on {DATE}')
    plt.xlabel('MT')
    plt.ylabel('Level')
    plt.xticks(rotation=45)
    plt.yticks(range(len(levels)), levels)
    plt.grid()
    plt.tight_layout()
    plt.savefig(IMAGE)
    plt.close()


if __name__ == '__main__':
    main()
