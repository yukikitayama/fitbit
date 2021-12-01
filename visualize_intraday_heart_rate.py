import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import json
import pprint
pd.set_option('display.max_columns', None)
pd.set_option('expand_frame_repr', False)


DATE = '2021-11-27'
DATA = f'data/heart_rate_intraday_{DATE}.json'
IMAGE = f'image/heart_rate_intraday_{DATE}.png'


def main():

    # Read data
    with open(DATA, 'r') as f:
        data = json.load(f)
    print(f'type: {type(data)}')
    # pprint.pprint(data)
    print()

    # Extract data
    df = pd.DataFrame(data['activities-heart-intraday']['dataset'])
    df['index'] = pd.to_datetime(df['time'])
    df = df.set_index('index')
    print(df.shape)
    print(df.dtypes)
    print(df.head())
    print(df.tail())
    print()

    # Visualize
    plt.plot(df['value'])
    plt.title(f'Intraday heart rate on {DATE}')
    plt.xlabel('MT')
    plt.ylabel('Beats per minute (BPM)')
    plt.xticks(rotation=45)
    plt.grid()
    plt.tight_layout()
    plt.savefig(IMAGE)
    plt.close()


if __name__ == '__main__':
    main()
