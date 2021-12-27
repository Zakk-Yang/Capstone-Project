#!/bin/bash

pip install --upgrade pip
pip install --upgrade jupyterlab
pip install autopep8
pip install --upgrade jupyterlab-git

venv_root_dir=${PWD##*/}
python -m ipykernel install --user --name=$venv_root_dir

pip install ipywidgets
#jupyter nbextension enable --py widgetsnbextension --sys-prefix
#jupyter labextension install @jupyter-widgets/jupyterlab-manager
#jupyter labextension install jupyterlab-execute-time
#jupyter serverextension enable --py jupyterlab_git

jupyter lab build
