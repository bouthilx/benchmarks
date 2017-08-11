from main import configuration_functions, build


def set_gaussians_dataset(full_config):
    full_config["layers"][0]["ndim"] = 2
    full_config["dataset"] = dict(
        name="gaussians",
        nb_of_modes=5,
        nb_of_dimensions=2,
        nb_of_points=1000,
        sources=["features"],
        centered=["features"],
        batch_size=100)


configuration_functions.append(set_gaussians_dataset)


if __name__ == "__main__":
    ex = build()
    ex.run_commandline()
