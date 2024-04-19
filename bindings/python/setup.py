from setuptools import setup

installation_requirements = [
    "requests==2.31.0",
    "user-agent==0.1.10"
]

test_requirements = [
    "pytest==8.1.1"
]

setup(
    name="underhill",
    description="You draw far too much attention to yourself, Mr. Underhill.",
    version="0.4",
    url="https://github.com/vagabond-systems/underhill",
    author="(~)",
    package_dir={"": "packages"},
    packages=["underhill"],
    install_requires=installation_requirements,
    tests_require=test_requirements,
)
