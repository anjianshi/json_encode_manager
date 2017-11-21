from setuptools import setup
import json_encode_manager

setup(
    name='json_encode_manager',
    version=json_encode_manager.__version__,
    url='https://github.com/anjianshi/json_encode_manager',
    license='MIT',
    author='anjianshi',
    author_email='anjianshi@gmail.com',
    description="JSON encode helper",
    py_modules=["json_encode_manager"],
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
    ],
)
