from distutils.core import setup

setup(
    name="cosmoplots",
    version="0.1.4",
    description="Definitions for figures and plots using matplotlib",
    author="Gregor Decristoforo",
    author_email="gregor.decristoforo@uit.no",
    url="https://github.com/uit-cosmo/cosmoplots",
    packages=["cosmoplots"],
    license="MiT",
    install_requires=["numpy>=1.15.0", "matplotlib>=3.3.2"],
    classifiers=[
        "Intended Audience :: Education",
        "Intended Audience :: Science/Research",
        "License :: MIT License",
        "Programming Language :: Python :: 3 :: Only",
        "Topic :: Scientific/Engineering :: Visualization",
    ],
    zip_safe=False,
)
