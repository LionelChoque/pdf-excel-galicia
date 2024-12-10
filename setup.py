from setuptools import setup, find_packages

setup(
    name="pdf_bank_extractor",
    version="1.0.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "pdfplumber>=0.10.2",
        "pandas>=2.1.1",
    ],
    entry_points={
        'console_scripts': [
            'pdf_extractor=pdf_bank_extractor.pdf_extractor:run',
        ],
    },
    author="Alan Choque",
    author_email="lionelchoque@gmail.com",
    description="Extractor de datos bancarios desde PDF",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    keywords="pdf, bank, extract, data, Galicia",
    url="https://github.com/LionelChoque/pdf-excel-galicia.git",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.11",
)