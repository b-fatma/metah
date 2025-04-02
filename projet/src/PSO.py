import time  # Importer le module time
from MaxCoveringProblem import MaxCoveringProblem
from Particle import ParticleFlipCount, ParticleProbabilistic
import numpy as np

class PSO:
    def __init__(self, problem: MaxCoveringProblem, num_particles=50, max_iterations=1000, strategy="random", inertia_type="fixed", inertia_value=0.7, neighborhood_size=None, c1=1.5, c2=1.5, dist_type="HD", selection_type="stochastic", mutate=False, mutation_rate=0.1):
        self.problem = problem
        self.num_particles = num_particles
        self.max_iterations = max_iterations
        self.initialization_strategy = strategy
        self.inertia_type = inertia_type
        self.inertia_value = inertia_value  # Tunable when inertia_type is 'fixed'
        self.neighborhood_size = neighborhood_size if neighborhood_size else num_particles  # Defaults to global best if None
        self.global_best_position = None
        self.global_best_score = 0
        
        self.particles = self.initialize_particles()

        # PSO optimize parameters
        self.c1 = c1
        self.c2 = c2
        self.dist_type = dist_type
        self.selection_type = selection_type
        self.mutate = mutate
        self.mutation_rate = mutation_rate

    def initialize_particles(self):
        particles = []
        for _ in range(self.num_particles):
            particle = ParticleProbabilistic(self.problem, self.initialization_strategy)
            particles.append(particle)
            if particle.best_score > self.global_best_score:
                self.global_best_position = np.copy(particle.best_position)
                self.global_best_score = particle.best_score

        print(f"Initial best particle fitness: {self.global_best_score}")
        return particles
    
    def get_inertia(self, iteration):
        if self.inertia_type == 'fixed':
            return self.inertia_value
        elif self.inertia_type == 'linear':
            return 0.9 - (0.5 * (iteration / self.max_iterations))
        elif self.inertia_type == 'nonlinear':
            return 0.9 * np.exp(-2 * (iteration / self.max_iterations))
    
    def get_neighborhood_best(self):
        neighborhood = np.random.choice(self.particles, self.neighborhood_size, replace=False)
        best_neighbor = max(neighborhood, key=lambda p: p.best_score)
        return best_neighbor.best_position
    
    def optimize(self, verbose=False):
        for iteration in range(self.max_iterations):
            w = self.get_inertia(iteration)
            for i, particle in enumerate(self.particles):
                best_position = self.get_neighborhood_best() if self.neighborhood_size < self.num_particles else self.global_best_position
                particle.update_velocity(best_position, w, self.c1, self.c2, self.dist_type)
                if self.mutate:
                    particle.mutate_velocity(self.mutation_rate)
                particle.update_position(selection_type=self.selection_type)
                particle.update_pbest()
                
                if particle.best_score > self.global_best_score:
                    self.global_best_position = np.copy(particle.best_position)
                    self.global_best_score = particle.best_score

                if self.global_best_score == self.problem.n:
                    if verbose:
                        print(f"EARLY STOPPING Iteration {iteration + 1}/{self.max_iterations} - Best Score: {self.global_best_score}")
                    return self.global_best_position, self.global_best_score
            
            if verbose:
                print(f"Iteration {iteration + 1}/{self.max_iterations} - Best Score: {self.global_best_score}")
        
        return self.global_best_position, self.global_best_score

if __name__ == "__main__":
    filename = "../data/scpc2.txt"  
    problem = MaxCoveringProblem(filename)
    
    start_time = time.time()  # Démarrer le chrono
    
    swarm = PSO(problem, num_particles=50, neighborhood_size=30, inertia_type="linear", max_iterations=5000, strategy="random", dist_type="bit-wise", selection_type="standard")
    best_position, best_score = swarm.optimize(verbose=True)
    
    end_time = time.time()  # Arrêter le chrono
    
    execution_time = end_time - start_time  # Calculer le temps d'exécution

    print("Best Position:", best_position)
    print("Best Score:", best_score)
    print("n:", problem.n)
    print(f"Execution Time: {execution_time:.4f} seconds")  # Afficher le temps avec 4 décimales
