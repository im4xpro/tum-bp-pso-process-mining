import sys
import warnings
from collections import Counter
from pathlib import Path

import pandas as pd
import pm4py

from evaluation import evaluate_model
from preprocessing import build_log_base, load_raw_log

warnings.filterwarnings('ignore')

DEFAULT_MODEL = Path(__file__).resolve().parent.parent / 'data' / '02_process_model.bpmn'


def evaluate_bpmn(path, log_base, raw):
    net, im, fm = pm4py.convert_to_petri_net(pm4py.read_bpmn(str(path)))
    labels = Counter(t.label for t in net.transitions if t.label)
    duplicates = sorted(label for label, count in labels.items() if count > 1)
    log_labels = set(log_base['concept:name'].unique())

    print(f'Model: {path}')
    print(f'Sound: {pm4py.check_soundness(net, im, fm)[0]}')
    print(f'Activities not in the log: {sorted(set(labels) - log_labels) or "none"}')
    print(f'Log activities not in the model: {sorted(log_labels - set(labels)) or "none"}')
    if duplicates:
        print(f'Duplicate activities: {duplicates}. Token replay is unreliable on these, compare with the alignment values.')

    # Same metrics and log as the iterations in runs/, so the scores are directly comparable
    metrics = evaluate_model(log_base, (net, im, fm))
    alignment_fitness = pm4py.fitness_alignments(log_base, net, im, fm, multi_processing=True)
    metrics['Fitness (alignments)'] = alignment_fitness['log_fitness']
    metrics['Perfect_Fit_Share (alignments)'] = alignment_fitness['percFitTraces'] / 100
    metrics['Precision (alignments)'] = pm4py.precision_alignments(log_base, net, im, fm, multi_processing=True)
    metrics['Fitness (raw log)'] = pm4py.fitness_token_based_replay(raw, net, im, fm)['log_fitness']
    return metrics


if __name__ == '__main__':
    model_path = Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_MODEL
    raw = load_raw_log()
    metrics = evaluate_bpmn(model_path, build_log_base(raw), raw)
    print(pd.Series(metrics).round(3).to_string())
