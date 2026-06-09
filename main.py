import pandas as pd
import time
import tracemalloc
# 1. Import Team Beta's optimized function
from gale_shapley import run_gale_shapley

def load_data(n_size):
    """Loads the synthetic datasets based on the requested batch size."""
    print(f"Loading datasets for N={n_size}...")
    applicants_df = pd.read_csv(f"applicants_N{n_size}.csv")
    jobs_df = pd.read_csv(f"jobs_N{n_size}.csv")
    return applicants_df, jobs_df

def main():
    # 1. Load the initial data (Change 500 to 100 or 2500 to test different sizes)
    applicants, jobs = load_data(2500)
    print("Data loaded successfully!")

    # --- TEAM ALPHA: SORTING & GREEDY ALGORITHM GOES HERE ---
    print("\nStarting Greedy Algorithm...")
    # TODO: Implement Matching Score & Sorting
    # TODO: Implement Greedy Matching
    
    # --- TEAM BETA: GALE-SHAPLEY STABLE MATCHING GOES HERE ---
    print("\nStarting Gale-Shapley Algorithm...")
    
    # Start performance metrics tracking
    start_time = time.time()
    tracemalloc.start()
    
    # Call your optimized algorithm using the loaded data
    engagements = run_gale_shapley(applicants, jobs)
    
    # Stop performance metrics tracking
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    end_time = time.time()
    
    # Print benchmarks and final matching results
    print("Gale-Shapley Matching complete!")
    print(f"Execution Time: {end_time - start_time:.4f} seconds")
    print(f"Peak Memory Usage: {peak / 10**6:.2f} MB")
    print("\nFinal Stable Engagements:")
    print(engagements)
    
if __name__ == "__main__":
    main()