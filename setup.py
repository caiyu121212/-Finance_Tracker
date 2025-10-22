from setuptools import setup,find_packages

setup(
    name="finance_tracker",
    version="1.0.0",
    description="个人记账系统",
    author="caiyu",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "python-dateutil>=2.8.2"
        "openpyxl>=3.0.10",
    ],
    python_requires=">=3.8",
)