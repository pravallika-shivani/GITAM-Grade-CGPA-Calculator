import streamlit as st

st.set_page_config(page_title="GITAM Grade, SGPA & CGPA Calculator", layout="centered")

st.title("🎓 GITAM Grade, SGPA & CGPA Calculator")
st.caption("As per Evaluation Policy 2025–26 (Absolute grading based MVP)")

# ------------------ GRADE FUNCTIONS ------------------

def absolute_grade(marks, is_practical=False):
    if is_practical and marks < 50:
        return "F", 0

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
    elif marks >= 41:
        return "C", 5
    elif marks >= 33:
        return "P", 4
    else:
        return "F", 0


def final_grade_from_wgp(wgp):
    if wgp > 9:
        return "O", 10
    elif wgp > 8:
        return "A+", 9
    elif wgp > 7:
        return "A", 8
    elif wgp > 6:
        return "B+", 7
    elif wgp > 5:
        return "B", 6
    elif wgp > 4:
        return "C", 5
    elif wgp == 4:
        return "P", 4
    else:
        return "F", 0


# ------------------ COURSE INPUT ------------------

num_courses = st.number_input("Number of Courses", min_value=1, step=1)

total_credits = 0
total_weighted_points = 0

st.divider()

for i in range(int(num_courses)):
    st.subheader(f"📘 Course {i+1}")

    course_type = st.selectbox(
        "Course Type",
        ["Theory (T)", "Practical (P)", "Combined (TP)"],
        key=f"type{i}"
    )

    credits = st.number_input("Credits", min_value=0.0, step=0.5, key=f"cred{i}")

    course_gp = 0
    course_grade = "F"

    # ---------------- THEORY ----------------
    if course_type == "Theory (T)":
        s1 = st.number_input("Sessional 1 Marks (out of 30)", 0, 30, key=f"s1{i}")
        s2 = st.number_input("Sessional 2 Marks (out of 45)", 0, 45, key=f"s2{i}")
        le = st.number_input("Learning Engagement Marks (out of 25)", 0, 25, key=f"le{i}")

        if (s1 + s2) < 25:
            course_grade, course_gp = "F", 0
        else:
            _, gp_s1 = absolute_grade((s1 / 30) * 100)
            _, gp_s2 = absolute_grade((s2 / 45) * 100)
            _, gp_le = absolute_grade((le / 25) * 100)

            wgp = (gp_s1 * 0.30) + (gp_s2 * 0.45) + (gp_le * 0.25)
            course_grade, course_gp = final_grade_from_wgp(wgp)

    # ---------------- PRACTICAL ----------------
    elif course_type == "Practical (P)":
        lab_marks = st.number_input("Practical / Lab Marks (out of 100)", 0, 100, key=f"lab{i}")
        course_grade, course_gp = absolute_grade(lab_marks, is_practical=True)

    # ---------------- COMBINED TP ----------------
    else:
        st.markdown("**Theory Component**")
        s1 = st.number_input("Sessional 1 (30)", 0, 30, key=f"tp_s1{i}")
        s2 = st.number_input("Sessional 2 (45)", 0, 45, key=f"tp_s2{i}")
        le = st.number_input("Learning Engagement (25)", 0, 25, key=f"tp_le{i}")

        st.markdown("**Practical Component**")
        lab_marks = st.number_input("Lab Marks (100)", 0, 100, key=f"tp_lab{i}")

        # Theory GP
        if (s1 + s2) < 25:
            theory_gp = 0
        else:
            _, gp_s1 = absolute_grade((s1 / 30) * 100)
            _, gp_s2 = absolute_grade((s2 / 45) * 100)
            _, gp_le = absolute_grade((le / 25) * 100)
            theory_gp = (gp_s1 * 0.30) + (gp_s2 * 0.45) + (gp_le * 0.25)

        # Practical GP
        _, practical_gp = absolute_grade(lab_marks, is_practical=True)

        if theory_gp == 0 or practical_gp == 0:
            course_grade, course_gp = "F", 0
        else:
            final_gp = (theory_gp * 0.70) + (practical_gp * 0.30)
            course_grade, course_gp = final_grade_from_wgp(final_gp)

    st.info(f"**Grade:** {course_grade} | **Grade Point:** {course_gp}")

    total_credits += credits
    total_weighted_points += credits * course_gp

# ---------------- SGPA ----------------

st.divider()
if total_credits > 0:
    sgpa = total_weighted_points / total_credits
    st.success(f"🎯 **SGPA: {sgpa:.2f}**")

# ---------------- CGPA ----------------

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
