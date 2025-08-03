import streamlit as st

part1_err = False
########### Subjects ###############
subject_list = ["英語","算数","国語","理科","社会","図工","音楽","体育","家庭科","総合","学活・道徳","生活","書写"] #教科名
# multi_period_subject_list = ["体育","理科","総合"] #2コマ連続授業の教科名

subject_symbol_dict = {
    "英語": "🌍",
    "算数": "📐",
    "国語": "📚",
    "理科": "🧪",
    "社会": "🏛️",
    "図工": "🎨",
    "音楽": "🎵",
    "体育": "🤸‍♂️",
    "家庭科": "🍲",
    "総合": "🤔",
    "学活・道徳": "🗣️",
    "生活": "🤔",
    "書写": "🖌️"
}

default_grade_subject_dict = {
    1:{
        "英語":0,
        "算数":4,
        "国語":9,
        "理科":0,
        "社会":0,
        "図工":2,
        "音楽":2,
        "体育":3,
        "家庭科":0,
        "総合":0,
        "学活・道徳":1,
        "生活":3,
        "書写":0},
    2:{
        "英語":0,
        "算数":5,
        "国語":9,
        "理科":0,
        "社会":0,
        "図工":2,
        "音楽":2,
        "体育":3,
        "家庭科":0,
        "総合":0,
        "学活・道徳":1,
        "生活":3,
        "書写":0},
    3:{
        "英語":0,
        "算数":5,
        "国語":7,
        "理科":2,
        "社会":2,
        "図工":2,
        "音楽":2,
        "体育":3,
        "家庭科":0,
        "総合":2,
        "学活・道徳":1,
        "生活":0,
        "書写":1},
    4:{
        "英語":0,
        "算数":5,
        "国語":7,
        "理科":2,
        "社会":2,
        "図工":2,
        "音楽":2,
        "体育":3,
        "家庭科":0,
        "総合":2,
        "学活・道徳":1,
        "生活":0,
        "書写":1},
    5:{
        "英語":1,
        "算数":5,
        "国語":5,
        "理科":3,
        "社会":3,
        "図工":1,
        "音楽":1,
        "体育":3,
        "家庭科":2,
        "総合":2,
        "学活・道徳":1,
        "生活":0,
        "書写":1},
    6:{
        "英語":1,
        "算数":5,
        "国語":5,
        "理科":3,
        "社会":3,
        "図工":1,
        "音楽":1,
        "体育":3,
        "家庭科":2,
        "総合":2,
        "学活・道徳":1,
        "生活":0,
        "書写":1}
    }

subject_teacher_option_dict = {
    "英語":["担任", "副担任", "英語教員(ALT)"],
    "算数":["担任", "副担任", "算数教員"],
    "国語":["担任", "副担任"],
    "理科":["担任", "副担任", "理科教員"],
    "社会":["担任", "副担任"],
    "図工":["担任", "副担任", "図工教員"],
    "音楽":["担任", "副担任", "音楽教員"],
    "体育":["担任", "副担任", "体育教員"],
    "家庭科":["担任", "副担任", "家庭科教員"],
    "総合": ["担任", "副担任"],
    "学活・道徳":["担任", "副担任"],
    "生活":["担任", "副担任", "生活教員"],
    "書写": ["担任", "副担任", "書写教員"]
}

subject_room_option_dict = {
    "英語":["教室", "特別教室"],
    "算数":["教室", "特別教室"],
    "国語":["教室", "特別教室"],
    "理科":["教室", "理科室"],
    "社会":["教室", "社会科室"],
    "図工":["教室", "図工室"],
    "音楽":["教室", "音楽室①", "音楽室②"],
    "体育": ["教室", "体育館"],
    "家庭科":["教室", "家庭科室"],
    "総合": ["教室", "特別教室"],
    "学活・道徳": ["教室", "特別教室"],
    "生活": ["教室", "特別教室"],
    "書写": ["教室", "特別教室"]
}

########### Day-Period ###############
week = ["月","火","水","木","金"]
period_list = [1,2,3,4,5,6]

#####################################
def make_class_teacher_and_room_dict(grade, grade_class_list):
    grade_class_teacher_dict = {}
    grade_class_room_dict = {}
    for cls in grade_class_list:
        grade_class_teacher_dict[cls] = f"{grade}-{cls}担任"
        grade_class_room_dict[cls] = f"{grade}-{cls}教室"
    
    return grade_class_teacher_dict, grade_class_room_dict

