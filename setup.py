from setuptools import setup, find_packages

VERSION = '0.1.0' 
DESCRIPTION = 'PgzAnimation - Create video animations using Pygame Zero and OOP'
LONG_DESCRIPTION = 'PgzAnimation - Create video animations using Pygame Zero and OOP. Object oriented animations with built-in tween methos.'

# Setting up
setup(
       # the name must match the folder name 'verysimplemodule'
        name="pgzanimation", 
        version=VERSION,
        author="Stewart Watkiss",
        author_email="pgzanimation@watkissonline.co.uk",
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        packages=find_packages(),
        install_requires=[], # add any additional packages that 
        # needs to be installed along with your package. Eg: 'caer'
        
        keywords=['python', 'first package'],
        classifiers= [
            "Development Status :: 3 - Alpha",
            "Intended Audience :: Education",
            "Programming Language :: Python :: 3",
            "Operating System :: Linux :: Linux",
        ]
)