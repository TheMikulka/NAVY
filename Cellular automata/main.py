from ForestFireSimulation import ForestFireSimulation

if __name__ == '__main__':
    sim = ForestFireSimulation(
        size=100,
        p=0.05,
        f=0.001,
        forest_density=0.5,
        neighborhood="vonneumann"  
    )
    sim.run(title="Von Neumann Neighborhood")

    sim = ForestFireSimulation(
        size=100,
        p=0.05,
        f=0.001,
        forest_density=0.5,
        neighborhood="moore"
    )
    sim.run(title="Moore Neighborhood")