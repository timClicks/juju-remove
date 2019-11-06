#! /usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright 2019 Fiorenza Limited
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import argparse
import re
import sys
from functools import partial
from typing import Optional, Tuple

from juju.controller import Controller
from juju.model import Model
from juju import loop

__doc__ = """
Removes entities from a Juju model, without needing to remember which specific command to use.
Supports applications, machines, relations, and units.
"""

# these patterns are less strict, but much more readable
# than those provided in the http://github.com.juju/names package
APPLICATION_SNIPPET = "[a-z][a-z0-9-_]*"
UNIT_SNIPPET = APPLICATION_SNIPPET + "/\d+"
RELATION_IMPLICIT_SNIPPET = f"{APPLICATION_SNIPPET} {APPLICATION_SNIPPET}"
RELATION_ENDPOINT_LEFT_SNIPPET = (
    f"{APPLICATION_SNIPPET}:{APPLICATION_SNIPPET} {APPLICATION_SNIPPET}"
)
RELATION_ENDPOINT_RIGHT_SNIPPET = (
    f"{APPLICATION_SNIPPET} {APPLICATION_SNIPPET}:{APPLICATION_SNIPPET}"
)
RELATION_EXPLICIT_SNIPPET = f"{APPLICATION_SNIPPET}:{APPLICATION_SNIPPET} {APPLICATION_SNIPPET}:{APPLICATION_SNIPPET}"

APPLICATION_PATTERN = re.compile(f"^{APPLICATION_SNIPPET}$")
UNIT_PATTERN = re.compile(f"^{UNIT_SNIPPET}$")
RELATION_PATTERNS = [
    re.compile(f"^{RELATION_IMPLICIT_SNIPPET}$"),
    re.compile(f"^{RELATION_ENDPOINT_LEFT_SNIPPET}$"),
    re.compile(f"^{RELATION_ENDPOINT_RIGHT_SNIPPET}$"),
    re.compile(f"^{RELATION_EXPLICIT_SNIPPET}$"),
]


def _matcher(pattern):
    def predicate(name: str) -> bool:
        return bool(re.match(pattern, name))

    return predicate


def looks_like_application(name: str, pattern=APPLICATION_PATTERN) -> bool:
    return _matcher(pattern)(name)


def looks_like_unit(name: str, pattern=UNIT_PATTERN) -> bool:
    # TODO: units that are inside containers
    return _matcher(pattern)(name)


def looks_like_machine(name: str) -> bool:
    # TODO: instance ids
    return name.isdigit()


def looks_like_relation(name: str, patterns=RELATION_PATTERNS) -> bool:
    for pattern in patterns:
        if _matcher(pattern)(name):
            return True
    return False


async def connect(
    controller_name: Optional[str] = None, model_name: Optional[str] = None
) -> Tuple[Controller, Model]:
    c = Controller()
    await c.connect(controller_name=controller_name)
    m = Model()
    await m.connect(model_name=model_name)
    return c, m


async def is_machine(entity: str, model: Optional[Model] = None):
    if not looks_like_machine(entity):
        return None

    if model is None:
        _, model = await connect()

    return entity in model.machines.keys()


async def is_relation(entity, model=None):
    if not looks_like_relation(entity):
        return None


log = partial(print, file=sys.stderr)


def report_finding(entity, controller, model, entity_type, verbose=False):
    if verbose:
        log(
            f'[i] interpreting "{entity}" as a {entity_type} on {controller.controller_name}:{model.model_name}'
        )


async def _main(args):
    if args.v:
        controller_pseduo_name = args.controller or "<current>"
        model_pseduo_name = args.model or "<current>"
        log(
            f"connecting to model {model_pseduo_name} on controller {controller_pseduo_name}"
        )
    controller, model = await connect(args.controller, args.model)
    reporter = partial(report_finding, args.entity, controller, model, verbose=args.v)
    if looks_like_machine(args.entity):
        reporter("machine")
        live_entities = model.machines
    elif looks_like_unit(args.entity):
        reporter("unit")
        live_entities = model.units
    elif looks_like_application(args.entity):
        reporter("application")
        live_entities = model.applications
    elif looks_like_relation(args.entity):
        reporter("relation")
        live_entities = {}
        for relation in model.relations:
            if relation.matches(args.entity):
                live_entities[args.entity] = relation
                break

    try:
        entity = live_entities[args.entity]
    except LookupError:
        log(f"{args.entity} not found")
    else:
        await entity.destroy(force=True)

    await model.disconnect()


def main():
    parser = argparse.ArgumentParser("juju remove", description=__doc__)

    parser.add_argument(
        "-c",
        "--controller",
        metavar="<controller>",
        type=str,
        help="Controller to operate in [default: current]",
    )
    parser.add_argument(
        "-m",
        "--model",
        metavar="<model>",
        type=str,
        help="Model to operate in [default: current]",
    )

    # TODO: add support for custom behaviour when a duplicate name is encountered
    # parser.add_argument('-d', '--on-duplicate', choices={'abort', 'remove-all'}, default='abort', help="Behaviour for resolving duplicate names.")
    parser.add_argument("-v", action="store_true", help="Provide verbose output.")
    parser.add_argument(
        "entity",
        metavar="<modelled-entity>",
        help="An application, machine, unit, or relation",
    )

    args = parser.parse_args()
    loop.run(_main(args))


if __name__ == "__main__":
    main()
