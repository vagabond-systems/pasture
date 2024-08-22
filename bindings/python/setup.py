from setuptools import setup

installation_requirements = [
    "requests==2.31.0",
]

test_requirements = [

]

setup(
    name="flockmate",
    description="tend your flock",
    version="0.8",
    url="https://github.com/vagabond-systems/pasture",
    author="(~)",
    package_dir={"": "packages"},
    packages=["flockmate"],
    install_requires=installation_requirements,
    tests_require=test_requirements,
)
