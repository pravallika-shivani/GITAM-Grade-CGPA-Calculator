import streamlit as st
import pandas as pd

st.set_page_config(page_title="GITAM SGPA & CGPA Calculator", layout="centered")

st.title("🎓 GITAM SGPA & CGPA Calculator")
st.caption("Relative Grading | Evaluation Policy 2025–26")

# ------------------ FINAL GRADE FROM WGP ------------------

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

courses = []

st.divider()

for i in range(int(num_courses)):
    st.subheader(f"📘 Course {i+1}")

    subject = st.text_input("Subject Name", key=f"name{i}")

    course_type = st.selectbox(
        "Course Type",
        ["Theory (T)", "Practical (P)", "Combined (TP)"],
        key=f"type{i}"
    )

    credits = st.number_input("Credits", min_value=0.0, step=0.5, key=f"cred{i}")

    final_gp = 0
    final_grade = "F"

    # -------- THEORY --------
    if course_type == "Theory (T)":
        gp_s1 = st.number_input("Sessional 1 Grade Point", 0.0, 10.0, step=0.1, key=f"s1{i}")
        gp_s2 = st.number_input("Sessional 2 Grade Point", 0.0, 10.0, step=0.1, key=f"s2{i}")
        gp_le = st.number_input("Learning Engagement Grade Point", 0.0, 10.0, step=0.1, key=f"le{i}")

        wgp = (gp_s1 * 0.30) + (gp_s2 * 0.45) + (gp_le * 0.25)
        final_grade, final_gp = final_grade_from_wgp(wgp)

    # -------- PRACTICAL --------
    elif course_type == "Practical (P)":
        final_gp = st.number_input("Practical Grade Point", 0.0, 10.0, step=0.1, key=f"p{i}")
        final_grade, final_gp = final_grade_from_wgp(final_gp)

    # -------- COMBINED TP --------
    else:
        st.markdown("**Theory Component (Weighted GP)**")
        theory_gp = st.number_input("Theory Grade Point", 0.0, 10.0, step=0.1, key=f"tpgp{i}")

        st.markdown("**Practical Component**")
        practical_gp = st.number_input("Practical Grade Point", 0.0, 10.0, step=0.1, key=f"tplab{i}")

        combined_gp = (theory_gp * 0.70) + (practical_gp * 0.30)
        final_grade, final_gp = final_grade_from_wgp(combined_gp)

    courses.append({
        "Subject": subject,
        "Type": course_type,
        "Credits": credits,
        "Grade": final_grade,
        "Grade Point": round(final_gp, 2),
        "Weighted Points": round(final_gp * credits, 2)
    })

# ------------------ RESULTS TABLE ------------------

st.divider()
st.header("📋 Semester Result Summary")

if courses:
    df = pd.DataFrame(courses)
    st.dataframe(df, use_container_width=True)

    total_credits = df["Credits"].sum()
    total_points = df["Weighted Points"].sum()

    if total_credits > 0:
        sgpa = total_points / total_credits
        st.success(f"🎯 **SGPA: {sgpa:.2f}**")

# ------------------ CGPA ------------------

st.divider()
st.header("📊 CGPA Calculator")

prev_credits = st.number_input("Previous Total Credits", min_value=0.0)
prev_cgpa = st.number_input("Previous CGPA", min_value=0.0, max_value=10.0)

if st.button("Calculate CGPA"):
    combined_credits = prev_credits + total_credits
    combined_points = (prev_credits * prev_cgpa) + total_points

    if combined_credits > 0:
        cgpa = combined_points / combined_credits
        st.success(f"🏆 **CGPA: {cgpa:.2f}**")
