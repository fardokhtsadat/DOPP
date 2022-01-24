# pd.set_option('display.max_rows', 500)
# pd.set_option('display.max_columns', 500)
# pd.set_option('display.max_rows', 10)
# pd.set_option('display.max_columns', 10)

# Import libraries
import pandas as pd
import numpy as np
import re
import argparse
import json

def change_jsontypes(configuration):
    for key, value in configuration.items():
        if value == "True":
            configuration[key] = True
        elif value == "False":
            configuration[key] = False
        elif value == "None":
            configuration[key] = None
        else:
            continue

    return configuration

def pipeline(path, split_which, split_by, keep_which, extract_which, info_cols, year_from, year_to, flip, melt_by, target_name, convert_which, aggregate_by, reshape_by):
    if exists(path): data = load_file(path)
    if exists(split_which): data = split_col(data=data, split_which=split_which, split_by=split_by, keep_which=keep_which)
    if exists(extract_which): data = extract_ctr_code(data=data, extract_which=extract_which)
    if exists(info_cols): data = assign_column_names(data=data, info_cols=info_cols, year_from=year_from, year_to=year_to, flip=flip)
    data = fill_nas(data=data)
    if exists(melt_by): data = melt_data(data=data, info_cols=info_cols, year_from=year_from, year_to=year_to, melt_by=melt_by,
                     target_name=target_name)
    data = drop_nas(data=data)
    if exists(convert_which): data = convert_to_numeric(data=data, convert_which=convert_which)
    if exists(aggregate_by): data = aggregate_sum(data=data, aggregate_by=aggregate_by)
    return data

def exists(argument):
    if argument is not None:
        return True
    else:
        return False

def load_file(file_name=""):
    ### Loop the data lines
    with open(file_name, 'r') as temp_f: #e.g. "Co2Emissions/sdg_12_30.tsv"
        # get No of columns in each line
        col_count = [len(re.split('\s', l)) for l in temp_f.readlines()]

    ### Generate column names  (names will be 0, 1, 2, ..., maximum columns - 1)
    column_names = [i for i in range(0, max(col_count) - 1)]

    # Load data
    data = pd.read_csv(file_name, sep='\s', engine='python', header=None, names=column_names)
    data = data.drop(data.index[0])
    return data

def split_col(data=None, split_which=None, split_by=",", keep_which=None):
    data_split = data[split_which].str.split(",", expand=True)
    data_split = data_split.iloc[:, keep_which]
    data = data.drop(data.columns[[split_which]], axis=1)
    data = pd.concat([data_split, data], ignore_index=True, sort=False, axis=1)
    return data

def extract_ctr_code(data=None, extract_which=None):
    data.iloc[:, extract_which] = data.iloc[:,extract_which].str[:2]
    return data

def assign_column_names(data=None, info_cols=[], year_from=None, year_to=None, flip=False):
    # Preprocess and assign column names
    # NOTE: status variable stores the information of the data point status, i.e. is the data successfully retrieved (NaN), estimated (e), definition differs (d), not applicable (z), definition differs and estimated (de), or break in time series and estimated (be)
    if flip:
        years = np.flip(np.arange(year_from, year_to+1))
    else:
        years = np.arange(year_from, year_to+1)
    status = np.full((1, years.size), [str(year) + '_status' for year in years])
    cols = np.empty((years.size + status.size,), dtype=status.dtype)
    cols[0::2] = years
    cols[1::2] = status

    # Stack the two data frames horizontally
    data.columns = info_cols + cols.tolist()
    return data

def fill_nas(data=None):
    return data.fillna('ok').replace(':', np.nan)

def drop_nas(data=None):
    return data.dropna()

def convert_to_numeric(data=None, convert_which=None):
    data[convert_which] = pd.to_numeric(data[convert_which], downcast="float")
    return data

def aggregate_sum(data=None, aggregate_by=None):
    return data.groupby(aggregate_by).sum().reset_index()

def melt_data(data=None, info_cols=None, year_from=None, year_to=None, melt_by=None, target_name=None):
    data = data[info_cols + [str(year) for year in np.arange(year_from,year_to+1)]]. \
        melt(info_cols, var_name=melt_by, value_name=target_name)
    return data

def reshape_data(data=None, reshape_by=None):
    return data.set_index(reshape_by).unstack().reset_index()



if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--path_to_config", default="related_to_transport.json")
    args = parser.parse_args()

    dataframes = []
    with open(args.path_to_config) as config_file:
        config_file = json.load(config_file)

    for dataset in config_file:
        configuration = change_jsontypes(config_file[dataset])

        data = pipeline(path=configuration['path'],
                        split_which=configuration['split_which'],
                        split_by=configuration['split_by'],
                        keep_which=configuration['keep_which'],
                        extract_which=configuration['extract_which'],
                        info_cols=configuration['info_cols'],
                        year_from=configuration['year_from'],
                        year_to=configuration['year_to'],
                        flip=configuration['flip'],
                        melt_by=configuration['melt_by'],
                        target_name=configuration['target_name'],
                        convert_which=configuration['convert_which'],
                        aggregate_by=configuration['aggregate_by'],
                        reshape_by=configuration['reshape_by'])

        data.to_csv("RelatedToTransport/"+dataset+".csv", index=False)

        #Prepare datasets to be joined all together by Year and Country.
        data.columns = [dataset+"_"+col if col not in ['Year', 'Country'] else col for col in data.columns.to_list()]
        dataframes.append(data)

    dataframes = [df.set_index(['Country', 'Year']) for df in dataframes]
    joined_df = dataframes[0].join(dataframes[1:], how="outer").reset_index()
    joined_df.to_csv("RelatedToTransport/All_data_outer_join_by_country_and_year.csv", index=False)
    joined_df = dataframes[0].join(dataframes[1:], how="inner").reset_index()
    joined_df.to_csv("RelatedToTransport/All_data_inner_join_by_country_and_year.csv", index=False)
