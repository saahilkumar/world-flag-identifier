from setuptools import setup, find_packages

def readme():
    with open("README.md") as f:
        return f.read()

setup(
    name = "flagpy",
    version = "1.0.2",
    description = "Country Flag Classifier.",
    long_description = readme(),
    long_description_content_type = "text/markdown",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3"
    ],
    url = "https://github.com/saahilkumar/world-flag-identifier",
    author = "Saahil Kumar",
    author_email = "kumar.saa@northeastern.edu",
    license = "MIT",
    packages = ["flagpy"],
    package_data = {"": ["flag_df.csv", "flags/*.pkl"]},
    include_package_data = True,
    install_requires = [
        "Pillow", 
        "requests",
        "numpy",
        "pandas",
        "ImageHash",
        "scikit-image"
    ]
)