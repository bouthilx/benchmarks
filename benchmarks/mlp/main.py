from collections import OrderedDict
import inspect
import logging
import os

import numpy

from blocks.extensions import Printing

from research.utils import imports
from research.utils.json import turn_to

from research.framework import experiments

logger = logging.getLogger(__name__)


def config():
    config = os.path.join(
        os.path.dirname(
            os.path.abspath(inspect.getfile(inspect.currentframe()))),
        "full.sacred.json")
    optimization = dict(
        nb_of_epochs=200,
        step_rule=dict(
            components={
                "0": dict(
                    learning_rate=0.1,
                    momentum=0.7),
                "1": dict(step_rule=dict(threshold=1.))}))

    weights_init = {
        imports.object_key: "blocks.initialization.Uniform",
        'width': 2 * 4 * numpy.sqrt(6. / (4096 + 4096))}

    biases_init = {
        imports.object_key: "blocks.initialization.Constant",
        'constant': 0.}

    graphs = {}


# Must be inplace functions
configuration_functions = []


def setup_config(full_config_path, sub_config):
    sub_config = turn_to(sub_config, OrderedDict)

    full_config = experiments.setup_config(
        full_config_path, sub_config,
        ignore=["seed", "config"])

    for configuration_function in configuration_functions:
        configuration_function(full_config)

    return full_config


def _contains_uninstantiated(definitions, cls):
    for definition in definitions:
        try:
            o = imports.instantiate(definition)
            if isinstance(o, cls):
                return True
        except (ImportError, TypeError):
            continue

    return False


def run(config, _config, _run):

    mongodb_observer = experiments.get_mongodb_observer(_run)

    # First run
    if (mongodb_observer is None or
            "config" not in mongodb_observer.run_entry["info"]):
        logger.info("Setting up config")
        logger.debug("mongodb_observer is %s" % str(mongodb_observer))
        if mongodb_observer is not None:
            logger.debug("config in run_entry.info: %r" %
                         ("config" in mongodb_observer.run_entry["info"]))

        full_config = setup_config(config, _config)
        # The experiment is unobserved, which means it is meant for debugging
        if (_run.unobserved and not
                _contains_uninstantiated(full_config["extensions"], Printing)):
            full_config["extensions"].append(Printing())
    # Was queued (and maybe never ran)
    else:
        logger.info("Logging config from DB id=%d" %
                    mongodb_observer.run_entry["_id"])
        full_config = mongodb_observer.run_entry["info"]["config"]

    experiments.run(full_config, _run)


def build():
    return experiments.create_experiment(run, config)


if __name__ == "__main__":
    ex = build()
    ex.run_commandline()
