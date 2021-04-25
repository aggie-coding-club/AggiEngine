from distutils.core import setup
setup(
  name = 'AggiEngine',
  packages = ['AggiEngine'],
  version = '0.1',
  license='MIT',
  description = 'A game engine written in python',
  author = 'Brady Langdale, Nurivan Gomez',
  author_email = 'bradylangdale@tamu.edu, nurivan@tamu.edu',
  url = 'https://github.com/aggie-coding-club/AggiEngine/',
  download_url = 'https://github.com/aggie-coding-club/AggiEngine/archive/refs/tags/0.1.tar.gz',
  keywords = ['Python', 'Game Engine'],
  install_requires=[
        'PySide2',
        'PyOpenGL',
        'Box2D',
        'pytmx',
        'pillow',
        'numpy',
        'simpleaudio'
    ],
  classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
)