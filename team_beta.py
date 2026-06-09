import pandas as pd
from collections import deque

def generate_preference_dicts(applicants_df, jobs_df):
    """
    Translates our raw Pandas data into instant-lookup dictionaries.
    
    QUESTION: Why avoid Pandas for the actual matching loop?
    ANSWER: Pandas is amazing for loading and analyzing data, but iterating over 
    dataframe rows is computationally slow. By extracting the data into native Python 
    dictionaries first, we speed up the matching process tremendously!
    """
    app_skills = applicants_df.set_index('Applicant_ID')['Skill_Level'].to_dict()
    app_exp = applicants_df.set_index('Applicant_ID')['Years_Experience'].to_dict()
    app_salary = applicants_df.set_index('Applicant_ID')['Expected_Salary'].to_dict()

    job_req_skills = jobs_df.set_index('Job_ID')['Required_Skill_Level'].to_dict()
    job_req_exp = jobs_df.set_index('Job_ID')['Required_Experience'].to_dict()
    job_offer = jobs_df.set_index('Job_ID')['Salary_Offer'].to_dict()
    
    employer_prefs = {}
    employer_ranks = {}

    # 1. Employers evaluate and rank all applicants
    for job_id in job_req_skills.keys():
        scores = []
        for app_id in app_skills.keys():
            # Scoring formula: How much does the applicant exceed the minimum requirements?
            score = (app_skills[app_id] - job_req_skills[job_id]) + \
                    (app_exp[app_id] - job_req_exp[job_id])
            scores.append((app_id, score))

        # Sort the applicants from highest score to lowest for this specific job
        scores.sort(key=lambda x: x[1], reverse=True)
        sorted_applicants = [x[0] for x in scores]

        employer_prefs[job_id] = sorted_applicants
        
        # QUESTION: What is this employer_ranks dictionary doing?
        # ANSWER: It acts as an O(1) "cheat sheet". Later on, instead of scanning a long list 
        # to find out if an employer likes Applicant A more than Applicant B, we can just 
        # instantly look up their exact rank number!
        employer_ranks[job_id] = {app: rank for rank, app in enumerate(sorted_applicants)}
    
    applicant_prefs = {}

    # 2. Applicants evaluate and rank all available jobs
    for app_id in app_salary.keys():
        scores = []
        for job_id in job_offer.keys():
            # Scoring formula: How much higher is the offer compared to their expected salary?
            score = job_offer[job_id] - app_salary[app_id]
            scores.append((job_id, score))

        # Sort the jobs from most lucrative to least for this specific applicant
        scores.sort(key=lambda x: x[1], reverse=True)
        sorted_jobs = [x[0] for x in scores]
        applicant_prefs[app_id] = sorted_jobs

    return applicant_prefs, employer_prefs, employer_ranks


def run_gale_shapley(applicants_df, jobs_df):
    """
    Team Beta's O(n^2) Stable Matching Algorithm.
    
    QUESTION: What makes a match "Stable"?
    ANSWER: It guarantees that there are no "blocking pairs." Meaning, there is absolutely 
    no applicant and employer out there who would secretly prefer to be with each other 
    over the matches the algorithm assigned them!
    """
    
    # Pre-process our data into fast dictionaries
    applicant_prefs, employer_prefs, employer_ranks = generate_preference_dicts(applicants_df, jobs_df)

    # QUESTION: Why use a 'deque' instead of a standard Python list?
    # ANSWER: In a standard list, using .pop(0) takes O(n) time because the computer has to 
    # shift every single remaining item over by one slot. A deque allows us to use .popleft(), 
    # which removes the first item instantly in O(1) time. This prevents our algorithm from lagging!
    free_applicants = deque(applicants_df['Applicant_ID'])
    engagements = {}
    
    # Keep track of how many job offers each applicant has made so they don't apply twice
    proposal_index = {app: 0 for app in free_applicants}

    # ==========================================
    # The Propose-and-Reject Loop
    # ==========================================
    while free_applicants:
        app = free_applicants.popleft()  
        
        # The applicant proposes to the next job on their preference list
        job = applicant_prefs[app][proposal_index[app]]
        proposal_index[app] += 1

        # Scenario A: The job is vacant. They get hired immediately!
        if job not in engagements:
            engagements[job] = app
            
        # Scenario B: The job is already taken. The employer must make a choice.
        else:
            current_app = engagements[job]

            # The O(1) Lookup: Does the employer prefer this NEW applicant over their CURRENT worker?
            if employer_ranks[job][app] < employer_ranks[job][current_app]:
                engagements[job] = app                   # The new applicant steals the job!
                free_applicants.append(current_app)      # The old worker goes back into the unemployment pool
            else:
                free_applicants.append(app)              # The applicant is rejected and tries again

    # ==========================================
    # AUDIT PHASE: Verify Match Stability
    # ==========================================
    # QUESTION: Why do we need an audit phase?
    # ANSWER: To scientifically prove our algorithm works! We double check every single 
    # matched pair to ensure no mathematical constraints were broken during the loop.
    
    print("Verifying match stability...")
    is_stable = True
    
    for job, assigned_app in engagements.items():
        pref_jobs = applicant_prefs[assigned_app]
        current_job_rank = pref_jobs.index(job)
        
        # Look exclusively at the jobs this applicant wanted MORE than what they actually got
        preferred_jobs = pref_jobs[:current_job_rank]
        
        for better_job in preferred_jobs:
            current_match_of_better_job = engagements.get(better_job)
            
            # The Ultimate Test: If the applicant wanted this better job, did that better job 
            # ALSO want this applicant more than its current worker?
            if current_match_of_better_job is not None:
                if employer_ranks[better_job][assigned_app] < employer_ranks[better_job][current_match_of_better_job]:
                    
                    # If YES, we have a blocking pair, and the algorithm failed.
                    print(f"Instability Found: Applicant {assigned_app} and Job {better_job} prefer each other!")
                    is_stable = False
                    break
                    
        if not is_stable:
            break

    # The Final Verdict
    if is_stable:
        print("Verification Success: Perfect stability achieved! No blocking pairs exist.")
    else:
        print("Verification Failure: The matching contains instabilities.")

    return engagements