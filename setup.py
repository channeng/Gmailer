from setuptools import setup, find_packages


classifiers = [
    # How mature is this project? Common values are
    #   3 - Alpha
    #   4 - Beta
    #   5 - Production/Stable
    'Development Status :: 3 - Alpha',

    # Indicate who your project is intended for
    'Intended Audience :: Developers',
    'Intended Audience :: Information Technology',
    'Intended Audience :: End Users/Desktop',
    'Intended Audience :: Financial and Insurance Industry',
    'Intended Audience :: Other Audience',

    'Topic :: Software Development :: Build Tools',

    # Pick your license as you wish (should match "license" above)
    'License :: OSI Approved :: MIT License',

    'Natural Language :: English',

    # Specify the Python versions you support here. In particular, ensure
    # that you indicate whether you support Python 2, Python 3 or both.
    'Programming Language :: Python :: 2.7',
    # Topic
    'Topic :: Communications :: Email',
    'Topic :: Utilities'
]

keywords = ['gmail', 'reports', 'email', 'email tables', 'analytics', 'report', 'BI', 'Business Intelligence']

setup(name='gmailer_report',
      version='0.1a3',
      description='Gmailer_report simplifies the dispatch of standard html email reports that includes tabular data from Gmail.',
      url='https://github.com/channeng/Gmailer',
      author='Shannon Chan',
      author_email='channeng@hotmail.com',
      license='MIT',
      packages=["gmailer_report"] + ["gmailer_report." + package for package in find_packages('gmailer_report')],
      include_package_data=True,  # To include templates/email.html
      classifiers=classifiers,
      keywords=keywords,
      zip_safe=False)
