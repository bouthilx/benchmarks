import inspect
import logging
import os

from benchmarks.mlp.main import configuration_functions, setup_config
from benchmarks.mlp.main import build as parent_build


logger = logging.getLogger()


def config():
    config = os.path.join(
        os.path.dirname(
            os.path.abspath(inspect.getfile(inspect.currentframe()))),
        "full.sacred.json")

    optimization = dict(
        nb_of_epochs=1000,
        step_rule=dict(
            components={
                "0": dict(
                    learning_rate=0.001,
                    momentum=0.0),
                "1": dict(step_rule=dict(threshold=100000.))}),
        cost={
            "layer_1_reconstruction_error": {
                "coefficient": {"0": 1.0}},
            "layer_1_maximum_variance": {
                "coefficient": {"0": 0.0}},
            "layer_1_weight_orthogonality_penalty": {
                "coefficient": {"0": 0.0}},
            "layer_1_code_orthogonality_penalty": {
                "coefficient": {"0": 0.0}}})


def configure_cost(full_config):
    # Help for problems with ReconstructionError
    if logger.getEffectiveLevel() == logging.DEBUG:
        cost_config = full_config["optimization"]["cost"]
        for cost_name, cost_config in cost_config.iteritems():
            if "reconstruction_error" in cost_name:
                cost_config["debug_graph"] = True


configuration_functions.append(configure_cost)


def build():
    ex = parent_build()
    ex.config(config)
    return ex


if __name__ == "__main__":
    ex = build()
    ex.run_commandline()
