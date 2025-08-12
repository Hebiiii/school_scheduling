import streamlit as st
import pandas as pd
import re
from _functions import assign_course, assign_fixed_course, assign_joint_course

# ====== Constants ======
subjects = ["国語", "算数", "英語", "理科", "社会", "総合", "学活・道徳", "図工", "音楽", "体育", "家庭科", "生活", "書写"]
subject_symbols = {
    "国語": "📚",
    "算数": "📐",
    "英語": "🌍",
    "理科": "🧪",
    "社会": "🏛️",
    "総合": "🤔",
    "書写": "🖌️",
    "学活・道徳": "🗣️",
    "図工": "🎨",
    "音楽": "🎵",
    "体育": "🤸‍♂️",
    "家庭科": "🍲",
    "生活": "🤔",
}

# default number of weekly periods for each subject by grade
default_periods = {
    1: {"英語": 0, "算数": 4, "国語": 9, "理科": 0, "社会": 0, "図工": 2, "音楽": 2, "体育": 3,
        "家庭科": 0, "総合": 0, "学活・道徳": 1, "生活": 3, "書写": 0},
    2: {"英語": 0, "算数": 5, "国語": 9, "理科": 0, "社会": 0, "図工": 2, "音楽": 2, "体育": 3,
        "家庭科": 0, "総合": 0, "学活・道徳": 1, "生活": 3, "書写": 0},
    3: {"英語": 0, "算数": 5, "国語": 7, "理科": 2, "社会": 2, "図工": 1, "音楽": 2, "体育": 3,
        "家庭科": 0, "総合": 2, "学活・道徳": 1, "生活": 0, "書写": 1},
    4: {"英語": 0, "算数": 5, "国語": 7, "理科": 2, "社会": 2, "図工": 2, "音楽": 2, "体育": 3,
        "家庭科": 0, "総合": 2, "学活・道徳": 1, "生活": 0, "書写": 1},
    5: {"英語": 1, "算数": 5, "国語": 5, "理科": 3, "社会": 3, "図工": 1, "音楽": 1, "体育": 3,
        "家庭科": 2, "総合": 2, "学活・道徳": 1, "生活": 0, "書写": 1},
    6: {"英語": 1, "算数": 5, "国語": 5, "理科": 3, "社会": 3, "図工": 1, "音楽": 1, "体育": 3,
        "家庭科": 2, "総合": 2, "学活・道徳": 1, "生活": 0, "書写": 1},
}

teacher_options = {
    "英語": ["担任", "副担任", "英語教員(ALT)"],
    "算数": ["担任", "副担任", "算数教員"],
    "国語": ["担任", "副担任"],
    "理科": ["担任", "副担任", "理科教員"],
    "社会": ["担任", "副担任"],
    "図工": ["担任", "副担任", "図工教員"],
    "音楽": ["担任", "副担任", "音楽教員"],
    "体育": ["担任", "副担任", "体育教員"],
    "家庭科": ["担任", "副担任", "家庭科教員"],
    "総合": ["担任", "副担任"],
    "学活・道徳": ["担任", "副担任"],
    "生活": ["担任", "副担任", "生活教員"],
    "書写": ["担任", "副担任", "書写教員"],
}

room_options = {
    "英語": ["教室", "特別教室"],
    "算数": ["教室", "特別教室"],
    "国語": ["教室", "特別教室"],
    "理科": ["教室", "理科室"],
    "社会": ["教室", "社会科室"],
    "図工": ["教室", "図工室"],
    "音楽": ["教室", "音楽室①", "音楽室②"],
    "体育": ["教室", "体育館"],
    "家庭科": ["教室", "家庭科室"],
    "総合": ["教室", "特別教室"],
    "学活・道徳": ["教室", "特別教室"],
    "生活": ["教室", "特別教室"],
    "書写": ["教室", "特別教室"],
}

week = ["月", "火", "水", "木", "金"]
periods = [1, 2, 3, 4, 5, 6]

default_six_days = {
    1: ["なし"],
    2: ["水"],
    3: ["火"],
    4: ["火", "水", "木", "金"],
    5: ["火", "水", "木", "金"],
    6: ["火", "水", "木", "金"],
}

