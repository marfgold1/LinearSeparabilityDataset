from setuptools import find_packages, setup

setup(
    name='myConvexHull',
    version='1.0.0',
    author='Amar Fadil',
    author_email='13520103@std.stei.itb.ac.id',
    description=' '.join([
        'Custom convex hull algorithm for 2D points',
        'using Decrease and Conquer strategy.',
    ]),
    url='https://github.com/marfgold1/stima-tucil2',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'matplotlib',
        'pandas',
        'numpy',
    ],
    extras_require={
        'datasets': [
            'scikit-learn'
        ],
        'tests': [
            'scipy',
            'scikit-learn'
        ],
    },
    python_requires='>=3.7',
)