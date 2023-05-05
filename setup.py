from setuptools import setup, find_packages
import pathlib

# Get the README.md content
here = pathlib.Path(__file__).parent.resolve()
long_description = (here / "README.md").read_text(encoding="utf-8")

setup(
    name="canvas-pilot",
    version="0.1.2",
    packages=find_packages(),
    install_requires=[
        "requests",
        "icalendar",
        "click",
    ],
    entry_points={
        "console_scripts": [
            "canvas=canvas_tools.canvas:main",
        ],
    },
    author="Ziang Zhou",
    author_email="ziang.zhou518@gmail.com",
    description="A command-line tool for managing Canvas courses, fetching assignments, and grades.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="GPLv3+",
    keywords="canvas api cli",
    url="https://github.com/realzza/canvas-cli",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Education",
        "License :: OSI Approved :: GNU General Public License v3 or later",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    python_requires=">=3.6, <4",
)