# ====== UI helper utilities ======
def input_basic_info(grade: int):
    st.markdown(f"#### {grade}年生")
    class_num = st.number_input(
        "クラス数は？",
        min_value=1,
        value=3,
        step=1,
        key=f"{grade}_class_num",
    )
    six_days = st.multiselect(
        "6限授業の日を全て選んでください",
        options=["なし"] + week,
        default=default_six_days[grade],
        key=f"{grade}_six_days",
    )
    if "なし" in six_days:
        if len(six_days) > 1:
            st.error('"なし"と他の曜日を同時に選択できません')
        six_days = []
    if len(six_days) == 0 and st.session_state.get(f"{grade}_six_days") == []:
        st.error('6限まで授業がある日を選択してください')
    return class_num, six_days


def get_available_day_periods(six_days):
    available = []
    for day in week:
        max_period = 6 if day in six_days else 5
        for p in periods[:max_period]:
            available.append((day, p))
    return available


# ====== Timetable generation ======
def build_base_df(grade_info):
    rows = []
    for grade, info in grade_info.items():
        classes = range(1, info["class_num"] + 1)
        six_days = set(info["six_days"])
        for cls in classes:
            for day in week:
                max_p = 6 if day in six_days else 5
                for period in periods[:max_p]:
                    rows.append([grade, cls, day, period, "", "", ""])
    return pd.DataFrame(
        rows, columns=["grade", "class", "day", "period", "subject", "teacher", "room"]
    )


def class_specific_labels(teacher: str, room: str, grade: int, cls: int):
    """Return teacher and room labels unique to each class.

    Placeholder names like "担任" or "教室" are prefixed with the
    grade and class number (e.g. 1-1担任). Other names are left
    unchanged so that shared specialists can be represented properly.
    """
    teacher_parts = []
    for t in teacher.split("/"):
        t = t.strip()
        if t in {"担任", "副担任"}:
            teacher_parts.append(f"{grade}-{cls}{t}")
        else:
            teacher_parts.append(t)
    teacher_label = "/".join(teacher_parts)

    if room == "教室":
        room_label = f"{grade}-{cls}{room}"
    else:
        room_label = room

    return teacher_label, room_label


def joint_labels(teacher: str, room: str, grade: int, classes):
    """Return labels for joint lessons spanning multiple classes."""
    teacher_parts = []
    for t in teacher.split("/"):
        t = t.strip()
        if t in {"担任", "副担任"}:
            teacher_parts.extend(f"{grade}-{c}{t}" for c in classes)
        else:
            teacher_parts.append(t)
    teacher_label = "/".join(teacher_parts)

    if room == "教室":
        room_label = "/".join(f"{grade}-{c}教室" for c in classes)
    else:
        room_label = room

    return teacher_label, room_label


def validate_settings(grade_info, subject_settings):
    """Validate if the requested periods fit into the timetable.

    For each grade we ensure that the total number of requested periods does not
    exceed the available slots (5 days * 5 periods + days with a 6th period).
    We also validate that per-subject settings such as joint lessons, fixed
    slots and consecutive lessons do not exceed the total number of periods
    requested for that subject.
    """

    for grade, info in grade_info.items():
        available = 5 * 5 + len(info["six_days"])
        required = sum(s["num"] for s in subject_settings[grade].values())
        if required > available:
            raise ValueError(
                f"{grade}年生のコマ数({required})が利用可能な{available}コマを超えています"
            )

        for subject, s in subject_settings[grade].items():
            num = s["num"]
            joint = s["joint"]
            fixed = len(s["day_periods"])
            consecutive = s["consecutive"]

            if joint > num:
                raise ValueError(
                    f"{grade}年生 {subject}: 合同授業の回数({joint})がコマ数({num})を超えています"
                )
            if fixed > num:
                raise ValueError(
                    f"{grade}年生 {subject}: 指定された曜日・時限の数({fixed})がコマ数({num})を超えています"
                )
            if joint + fixed + 2 * consecutive > num:
                raise ValueError(
                    f"{grade}年生 {subject}: コマ数に対して合同授業・固定・連続授業の設定が多すぎます"
                )


