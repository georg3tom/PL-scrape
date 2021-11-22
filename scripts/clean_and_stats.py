"""
This script reads the CSV scraped from the Premier League webiste and the 
JSON from the Wikipedia scrape, cleans them and writes them both to separate
JSON files, ready to be merged. While cleaning, it also performs some statistical
analysis on the data and visualizes the results in the form of Plots.
"""

import pandas as pd
import regex
import numpy as np
import matplotlib.pyplot as plt
import json
from collections import defaultdict


"""
Function to generate a barchart of the PL attributes and the 
percentage of NaN values in those columns.
"""


def plot_pl_nan_stats(df):
    x = []
    y = []

    for col in df.columns:
        na_count = df[col].isna().sum()
        x.append(col)
        y.append(0 if na_count == 0 else round(na_count / len(df[col]) * 100))

    fig, ax = plt.subplots(1, 1)
    fig.set_size_inches(16, 8)
    ax.bar(range(len(x)), y, )
    ax.set_xticks(range(len(x)))
    ax.set_xticklabels(x, rotation='vertical', fontsize=10)
    ax.set_title("NaN Percentages per Column")
    ax.set_xlabel("Columns")
    ax.set_ylabel("NaN Percentage")
    plt.show()


"""
Function to clean PL scrapped data. This includes:
1. Rectifying the Goals Per Match values.
2. Giving the Date Of Birth values a Uniform Format and filling NaN values
3. Turning the Height column from a column of strings to a column of Integers
4. Filling NaN values in the Club column
5. Turning required Float columns into Integer columns
6. Turning percent columns to Float columns from string columns
7. Titlizing all attribute names

"""


def clean_pl_data(df):
    new_names = {col: col.title() for col in df.columns}
    df = df.rename(columns=new_names)

    df['Goals Per Match'] = (
        df['Goals'] / df['Appearances']).round(2).fillna(0)
    df['Date Of Birth'] = df['Date Of Birth'].fillna("DOB Not Available").apply(
        lambda x: (x if '(' not in x else regex.sub(r' \(\d+\)', '', x)))
    df['Height (cm)'] = df['Height'].apply(
        lambda x: int(x[:-2]) if not pd.isnull(x) else float('NaN'))
    del df['Height']
    df['Club'] = df['Club'].fillna('No Current Club')

    float_columns = df.select_dtypes(include=[np.float]).columns
    actual_float_columns = ["Goals Per Match", "Passes Per Match"]
    int_columns = [
        col for col in float_columns if col not in actual_float_columns]
    percent_columns = list(filter(lambda x: '%' in x, df.columns))

    df[percent_columns] = df[percent_columns].apply(
        lambda x: [int(p[:-1]) if not pd.isnull(p) else float('NaN') for p in x])
    df[int_columns] = df[int_columns].astype('Int64')

    return [*float_columns, *percent_columns], df


"""
Function to generate a histogram for each available numeric attribute
"""


def plot_pl_stats(df, attributes_to_plot):
    N_COLUMNS = 3
    columns = attributes_to_plot

    fig, ax = plt.subplots(len(columns) //
                           N_COLUMNS + 1, N_COLUMNS, figsize=(10, 50))

    for i, col_name in enumerate(columns):
        row = i // N_COLUMNS
        col = i % N_COLUMNS

        X = list(filter(lambda x: x > 0, df[col_name].dropna().tolist()))
        mean = np.mean(X)
        median = np.mean(X)
        stddev = np.std(X)

        ax[row, col].hist(X, bins=30)
        ax[row, col].legend(
            [f"Mean: {mean:.2f}\nMedian: {median:.2f}\nStd Dev: {stddev:.2f}"])
        ax[row, col].set_title(col_name)
    plt.tight_layout()
    plt.show()


"""
Function to clean Wikipedia scraped data. This includes:
1. Removing unnecessary columns
2. Renaming certain columns
3. Make the data rectangular: Every row has all attributes, even if its value is None
4. Titilizing all attribute names
"""


