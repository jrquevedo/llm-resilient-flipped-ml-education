# LLM-Resilient Flipped Classroom – Machine Learning Education

This repository contains the data and analysis code used in the study:

**Designing LLM-Resilient Flipped Classrooms in Undergraduate Machine Learning Education: A Framework and Empirical Case Study**

## Repository Contents

### Data

The `.csv` files contain the grade data used in the empirical analysis of the article.

Each dataset corresponds to a different academic year:

- **2024–2025** – baseline cohort
- **2025–2026** – cohort following the LLM-resilient flipped classroom design

The CSV files include:

- grades from the **practical activities (PA1–PA10)**
- **final practical exam grades**

Missing values correspond to students who did not complete a given activity.

---

### Analysis Script

The script: **PlotsAndStatistical.py** reproduces the statistical analyses and figures reported in the article.

When executed, the script:

1. Reads the `.csv` datasets
2. Computes the statistical analyses used in the paper
3. Generates the figures included in the article
4. Prints the statistical results in the console
5. Outputs the **LaTeX code for the tables** used in the manuscript

---

### Figures and Output

This repository also includes:

- the **generated figures** used in the article
- the **program output**, containing:
  - computed statistics
  - LaTeX table code included in the manuscript

These files allow verification of the results without re-running the analysis.

---

## Reproducibility

To reproduce the results:

```bash
python PlotsAndStatistical.py
