import pandas as pd

def generate_preference_dicts(applicants_df, jobs_df):
    employer_prefs = {}
    for _, job in jobs_df.iterrows():
        scores = applicants_df.copy()
        scores['score'] = (scores['Skill_Level'] - job['Required_Skill_Level']) + \
                          (scores['Years_Experience'] - job['Required_Experience'])
        
        sorted_applicants = scores.sort_values(by='score', ascending=False)['Applicant_ID'].tolist()
        employer_prefs[job['Job_ID']] = sorted_applicants

    applicant_prefs = {}
    for _, app in applicants_df.iterrows():
        scores = jobs_df.copy()
        scores['score'] = scores['Salary_Offer'] - app['Expected_Salary']
        
        sorted_jobs = scores.sort_values(by='score', ascending=False)['Job_ID'].tolist()
        applicant_prefs[app['Applicant_ID']] = sorted_jobs
        
    return applicant_prefs, employer_prefs

def gale_shapley(applicants_df, jobs_df):
    applicant_prefs, employer_prefs = generate_preference_dicts(applicants_df, jobs_df)
    
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
            job_pref_list = employer_prefs[job]
            
            if job_pref_list.index(app) < job_pref_list.index(current_app):
                engagements[job] = app
                free_applicants.append(current_app)
            else:
                free_applicants.append(app)
                
    return engagements

# Execution starts here
if __name__ == "__main__":
    applicants_df = pd.read_csv('applicants_N500.csv')
    jobs_df = pd.read_csv('jobs_N500.csv')
    matches = gale_shapley(applicants_df, jobs_df)
    print("Final Matches (Job_ID : Applicant_ID):")
    print(matches)