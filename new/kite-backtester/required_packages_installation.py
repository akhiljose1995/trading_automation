import subprocess
import sys

def install(package):
    print(f"\n# Installing: {package}")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        #subprocess.check_call([sys.executable, "pip", "install", "pip-", package])
        print(f"# Successfully installed {package}")
    except subprocess.CalledProcessError as e:
        print(f"# Failed to install {package}: {e}")

if __name__ == "__main__":
    packages = [
        "kiteconnect",
        "pandas",
        "matplotlib",
        "pytest"
    ]

    for pkg in packages:
        install(pkg)
