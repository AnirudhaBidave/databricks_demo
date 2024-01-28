from setuptools import setup, find_packages
import src

setup(
  name = "azure_rest",
  version = "0.0.1",
  author = "anirudhabidave",
  author_email = "bidaveanirudha@gmail.com",
  description = "This package hepls you to generate metrics cost and resource usage on Microsoft Azure",
  packages=find_packages(where='./src'),
  package_dir={'': 'src'},
  entry_points={
    "packages": [
      "main=azure_rest.main:main"
    ]
  },
  license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.10",
        "Operating System :: OS Independent",
    ],
    install_requires=["setuptools", "bson >= 0.5.10", "requests>=2.30.0", "datetime>=5.0", "uuid>=1.30", "pandas>=2.0.0"],
    extras_require={
        "dev": ["pytest>=7.0", "twine>=4.0.2"],
    },
    python_requires=">=3.8",
)