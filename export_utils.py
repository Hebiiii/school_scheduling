"""Utility functions for exporting timetable data to Excel files.

Each export helper returns ``bytes`` representing an Excel workbook. In
addition to the requested summary sheets, every workbook now contains a
``raw_data`` sheet with the original timetable ``DataFrame`` so that users
can inspect or further process the underlying data easily.

The module provides exports for class schedules, teacher schedules,
room usage and subject summaries.
"""

import pandas as pd
from io import BytesIO
import re
import io
import openpyxl
import xlsxwriter
import zipfile

# Common ordering for days of the week and periods so that all exports share
# the same layout. Previously these were imported from the streamlit app which
# caused a ``NameError`` when the functions were used independently.  Defining
# them here keeps the utilities self‑contained.
WEEK = ["月", "火", "水", "木", "金"]
PERIODS = [1, 2, 3, 4, 5, 6]

def export_class_schedule(df: pd.DataFrame) -> bytes:
    """Create an Excel file of class schedules from a timetable DataFrame.

    Parameters
    ----------
    df: DataFrame
        Timetable with columns [grade, class, day, period, subject, teacher, room].

    Returns
    -------
    bytes
        Excel file bytes where each sheet corresponds to a class and contains a
        pivot table with days as columns and periods as rows. Each cell shows the
        subject, teacher and room separated by new lines.
    """
    buffer = BytesIO()

    with pd.ExcelWriter(buffer, engine="openpyxl") as writer:
        # Include raw data sheet for reference
        df.to_excel(writer, sheet_name="raw_data", index=False)

        for (grade, cls), group in df.groupby(["grade", "class"]):
            tmp = group.copy()
            tmp["info"] = tmp.apply(
                lambda r: f"{r['subject']}\n{r['teacher']}\n{r['room']}", axis=1
            )
            pivot = (
                tmp.pivot_table(
                    index="period",
                    columns="day",
                    values="info",
                    aggfunc=lambda x: "\n".join(x),
                    fill_value="",
                )
                .reindex(index=PERIODS, columns=WEEK, fill_value="")
            )
            pivot.to_excel(writer, sheet_name=f"{grade}-{cls}")
    buffer.seek(0)
    return buffer.getvalue()

def export_teacher_schedule(df: pd.DataFrame) -> bytes:
    """Create an Excel file of teacher schedules.

    A pivot table is generated for each teacher with days as rows and
    periods as columns. Each cell contains the class and subject for the
    assigned slot. Teachers appear as individual sheets in the workbook.

    Parameters
    ----------
    df : pandas.DataFrame
        Scheduling table containing at least the columns
        ``['grade', 'class', 'day', 'period', 'subject', 'teacher']``.

    Returns
    -------
    bytes
        Excel file data.
    """

    # Split rows for multiple teachers separated by '/'
    expanded = df.copy()
    expanded = expanded[expanded['teacher'] != '']
    expanded = expanded.assign(teacher=expanded['teacher'].str.split('/')).explode('teacher')

    # Display "{grade}-{class} {subject}" in each cell
    expanded['label'] = (
        expanded['grade'].astype(str)
        + '-' + expanded['class'].astype(str)
        + ' ' + expanded['subject']
    )

    output = BytesIO()
    with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
        # Add raw data
        df.to_excel(writer, sheet_name="raw_data", index=False)

        for teacher, group in expanded.groupby('teacher'):
            pivot = (
                group.pivot_table(
                    index='day',
                    columns='period',
                    values='label',
                    aggfunc=lambda x: "\n".join(x),
                    fill_value="",
                )
                .reindex(index=WEEK, columns=PERIODS, fill_value="")
            )

            # Remove characters invalid for Excel sheet names / file names
            safe_name = re.sub(r'[\\/*?\[\]:]', '', teacher)[:31]
            pivot.to_excel(writer, sheet_name=safe_name)

    output.seek(0)
    return output.getvalue()

def export_room_usage(df: pd.DataFrame):
    """Export room usage as an Excel file with one sheet per room."""
    df = df.copy()
    df["class_subject"] = df.apply(
        lambda r: f"{r['grade']}-{r['class']} {r['subject']}", axis=1
    )
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
        # Add raw data
        df.to_excel(writer, sheet_name="raw_data", index=False)

        for room, group in df.groupby("room"):
            pivot = (
                group.pivot_table(
                    index="day",
                    columns="period",
                    values="class_subject",
                    aggfunc=lambda x: "\n".join(x),
                    fill_value="",
                )
                .reindex(index=WEEK, columns=PERIODS, fill_value="")
            )
            pivot.to_excel(writer, sheet_name=str(room))
    output.seek(0)
    return output.getvalue()

def export_subject_summary(df: pd.DataFrame) -> bytes:
    """Aggregate timetable by grade, class and subject and export as Excel.

    The resulting workbook contains two sheets:
    ``summary`` – the aggregated subject counts, and ``raw_data`` – the
    original timetable.
    """

    summary = (
        df.groupby(["grade", "class", "subject"])
        .size()
        .reset_index(name="periods_per_week")
        .sort_values(["grade", "class", "subject"])
    )

    output = BytesIO()
    with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
        summary.to_excel(writer, sheet_name="summary", index=False)
        df.to_excel(writer, sheet_name="raw_data", index=False)

    output.seek(0)
    return output.getvalue()


def export_all_excel(df: pd.DataFrame) -> bytes:
    """Package key Excel exports into a single ZIP archive.

    The archive contains class schedules, teacher schedules and room usage
    workbooks. Each workbook already includes a ``raw_data`` sheet.
    """
    
    buffer = BytesIO()
    with zipfile.ZipFile(buffer, "w") as zf:
        zf.writestr("class_schedule.xlsx", export_class_schedule(df))
        zf.writestr("teacher_schedule.xlsx", export_teacher_schedule(df))
        zf.writestr("room_usage.xlsx", export_room_usage(df))
    buffer.seek(0)
    return buffer.getvalue()
