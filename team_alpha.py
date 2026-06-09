import pandas as pd

def run_greedy_matching(applicants_df, jobs_df):
    """
    Team Alpha's O(n log n) Sorting and Greedy Matching Algorithm.
    
    QUESTION: What makes an algorithm "Greedy"?
    ANSWER: It makes the locally optimal choice at each stage. Instead of 
    checking every possible combination like Gale-Shapley does, it just looks 
    at the best candidate right now and gives them the first job they qualify for.
    """
    
    # QUESTION: Why are we making copies of the dataframes?
    # ANSWER: To protect the original data! If we modify the main datasets directly, 
    # it could mess up the data before Team Beta's algorithm gets a chance to run.
    applicants = applicants_df.copy()
    jobs = jobs_df.copy()

    # ==========================================
    # STEP 1: The Multi-Parameter Scoring System
    # ==========================================
    # We combine multiple metrics into a single "Hireability Score".
    # This gives us a single number to rank everyone by.
    applicants['Hireability_Score'] = applicants['Skill_Level'] + applicants['Years_Experience']

    # ==========================================
    # STEP 2: The O(n log n) Sort
    # ==========================================
    # QUESTION: Why is this step so important?
    # ANSWER: Sorting algorithms generally run in O(n log n) time. By putting our best 
    # candidates at the very top, we guarantee that the highest-skilled people get 
    # first pick of the jobs in our greedy loop!
    sorted_applicants = applicants.sort_values(by='Hireability_Score', ascending=False)

    engagements = {}
    
    # QUESTION: Why convert the Pandas dataframe to a list of dictionaries?
    # ANSWER: Because looping through Pandas rows is notoriously slow. A native Python list 
    # of dictionaries is much faster, and it allows us to instantly .pop() (remove) jobs!
    available_jobs = jobs.to_dict('records')

    # ==========================================
    # STEP 3: The Greedy Loop O(n)
    # ==========================================
    # We iterate through our pre-sorted applicants one by one.
    for _, app in sorted_applicants.iterrows():
        
        # Look through the currently available jobs
        for i, job in enumerate(available_jobs):
            
            # The strict criteria check: Does this candidate meet the exact SDG 8 requirements?
            if (app['Skill_Level'] >= job['Required_Skill_Level'] and
                app['Years_Experience'] >= job['Required_Experience'] and
                app['Expected_Salary'] <= job['Salary_Offer']):

                # MATCH FOUND!
                # 1. We record the engagement (Job ID -> Applicant ID)
                engagements[job['Job_ID']] = app['Applicant_ID']
                
                # 2. We remove the job from the pool so nobody else can take it.
                # Because we used a list, this .pop() removes it instantly!
                available_jobs.pop(i)
                
                # 3. Break the inner loop so this applicant stops looking for jobs
                # and we move on to the next person in line.
                break 

    # Return the final dictionary of who got hired where!
    return engagements