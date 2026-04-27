from setuptools import setup, find_packages
import os

with open(os.path.join(os.path.dirname(__file__), 'README.md'), 'r', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='ucs-optimizer',
    version='1.0.0',
    description='水泥强度预测和环境影响评估工具',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Your Name',
    author_email='your.email@example.com',
    url='https://github.com/yourusername/ucs-optimizer',
    packages=find_packages(),
    include_package_data=True,
    package_data={
        'ucs_optimizer': ['data/*', 'config/*'],
    },
    entry_points={
        'console_scripts': [
            'ucs-optimizer=ucs_optimizer.cli.main:main',
        ],
    },
    install_requires=[
        'pandas>=1.3.0',
        'numpy>=1.20.0',
        'scikit-learn>=0.24.0',
        'matplotlib>=3.4.0',
        'joblib>=1.0.0',
        'openpyxl>=3.0.0',
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)