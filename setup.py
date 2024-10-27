from setuptools import setup, find_packages

# Read the version from the version file
version = {}
with open("REMG/__version__.py") as fp:
    exec(fp.read(), version)

setup(
    name="rheo",
    version=version['version'],
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "numpy",
        "pandas",
        "matplotlib",
        "ipympl",
        "pyserial"
        # Add your project dependencies here
    ],
    entry_points={
        'console_scripts': [
            # Add your console scripts here
        ],
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.8',
)