def basic_info_input(grade, default):
    st.header(f"{grade}年生")
    err = False

    # 基本情報(クラス数と6限まで授業がある日)の入力
    with st.container(border=True):
        st.subheader("基本情報入力")
        subcol1, subcol2 = st.columns(2)
        with subcol1:
            grade_class_num = st.number_input(
                "クラス数は？",
                min_value=1,
                value=3,
                step=1,
                key=f"{grade}_grade_class_num"  
            )
        with subcol2:
            # multiselect の key も追加
            grade_selected_6_period_days = st.multiselect(
                label="6限まで授業がある日を選んでください",
                options=["なし", "月", "火", "水", "木", "金"],
                default=default,
                max_selections=5,
                placeholder="選択してください",
                key=f"{grade}_selected_6_period_days"  
            )
            if len(grade_selected_6_period_days) > 1 and "なし" in grade_selected_6_period_days:
                st.error('"なし"と他の曜日を選ぶことはできません')
                err = True
            elif len(grade_selected_6_period_days) < 1:
                st.error('6限まで授業がある日に値を入力してください。(ないのであれば、"なし"を選択)')
                err = True
    return grade_class_num, grade_selected_6_period_days, err

def subject_info_input(grade, subject, available_day_periods):
    st.write(f"{subject_symbol_dict[subject]} **{subject}**")
    col1, col2, col3 = st.columns([1,2,3])
    consecutive = False

    with col1:
        num_per_week = st.number_input(
            "週何コマ？", 
            value=default_grade_subject_dict[grade][subject], 
            min_value=0, 
            placeholder="値を入力してください",
            key=f"{grade}_{subject}_num_per_week"
        )
        
    with col2:
        teacher_for = st.multiselect(
            label="担当教員は？", 
            default="担任", 
            options=subject_teacher_option_dict[subject], 
            placeholder="選択してください",
            key=f"{grade}_{subject}_teacher_for"
        )
    with col3:
        room_for = st.segmented_control(
            label="普段使う教室は？", 
            options=subject_room_option_dict[subject], 
            default="教室",
            key=f"{grade}_{subject}_room_for" 
        )

        with st.popover("詳細設定"):
            st.write("**曜日・時限の指定**")
            days_period = st.multiselect(
                label="指定する曜日と時限は？", 
                options=[f"{d}曜 {p}限" for d,p in available_day_periods] + ["なし"],
                default=["なし"],
                max_selections=num_per_week,
                placeholder="選択してください",
                key=f"{grade}_{subject}_days_period"
            )

            st.write("**時限制限の設定**")
            period_limit = st.multiselect(
                label="時限制限は？", 
                options=["なし"] + [f"{p}限" for p in period_list],
                default=["なし"],
                max_selections=len(period_list),
                placeholder="選択してください",
                key=f"{grade}_{subject}_period_limit"
            )

            if num_per_week == 2:
                consecutive = st.checkbox(
                    "連続授業にする", 
                    value=False,
                    key=f"{grade}_{subject}_consecutive_bool"
                )
            elif num_per_week > 2:
                consecutive = st.number_input(
                    "週何回連続授業にする？", 
                    value=0, 
                    max_value=num_per_week//2, 
                    placeholder="値を入力してください",
                    key=f"{grade}_{subject}_consecutive_num"
                )

            st.write("**クラス合同授業の設定**")
            joint_class = st.number_input(
                "週何回クラス合同授業にする？", 
                value=0, 
                max_value=num_per_week, 
                placeholder="値を入力してください",
                key=f"{grade}_{subject}_joint_class"
            )
        
    return num_per_week, teacher_for, room_for, days_period, period_limit, consecutive, joint_class


