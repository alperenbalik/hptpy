from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(name='hptpy',
      version='0.0.2',
      packages=["hptpy", "hptpy.midcal"],
      author="Alperen Balık",
      author_email="alperenbalik@outlook.com",
      description="Hypothesis Testing Python Library",
      long_description=long_description,
      long_description_content_type="text/markdown",
      url="https://github.com/alperenbalik/hptpy",
      install_requires=['scipy>=0.9.0',
                        'numpy==1.15.4',
                        'statsmodels>=0.9.0']
      )
