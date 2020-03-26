from setuptools import setup, find_packages

setup(name='google-model',
          version='0.0.1',
          description='Modelo de la plataforma de google',
          url='https://github.com/pablodanielrey/google-model',
          author='Desarrollo DiTeSi, FCE',
          author_email='ditesi@econo.unlp.edu.ar',
          classifiers=[
            #   3 - Alpha
            #   4 - Beta
            #   5 - Production/Stable
            'Development Status :: 3 - Alpha',
            'Programming Language :: Python :: 3',
            'Programming Language :: Python :: 3.5'
          ],
          packages=find_packages(exclude=['contrib', 'docs', 'test*']),
          install_requires=[
                            'dateutils',
                            'requests',
                            'pytz',
                            'pulsar-client',
                            'psycopg2-binary',
                            'SQLAlchemy'
                            ],
          entry_points={
            'console_scripts': [
            ]
          }
      )
