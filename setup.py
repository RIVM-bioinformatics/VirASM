import sys

from packaging import version as vv
from setuptools import find_packages, setup

from VirASM import __version__

if sys.version_info.major != 3 or sys.version_info.minor < 6:
    print("VirASM requires Python 3.6 or higher")
    sys.exit(1)

try:
    import conda
except SystemError:
    sys.exit(
        """
Error: conda could not be accessed.
Please make sure conda is installed and functioning properly before installing VirASM
"""
    )


try:
    import snakemake
except SystemError:
    sys.exit(
        """
Error: snakemake could not be accessed.
Please make sure snakemake is installed and functioning properly before installing VirASM
"""
    )


if vv.parse(snakemake.__version__) < vv.parse("6.0"):
    sys.exit(
        f"""
The installed SnakeMake version is older than the minimally required version:

Installed SnakeMake version: {snakemake.__version__}
Required SnakeMake version: 6.0 or later

Please update SnakeMake to a supported version and try again
"""
    )

with open("README.md", "r") as fh:
    long_description = fh.read()


setup(
    name="VirASM",
    author="Florian Zwagemaker",
    author_email="ids-bioinformatics@rivm.nl",
    license="AGPLv3",
    version=__version__,
    packages=find_packages(),
    scripts=["VirASM/workflow/Snakefile", "VirASM/workflow/directories.py"],
    package_data={
        "VirASM": ["workflow/envs/*", "workflow/scripts/*", "workflow/files/*"]
    },
    install_requires=["drmaa==0.7.9", "pyyaml==6.0", "biopython==1.79"],
    entry_points={
        "console_scripts": [
            "virasm = VirASM.VirASM:main",
            "VirASM = VirASM.VirASM:main",
        ]
    },
    keywords=[],
    include_package_data=True,
    zip_safe=False,
)
