import pandas as pd
import time
import tracemalloc

def load_data(n_size):
    """Loads the synthetic datasets based on the requested batch size."""
    print(f"Loading datasets for N={n_size}...")
    applicants_df = pd.read_csv(f"applicants_N{n_size}.csv")
    jobs_df = pd.read_csv(f"jobs_N{n_size}.csv")
    return applicants_df, jobs_df

def main():
    # 1. Load the initial data (Testing with N=500 for now)
    applicants, jobs = load_data(500)
    print("Data loaded successfully!")

    # --- TEAM ALPHA: SORTING & GREEDY ALGORITHM GOES HERE ---
    print("\nStarting Greedy Algorithm...")
    # TODO: Implement Matching Score & Sorting
    # TODO: Implement Greedy Matching
    
    # --- TEAM BETA: GALE-SHAPLEY STABLE MATCHING GOES HERE ---
    print("\nStarting Gale-Shapley Algorithm...")
    # TODO: Implement Stable Matching Loop
    
if __name__ == "__main__":
    main()