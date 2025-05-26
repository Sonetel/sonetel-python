from setuptools import setup

setup(
    name="sonetel",
    version="0.3.0",
    packages=["sonetel"],
    url="https://github.com/Sonetel/sonetel-python",
    license="MIT",
    author="aashish",
    author_email="dev.support@sonetel.com",
    description="A simple python wrapper for using Sonetel's REST APIs",
    install_requires=[
        "requests>=2.25.0",
        "PyJWT>=2.0.0",
    ],
    python_requires=">=3.6",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
)
