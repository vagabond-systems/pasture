from setuptools import setup

with open("../../version.txt", "r") as f:
    version_number = f.read().strip()

installation_requirements = [
    "requests==2.31.0",
]

test_requirements = [

]

setup(
    name="flockmate",
    description="tend your flock",
    version=version_number,
    url="https://github.com/vagabond-systems/pasture",
    author="(~)",
    package_dir={"": "packages"},
    packages=["flockmate"],
    install_requires=installation_requirements,
    tests_require=test_requirements,
)
