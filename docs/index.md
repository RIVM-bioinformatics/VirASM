# VirASM

[![CodeFactor](https://www.codefactor.io/repository/github/rivm-bioinformatics/virasm/badge)](https://www.codefactor.io/repository/github/rivm-bioinformatics/virasm)
![GitHub top language](https://img.shields.io/github/languages/top/RIVM-bioinformatics/VirASM)
![Snakemake](https://img.shields.io/badge/snakemake-6.13.1-brightgreen.svg?style=flat)

![GitHub release (latest by date including pre-releases)](https://img.shields.io/github/v/release/RIVM-bioinformatics/VirASM?include_prereleases)
![GitHub](https://img.shields.io/github/license/RIVM-bioinformatics/VirASM)

---

VirASM is a quick and minimal pipeline for assembling metagenomics/viromics samples from raw paired-end Illumina FastQ data.

VirASM performs high speeds data quality control and data cleanup, removal of background-host data, and assembly of cleaned reads into bigger scaffolds with a focus on full viral genomes.

VirASM is designed to run on High-Performance Computing (HPC) infrastructures, but can also run locally on a standalone (linux) computer if needed.

---

## Installation instructions

**Before you download and install VirASM, please make sure [Conda](https://docs.conda.io/projects/conda/en/latest/index.html) is installed on your system and functioning properly!**

### Download
Use the following command to download the latest release of VirASM and move to the newly downloaded `VirASM/` directory:

```bash
git clone https://github.com/RIVM-bioinformatics/VirASM.git; cd VirASM
```

### Installation

1. Create the required conda-environment and install the necessary dependencies:
    Copy and paste the code-snippet below in order to create the new conda-environment and directly activate it.

    `conda create --name VirASM -c conda-forge mamba python=3.7 -y; conda activate VirASM; mamba env update -f mamba-env.yml`

2. Now that all the necessary dependencies are installed you can actually install VirASM itself on your system with:  
    `pip install .`

VirASM is now installed!  
You can verify the installation by running `virasm -h` or `virasm -v` which should return the help-document or installed version respectively.

You can start VirASM from anywhere on your system as long as the VirASM conda-environment is active. If this environment isn't active you can activate it with `conda activate VirASM`.

### Auto-updating

VirASM is able to update itself to the latest released version.  
This makes it easier for everyone to use the latest available version without having to manually check the GitHub releases.

The check for new versions is done automatically.

If you wish to run VirASM without the updater checking for a new release, then add the `--skip-updates` flag to your command. in this case you wil **not** be notified if there is a new release available.

---

## Usage

**Note: VirASM is designed to work on the RIVM internal computing cluster. Other computing configurations are not included**

You can start VirASM without any configuration. It is only necessary to provide an input directory containing the raw Illumina FastQ files, and the desired output directory for all results and intermediate data.

As an example, you can start an analysis with a command such as the following:

```bash
virasm --input {path/to/input-directory} --output {path/to/desired-output-directory}
```