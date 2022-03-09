# PyFLEXTRKR
PyFLEXTRKR is a python package for feature tracking, with specific capabilities to track MCS and convective cells from Satellite, Radar and model data. 

---
To use PyFLEXTRKR please use the attached environment.yml file and create a conda virtual environment
```bash
conda env create -f environment.yml --prefix /conda_env_dir/flextrkr
```
Then when running pyflextrkr you can first activate its virtual environment with
```bash
conda activate flextrkr
```
Then the package can be installed (in editable/dev mode for now) with
```bash
pip install -e .
```
Then any changes to the source code will be reflected in the running version.  

Example to run the code:
```bash
python ./runscripts/run_cacti_csapr.py ./config/config_csapr500m_nersc.yml
```
```bash
python ./runscripts/run_mcs_tbpf.py ./config/config_wrfda_asia_mcs.yml
```