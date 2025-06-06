import os
import csv
from MaxCoveringProblem import MaxCoveringProblem
from DFS import DFS  
import sys

# sys.setrecursionlimit(10000)


class DFSTest:
    def __init__(self, dataset_folder, time_limit=10, output_file="dfs_results.csv"):
        self.dataset_folder = dataset_folder  
        self.time_limit = time_limit  
        self.output_file = output_file
        self.results = []  


    def run_tests(self, file_list):
        for filename in file_list:
            file_path = os.path.join(self.dataset_folder, filename)
            print(f"\nRunning DFS on {filename}...")

            problem = MaxCoveringProblem(file_path)
            dfs_solver = DFS(problem, time_limit=self.time_limit)

            best_fitness, best_selection, completed, execution_time = dfs_solver.solve_time_bound(verbose=False)
            used_budget = sum(best_selection)
            valid = (used_budget == problem.k)  

            print(f"File: {filename}, m={problem.m}, n={problem.n}, k={problem.k}, "
                f"Fitness: {best_fitness}, Used Budget: {used_budget}/{problem.k}, "
                f"Completed: {completed}, Valid: {valid}, Time: {execution_time:.2f} sec")

            self.results.append({
                "filename": filename,
                "m": problem.m,
                "n": problem.n,
                "k": problem.k,
                "fitness": best_fitness,
                "used_budget": used_budget,
                "completed": completed,
                "valid": valid,
                "execution_time(s)": execution_time
            })


    def save_results_to_csv(self):
        with open(self.output_file, mode="w", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=["filename", "m", "n", "k", "fitness", "used_budget", "completed", "valid", "execution_time(s)"])
            writer.writeheader()
            writer.writerows(self.results)
        print(f"\nResults saved to {self.output_file}")


    def print_summary(self):
        print("\n===== DFS Test Summary =====")
        for result in self.results:
            print(f"{result['filename']} → Fitness: {result['fitness']}, Used Budget: {result['used_budget']}/{result['k']}, "
                  f"Completed: {result['completed']}, Valid: {result['valid']}")
            

if __name__ == "__main__":
    dataset_folder = "../data"
    output_file = "../stats/dfs_1h.csv"
    time_limit = 60 * 60  # (1 hour)
    test_files = sorted([filename for filename in os.listdir(dataset_folder)])  

    dfs_tester = DFSTest(dataset_folder, time_limit=time_limit, output_file=output_file)
    dfs_tester.run_tests(test_files)
    dfs_tester.print_summary()
    dfs_tester.save_results_to_csv()
