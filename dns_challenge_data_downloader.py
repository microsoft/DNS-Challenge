import subprocess

azcopyexe = r"<Insert your path to azcopy.exe>"
#azcopyexe = r"C:\Users\chkarada\Downloads\Softwares\azcopy_windows_amd64_10.8.0\azcopy.exe"

# For wideband data - Uncomment the below line and comment line 10 if you want wideband data
SAS_URL = "<Send an email to dns_challenge@microsoft.com for the SAS URL >"

# Insert the path to your local directory where you want to save the data
local_dir = r"<Insert your path to the destination directory>"
#local_dir = r"C:\Downloads\"

command_azcopy = "{0} cp {1} {2} --recursive".format(azcopyexe, SAS_URL, local_dir)
subprocess.call(command_azcopy)