

from setuptools import find_packages, setup

setup(
    name='nasapy',
    version='0.2.6',
    author='Aaron Schlegel',
    author_email='aaron@aaronschlegel.me',
    description='Python wrapper for the NASA API',
    packages=find_packages(exclude=['docs', 'notebooks', 'tests*']),
    include_package_data=True,
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    install_requires=['requests >= 2.18'],
    home_page='',
    classifiers=[
        'Environment :: Console',
        'Intended Audience :: End Users/Desktop',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)
