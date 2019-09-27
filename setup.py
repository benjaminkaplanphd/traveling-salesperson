import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="traveling-salesperson",
    version="0.0.1",
    author="Benjamin Eric Kaplan",
    author_email="",
    description="Python package for efficiently solving the classic traveling salesperson problem",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/benjaminkaplanphd/traveling-salesperson",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)