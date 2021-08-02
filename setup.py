from setuptools import setup, find_packages


def get_version_and_cmdclass(package_path):
    """Load version.py module without importing the whole package.
    Template code from miniver
    """
    import os
    from importlib.util import module_from_spec, spec_from_file_location

    spec = spec_from_file_location(
        "version", os.path.join(package_path, "_clean_version.py")
    )
    module = module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.__version__, module.cmdclass


version, cmdclass = get_version_and_cmdclass("e2elink")

with open("README.md", "r", encoding="utf8") as fh:
    long_description = fh.read()

with open("requirements.txt") as f:
    install_requires = f.read().splitlines()

with open("requirements_extra.txt") as f:
    install_requires_extra = f.read().splitlines()
    extras_require = {"dev": install_requires_extra}

setup(
    name="e2elink",
    version=version,
    cmdclass=cmdclass,
    author="Mwansa Lumpa, Miquel Duran-Frigola",
    author_email="mwansa.lumpa@cidrz.org, miquel@ersilia.io",
    url="https://github.com/ersilia-os/e2elink",
    description="End-to-end record linkage aided by machine learning",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="MIT",
    python_requires=">=3.7",
    install_requires=install_requires,
    extras_require=extras_require,
    packages=find_packages(exclude=("utilities")),
    entry_points={"console_scripts": ["e2elink=e2elink.cli:cli"]},
    classifiers=(
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ),
    keywords="record-linkage machine-learning medical-informatics",
    project_urls={"Source Code": "https://github.com/ersilia-os/e2elink/",},
    include_package_data=True,
    package_data={"": ["example/files/*.csv"]},
)
