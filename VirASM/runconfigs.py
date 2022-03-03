"""
Construct and write configuration files for VirASM.
"""

import multiprocessing
import os

import yaml

from .functions import DefaultConfig


def set_cores(cores):
    """
    Set the maximum (viable) number of cores to use
    """
    available = multiprocessing.cpu_count()
    if cores == available:
        return cores - 2
    if cores > available:
        return available - 2
    return cores


def WriteConfigs(samplesheet, cores, cwd, local, bg, dryrun):
    if not os.path.exists(cwd + "/config"):
        os.makedirs(cwd + "/config")

    params = DefaultConfig.params
    conf = DefaultConfig.config["grid"]
    params["sample_sheet"] = samplesheet

    if dryrun is True:
        conf["dryrun"] = True

    if bg is not None:
        DefaultConfig.params["db"]["background"] = bg

    if local is True:
        conf = DefaultConfig.config["local"]
        conf["cores"] = set_cores(cores)
        if dryrun is True:
            conf["dryrun"] = True

        threads_highcpu = int(set_cores(cores))
        threads_midcpu = int(cores / 2)
        threads_lowcpu = 1

        params["computing_execution"] = "local"
        params["threads"]["Alignments"] = threads_highcpu
        params["threads"]["Filter"] = threads_midcpu
        params["threads"]["Assemble"] = threads_highcpu
        params["threads"]["MultiQC"] = threads_lowcpu

    with open(cwd + "/config/config.yaml", "w") as outfile:
        yaml.dump(conf, outfile, default_flow_style=False)
    with open(cwd + "/config/params.yaml", "w") as outfile:
        yaml.dump(params, outfile, default_flow_style=False)

    paramfile = cwd + "/config/params.yaml"
    conffile = cwd + "/config/config.yaml"
    return paramfile, conffile, params, conf
