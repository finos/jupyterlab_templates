from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='jupyterlab_templates',
    version='0.0.6',
    description='Templates for notebooks in JupyterLab',
    long_description=long_description,
    url='https://github.com/timkpaine/jupyterlab_templates',
    download_url='https://github.com/timkpaine/jupyterlab_templates/archive/v0.0.6.tar.gz',
    author='Tim Paine',
    author_email='t.paine154@gmail.com',
    license='Apache 2.0',

    classifiers=[
        'Development Status :: 3 - Alpha',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],

    keywords='jupyter jupyterlab',

    packages=find_packages(exclude=['tests', ]),
    package_data={'jupyterlab_templates': ['jupyterlab_templates/templates/*']},
    include_package_data=True,
    data_files=[('', ["LICENSE", "README.md"])],
    zip_safe=False,

    # entry_points={
    #     'console_scripts': [
    #         'sample=sample:main',
    #     ],
    # },
)
