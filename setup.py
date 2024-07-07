from setuptools import setup, find_packages

setup(
    name="juba0x00-flagger",
    version="2.1",
    author="juba0x00",
    description="Python tool automating flag searches using various methods, enhancing CTF challenge solving efficiency",
    packages=find_packages(),
    # package_data={'': ['data/*'], },
    # include_package_data=True,
    zip_safe=False,
    install_requires=["base45", "pillow", "colorama", "Requests"],
    entry_points={"console_scripts": ["flagger=flagger.__init__:main"]},
)