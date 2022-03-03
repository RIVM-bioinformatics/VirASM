"""
Starting point of the VirASM pipeline and wrapper

Copyright © 2022 RIVM

https://github.com/RIVM-bioinformatics/VirASM
"""

import argparse
import multiprocessing
import os
import pathlib
import sys

import snakemake
import yaml

from VirASM import __version__
from VirASM.functions import MyHelpFormatter, color
from VirASM.runconfigs import WriteConfigs
from VirASM.samplesheet import WriteSampleSheet
from VirASM.update import update

yaml.warnings({"YAMLLoadWarning": False})


def get_args(givenargs):
    """
    Parse the command line arguments
    """

    def dir_path(arginput):
        if os.path.isdir(arginput):
            return arginput
        print(f'"{arginput}" is not a directory. Exiting...')
        sys.exit(1)

    def currentpath():
        return os.getcwd()

    arg = argparse.ArgumentParser(
        prog="VirASM",
        usage="%(prog)s [required arguments] [optional arguments]",
        description="VirASM: a quick (barebones) pipeline for assembly of scaffolds from (viral) metagenomics samples",
        formatter_class=MyHelpFormatter,
        add_help=False,
    )

    required_args = arg.add_argument_group("required arguments")
    optional_args = arg.add_argument_group("optional arguments")

    required_args.add_argument(
        "--input",
        "-i",
        type=dir_path,
        metavar="DIR",
        help="The input directory containing the raw fastq(.gz) files",
        required=True,
    )

    required_args.add_argument(
        "--output",
        "-o",
        metavar="DIR",
        type=str,
        default=currentpath(),
        help="Output directory",
        required=True,
    )

    optional_args.add_argument(
        "--version",
        "-v",
        version=__version__,
        action="version",
        help="Show the VirASM version and exit",
    )

    optional_args.add_argument(
        "--help",
        "-h",
        action="help",
        default=argparse.SUPPRESS,
        help="Show this help message and exit",
    )

    optional_args.add_argument(
        "--skip-updates", action="store_true", help="Skip the update check"
    )

    optional_args.add_argument(
        "--local",
        action="store_true",
        help="Use VirASM locally instead of in a grid-computing configuration",
    )

    optional_args.add_argument(
        "--background",
        type=str,
        metavar="File",
        help="Override the default human genome background file",
    )

    optional_args.add_argument(
        "--dryrun",
        action="store_true",
        help="run the VirASM workflow without actually doing anything (check if the workflow will run as expected)",
    )

    optional_args.add_argument(
        "--threads",
        default=min(multiprocessing.cpu_count(), 128),
        type=int,
        metavar="N",
        help=f"Number of local threads that are available to use.\nDefault is the number of available threads in your system ({min(multiprocessing.cpu_count(), 128)})",
    )

    if len(givenargs) < 1:
        print(
            f"{arg.prog} was called but no arguments were given, please try again \n\tUse '{arg.prog} -h' to see the help document"
        )
        sys.exit(1)
    else:
        flags = arg.parse_args(givenargs)
    return flags


def CheckInputFiles(indir):
    """
    Check if the input files are valid fastq files
    """
    allowedextensions = [".fastq", ".fq", ".fastq.gz", ".fq.gz"]
    foundfiles = []

    for filenames in os.listdir(indir):
        extensions = "".join(pathlib.Path(filenames).suffixes)
        foundfiles.append(extensions)

    return bool(any(i in allowedextensions for i in foundfiles))


def main():
    """
    VirASM starting point
    """

    flags = get_args(sys.argv[1:])

    if not flags.skip_updates:
        update(sys.argv)

    inpath = os.path.abspath(flags.input)
    start_path = os.getcwd()
    outpath = os.path.abspath(flags.output)
    exec_folder = os.path.abspath(os.path.dirname(__file__))

    Snakefile = os.path.join(exec_folder, "workflow", "Snakefile")

    if CheckInputFiles(inpath) is False:
        print(
            f"""
{color.RED + color.BOLD}"{inpath}" does not contain any valid FastQ files.{color.END}
Please check the input directory and try again. Exiting...
            """
        )
        sys.exit(1)
    else:
        print(
            f"""
{color.GREEN}Valid input files were found in the input directory{color.END} ('{inpath}')
            """
        )
    if not os.path.exists(outpath):
        os.makedirs(outpath)

    if not os.getcwd() == outpath:
        os.chdir(outpath)
    workdir = outpath

    samplesheet = WriteSampleSheet(inpath)

    paramfile, conffile, paramdict, confdict = WriteConfigs(
        samplesheet,
        flags.threads,
        os.getcwd(),
        flags.local,
        flags.background,
        flags.dryrun,
    )

    if flags.local is True:
        status = snakemake.snakemake(
            Snakefile,
            workdir=workdir,
            conda_frontend="mamba",
            cores=confdict["cores"],
            use_conda=confdict["use-conda"],
            jobname=confdict["jobname"],
            latency_wait=confdict["latency-wait"],
            dryrun=confdict["dryrun"],
            configfiles=[paramfile],
            restart_times=3,
        )
    if flags.local is False:
        status = snakemake.snakemake(
            Snakefile,
            workdir=workdir,
            conda_frontend="mamba",
            cores=confdict["cores"],
            nodes=confdict["cores"],
            use_conda=confdict["use-conda"],
            jobname=confdict["jobname"],
            latency_wait=confdict["latency-wait"],
            drmaa=confdict["drmaa"],
            drmaa_log_dir=confdict["drmaa-log-dir"],
            dryrun=confdict["dryrun"],
            configfiles=[paramfile],
            restart_times=3,
        )

    if confdict["dryrun"] is False and status is True:
        snakemake.snakemake(
            Snakefile,
            workdir=workdir,
            report="results/snakemake_report.html",
            configfiles=[paramfile],
            quiet=True,
        )
