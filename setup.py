"""
python3 setup.py sdist bdist_wheel
python -m twine upload dist/*
"""
import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="dori-orm",
    version="4.6.1",
    author="Mohammad Dori",
    author_email="mr.dori.dev@gmail.com",
    description="simple orm, to manage your database.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/dori-dev/my-orm",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=setuptools.find_packages(),
    install_requires=[],
    python_requires=">=3.6",
)
