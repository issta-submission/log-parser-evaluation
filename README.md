# A Large-scale Evaluation for Log Parsing Techniques: How Far are We?

This is the anonymous replication package for the ISSTA2024 submission **#448 "A Large-scale Evaluation for Log Parsing Techniques: How Far are We?"**. This repository contains the full datasets of LogPub, the source code of our benchmark, and **the complete version of our experimental results**, which can be found at [RQ_experiments](RQs_experiments/README.md) 🔗.


## Repository Organization 

```
├── 2k_dataset/
├── full_dataset/
├── benchmark/
│   ├── evaluation/
│   ├── logparser/
│   ├── old_benchmark/
│   ├── LogPPT/ # contains the modified source code of LogPPT
│   ├── UniParser/ # contains the source code of implemented UniParser
│   └── run_statistic_all.sh # the script to run all statistic-based log parsers
├── result/
│   ├── ...... # contains the output evaluation metric files
│   └── ...... # you can also download the recorded parsed results into here
├── RQ_experiments/
│   ├── RQ1/
│       ├── RQ1_experiment.py
│       └── ...... # other output files
│   ├── RQ2/
│       ├── RQ2_experiment.py
│       └── ...... # other output files
│   ├── RQ3/
│       ├── RQ2_experiment.py
│       └── ...... # other output files
├── util/
│   ├── download_gdrive.py # code to automatically download the gdrive files
│   └── download_fulldataset.sh # script to download the full datasets, LogPub
├── requirements.txt
└── README.MD
```

## Requirements

Owing to the large scale of the benchmark in the experiments, the requirements of the benchmark of all log parsers are:

- At least 16GB memory.
- At least 100GB storage.
- GPU (for LogPPT and UniParser).

**Installation**

1. Install ```python >= 3.8```
2. ```pip install -r requirements.txt```

## Download the LogPub Dataset

Due to the size limitation of Github, we have uploaded the proposed collection of datasets, LogPub, to the Google Drive for download, which can be downloaded via this [link](https://drive.google.com/file/d/1pV_FOa8KPzD2UwPyGPoo-12tyaBqOKNo/view?usp=share_link) 🔗 (zip: ~0.95G; unzip: 11G). After downloding, please extract the downloaded files to the folder `full_dataset` for follow-up proceeding.


## Large-scale benchmarking 


### Quick Demo using Drain

We give a demo script to run Drain on both Loghub-2k and LogPub, this will takes about 2-3 hours.

```bash
cd benchmark/
./demo.sh
```

### Evaluation of all 15 parsers

One can follow the steps to evaluate all parsers using Loghub-2k or the proposed Logpub datasets. The overall time cost is more than 48 hours.

- Run all statistic-based log parsers on Loghub-2k

```bash
cd benchmark/
./run_statistic_2k.sh
```

- Run all statistic-based log parsers on LogPub

```bash
cd benchmark/
./run_statistic_full.sh
```

- Run Semantic-based log parsers: LogPPT & UniParser

  Since these methods are quite different with other log parsers, and they requires a GPU to support efficient parsing, we seperate their environments from other log parsers. Please refer to the README file of [LogPPT](benchmark/LogPPT/README.md) or [UniParser](benchmark/UniParser/README.md) to use one-click script to parse and evaluate each log parsers respectively.
