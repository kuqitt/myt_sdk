from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="myt-sdk",
    version="1.0.0",
    author="MYT Team",
    author_email="kuqitt1@163.com",
    maintainer="MYT Team",
    maintainer_email="kuqitt1@163.com",
    description="MYT SDK - 魔云腾SDK通用包，用于自动下载、管理和启动MYT SDK，支持完整的API客户端功能",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/kuqitt/myt_sdk",
    download_url="https://github.com/kuqitt/myt_sdk/archive/v1.0.0.tar.gz",
    project_urls={
        "Bug Reports": "https://github.com/kuqitt/myt_sdk/issues",
        "Source": "https://github.com/kuqitt/myt_sdk",
        "Documentation": "https://github.com/kuqitt/myt_sdk/blob/main/README.md",
        "Changelog": "https://github.com/kuqitt/myt_sdk/blob/main/CHANGELOG.md",
        "API Documentation": "https://github.com/kuqitt/myt_sdk/tree/main/docs",
        "Examples": "https://github.com/kuqitt/myt_sdk/tree/main/examples",
    },
    packages=find_packages(exclude=["tests*", "docs*", "examples*"]),
    package_data={
        "py_myt": ["*.txt", "*.md"],
    },
    include_package_data=True,
    keywords=[
        "myt", "sdk", "automation", "android", "container", "api", "client",
        "device", "management", "camera", "sensor", "location", "proxy",
        "video", "streaming", "rtmp", "webrtc", "monitoring", "github"
    ],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: POSIX :: Linux",
        "Operating System :: MacOS :: MacOS X",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3 :: Only",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: System :: Systems Administration",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
        "Topic :: Multimedia :: Video",
        "Topic :: Scientific/Engineering :: Interface Engine/Protocol Translator",
        "Environment :: Console",
        "Natural Language :: Chinese (Simplified)",
        "Natural Language :: English",
    ],
    python_requires=">=3.7",
    install_requires=requirements,
    extras_require={
        "dev": [
            "pytest>=6.0",
            "pytest-cov>=2.0",
            "black>=21.0",
            "flake8>=3.8",
            "mypy>=0.800",
            "twine>=3.0",
            "wheel>=0.36",
            "setuptools>=45.0",
        ],
        "monitoring": [
            "matplotlib>=3.0",
            "pandas>=1.0",
        ],
        "docs": [
            "sphinx>=3.0",
            "sphinx-rtd-theme>=0.5",
        ],
        "all": [
            "pytest>=6.0",
            "pytest-cov>=2.0",
            "black>=21.0",
            "flake8>=3.8",
            "mypy>=0.800",
            "twine>=3.0",
            "wheel>=0.36",
            "setuptools>=45.0",
            "matplotlib>=3.0",
            "pandas>=1.0",
            "sphinx>=3.0",
            "sphinx-rtd-theme>=0.5",
        ],
    },
    entry_points={
        "console_scripts": [
            "myt-sdk=py_myt.cli:main",
        ],
    },
    zip_safe=False,
    platforms=["Windows"],
)