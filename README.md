## `juju-remove`

A Juju plugin to make it easier to remove things from a model.


## Usage

```shell script
juju remove <modelled-entity>
``` 

Once installed, you can execute `juju-remove` as a Juju plugin, where `<modelled-entity>` accepts 
the name of a machine, unit, relation, or application. You can also execute  `juju-remove` directly:

```shell script
juju-remove <modelled-entity>
``` 


## Installation

> `juju-remove` is currently in a beta state. Once it has seen some usage, installation will be simplified.

Start by ensuring that you have `git` and Python 3 installed.

Retrieve the package and install it:

```shell script
git clone https://github.com/timClicks/juju-develop.git
cd juju-develop 
python3 -m pip install .
```

A new script, `juju-remove`, has just been added to your `PATH`. Congrats.


### Verify installation

To check that you've installed things correctly, try running it with `--help`:

```shell script
juju remove --help
```


## Asking for help

If you encounter any problems, please add a question in the [Juju Discourse forum](https://discourse.jujucharms.com/).


## Development

All contributions are welcome! For code contributions, you should install:

- [`just`](https://github.com/casey/just)
- GNU `make`*
- GNU `sed`*

To set up your system, create a virtual environment.

```shell script
python3 -m venv /path/to/new-env
source /path/to/new-env/bin/activate
```

You should now edit the `.env`

Get your hands on the source:

```shell script
git clone https://github.com/timClicks/juju-develop.git
cd juju-develop
```

You should now edit the `.env` file to update the `VENV` variable. This will help later on when
you need to keep the `requirements.txt` file up to date.

To install of the dependencies and to install `juju-develop` in developer mode with the right interpreter, use `just`:

```shell script
just develop
```


 


