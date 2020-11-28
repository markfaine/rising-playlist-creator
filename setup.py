from setuptools import setup, find_namespace_packages

setup(name='rising-playlist-creator',
      version="1.0.0",
      description='Rising Playlist Creator',
      author='Mark Faine',
      author_email='mark.faine@gmail.com',
      url='https://github.com/markfaine/rising-playlist-creator',
      packages=find_namespace_packages(include=['net.*']),
      zip_safe=False,
      entry_points={
          "console_scripts": [
             "rising-playlist-creator = net.markfaine.rising:main",
          ]
      },
      install_requires=[
          'python-dateutil',
          'praw',
          'autoclass',
          'pyfields',
          'argparse',
          'google-api-python-client',
          'google-auth-httplib2',
          'google-auth-oauthlib',
      ],
      setup_requires=['pytest-runner', 'flake8'],
      tests_require=['pytest'],
      classifiers=[
          "Programming Language :: Python :: 3",
          "License :: GNU GPL3 License",
          "Operating System :: Linux",
      ],
      python_requires='>=3.8',
      )

