# lager

⚠ Construction Ahead ⚠

Everything about my code and its underlying concepts is questionable, fantastical, and fragile-at-best right-down to its core premises of 'beating' the Halting Problem, novel intelligences, establishing co-learning architectures, knowledgebases, and 'Morphological source code' and its 'kernel agents'.

[[Morphological Source Code]] is a dynamic code generation approach where the source code is generated at runtime from a static database, aiming to model and mimic the behavior of other codebases using its own primitives, syntax, and pedagogical notions, essentially creating a self-modifying and adaptable codebase that can morph and evolve based on the codebases it encounters.

[![CI/CD](https://github.com/MOONLAPSED/tp-ob/actions/workflows/main.yaml/badge.svg)](https://github.com/MOONLAPSED/tp-ob/actions/workflows/main.yaml)


## installing cognosis.lager

### Video Instructions
[YouTube video link](https://youtu.be/XeeYZZujvAA?si=XhxOMCypKHpWKSjM)

### Setup Instructions

There is no direct setup for cognosis as it is managed by the invoking entity, a runtime abraxus instance within a CognOS morphological source code module.

However, if you wish to run cognosis locally for development purposes, follow the instructions below.

## Running Cognosis Locally

### Prerequisites
- Ensure you have `pipx` and `mamba` (or `conda`) installed on your system.

### Installation Steps

1. **Install mamba (or conda)**:
    ```sh
    conda install mamba -n base -c conda-forge
    ```

2. **Create and activate a new environment**:
    ```sh
    mamba create -n cognosis_env python=3.12
    mamba activate cognosis_env
    ```

3. **Install pipx**:
    ```sh
    python -m pip install --user pipx
    python -m pipx ensurepath
    source ~/.bashrc
    ```

4. **Install cognosis using pipx**:
    ```sh
    pipx install cognosis
    ```

5. **For the development version, use**:
    ```sh
    pipx install --editable .
    ```

## Windows Sandbox Version

### Using micromamba via `environment.yaml` (any hypervisor/OS)
```sh
cd {{app_dir}}
conda activate {{env_name}}
conda env create -f environment.yml
python -m {{app_name}}
```
#### This is for Ubuntu-22.04 version
```sh
python3 -m pip install --user pipx
python3 -m pipx ensurepath
source .bashrc
```

### Using pipx and pdm via pyproject.toml (WSL preferred)
```sh
* Clone to your local machine, set local $PATH manually in cfg.wsb and scoop.ps1.
* Run cfg.wsb to open container
* Inside container; try `boxy.bat` to initialize the container installation 
    - If it fails, try again. If nothing works, you need to exit and restart the whole container
* Run `Miniforge Prompt.lnk` to open a conda environment 
    - Press 'windows-key' + type 'terminal', select windows terminal
    - cd Desktop
    - .\"Miniforge Prompt.lnk"
    - conda create -n 3ten python=3.10
    - conda init
    - exit
    - Open cmd.exe (from inside windows terminal)
    - cd Desktop
    - .\"Miniforge Prompt.lnk"
    - conda activate 3ten
    - python3 -m pip install --upgrade pip
    - python3 -m pip install --user pipx
    - python -m pipx install virtualenv
    - python -m venv test_env
    - .\test_env\Scripts\activate  # unix->'source test_env/bin/activate'
    - pip install -e -r requirements.txt
```

### without mamba (using conda)
```sh
conda install mamba -n base -c conda-forge
mamba create -n cognosis_env python=3.12
mamba activate cognosis_env
python -m pip install --user pipx
python -m pipx ensurepath
source ~/.bashrc
pipx install --editable .
```

