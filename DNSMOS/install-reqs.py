import subprocess
# The script reads the requirements.txt file and installs all the packages listed in it using pip.
# If any package fails to install, it will print an error message and continue with the next package.
# Open the requirements.txt file and read all lines
with open('requirements.txt', 'r') as file:
    packages = file.readlines()

failed_packages = []  # List to store the packages that failed to install
# Iterate over each package and install it using pip
for package in packages:
    package = package.strip()  # Remove any leading/trailing whitespace
    if package:  # Check if the package name is not empty
        try:
            subprocess.run(['pip', 'install', package], check=True)  # Run the command and check for errors, if any error occurs, it will raise an exception
        except subprocess.CalledProcessError as e:
            print(f"Error while installing {package}: {e}")
            failed_packages.append(package)  # Add the package to the failed_packages list
# Print the list of packages that failed to install
if failed_packages:
    # Print the list of packages that failed to install
    # Print dashed lines to separate the failed packages from the success message
    print("-" * 50)
    print("Failed to install the following packages:")
    for package in failed_packages:
        print(package)
else:
    print("All packages installed successfully!")  # Print a success message if all packages were installed successfully