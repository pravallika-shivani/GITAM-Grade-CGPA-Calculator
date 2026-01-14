import streamlit as st

st.set_page_config(page_title="Grade & CGPA Calculator", layout="centered")

st.title("🎓 Grade, SGPA & CGPA Calculator")

st.markdown("Supports **Theory, Practical, and TP (70:30)** courses")

# ---------- Grade Mapping ----------
def grade_point(marks):
    if marks >= 90:
        return "O", 10
    elif marks >= 80:
        return "A+", 9
    elif marks >= 70:
        return "A", 8
    elif marks >= 60:
        return "B+", 7
    elif marks >= 50:
        return "B", 6
    elif marks >= 40:
        return "C", 5
    else:
        return "F", 0

# ---------- Course Input ----------
num_courses = st.number_input("Number of Courses", min_value=1, step=1)

total_credits = 0
total_weighted_points = 0

st.divider()

for i in range(int(num_courses)):
    st.subheader(f"Course {i+1}")

    col1, col2 = st.columns(2)
    with col1:
        course_type = st.selectbox(
            "Course Type",
            ["Theory (T)", "Practical (P)", "TP (70% Theory + 30% Practical)"],
            key=f"type{i}"
        )
    with col2:
        credits = st.number_input("Credits", min_value=0.0, step=0.5, key=f"cred{i}")

    if course_type == "TP (70% Theory + 30% Practical)":
        t_marks = st.number_input("Theory Marks", 0, 100, key=f"tm{i}")
        p_marks = st.number_input("Practical Marks", 0, 100, key=f"pm{i}")
        final_marks = 0.7 * t_marks + 0.3 * p_marks
    else:
        final_marks = st.number_input("Marks", 0, 100, key=f"m{i}")

    grade, gp = grade_point(final_marks)

    st.write(f"**Final Marks:** {final_marks:.2f}")
    st.write(f"**Grade:** {grade} | **Grade Point:** {gp}")

    total_credits += credits
    total_weighted_points += credits * gp

st.divider()

# ---------- SGPA ----------
if total_credits > 0:
    sgpa = total_weighted_points / total_credits
    st.success(f"🎯 **SGPA: {sgpa:.2f}**")

# ---------- CGPA ----------
st.divider()
st.header("📊 CGPA Calculator")

prev_credits = st.number_input("Previous Total Credits", min_value=0.0)
prev_cgpa = st.number_input("Previous CGPA", min_value=0.0, max_value=10.0)

if st.button("Calculate CGPA"):
    combined_credits = prev_credits + total_credits
    combined_points = (prev_credits * prev_cgpa) + total_weighted_points

    if combined_credits > 0:
        cgpa = combined_points / combined_credits
        st.success(f"🏆 **CGPA: {cgpa:.2f}**")
