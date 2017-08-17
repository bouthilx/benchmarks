from main import configuration_functions, build, setup_config


def set_spirals_dataset(full_config):
    full_config["layers"][0]["ndim"] = 2
    full_config["dataset"] = dict(
        name="spirals",
        num_examples=1000,
        classes=1,
        cycles=1,
        noise=0.0,
        sources=["features"],
        centered=["features"],
        batch_size=100)


configuration_functions.append(set_spirals_dataset)


if __name__ == "__main__":
    ex = build()
    ex.run_commandline()