def main():
    st.set_page_config(page_title="elementary_school_scheduling", layout="wide")
    st.title("\U0001F4C5 小学校時間割作成アプリ")
    st.markdown("---")

    col1, col2, col3 = st.columns(3)

    with col1:
        first_grade_class_num, first_grade_selected_6_period_days, err = basic_info_input(grade=1, default="なし")
        
        first_grade_class = range(1, first_grade_class_num + 1)
        first_grade_class_teacher_dict, first_grade_class_room_dict = make_class_teacher_and_room_dict(grade=1, grade_class_list=first_grade_class)
        
        first_available_day_periods = []
        for day in week:
            if day in first_grade_selected_6_period_days:
                first_available_day_periods.extend([(day, period) for period in period_list])
            else:
                first_available_day_periods.extend([(day, period) for period in [1,2,3,4,5]])

        first_japanese_num_per_week, first_japanese_teacher_for, first_japanese_room_for, first_japanese_days_period, first_japanese_period_limit, first_japanese_consecutive, first_japanese_joint_class = subject_info_input(
            grade=1, 
            subject="国語", 
            available_day_periods=first_available_day_periods)

        st.write("---")

        first_math_num_per_week, first_math_teacher_for, first_math_room_for, first_math_days_period, first_math_period_limit, first_math_consecutive, first_math_joint_class = subject_info_input(
            grade=1, 
            subject="算数", 
            available_day_periods=first_available_day_periods)

        st.write("---")

        first_seikatsu_num_per_week, first_seikatsu_teacher_for, first_seikatsu_room_for, first_seikatsu_days_period, first_seikatsu_period_limit, first_seikatsu_consecutive, first_seikatsu_joint_class = subject_info_input(
            grade=1, 
            subject="生活", 
            available_day_periods=first_available_day_periods)

        st.write("---")

        first_music_num_per_week, first_music_teacher_for, first_music_room_for, first_music_days_period, first_music_period_limit, first_music_consecutive, first_music_joint_class = subject_info_input(
            grade=1, 
            subject="音楽", 
            available_day_periods=first_available_day_periods)

        st.write("---")

        first_zukou_num_per_week, first_zukou_teacher_for, first_zukou_room_for, first_zukou_days_period, first_zukou_period_limit, first_zukou_consecutive, first_zukou_joint_class = subject_info_input(
            grade=1, 
            subject="図工", 
            available_day_periods=first_available_day_periods)

        st.write("---")

        first_p_e_num_per_week, first_p_e_teacher_for, first_p_e_room_for, first_p_e_days_period, first_p_e_period_limit, first_p_e_consecutive, first_p_e_joint_class = subject_info_input(
            grade=1, 
            subject="体育", 
            available_day_periods=first_available_day_periods)

        st.write("---")

        first_gakkatsu_num_per_week, first_gakkatsu_teacher_for, first_gakkatsu_room_for, first_gakkatsu_days_period, first_gakkatsu_period_limit, first_gakkatsu_consecutive, first_gakkatsu_joint_class = subject_info_input(
            grade=1, 
            subject="学活・道徳", 
            available_day_periods=first_available_day_periods)

        st.write("---")

    with col2:
        second_grade_class_num, second_grade_selected_6_period_days, err = basic_info_input(grade=2, default="なし")
        
        second_grade_class = range(1, second_grade_class_num + 1)
        second_grade_class_teacher_dict, second_grade_class_room_dict = make_class_teacher_and_room_dict(grade=2, grade_class_list=second_grade_class)
        
        second_available_day_periods = []
        for day in week:
            if day in second_grade_selected_6_period_days:
                second_available_day_periods.extend([(day, period) for period in period_list])
            else:
                second_available_day_periods.extend([(day, period) for period in [1,2,3,4,5]])

        second_japanese_num_per_week, second_japanese_teacher_for, second_japanese_room_for, second_japanese_days_period, second_japanese_period_limit, second_japanese_consecutive, second_japanese_joint_class = subject_info_input(
            grade=2, 
            subject="国語", 
            available_day_periods=second_available_day_periods)

        st.write("---")

        second_math_num_per_week, second_math_teacher_for, second_math_room_for, second_math_days_period, second_math_period_limit, second_math_consecutive, second_math_joint_class = subject_info_input(
            grade=2, 
            subject="算数", 
            available_day_periods=second_available_day_periods)

        st.write("---")

        second_seikatsu_num_per_week, second_seikatsu_teacher_for, second_seikatsu_room_for, second_seikatsu_days_period, second_seikatsu_period_limit, second_seikatsu_consecutive, second_seikatsu_joint_class = subject_info_input(
            grade=2, 
            subject="生活", 
            available_day_periods=second_available_day_periods)

        st.write("---")

        second_music_num_per_week, second_music_teacher_for, second_music_room_for, second_music_days_period, second_music_period_limit, second_music_consecutive, second_music_joint_class = subject_info_input(
            grade=2, 
            subject="音楽", 
            available_day_periods=second_available_day_periods)

        st.write("---")

        second_zukou_num_per_week, second_zukou_teacher_for, second_zukou_room_for, second_zukou_days_period, second_zukou_period_limit, second_zukou_consecutive, second_zukou_joint_class = subject_info_input(
            grade=2, 
            subject="図工", 
            available_day_periods=second_available_day_periods)

        st.write("---")

        second_p_e_num_per_week, second_p_e_teacher_for, second_p_e_room_for, second_p_e_days_period, second_p_e_period_limit, second_p_e_consecutive, second_p_e_joint_class = subject_info_input(
            grade=2, 
            subject="体育", 
            available_day_periods=second_available_day_periods)

        st.write("---")

        second_gakkatsu_num_per_week, second_gakkatsu_teacher_for, second_gakkatsu_room_for, second_gakkatsu_days_period, second_gakkatsu_period_limit, second_gakkatsu_consecutive, second_gakkatsu_joint_class = subject_info_input(
            grade=2, 
            subject="学活・道徳", 
            available_day_periods=second_available_day_periods)

        st.write("---")
    



if __name__ == "__main__":
    main()

# streamlit run main.py