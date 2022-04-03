# SnapperML

[![Documentation Status](https://readthedocs.org/projects/snapperml/badge/?version=latest)](https://snapperml.readthedocs.io/en/latest/?badge=latest)

![](docs/assets/banner.png)

SnapperML is a framework for experiment tracking and machine learning operationalization that combines existent and well-supported technologies.
These technologies include Docker, [Mlflow](https://mlflow.org/), [Ray](https://github.com/ray-project/ray/), among others.

The framework provides an opinionated workflow to design and execute experiments either on a local environment or the cloud. SnapperML includes:

- CLI autogeneration for training scripts
- Extended tracking capabilities,
  - Automatic tracking of hyperparameters and cli arguments
  - Log and traceback collection 
  - Track basic running operating system specs
- Easy distributed training and hyperparameter optimization with Ray
- Command Line Interface (CLI) for packaging and running projects inside docker containers.
- GitOps-friendly experiment configuration based on YAML/JSON files

## How to install?

SnapperML requires Python>=3.7. The python package can be installed using **pip**:

```
pip install snapper-ml
```

Ray support for distributed execution can be installed using the following

```
pip install snapper-ml[ray]
```

## Architecture

The framework main core is divided into four modules that interact with the user through a Command-Line Interface (CLI) and a Python library.
The objective of the library is to minimize the code changes required to instrument scripts to be executed by the Job Runner and to provide the abstractions to interact with the Tracking and Hyperparameter Optimization engines. On the other hand, the CLI is in charge of executing scripts either in a local
environment or a remote environment.

![Architecture Overview](./thesis/source/figures/ml_experiment_overview.svg)


## Documentation

The documentation is available [here](https://snapperml.readthedocs.io/en/latest/)


## Example

```python
# train_svm.py

from snapper_ml import job

@job
def main(C, kernel, gamma='scale'):
    np.random.seed(1234)
    X_train, X_val, y_train, y_val = load_data()
    model = SVC(C=C, gamma=gamma, kernel=kernel)
    model.fit(X_train, y_train)
    accuracy = model.score(X_val, y_val)
    return {'val_accuracy': accuracy}


if __name__ == '__main__':
    main()
```

```yaml
# train_svm.yaml

name: "SVM"
kind: 'group'
num_trials: 12
sampler: TPE

param_space:
  C: loguniform(0.01, 1000)
  gamma: choice(['scale', 'auto'])

metric:
  name: val_accuracy
  direction: maximize

ray_config:
  num_cpus: 4

run:
  - train_svm.py
```

```bash

snapper-ml run --config_file=train_svm.yaml
```
