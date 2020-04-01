import setuptools

name = "moldynquick"
version = "0.1.0"

with open("README.md", "r") as f:
    long_description = f.read()

setuptools.setup(
    name=name,
    version=version,
    author="Alicia Key",
    author_email="confidential@confidential.com",
    description="Tools for analyzing NAMD runs",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=["moldynquick"],
    install_requires=[
        "pandas",
        "numpy",
        "pytest",
        "mypy",
        "mdanalysis",
        "openpyxl"
    ]
)
