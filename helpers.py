import os
import subprocess as sp
import sys

__all__ = [
    "acknowledge_deletion",
    "API_MAPPING",
    "GET_KUBECTL_CONTEXT",
    "GET_PODS_CMD",
    "GET_PODS_NAME_CMD",
    "KAFKA_STANDARD_NAMESPACES"
    "run_cmd",
    "STANDARD_NAMESPACES",
]


STANDARD_NAMESPACES = [
    "auxtel",
    "calsys",
    "eas",
    "love",
    "maintel",
    "simonyitel",
    "uws",
    "obssys",
    "dds-test",
    "kafka-producers",
    "ospl-daemon",
]

KAFKA_STANDARD_NAMESPACES = [
    "auxtel",
    "calsys",
    "eas",
    "simonyitel",
    "uws",
    "obssys",
    "control-system-test",
]

API_MAPPING = {
    "obssys": "job",
    "dds-test": "job",
    "control-system-test": "job",
    "eas": "job",
    "auxtel": "job",
    "maintel": "job",
    "love": ["deployment", "job", "hpa"],
    "simonyitel": "job",
    "uws": "job",
    "calsys": "job",
    "kafka-producers": "deployment",
    "ospl-daemon": "daemonset",
}

GET_PODS_CMD = (
    "kubectl get pod -o=custom-columns=NODE:.spec.nodeName,NAME:.metadata.name"
)

GET_PODS_NAME_CMD = "kubectl get pod -o=custom-columns=NAME:.metadata.name"

GET_KUBECTL_CONTEXT = "kubectl config current-context"


def run_cmd(command, as_lines=False):
    """Run a command via subprocess::run.

    Parameters
    ----------
    command : str
        The command to run. Should be space separated.
    as_lines : bool, optional
        Return the output as a list instead of a string.

    Returns
    -------
    str or list
        The output from the command.
    """
    try:
        cmd = command.split()
    except AttributeError:
        cmd = command
    output = sp.run(cmd, stdout=sp.PIPE, stderr=sp.STDOUT)
    decoded_output = output.stdout.decode("utf-8")
    if as_lines:
        return decoded_output.split(os.linesep)
    else:
        return decoded_output[:-1]


def acknowledge_deletion():
    """Check the kubectl context before allowing deletion."""
    output = run_cmd(GET_KUBECTL_CONTEXT)
    print(f"{output} resources to be deleted. Are you sure?")
    response = input("y to proceed, any other key to exit: ")
    if response != "y":
        print("Exiting")
        sys.exit(255)
    else:
        print(f"Proceeding with {output} resource deletion.")
