import pandas as pd
import matplotlib.pyplot as plt
import json
import pprint
pd.set_option('display.max_columns', None)
pd.set_option('expand_frame_repr', False)


DATE = '2021-12-04'
DATA = f'data/activity_time_series_calories_{DATE}.json'
SAVEFIG = f'image/calories_time_series_{DATE}.png'


def main():

    # Read data
    with open(DATA, 'r') as f:
        data = json.load(f)
    pprint.pprint(data)

    # Extract data
    df = pd.DataFrame(data['activities-calories-intraday']['dataset'])
    df['index'] = pd.to_datetime(df['time'])
    df = df.set_index('index')
    total_calories = df['value'].sum()
    print(f'Total calories burned on {DATE}: {total_calories}')
    print(df.shape)
    print(df.dtypes)
    print(df.head())
    print(df.tail())
    print()

    # Visualize data
    plt.plot(df['value'])
    plt.title(f'Intraday calories burned on {DATE} (Total calories burned: {total_calories:.0f})')
    plt.xlabel('MT')
    plt.ylabel('Calories')
    plt.xticks(rotation=45)
    plt.grid()
    plt.tight_layout()
    plt.savefig(SAVEFIG)
    plt.close()


if __name__ == '__main__':
    main()
