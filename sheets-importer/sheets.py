#!/usr/bin/env python3

import gspread
import pandas as pd, numpy as np

gc = gspread.service_account()

def get_worksheet_as_df(worksheet):
    df = pd.DataFrame(a:=worksheet.get_all_records(head=2))

    df = df.replace('', None)

    return df

def get_datasets_and_resources(url):
    sh = gc.open_by_url(url)
    datasets = sh.worksheet('Datasets')
    resources = sh.worksheet('Resources')
    assert datasets and resources
    datasets, resources = get_worksheet_as_df(datasets), get_worksheet_as_df(resources)
    return datasets, resources
