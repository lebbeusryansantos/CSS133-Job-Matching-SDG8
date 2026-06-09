import pandas as pd
import time         # QUESTION: Why import time? ANSWER: To act as a stopwatch so we can measure execution speed!
import tracemalloc  # QUESTION: Why tracemalloc? ANSWER: To track exactly how much RAM (memory) our algorithms eat up.

# 1. Import the algorithms from our modular team files!
# Keeping code in separate files (Separation of Concerns) makes our project clean and easy to read.
from team_alpha import run_greedy_matching
from team_beta import run_gale_shapley

def load_data(n_size):
    """
    Loads our synthetic datasets based on the requested size.
    QUESTION: Why pass 'n_size' as a variable?
    ANSWER: It allows us to dynamically load the N=100, 500, or 2500 CSVs without hardcoding the file names!
    """
    applicants_df = pd.read_csv(f"applicants_N{n_size}.csv")
    jobs_df = pd.read_csv(f"jobs_N{n_size}.csv")
    return applicants_df, jobs_df

def main():
    # We define the three dataset sizes we want to test to see how our algorithms scale.
    batch_sizes = [100, 500, 2500]

    # QUESTION: Why use a loop here?
    # ANSWER: So the computer automatically runs all our empirical tests back-to-back. No manual editing required!
    for n_size in batch_sizes:
        print(f"\n{'='*60}")
        print(f"🚀 RUNNING EMPIRICAL TESTS FOR DATASET SIZE: N = {n_size}")
        print(f"{'='*60}")

        # Step 1: Load the data into memory
        applicants, jobs = load_data(n_size)
        print("Data loaded successfully! Let's see how the algorithms handle it.\n")

        # =====================================================================
        # --- TEAM ALPHA: GREEDY ALGORITHM ---
        # Hypothesis: This O(n log n) algorithm will be incredibly fast and 
        # use very little memory, but it might leave a lot of people unmatched.
        # =====================================================================
        print("--- [ Team Alpha: Greedy Algorithm ] ---")
        
        start_time_alpha = time.time()  # Start the stopwatch
        tracemalloc.start()             # Start recording RAM usage
        
        # Execute the matching logic
        greedy_matches = run_greedy_matching(applicants, jobs)
        
        # Stop tracking metrics
        current_alpha, peak_alpha = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        end_time_alpha = time.time()
        
        # Print the final data for our research paper
        print(f"Execution Time    : {end_time_alpha - start_time_alpha:.4f} seconds")
        print(f"Peak Memory Usage : {peak_alpha / 10**6:.2f} MB")
        print(f"Total Matches Made: {len(greedy_matches)} out of {n_size}\n")
        
        
        # =====================================================================
        # --- TEAM BETA: GALE-SHAPLEY STABLE MATCHING ---
        # Hypothesis: This O(n^2) algorithm guarantees a 100% stable match rate,
        # but the tradeoff is that it will consume significantly more time and memory.
        # =====================================================================
        print("--- [ Team Beta: Gale-Shapley Stable Matching ] ---")
        
        start_time_beta = time.time()   # Start the stopwatch
        tracemalloc.start()             # Start recording RAM usage
        
        # Execute the matching logic
        gs_matches = run_gale_shapley(applicants, jobs)
        
        # Stop tracking metrics
        current_beta, peak_beta = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        end_time_beta = time.time()
        
        # Print the final data for our research paper
        print(f"Execution Time    : {end_time_beta - start_time_beta:.4f} seconds")
        print(f"Peak Memory Usage : {peak_beta / 10**6:.2f} MB")
        print(f"Total Matches Made: {len(gs_matches)} out of {n_size}")
        print(f"{'-'*60}\n")

# This is the standard entry point for Python scripts. 
# It tells Python to run the main() function only if this file is executed directly.
if __name__ == "__main__":
    main()