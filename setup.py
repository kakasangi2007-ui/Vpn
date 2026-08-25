"""
Setup script for VPN Application
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="vpn-app",
    version="1.0.0",
    author="VPN App Team",
    author_email="support@vpn-app.com",
    description="Professional VPN Client with Xray-core and Flet",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/vpn-app/vpn-app",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.10",
    install_requires=[
        "flet>=0.20.0",
        "requests>=2.31.0",
        "python-dotenv>=1.0.0",
        "psutil>=5.9.0",
    ],
    entry_points={
        "console_scripts": [
            "vpn-app=vpn:main",
        ],
    },
    include_package_data=True,
    package_data={
        "": ["core/windows/*", "assets/*", "config/*"],
    },
)
