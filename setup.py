from setuptools import setup, find_packages

with open("README.md", mode="r", encoding="utf-8") as f:
    readme = f.read()

test_requirements = ["pytest>=4.0.0", "codecov", "pytest-cov"]
required = ["python_jwt", "jwcrypto"]

setup(
    name="labelbot",
    version="0.0.1",
    description=(
        "A GitHub label bot for allowing unprivileged users to label issues "
        "with allowed labels."
    ),
    long_description=readme,
    long_description_content_type="text/markdown",
    author="Joakim Croona, Simon Larsén",
    author_email="jcroona@kth.se, slarse@kth.se",
    license="MIT",
    packages=find_packages(exclude=("tests", "docs")),
    install_requires=required,
    tests_require=test_requirements,
    extras_require=dict(TEST=test_requirements),
    python_requires=">=3.7",
)
