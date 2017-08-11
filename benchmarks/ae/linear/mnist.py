from main import configuration_functions, build


def set_mnist_dataset(full_config):
    full_config["layers"][0]["ndim"] = 784
    full_config["dataset"] = dict(
        name="mnist",
        sources=["features"],
        centered=["features"],
        batch_size=100)


configuration_functions.append(set_mnist_dataset)


if __name__ == "__main__":
    ex = build()
    ex.run_commandline()
