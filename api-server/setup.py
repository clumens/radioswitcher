from setuptools import find_packages, setup

setup(name="switchapi",
      version="0.1.0",
      packages=find_packages(),
      install_requires=["Adafruit_BBIO", "flask", "flask-basicauth"])
