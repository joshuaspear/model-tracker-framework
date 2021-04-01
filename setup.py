from distutils.core import setup
import pathlib
import setuptools


HERE = pathlib.Path(__file__).parent

README = (HERE / "README.md").read_text()

setuptools.setup(
    name='model_tracker_framework',
    version='1.0.5',
    description="An object-orientated framework for tracking machine learning projects.",
    long_description=README,
    packages=setuptools.find_packages(where="src"),
    author="Joshua Spear",
    author_email="josh.spear9@gmail.com",
    long_description_content_type="text/markdown",
    url="https://gitlab.com/kaggle-tings/mtf",
    license='MIT',
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Development Status :: 4 - Beta"
    ],
    package_dir={"": "src"},
    python_requires=">=3.6",
    install_requires=["pandas>=1.2.3"]
)