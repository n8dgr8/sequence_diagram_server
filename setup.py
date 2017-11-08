from setuptools import setup

setup(
    name='Sequence Diagram Server',
    version='1.0',
    long_description=__doc__,
    packages=[],
    include_package_data=True,
    zip_safe=False,
    install_requires=['Flask'],
    entry_points={
        'flask.commands': [
          'assets = flask_assets:assets',
        ],
    },
)


