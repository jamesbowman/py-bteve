from distutils.core import setup

for l in open("bteve/__init__.py", "rt"):
    if l.startswith("__version__"):
        exec(l)

setup(name='bteve',
      version=__version__,
      author='James Bowman',
      author_email='jamesb@excamera.com',
      url='http://gameduino.com',
      description='Interface to the Bridgetek EVE embedded GPUs',
      long_description='Interface to the Bridgetek EVE embedded GPUs, as used in the Gameduino and Gameduino Dazzler',
      license='GPL',
      packages=['bteve'],
      install_requires=[],
      project_urls={
        'Documentation': 'https://bteve.readthedocs.io/en/latest/',
      }
)
