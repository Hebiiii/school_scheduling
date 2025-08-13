import sys
import types
import importlib.util
from pathlib import Path

# Provide a stub for the external streamlit package
sys.modules['streamlit'] = types.SimpleNamespace()

# Load the local streamlit.py module under a different name
spec = importlib.util.spec_from_file_location('app', Path(__file__).resolve().parents[1] / 'streamlit.py')
app = importlib.util.module_from_spec(spec)
spec.loader.exec_module(app)


def test_special_teacher_not_double_assigned():
    grade_info = {1: {"class_num": 1, "six_days": []}}
    subject_settings = {
        1: {
            "音楽": {
                "num": 2,
                "teacher": "音楽教員",
                "room": "音楽室(低学年用)",
                "day_periods": [],
                "period_limit": None,
                "consecutive": 0,
                "joint": 0,
            }
        }
    }
    df = app.generate_timetable(grade_info, subject_settings)
    music = df[(df.grade == 1) & (df["class"] == 1) & (df.subject == "音楽")]
    assert len(music) == 2
