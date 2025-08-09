import importlib.util
from pathlib import Path


def load_streamlit_module():
    path = Path(__file__).resolve().parent.parent / "streamlit.py"
    spec = importlib.util.spec_from_file_location("app_streamlit", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_generate_timetable_twice_no_error():
    sl = load_streamlit_module()
    grade_info = {1: {"class_num": 1, "six_days": ["火"]}}
    subject_settings = {
        1: {
            "算数": {
                "num": 1,
                "teacher": "担任",
                "room": "教室",
                "day_periods": [],
                "period_limit": None,
                "consecutive": 0,
                "joint": 0,
            }
        }
    }
    sg = sl.serialize_grade_info(grade_info)
    ss = sl.serialize_subject_settings(subject_settings)
    df1 = sl.generate_timetable(sg, ss)
    df2 = sl.generate_timetable(sg, ss)
    assert df1.shape == df2.shape
