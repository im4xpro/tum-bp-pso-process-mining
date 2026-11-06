from pathlib import Path

import pandas as pd

DATA_PATH = Path(__file__).resolve().parent.parent / 'data' / 'bpic2017.csv'


def load_raw_log():
    df = pd.read_csv(DATA_PATH, low_memory=False)
    df['time:timestamp'] = pd.to_datetime(df['time:timestamp'], format='ISO8601')
    return df.sort_values(['case:concept:name', 'time:timestamp'], kind='stable').reset_index(drop=True)


def build_log_base(raw):
    # Keep all cases. Application and offer events stay, work items are reduced to their start events,
    # because suspend/resume/abort events describe the handling of a work item and not a process step.
    is_kept = (raw['EventOrigin'] != 'Workflow') | (raw['lifecycle:transition'] == 'start')
    return raw[is_kept].reset_index(drop=True)