def clean_wiki_data(wiki_data):
    attribute_set = set()
    attribute_count = {}

    cols_to_remove = [
        "dissolved, abolished or demolished date", "different from"]

    clean_data = {}

    for player, attributes in wiki_data.items():
        clean_data[player] = {}
        for attribute in attributes:
            if attribute in cols_to_remove:
                continue
            if attribute == 'headquarters location':
                attribute_set.add('Work Venue')
                clean_data[player]['Work Venue'] = wiki_data[player]['headquarters location']
            else:
                attribute_set.add(attribute.title())
                clean_data[player][attribute.title(
                )] = wiki_data[player][attribute]

        attribute_count[player] = len(attributes)

    nan_count = defaultdict(lambda: 0)

    for player in clean_data:
        for attribute in attribute_set:
            if attribute not in clean_data[player]:
                clean_data[player][attribute] = None
                nan_count[attribute] += 1

    return attribute_count, nan_count, clean_data


"""
Function to print quantitative about the data scraped from Wikipedia
"""


def print_wiki_stats(attribute_count):
    print("Attribute Stats")
    print(
        f"Mean Attribute Count: {np.mean(list(attribute_count.values())):.2f}")
    print(
        f"Median Attribute Count: {np.median(list(attribute_count.values())):.2f}")
    print(
        f"Standard Deviation in Attribute Count: {np.std(list(attribute_count.values())):.2f}")
    print(f"Max Attribute Count: {np.max(list(attribute_count.values()))}")
    print(f"Min Attribute Count: {np.min(list(attribute_count.values()))}")


"""
Function to generate a barchart of the Wikipedia attributes and the 
percentage of NaN values in those columns.
"""


def plot_wiki_nan_stats(wiki_data, nan_count):
    fig, ax = plt.subplots(1, 1)
    fig.set_size_inches(16, 8)
    ax.bar(range(len(nan_count)), [
           x * 100 / len(wiki_data) for x in nan_count.values()])
    ax.set_xticks(range(len(nan_count)))
    ax.set_xticklabels(nan_count.keys(), rotation='vertical', fontsize=10)
    ax.set_title("NaN Percentages per Column")
    ax.set_xlabel("Columns")
    ax.set_ylabel("NaN Percentage")
    plt.show()


"""
Driver code. Reads the two files, calls cleaning and analysis functions on the data
and writes two new JSON files that have cleaned data.
"""


def main():

    # PL Scrape Cleaning
    print("Cleaning uncleaned_pl_scrape.csv")
    df = pd.read_csv('../outputs/uncleaned_pl_scrape.csv', thousands=',')
    plot_pl_nan_stats(df)
    attributes_to_plot, df = clean_pl_data(df)
    plot_pl_stats(df, attributes_to_plot)

    json_string = df.to_json(orient='records')
    player_list = json.loads(json_string)

    out_list = {}

    for player in player_list:
        out_list[player['Name']] = {key: value for (
            key, value) in player.items() if key != 'Name'}

    with open('../outputs/cleaned_pl_scrape.json', 'w') as f:
        json.dump(out_list, f, indent=2)
    print("Generated cleaned_pl_scrape.json")

    # Wikidata cleaning
    print("Cleaning uncleaned_wiki_scrape.json")
    with open('../outputs/uncleaned_wiki_scrape.json', 'r', encoding='utf-8') as f:
        wiki_data = json.load(f)

    attribute_count, nan_count, clean_data = clean_wiki_data(wiki_data)
    print_wiki_stats(attribute_count)
    plot_wiki_nan_stats(wiki_data, nan_count)

    with open('../outputs/cleaned_wiki_scrape.json', 'w') as f:
        json.dump(clean_data, f, indent=2)
    print("Generated cleaned_pl_scrape.json")


if __name__ == "__main__":
    main()
