from setuptools import find_packages, setup

setup(
    name='mcqgenerator',
    version='0.0.2',
    author='sridhana ankathi',
    author_email='sridhanaankathi2003@gmail.com',
    install_requires=[
    "langchain",
    "langchain-huggingface",
    "python-dotenv",
    "pandas",
    "huggingface_hub",
    "ipywidgets"  # only if needed
],
    packages=find_packages(),
)
