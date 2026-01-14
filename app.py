import streamlit as st
import pandas as pd

st.set_page_config(page_title="GITAM SGPA & CGPA Calculator", layout="centered")

st.title("🎓 GITAM SGPA & CGPA Calculator")
st.caption("Marks → Grade Point → Weighted GP → SGPA → CGPA")

# ---------- MARKS → GRADE POINT (ABSOLUTE SCALE) ----------
def marks_to_gp(marks):
    if marks >= 90: return 10
    elif marks >= 80: return 9
    elif marks >= 70: return 8
    elif marks >= 60: return 7
    elif marks >= 50: return 6
    elif marks >= 40: return 5
    elif marks >= 33: return 4
    else: return 0

# ---------- WGP → FINAL GRADE ----------
def wgp_to_final(wgp):
    if wgp > 9: return "O", 10
    elif wgp > 8: return "A+", 9
    elif wgp > 7: return "A", 8
    elif wgp > 6: return "B+", 7
    elif wgp > 5: return "B", 6
    elif wgp > 4: return "C", 5
    elif wgp == 4: return "P", 4
    else: return "F", 0

# ---------- INPUT ----------
num_courses = st.number_input("Number of Courses", min_value=1, step=1)
courses = []

for i in range(int(num_courses)):
    st.subheader(f"📘 Course {i+1}")

    subject = st.text_input("Subject Name", key=f"name{i}")
    credits = st.number_input("Credits", min_value=0.0, step=0.5, key=f"cred{i}")

    course_type = st.selectbox(
        "Course Type",
        ["Theory (T)", "Practical (P)", "Combined (TP)"],
        key=f"type{i}"
    )

    # ---------- THEORY ----------
    if course_type == "Theory (T)":
        s1 = st.number_input("Sessional 1 Marks (30)", 0, 30, key=f"s1{i}")
        s2 = st.number_input("Sessional 2 Marks (45)", 0, 45, key=f"s2{i}")
        le_gp = st.number_input("Learning Engagement Grade Point", 0.0, 10.0, step=0.1, key=f"le{i}")

        gp_s1 = marks_to_gp((s1 / 30) * 100)
        gp_s2 = marks_to_gp((s2 / 45) * 100)

        theory_wgp = (gp_s1 * 0.30) + (gp_s2 * 0.45) + (le_gp * 0.25)
        grade, final_gp = wgp_to_final(theory_wgp)

    # ---------- PRACTICAL ----------
    elif course_type == "Practical (P)":
        p_marks = st.number_input("Practical Marks (100)", 0, 100, key=f"p{i}")
        final_gp = marks_to_gp(p_marks)
        grade, final_gp = wgp_to_final(final_gp)

    # ---------- COMBINED TP ----------
    else:
        st.markdown("**Theory Component**")
        s1 = st.number_input("Sessional 1 Marks (30)", 0, 30, key=f"tp_s1{i}")
        s2 = st.number_input("Sessional 2 Marks (45)", 0, 45, key=f"tp_s2{i}")
        le_gp = st.number_input("Learning Engagement Grade Point", 0.0, 10.0, step=0.1, key=f"tp_le{i}")

        gp_s1 = marks_to_gp((s1 / 30) * 100)
        gp_s2 = marks_to_gp((s2 / 45) * 100)
        theory_wgp = (gp_s1 * 0.30) + (gp_s2 * 0.45) + (le_gp * 0.25)

        st.markdown("**Practical Component**")
        p_marks = st.number_input("Practical Marks (100)", 0, 100, key=f"tp_p{i}")
        practical_gp = marks_to_gp(p_marks)

        final_wgp = (theory_wgp * 0.70) + (practical_gp * 0.30)
        grade, final_gp = wgp_to_final(final_wgp)

    courses.append({
        "Subject": subject,
        "Type": course_type,
        "Credits": credits,
        "Grade": grade,
        "Grade Point": round(final_gp, 2),
        "Weighted Points": round(final_gp * credits, 2)
    })

# ---------- RESULTS ----------
st.divider()
st.header("📋 Semester Summary")

if courses:
    df = pd.DataFrame(courses)
    st.dataframe(df, use_container_width=True)

    total_credits = df["Credits"].sum()
    total_points = df["Weighted Points"].sum()

    if total_credits > 0:
        sgpa = total_points / total_credits
        st.success(f"🎯 **SGPA: {sgpa:.2f}**")

# ---------- CGPA ----------
st.divider()
st.header("📊 CGPA Calculator")

prev_credits = st.number_input("Previous Total Credits", min_value=0.0)
prev_cgpa = st.number_input("Previous CGPA", min_value=0.0, max_value=10.0)

if st.button("Calculate CGPA"):
    combined_credits = prev_credits + total_credits
    combined_points = (prev_cgpa * prev_credits) + total_points

    if combined_credits > 0:
        cgpa = combined_points / combined_credits
        st.success(f"🏆 **CGPA: {cgpa:.2f}**")
