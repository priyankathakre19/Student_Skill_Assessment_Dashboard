# 🎓 Student Skill Assessment Dashboard

An interactive **Student Skill Assessment Dashboard** built using Python and Streamlit to analyze student skills, compare academic groups, identify strengths and weaknesses, and generate actionable performance insights.

---

## 📊 Project Overview

The Student Skill Assessment Dashboard analyzes multiple student skills:

- 🐍 Python
- 🧩 Problem Solving
- 💬 Communication
- 🤝 Teamwork
- 👑 Leadership
- 🎨 Creativity
- ⏱️ Time Management
- 🎤 Presentation

The dashboard provides both **group-level** and **individual student-level** analysis.

Users can filter the dashboard by:

- Department
- Academic Year
- Gender

All charts, KPIs, rankings, insights, and downloadable reports automatically update according to the selected filters.

---

## ✨ Key Features

### 🎛️ Interactive Filters

Filter student records by:

- Department
- Academic Year
- Gender

All dashboard components respond to the selected filters.

### 📈 Performance KPIs

The dashboard provides:

- Total Students
- Average Overall Score
- Advanced Students
- Strongest Skill
- Weakest Skill
- Skill Gap
- Department Performance

### 📊 Skill Performance Analysis

Compare the average performance of all assessed skills to identify strengths and areas requiring improvement.

### 🏆 Skill Level Distribution

Students are categorized into:

- Beginner
- Intermediate
- Advanced

### 🏢 Department Performance

Compare student performance across:

- CSE
- IT
- ECE
- Mechanical
- Civil
- AIDS
- IoT
- Robotics

### 📚 Academic Year Analysis

Compare performance across:

- First Year
- Second Year
- Third Year
- Fourth Year

### 👥 Gender Analysis

Compare average overall performance across genders.

### 👤 Student Profile Explorer

Select an individual student and view:

- Student name
- Department
- Academic year
- Overall score
- Skill level
- Individual skill performance
- Strongest skill
- Weakest skill
- Personalized improvement recommendation

### 🥇 Top Students Leaderboard

The dashboard generates a Top 10 leaderboard based on overall performance.

It displays:

- Rank
- Student name
- Department
- Academic year
- Overall score
- Skill level

### 💡 Automatic Performance Insights

The dashboard automatically identifies:

- Strongest skill
- Weakest skill
- Overall skill gap
- Best performing department
- Department requiring improvement
- Highest performing academic year
- Gender with highest average performance
- Number of Advanced students
- Number of Intermediate students
- Number of Beginner students

### 📅 Assessment Trend Analysis

Analyze:

- Monthly average performance
- Number of assessments per month
- Best assessment month
- Lowest assessment month
- Performance changes over the assessment period

### 🔥 Skill Gap & Improvement Analysis

The dashboard provides:

- Department-wise skill comparison
- Skill ranking
- Strongest and weakest skills
- Department improvement areas
- Recommended improvement focus

### 📥 Export & Reports

Users can download:

- Filtered student assessment data
- Top 10 student leaderboard

Exported data respects the currently selected dashboard filters.

---

## 🛠️ Technologies Used

| Technology | Purpose |
|---|---|
| Python | Core programming language |
| Pandas | Data processing and analysis |
| NumPy | Numerical operations |
| Plotly | Interactive visualizations |
| Streamlit | Dashboard development |
| CSV | Dataset storage |

---

## 📂 Project Structure

```text
Student_Skill_Assessment_Dashboard/
│
├── app.py
├── data_analysis.py
├── student_skill_assessment.csv
├── student_skill_assessment.xlsx
├── README.md
└── requirements.txt