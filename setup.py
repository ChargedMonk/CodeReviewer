from setuptools import setup, find_packages

setup(
    name="code-reviewer",
    version="0.1.0",
    description="AI-based local code reviewer that runs on every git commit.",
    author="Vatsalya Bajpai",
    author_email="vatsalyabajpai03@example.com",
    url="https://github.com/ChargedMonk/CodeReviewer",
    packages=find_packages(),
    include_package_data=True,
    install_requires=["llama-cpp-python==0.3.8", "gdown==5.2.0"],
    entry_points={
        "console_scripts": [
            "code-reviewer=code_reviewer.main:main"
        ]
    },
    package_data={
        "": ["../hooks/pre-commit"]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
)
