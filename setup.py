from setuptools import setup

def readme():
    with open('README.md.md') as f:
        return f.read()

setup(
    name="juju-remove",
    version="0.1",
    description="Juju plugin to simplify removing things that have been added to a Juju model.",
    author="Tim McNamara",
    author_email="paperless@timmcnamara.co.nz",
    url="https://github.com/timClicks/juju-remove",
    license="Apache 2",
    py_modules=[
        'juju_remove',
    ],
    entry_points={
        'console_scripts': [
            'juju-remove = juju_remove:main',
        ]
    },
    requires=[
        'juju',
    ],
    install_requires=[
        'juju'
    ],
    extras_require={
        'dev': [
            'black'
        ]
    },
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Environment :: Plugins',
        'License :: OSI Approved :: Apache Software License',
        'Framework :: Juju',
    ],
    python_requires=">= 3.6",
)

