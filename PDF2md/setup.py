from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="pdf-to-markdown-converter",
    version="0.1.0",
    author="Henrique A de Mesquita",
    author_email="eng.henrique.a.mesquita@gmail.com",
    description="Conversor de PDF para Markdown com barra de progresso",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/mablemb/pdf-to-markdown-converter",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=[
        "pymupdf4llm",
        "tqdm",
    ],
    entry_points={
        "console_scripts": [
            "pdf-to-markdown=pdf_to_markdown.cli:main",
        ],
    },
)