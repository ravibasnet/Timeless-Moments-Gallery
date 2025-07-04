from setuptools import setup, find_packages

setup(
    name="timeless_moments",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        'django',
        'crispy-forms',
        'crispy-bootstrap5',
        'whitenoise',
    ],
) 