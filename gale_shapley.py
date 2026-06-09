import pandas as pd

def generate_preference_dicts(applicants_df, jobs_df):
    """Generates preference lists and O(1) ranking dictionaries."""

    # Pre-extract data into dictionaries to avoid slow Pandas dataframe copying in loops 
    app_skills = applicants_df.set_index('Applicant_ID')['Skill_Level'].to_dict()
    app_exp = applicants_df.set_index('Applicant_ID')['Years_Experience'].to_dict()
    app_salary = applicants_df.set_index('Applicant_ID')['Expected_Salary'].to_dict()

    job_req_skills = jobs_df.set_index('Job_ID')['Required_Skill_Level'].to_dict()
    job_req_exp = jobs_df.set_index('Job_ID')['Required_Experience'].to_dict()
    job_offer = jobs_df.set_index('Job_ID')['Salary_Offer'].to_dict()
    
    employer_prefs = {}
    employer_ranks = {} # O(1) lookup dictionary [cite: 33]

    # Generate Employer Preferences [cite: 34]
    for job_id in job_req_skills.keys():
        scores = []
        for app_id in app_skills.keys():
            score = (app_skills[app_id] - job_req_skills[job_id]) + \
                    (app_exp[app_id] - job_req_exp[job_id])
            scores.append((app_id, score))

        # Sort descending by score [cite: 41]
        scores.sort(key=lambda x: x[1], reverse=True)
        sorted_applicants = [x[0] for x in scores]

        employer_prefs[job_id] = sorted_applicants
        # Map applicant ID to their rank index for instant O(1) lookup later [cite: 45, 46]
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
    """Executes the O(n^2) Stable Matching algorithm."""
    applicant_prefs, employer_prefs, employer_ranks = generate_preference_dicts(applicants_df, jobs_df)

    free_applicants = list(applicants_df['Applicant_ID'])
    engagements = {}
    proposal_index = {app: 0 for app in free_applicants}

    while free_applicants:
        app = free_applicants.pop(0)
        job = applicant_prefs[app][proposal_index[app]]
        proposal_index[app] += 1

        if job not in engagements:
            engagements[job] = app
        else:
            current_app = engagements[job]

            # The O(1) Fix: Compare dictionary ranks instead of running .index() [cite: 72]
            if employer_ranks[job][app] < employer_ranks[job][current_app]:
                engagements[job] = app
                free_applicants.append(current_app)
            else:
                free_applicants.append(app)

    return engagements