def generate_timetable(grade_info, subject_settings):
    validate_settings(grade_info, subject_settings)
    df = build_base_df(grade_info).copy()

    # 1. Assign courses with fixed (day, period)
    for grade, subjects in subject_settings.items():
        classes = range(1, grade_info[grade]["class_num"] + 1)
        for cls in classes:
            for subject, info in subjects.items():
                if info["num"] <= 0:
                    continue
                day_periods = info["day_periods"]
                if day_periods:
                    teacher, room = class_specific_labels(
                        info["teacher"], info["room"], grade, cls
                    )
                    df = assign_fixed_course(
                        df,
                        grade,
                        cls,
                        subject,
                        teacher,
                        room,
                        day_periods,
                    )

    # 2. Assign joint classes
    for grade, subjects in subject_settings.items():
        classes = range(1, grade_info[grade]["class_num"] + 1)
        for subject, info in subjects.items():
            for _ in range(info["joint"]):
                group = [(grade, c) for c in classes]
                teacher, room = joint_labels(
                    info["teacher"], info["room"], grade, classes
                )
                df = assign_joint_course(
                    df, subject, group, teacher=teacher, room=room
                )

    # 3. Assign consecutive lessons
    for grade, subjects in subject_settings.items():
        classes = range(1, grade_info[grade]["class_num"] + 1)
        for cls in classes:
            for subject, info in subjects.items():
                num = info["num"]
                if num <= 0:
                    continue
                remaining = num - info["joint"] - len(info["day_periods"])
                if remaining <= 0:
                    continue
                consecutive = info["consecutive"]
                if consecutive:
                    teacher, room = class_specific_labels(
                        info["teacher"], info["room"], grade, cls
                    )
                    df = assign_course(
                        df,
                        grade,
                        cls,
                        subject,
                        teacher,
                        room,
                        num_slots=consecutive,
                        consecutive=True,
                        allow_same_day=num >= 4,
                    )

    # 4. Assign lessons with period limits
    for grade, subjects in subject_settings.items():
        classes = range(1, grade_info[grade]["class_num"] + 1)
        for cls in classes:
            for subject, info in subjects.items():
                num = info["num"]
                if num <= 0:
                    continue
                remaining = (
                    num
                    - info["joint"]
                    - len(info["day_periods"])
                    - 2 * info["consecutive"]
                )
                if remaining <= 0:
                    continue
                period_limit = info["period_limit"]
                if period_limit:
                    teacher, room = class_specific_labels(
                        info["teacher"], info["room"], grade, cls
                    )
                    df = assign_course(
                        df,
                        grade,
                        cls,
                        subject,
                        teacher,
                        room,
                        num_slots=remaining,
                        period_limit=period_limit,
                        allow_same_day=(num >= 4),
                    )

    # 5. Assign remaining lessons normally
    for grade, subjects in subject_settings.items():
        sorted_subjects = sorted(
            subjects.items(), key=lambda item: item[1]["num"]
        )
        for subject, info in sorted_subjects:
            for cls in range(1, grade_info[grade]["class_num"] + 1):
                num = info["num"]
                if num <= 0:
                    continue
                remaining = (
                    num
                    - info["joint"]
                    - len(info["day_periods"])
                    - 2 * info["consecutive"]
                )
                if remaining <= 0 or info["period_limit"]:
                    continue
                teacher, room = class_specific_labels(
                    info["teacher"], info["room"], grade, cls
                )
                df = assign_course(
                    df,
                    grade,
                    cls,
                    subject,
                    teacher,
                    room,
                    num_slots=remaining,
                    allow_same_day=(num >= 4),
                )

    return df


