#------------------------------------------------------------------------
#IMPORTS
#------------------------------------------------------------------------
import os
import subprocess
#------------------------------------------------------------------------
#FUNCTIONS
#------------------------------------------------------------------------
def run_command(command):
    flags = subprocess.CREATE_NO_WINDOW
    result = subprocess.run(
        command,
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        creationflags=flags
    )
    return result.stdout, result.stderr, result.returncode
#------------------------------------------------------------------------
def sfc():
    stdout, stderr, returncode = run_command("sfc /scannow")
    global sfc_success, sfc_code
    if returncode == 0:
        sfc_success = "SFC scan completed successfully."
        return sfc_success, stdout, stderr
    else:
        sfc_success = False
        if "Windows Resource Protection found corrupt files and successfully repaired them" in stderr.decode():
            sfc_code = 1
        elif "Windows Resource Protection did not find any integrity violations" in stderr.decode():
            sfc_code = 0
        elif "Windows Resource Protection found corrupt files but was unable to fix some of them" in stderr.decode():
            sfc_code = 2
        elif "Windows Resource Protection could not perform the requested operation" in stderr.decode():
            sfc_code = 3
        elif "Windows Resource Protection could not start the repair service" in stderr.decode():
            sfc_code = 4
        else:
            sfc_success = False
            sfc_code = -1

sfc()
print(sfc_success, sfc_code)