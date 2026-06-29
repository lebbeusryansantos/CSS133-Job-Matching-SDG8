# 🎯 SDG 8: Job Matching Algorithm Optimization

## 📖 Project Overview

This repository contains the empirical testing framework for **Group 3's** comparative analysis of job matching algorithms.

Built for our Week 13 defense, this project evaluates two distinct algorithmic approaches to solving labor market inefficiencies, directly aligning with **UN Sustainable Development Goal (SDG) 8: Decent Work and Economic Growth**.

We generated synthetic datasets representing applicants and job postings at three different scales (**N = 100**, **N = 500**, and **N = 2500**) to benchmark:

- Execution Time
- Peak Memory Usage
- Match Stability

---

## 👥 The Team

- **Ryan (Group Leader)** — Project leadership, repository architecture, data generation, integration of all modules, and empirical benchmarking framework.
- **Kurt (Team Alpha)** — O(n log n) Greedy Algorithm implementation, data visualization, graphical analysis, and IEEE paper contributions.
- **Lawrenze (Team Alpha)** — O(n log n) Greedy Algorithm implementation, data visualization, graphical analysis, and IEEE paper contributions.
- **Nikolai (Team Beta)** — O(n²) Gale-Shapley Stable Matching implementation.
- **Jhico (Team Beta)** — Gale-Shapley implementation support, sorting logic, and IEEE paper contributions.
- **Ramuell** — Empirical testing, results validation, and IEEE paper formatting.

---

## 🗂️ File Structure (Modular Architecture)

We separated responsibilities to keep the codebase clean, modular, and easy to maintain.

| File | Description |
|--------|------------|
| `main.py` | Central benchmarking script. Loads datasets, executes both algorithms, and tracks performance metrics using `time` and `tracemalloc`. |
| `team_alpha.py` | Contains the Greedy matching algorithm implementation. |
| `team_beta.py` | Contains the Gale-Shapley Stable Matching algorithm and Match Stability Auditor. |
| `*.csv` | Synthetic applicant and job datasets across varying dataset sizes. |
| `Graphs.ipynb` | Comparing of the results made by two teams. |

---

## 🚀 How to Run the Code

### 1. Clone the Repository

```bash
git clone https://github.com/YOUR-USERNAME/CSS133-Job-Matching-SDG8.git
cd CSS133-Job-Matching-SDG8
```

### 2. Install Dependencies

Ensure that Pandas is installed in your Python environment.

```bash
pip install pandas
```

### 3. Execute the Benchmark

```bash
python main.py
```

Depending on your system configuration, you may need to use:

```bash
py main.py
```

or

```bash
python3 main.py
```

---

## 📊 Empirical Results Summary (N = 2500)

Our testing revealed a classic computer science trade-off between computational efficiency and optimization quality.

| Metric | Team Alpha (Greedy) | Team Beta (Gale-Shapley) |
|----------|-------------------|-------------------------|
| Time Complexity | O(n log n) | O(n²) |
| Execution Time | ~17.74 seconds | ~79.08 seconds |
| Peak Memory Usage | 1.12 MB | 412.94 MB |
| Matches Made | 49% (1228/2500) | 100% (2500/2500) |
| Match Stability | Sub-optimal | Perfect (Zero Blocking Pairs) |

---

## 🎯 Key Findings

### Team Alpha (Greedy Algorithm)

**Strengths**
- Fast execution
- Low memory consumption
- Scales efficiently to larger datasets

**Limitations**
- Does not guarantee stable matches
- Leaves many applicants and jobs unmatched
- May produce sub-optimal labor market utilization

### Team Beta (Gale-Shapley Algorithm)

**Strengths**
- Produces stable matchings
- Achieves 100% matching coverage
- Eliminates blocking pairs

**Limitations**
- Higher computational cost
- Significantly greater memory usage
- Slower execution on large datasets

---

## 📌 Conclusion

The results demonstrate a fundamental trade-off in algorithm design:

- **Team Alpha's Greedy Algorithm** prioritizes speed and resource efficiency.
- **Team Beta's Gale-Shapley Algorithm** prioritizes match quality and stability.

While the Greedy approach performs well in terms of computational efficiency, the Gale-Shapley algorithm is necessary when the goal is to guarantee stable and complete job matching.

For labor market applications aligned with **UN Sustainable Development Goal 8 (Decent Work and Economic Growth)**, the Gale-Shapley approach provides superior outcomes by ensuring full utilization of available opportunities and mathematically stable matches.

---

## 📚 Technologies Used

- Python 3
- Pandas
- Time Module
- Tracemalloc
- CSV Datasets

---

## 🏫 Academic Context

This project was developed as part of the **CSS133 Algorithm Analysis and Design** course and serves as an empirical comparison of algorithmic strategies for solving job matching problems under realistic scalability constraints.
