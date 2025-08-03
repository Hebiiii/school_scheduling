import pandas as pd
from functools import reduce
import random

# --- Helper functions to find unavailable slots ---
def get_unavailable_day_periods(df, teacher=None, room=None, limit=1):
    """
    Returns a list of (day, period) tuples where the given teacher or room
    is already used at least `limit` times.
    """
    mask = pd.Series(True, index=df.index)
    if teacher:
        mask &= (df['teacher'] == teacher)
    if room:
        mask &= (df['room'] == room)
    grouped = df[mask].groupby(['day', 'period']).size().reset_index(name='count')
    return grouped.loc[grouped['count'] >= limit, ['day','period']].apply(tuple, axis=1).tolist()


def get_unavailable_for_consecutive(df, teacher=None, room=None, limit=1):
    """
    Returns a list of (day, period) to avoid when scheduling 2-period blocks,
    i.e. any period where either the slot itself or the following slot is full.
    """
    single = set(get_unavailable_day_periods(df, teacher=teacher, room=room, limit=limit))
    consec = set()
    for day, period in single:
        consec.add((day, period))       # can't start at a busy slot
        consec.add((day, period - 1))   # can't start if next slot is busy
    return list(consec)


# --- Finding and filtering candidate slots ---
def find_available_slots(df, grade, cls,
                         period_limit=None,
                         exclude_days=None,
                         exclude_day_periods=None):
    """
    Returns all empty slots for a given class, optionally restricting to
    certain periods and excluding specific days or day-period pairs.
    """
    slots = df[(df.grade == grade) & (df['class'] == cls) & (df.subject == '')]
    if period_limit is not None:
        slots = slots[slots.period.isin(period_limit)]
    if exclude_days is not None:
        slots = slots[~slots.day.isin(exclude_days)]
    if exclude_day_periods is not None:
        idxs = slots.set_index(['day','period']).index
        slots = slots[~idxs.isin(exclude_day_periods)]
    return slots.copy()


# --- Core assignment functions ---
def assign_fixed_course(df, grade, cls,
                        subject, teacher, room,
                        day_periods):
    """Assign `subject` to specific `day_periods` for a class.

    Parameters
    ----------
    df : DataFrame
        Scheduling table.
    grade, cls : int
        Target grade and class.
    subject, teacher, room : str
        Information to fill for each slot.
    day_periods : list of (day, period)
        Exact slots to occupy.
    """
    for day, period in day_periods:
        idx = df[(df.grade == grade) & (df['class'] == cls)
                 & (df.day == day) & (df.period == period)]
        if idx.empty:
            raise RuntimeError(
                f"Slot ({day}, {period}) for {grade}-{cls} not in schedule"
            )
        if (idx.subject != '').any():
            raise RuntimeError(
                f"Slot ({day}, {period}) for {grade}-{cls} already filled"
            )
        df.loc[idx.index, ['subject','teacher','room']] = subject, teacher, room
    return df

def assign_course(df, grade, cls,
                  subject, teacher, room,
                  num_slots=1,
                  period_limit=None,
                  consecutive=False,
                  capacity_limit=1):
    """
    Assigns `subject` to `num_slots` slots for a single class ({grade}-{cls}),
    respecting teacher/room capacity, optional period restrictions, and
    (if `consecutive=True`) requiring two back-to-back periods.
    """
    assigned = 0
    while assigned < num_slots:
        if consecutive:
            unavailable = get_unavailable_for_consecutive(
                df, teacher=teacher, room=room, limit=capacity_limit
            )
        else:
            unavailable = get_unavailable_day_periods(
                df, teacher=teacher, room=room, limit=capacity_limit
            )
        # avoid scheduling the subject twice on the same day
        used_days = df.query(
            f'grade=={grade} and `class`=={cls} and subject==@subject'
        )['day'].tolist()

        candidates = find_available_slots(
            df, grade, cls,
            period_limit=period_limit,
            exclude_days=used_days,
            exclude_day_periods=unavailable
        )
        if consecutive:
            # require the very next period also to be free
            candidates['period_next'] = candidates.period + 1
            merged = candidates.merge(
                df[['day','period','subject']],
                left_on=['day','period_next'],
                right_on=['day','period'],
                suffixes=('','_next')
            )
            candidates = merged[merged['subject_next'] == '']

        if candidates.empty:
            raise RuntimeError(
                f"No available slots for {grade}-{cls}, subject '{subject}'"
            )
        pick = candidates.sample(1).iloc[0]
        day, period = pick['day'], pick['period']

        # assign the chosen slot
        idx1 = df[(df.grade == grade) & (df['class'] == cls)
                  & (df.day == day) & (df.period == period)].index
        df.loc[idx1, ['subject','teacher','room']] = subject, teacher, room

        if consecutive:
            # assign the next period as well
            idx2 = df[(df.grade == grade) & (df['class'] == cls)
                      & (df.day == day) & (df.period == period + 1)
                      & (df.subject == '')].index
            df.loc[idx2, ['subject','teacher','room']] = subject, teacher, room

        assigned += 1
    return df


def assign_joint_course(df, subject,
                        class_group,
                        teacher, room,
                        capacity_limit=2):
    """
    Assigns the same `subject` to *all* classes in `class_group` at a
    common empty slot, respecting room capacity.
    `class_group` should be a list of (grade, class) tuples.
    """
    # find time slots where room already has >= capacity_limit classes
    unavailable = get_unavailable_day_periods(
        df, teacher=None, room=room, limit=capacity_limit
    )
    # find common empty slots across all classes
    dfs = []
    for grade, cls in class_group:
        dfs.append(
            df[(df.grade == grade)
               & (df['class'] == cls)
               & (df.subject == '')][['day','period']]
        )
    common = reduce(lambda a, b: pd.merge(a, b, on=['day','period']), dfs)
    common = common.drop_duplicates()
    # exclude fully booked slots
    idxs = common.set_index(['day','period']).index
    common = common[~idxs.isin(unavailable)]

    if common.empty:
        raise RuntimeError(
            f"No common slots for joint subject '{subject}' in {class_group}"
        )
    day, period = common.sample(1).iloc[0]
    for grade, cls in class_group:
        idx = df[(df.grade == grade)
                 & (df['class'] == cls)
                 & (df.day == day)
                 & (df.period == period)].index
        df.loc[idx, ['subject','teacher','room']] = subject, teacher, room
    return df
