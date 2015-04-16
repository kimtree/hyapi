# -*- coding: utf-8 -*-


from setuptools import setup

setup(name='hyapi',
      version='0.0.1',
      description='Python SDK for Hanyang Univ API',
      url='http://github.com/kimtree/hyapi',
      author='Namwoo Kim',
      author_email='kimtree@hanyang.ac.kr',
      license='MIT',
      packages=['hyapi'],
      zip_safe=False,
      install_requires=[
        'pycrypto==2.6.1',
        'requests==2.6.0'
      ],
      keywords='hanyang university',
      classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Topic :: Software Development :: Libraries',
        'Operating System :: OS Independent',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7'
      ])
