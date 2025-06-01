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
    global sfc_success, sfc_code, returncode, elevation_required, sfc_output, sfc_error
    stdout, stderr, returncode = run_command("sfc /scannow")
    output = stdout.decode('utf-8')
    print(output)
    output_stripped = output.strip().lower()
    print(output_stripped)
    if "windows resource protection did not find any integrity violations" in output_stripped:
        sfc_code = 0
    elif "windows resource protection found corrupt files and successfully repaired them" in output_stripped:
        sfc_code = 1
    elif "windows resource protection found corrupt files but was unable to fix some of them" in output_stripped:
        sfc_code = 2
    elif "windows resource protection could not perform the requested operation" in output_stripped:
        sfc_code = 3
    elif "windows resource protection could not start the repair service" in output_stripped:
        sfc_code = 4
    elif "you must be an administrator" in output_stripped:
        elevation_required = True
        sfc_code = 5
    else:
        sfc_success = False
        sfc_code = -1

sfc()
print(sfc_success, sfc_code)