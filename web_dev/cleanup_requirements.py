import subprocess

# Read the original requirements.txt
with open('requirements.txt', 'r') as file:
    lines = file.readlines()

clean_lines = []
for line in lines:
    # Ignore local paths like `file:///` and fetch from PyPI
    if "@" in line:
        package_name = line.split()[0]  # Extract package name (e.g., 'altair')
        version = subprocess.check_output([f"pip show {package_name}"], shell=True).decode().split('\n')[1].split(':')[1].strip()
        clean_lines.append(f"{package_name}=={version}\n")
    else:
        clean_lines.append(line)

# Write the cleaned lines back to requirements.txt
with open('requirements.txt', 'w') as file:
    file.writelines(clean_lines)

