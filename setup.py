from setuptools import setup, find_packages

setup(
    name="ff_like_api",
    version="1.0.0",
    packages=find_packages(),
    description="Free Fire Custom Like API Library - One command setup",
    author="ZEXXY",
    install_requires=[
        "Flask>=2.0.0",
        "requests>=2.25.0",
        "aiohttp>=3.7.0",
        "pycryptodome>=3.10.0",
        "protobuf>=3.20.0",
        "Werkzeug>=2.0.0",
    ],
    entry_points={
        "console_scripts": [
            "ff-like-server=ff_like_api.server:start_server",
        ],
    },
    python_requires=">=3.7",
)