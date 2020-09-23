import os
import subprocess as sp

__all__ = [
    "API_MAPPING",
    "GET_PODS_CMD",
    "GET_PODS_NAME_CMD",
    "run_cmd",
    "STANDARD_NAMESPACES",
]


STANDARD_NAMESPACES = ["auxtel", "maintel", "obssys", "kafka-producers", "ospl-daemon"]

API_MAPPING = {
    "obssys": "job",
    "auxtel": "job",
    "maintel": "job",
    "kafka-producers": "deployment",
    "ospl-daemon": "daemonset",
}

GET_PODS_CMD = (
    "kubectl get pod -o=custom-columns=NODE:.spec.nodeName,NAME:.metadata.name"
)

GET_PODS_NAME_CMD = "kubectl get pod -o=custom-columns=NAME:.metadata.name"


def run_cmd(command, as_lines=False):
    """Run a command via subprocess::run.

    Parameters
    ----------
    command : str
        The command to run. Shoud be space separated.
    as_lines : bool, optional
        Return the output as a list instead of a string.

    Returns
    -------
    str or list
        The output from the command.
    """
    output = sp.run(command.split(), stdout=sp.PIPE, stderr=sp.STDOUT)
    decoded_output = output.stdout.decode("utf-8")
    if as_lines:
        return decoded_output.split(os.linesep)
    else:
        return decoded_output[:-1]
