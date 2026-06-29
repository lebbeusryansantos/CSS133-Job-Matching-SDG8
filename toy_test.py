from collections import deque
import time

print("==================================================")
print("   LIVE DESK-TRACE: GALE-SHAPLEY (N = 3)")
print("==================================================\n")

# 1. THE QUEUE (Proposers using O(1) popleft)
free_applicants = deque(["Applicant_A", "Applicant_B", "Applicant_C"])

# Applicant Preference Lists (Ordered 1st choice to 3rd choice)
app_prefs = {
    "Applicant_A": deque(["Job_X", "Job_Y", "Job_Z"]),
    "Applicant_B": deque(["Job_X", "Job_Z", "Job_Y"]),
    "Applicant_C": deque(["Job_Y", "Job_X", "Job_Z"])
}

# 2. THE DICTIONARY (O(1) Hash-map lookups for Employer rankings)
# Lower number = Higher rank (1 is top tier)
job_rankings = {
    "Job_X": {"Applicant_B": 1, "Applicant_A": 2, "Applicant_C": 3},
    "Job_Y": {"Applicant_A": 1, "Applicant_C": 2, "Applicant_B": 3},
    "Job_Z": {"Applicant_C": 1, "Applicant_B": 2, "Applicant_A": 3}
}

current_matches = {} 
step = 1

while free_applicants:
    proposer = free_applicants.popleft()
    target_job = app_prefs[proposer].popleft()
    
    print(f"[Step {step}] {proposer} proposes to {target_job}...")
    time.sleep(1.5)
    
    if target_job not in current_matches:
        current_matches[target_job] = proposer
        print(f"   └── RESULT: {target_job} was vacant. MATCHED ({proposer} <-> {target_job})\n")
    else:
        current_holder = current_matches[target_job]
        print(f"   └── CONFLICT: {target_job} is currently held by {current_holder}.")
        
        # O(1) Dictionary Lookup comparison
        rank_new = job_rankings[target_job][proposer]
        rank_old = job_rankings[target_job][current_holder]
        
        if rank_new < rank_old:
            print(f"   └── DECISION: {target_job} prefers {proposer} (Rank {rank_new}) over {current_holder} (Rank {rank_old}).")
            print(f"   └── SWAP: {current_holder} is dumped back to the queue!\n")
            current_matches[target_job] = proposer
            free_applicants.append(current_holder)
        else:
            print(f"   └── DECISION: {target_job} prefers current match. {proposer} rejected!\n")
            free_applicants.append(proposer)
            
    step += 1

print("==================================================")
print("FINAL STABLE EQUILIBRIUM ACHIEVED:")
for job, app in current_matches.items():
    print(f" * {job} <---> {app}")
print("==================================================")