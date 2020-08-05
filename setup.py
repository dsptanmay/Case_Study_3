import pkg_resources
import subprocess as sp
import sys

python = sys.executable
installed = {pkg.key for pkg in pkg_resources.working_set}
required = {"questionary", "tabulate"}

missing = required - installed

if missing:
    sp.check_call(
        [python, "-m", "pip", "--install", "--upgrade", "--no-cache-dir", *missing],
        stdout=sp.DEVNULL,
    )
