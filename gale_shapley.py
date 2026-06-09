import pandas as pd
from collections import deque  # Optimized for fast popping

def generate_preference_dicts(applicants_df, jobs_df):
    """Generates preference lists and O(1) ranking dictionaries."""
    app_skills = applicants_df.set_index('Applicant_ID')['Skill_Level'].to_dict()
    app_exp = applicants_df.set_index('Applicant_ID')['Years_Experience'].to_dict()
    app_salary = applicants_df.set_index('Applicant_ID')['Expected_Salary'].to_dict()

    job_req_skills = jobs_df.set_index('Job_ID')['Required_Skill_Level'].to_dict()
    job_req_exp = jobs_df.set_index('Job_ID')['Required_Experience'].to_dict()
    job_offer = jobs_df.set_index('Job_ID')['Salary_Offer'].to_dict()
    
    employer_prefs = {}
    employer_ranks = {}

    # Generate Employer Preferences
    for job_id in job_req_skills.keys():
        scores = []
        for app_id in app_skills.keys():
            score = (app_skills[app_id] - job_req_skills[job_id]) + \
                    (app_exp[app_id] - job_req_exp[job_id])
            scores.append((app_id, score))

        scores.sort(key=lambda x: x[1], reverse=True)
        sorted_applicants = [x[0] for x in scores]

        employer_prefs[job_id] = sorted_applicants
        employer_ranks[job_id] = {app: rank for rank, app in enumerate(sorted_applicants)}
    
    applicant_prefs = {}

    # Generate Applicant Preferences
    for app_id in app_salary.keys():
        scores = []
        for job_id in job_offer.keys():
            score = job_offer[job_id] - app_salary[app_id]
            scores.append((job_id, score))

        scores.sort(key=lambda x: x[1], reverse=True)
        sorted_jobs = [x[0] for x in scores]
        applicant_prefs[app_id] = sorted_jobs

    return applicant_prefs, employer_prefs, employer_ranks

def run_gale_shapley(applicants_df, jobs_df):
    """Executes the O(n^2) Stable Matching algorithm using an optimized queue."""
    applicant_prefs, employer_prefs, employer_ranks = generate_preference_dicts(applicants_df, jobs_df)

    # O(1) popping optimization
    free_applicants = deque(applicants_df['Applicant_ID'])
    engagements = {}
    proposal_index = {app: 0 for app in free_applicants}

    while free_applicants:
        app = free_applicants.popleft()  # Instant O(1) removal
        job = applicant_prefs[app][proposal_index[app]]
        proposal_index[app] += 1

        if job not in engagements:
            engagements[job] = app
        else:
            current_app = engagements[job]

            if employer_ranks[job][app] < employer_ranks[job][current_app]:
                engagements[job] = app
                free_applicants.append(current_app)
            else:
                free_applicants.append(app)

    # Stability Verification (Verify no pair prefers each other)
    print("\nVerifying match stability...")
    is_stable = True
    
    # Create a quick inverse lookup to find an applicant's assigned job
    app_to_job = {app_id: job_id for job_id, app_id in engagements.items()}

    # Check each job-applicant pairing for potential blocking pairs
    for job, assigned_app in engagements.items():
        # Get the preference list for this applicant
        pref_jobs = applicant_prefs[assigned_app]
        current_job_rank = pref_jobs.index(job)
        
        # Look at all jobs this applicant ranked HIGHER than their assigned job
        preferred_jobs = pref_jobs[:current_job_rank]
        
        for better_job in preferred_jobs:
            # Find who currently holds that preferred job
            current_match_of_better_job = engagements.get(better_job)
            
            if current_match_of_better_job is not None:
                # Use optimized O(1) rank dictionary to see if the better job 
                # also prefers our assigned_app over its current worker
                if employer_ranks[better_job][assigned_app] < employer_ranks[better_job][current_match_of_better_job]:
                    print(f"Instability Found: Applicant {assigned_app} and Job {better_job} prefer each other!")
                    is_stable = False
                    break
        if not is_stable:
            break

    if is_stable:
        print("Verification Success: Perfect stability achieved! No blocking pairs exist.")
    else:
        print("Verification Failure: The matching contains instabilities.")

    return engagements