# ====== Main UI ======
def main():
    st.set_page_config(page_title="elementary_school_scheduling", layout="wide")
    st.title("\U0001F4C5 小学校時間割作成アプリ")
    st.markdown("---")

    grades = [1, 2, 3, 4, 5, 6]
    grade_info = {}

    st.subheader("基本情報入力")
    cols = st.columns(len(grades))
    for col, grade in zip(cols, grades):
        with col:
            class_num, six_days = input_basic_info(grade)
            grade_info[grade] = {"class_num": class_num, "six_days": six_days}

    available_day_periods = {g: get_available_day_periods(info["six_days"]) for g, info in grade_info.items()}

    st.markdown("---")
    st.subheader("教科ごとの設定")
    st.markdown(
        """
        <style>
        div[data-testid="stColumn"]:has(input[aria-label="コマ数"][value="0"]) {
            background-color: #EEEEEE;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )
    with st.form("settings_form", border=False):
        for subject in subjects:
            st.markdown("---")
            st.subheader(f"{subject_symbols[subject]} {subject}")
            cols = st.columns(len(grades))
            for col, grade in zip(cols, grades):
                with col:
                    st.markdown(f"**{grade}年**")
                    num = st.number_input(
                        "コマ数",
                        min_value=0,
                        value=default_periods[grade][subject],
                        key=f"{grade}_{subject}_num",
                    )
                    teacher = st.multiselect(
                        "担当教員",
                        teacher_options[subject],
                        default=["担任"],
                        key=f"{grade}_{subject}_teacher",
                    )
                    room = st.selectbox(
                        "教室",
                        room_options[subject],
                        key=f"{grade}_{subject}_room",
                    )
                    with st.popover("詳細設定"):
                        day_period = st.multiselect(
                            "曜日・時限の指定",
                            options=[f"{d}曜 {p}限" for d, p in available_day_periods[grade]] + ["なし"],
                            default=["なし"],
                            max_selections=num if num else None,
                            key=f"{grade}_{subject}_day_period",
                        )
                        period_limit = st.select_slider(
                            "時限制限",
                            options=[f"{p}限" for p in periods],
                            value=("1限","6限"),
                            key=f"{grade}_{subject}_period_limit",
                        )
                        if num == 2:
                            st.checkbox(
                                "連続授業にする",
                                value=False,
                                key=f"{grade}_{subject}_consecutive_bool",
                            )
                        elif num > 2:
                            st.number_input(
                                "週何回連続授業にする？",
                                value=0,
                                min_value=0,
                                max_value=num // 2,
                                step=1,
                                key=f"{grade}_{subject}_consecutive_num",
                            )
                        st.number_input(
                            "週何回クラス合同授業にする？",
                            value=0,
                            min_value=0,
                            max_value=num,
                            step=1,
                            key=f"{grade}_{subject}_joint_class",
                        )

        st.markdown("---")
        st.markdown("#### 選択された合計のコマ数/総コマ数")
        summary_cols = st.columns(len(grades))
        for col, grade in zip(summary_cols, grades):
            total_selected = sum(
                st.session_state.get(f"{grade}_{subject}_num", 0)
                for subject in subjects
            )
            total_slots = 25 + len(grade_info[grade]["six_days"])
            with col:
                st.markdown(f"{grade}年: {total_selected}/{total_slots}")

        st.markdown("---")
        submitted = st.form_submit_button("時間割りを作成する")

    if submitted:
        subject_settings = {}
        for grade in grades:
            subject_settings[grade] = {}
            for subject in subjects:
                num = st.session_state[f"{grade}_{subject}_num"]
                teacher = "/".join(st.session_state[f"{grade}_{subject}_teacher"])
                room = st.session_state[f"{grade}_{subject}_room"]
                day_raw = st.session_state[f"{grade}_{subject}_day_period"]
                day_periods = []
                if "なし" not in day_raw:
                    for dp in day_raw:
                        d, rest = dp.split("曜 ")
                        day_periods.append((d, int(rest.replace("限", ""))))
                period_raw = st.session_state[f"{grade}_{subject}_period_limit"]
                start = int(period_raw[0].replace("限", ""))
                end = int(period_raw[1].replace("限", ""))
                if start == 1 and end == 6:
                    period_limit = None
                else:
                    period_limit = list(range(start, end + 1))
                
                if num == 2:
                    consecutive = 1 if st.session_state.get(f"{grade}_{subject}_consecutive_bool") else 0
                elif num > 2:
                    consecutive = st.session_state.get(f"{grade}_{subject}_consecutive_num", 0)
                else:
                    consecutive = 0
                joint = st.session_state[f"{grade}_{subject}_joint_class"]
                subject_settings[grade][subject] = {
                    "num": num,
                    "teacher": teacher,
                    "room": room,
                    "day_periods": day_periods,
                    "period_limit": period_limit,
                    "consecutive": consecutive,
                    "joint": joint,
                }
        try:
            df = generate_timetable(grade_info, subject_settings)
            st.success("時間割を生成しました")
            st.dataframe(df)
            csv = df.to_csv(index=False).encode("utf-8-sig")
            st.download_button("CSVをダウンロード", csv, "timetable.csv", "text/csv")
        except RuntimeError as e:
            msg = str(e)
            m = re.search(r"Slot \((.+), (\d+)\) for (\d+)-(\d+) (.+)", msg)
            if m:
                day, period, grade, cls, reason = m.groups()
                if "already filled" in reason:
                    st.error(
                        f"{grade}年{cls}組の{day}曜{period}限には既に他の授業が設定されています。"
                    )
                elif "not in schedule" in reason:
                    st.error(
                        f"{grade}年{cls}組の{day}曜{period}限は時間割に存在しません。"
                    )
                else:
                    st.error(f"エラー: {msg}")
            else:
                st.error(f"エラー: {msg}")
        except Exception as e:
            st.error(f"エラー: {e}")


if __name__ == "__main__":
    main()
