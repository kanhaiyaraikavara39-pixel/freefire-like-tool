from setuptools import setup, find_packages

setup(
    name="ff_like_api",
    version="0.1.0",
    packages=find_packages(),
    description="Free Fire Custom Like API Library",
    author="ZEXXY (Your Name)",
    install_requires=[
        "Flask",
        "requests",
        "aiohttp",
        "pycryptodome",
        "protobuf",
        "Werkzeug"
    ],
)
