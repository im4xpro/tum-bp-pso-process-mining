# Process and Data Science on the BPIC-17 Event Log

Code for the first assignment of *Business Process Prediction, Simulation, and Optimization* (TUM, winter semester 2026/27).
The loan application process of the [BPI Challenge 2017](https://ais.win.tue.nl/bpi/2017/challenge.html) log is analysed in five steps: basic statistics, process discovery, iterative model improvement, decision mining and a cluster analysis of the cases.

## Repository structure

```
analysis/                  Notebooks (run in this order) and shared helper modules
  00_data_exploration        Converts the XES log to CSV, basic statistics of the log (Table 1)
  01_process_discovery       DFG and Inductive Miner on the unfiltered log (Table 2, columns DFG / Ind. Miner)
  02_process_model_improvement  Filtering, Inductive Miner on the filtered log, evaluation of the final model (Table 2, column Final)
  03_decision_mining         Decision points, alignments, decision trees, annotated BPMN
  04_clustering              K-means clustering of the cases (Table 3, cluster figures)
  preprocessing.py           Loads the CSV log; build_log_base() applies the event filter
  evaluation.py              Quality metrics (fitness, precision, generalization, simplicity, max node degree, max depth)
  evaluate_bpmn.py           CLI: evaluates a BPMN file, additionally with alignment-based fitness and precision
data/                      BPIC-17 event log (git-ignored, see Setup): the downloaded XES and the CSV created from it
process_model/             Final process model (BPMN + SVG) and its manually laid out annotated version
output/                    Generated files (git-ignored): intermediate models, alignment caches, figures
```

## Setup

Requires Python 3.12 and [Graphviz](https://graphviz.org) (`brew install graphviz` / `apt install graphviz`) for the pm4py visualisations.

```bash
python3.12 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### Event log

The event log is not part of the repository because of its size (about 550 MB unpacked).

1. Download the [BPIC 2017 event log](https://data.4tu.nl/articles/_/12696884/1)
2. Unpack it and save it as `data/bpic2017.xes`:
   ```bash
   gunzip -c "BPI Challenge 2017.xes.gz" > data/bpic2017.xes
   ```
3. Run `analysis/00_data_exploration.ipynb` first. It reads the XES file and writes `data/bpic2017.csv`, which all later notebooks load because it is much faster to read.

### Running the analysis

Run the notebooks from the `analysis/` folder in numerical order, with the `.venv` kernel.

## Manual steps

Two steps of the workflow were done by hand in the [bpmn.io](https://bpmn.io) editor and cannot be reproduced by running the notebooks:

1. **Final model.** The model discovered on the filtered log (`output/inductive_miner_filtered.bpmn`, notebook 02) was simplified manually by removing very rare activities, unused gateways and loops. The result is `process_model/final_model.bpmn`, which is the input of notebooks 02 (evaluation) and 03.
2. **Annotated model.** Notebook 03 writes the conditions and branch probabilities onto the gateway flows (`output/final_model_annotated.bpmn`). For readability, these labels were moved into text annotations attached to the flows and arranged manually, which gives `process_model/final_model_annotated_manual.bpmn`.
