# Three-dimensional study of the lateral lips of a gliding snake using OpenFOAM on Azure

[![BSD-3 clause](https://img.shields.io/badge/License-BSD%203--Clause-blue.svg)](https://opensource.org/licenses/BSD-3-Clause)
[![Docker Hub](https://img.shields.io/badge/hosted-docker--hub-informational.svg)](https://hub.docker.com/repository/docker/mesnardo/openfoam)

The motion of the flying snake *Chrysopelea paradisi* is characterized by active deformations of the whole body to generate aerodynamic forces necessary for gliding, stabilization, and maneuvering.
One active deformation is the expansion of the rib cage to produce a concave ventral surface with the formation of a pair of ventrally-oriented lips.
Here, we aim to identify the role of the lips and quantify their effect on the aerodynamic performance of the glider.
Our approach is to modify the anatomically accurate cross-section by removing one or both lips and measure the relative change in aerodynamic forces.

![geometries](data/figures/modified_sections_aoa35.png)

**Figure:** Original and modified geometries of the snake section (oriented at a $35$-degree angle of attack).}{From left to right: (1) original profile, (2) profile with the front lip only, (3) profile with the back lip only, and (4) profile with no lips.

The original geometry of the body cross-section of the snake *Chrysopelea paradisi* is available on [FigShare](https://doi.org/10.6084/m9.figshare.705877.v1):

> Krishnan, Anush; J. Socha, John; P. Vlachos, Pavlos; Barba, Lorena A. (2013): Body cross-section of the flying snake Chrysopelea paradisi. figshare. Dataset. https://doi.org/10.6084/m9.figshare.705877.v1

We used [OpenFOAM](https://openfoam.org) (version `v6`) to compute the flow past cylinders with different cross-sections (original and modified shapes of the gliding snake) at Reynolds number $1000$, $2000$, and $3000$ over a range of angles of attack.
All simulations ran inside Docker containers on Microsoft Azure.
We used [Batch Shipyard](https://github.com/Azure/batch-shipyard) (version `3.9.1`) and [Azure CLI](https://github.com/Azure/azure-cli) (version `2.3.1`) to deploy resources on Azure and submit containerized jobs to Azure Batch.

## Create a conda environment for pre- and post-processing of the simulations

```shell
conda env create --name=py37-snakelips-3d --file=environment.yml
conda activate py37-snakelips-3d
pip install --no-deps --editable rodney/
```

## Example of running a simulation on Azure Batch

Navigate to a simulation directory, e.g., `runs/snake3d/both_lips/2k35`:

```shell
SNAKELIPS_DIR=$(pwd)
cd runs/snake3d/both_lips/2k35
```

Copy and update the template `credentials.yaml` with your credentials:

```shell
cp ${SNAKELIPS_DIR}/misc/template-credentials.yaml config_shipyard/credentials.yaml
# Edit the file with your credentials
```

Create the geometry of the snake section:

```shell
python scripts/create_body_obj.py
```

Create a directory in your Azure Storage fileshare to save the output of the simulation:

```shell
az storage directory create --name snake3d2k35_both --account-name <your-account-name> --share-name fileshare
```

Deploy resources (2 dedicated CentOS-based H16r instances) on Azure with Batch Shipyard:

```shell
export SHIPYARD_CONFIGDIR=config_shipyard
shipyard pool add
```

Upload input data to the Gluster FS on the compute nodes:

```shell
shipyard data ingress
```

Submit the jobs:

```shell
shipyard jobs add
```

Once the job has completed, delete the compute resources and download the numerical solution output from Azure Storage:

```shell
shipyard pool del
mkdir output
az storage file download-batch --source fileshare/snake3d2k35_both --destination output --account-name <your-account-name>
```

## Results: mean force coefficients

![fig_mean_force_coefficients](./runs/snake3d/figures/mean_force_coefficients.png)

**Figure:** Mean lift (top) and drag (bottom) coefficients at Reynolds numbers $1000$, $2000$,
and $3000$ versus the angle of attack of a snake cross-section with both lips, only the front
lip or the back lip, and no lips. All values are averaged along the spanwise direction and in
time (between $100$ and $200$ non-dimensional time units of flow simulation).
