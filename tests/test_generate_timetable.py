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


def test_generate_timetable_retries_on_failure():
    grade_info = {1: {"class_num": 1, "six_days": []}}
    subject_settings = {
        1: {
            "音楽": {
                "num": 1,
                "teacher": "音楽教員",
                "room": "音楽室(低学年用)",
                "day_periods": [],
                "period_limit": None,
                "consecutive": 0,
                "joint": 0,
            }
        }
    }

    calls = {"n": 0}
    original = app.assign_course

    def flaky_assign_course(*args, **kwargs):
        calls["n"] += 1
        if calls["n"] == 1:
            raise RuntimeError("forced failure")
        return original(*args, **kwargs)

    app.assign_course = flaky_assign_course
    df = app.generate_timetable(grade_info, subject_settings, max_attempts=5)
    app.assign_course = original

    assert not df.empty
    assert calls["n"] >= 2
