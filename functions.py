def empty_place_day_periods(df, limit=2):
  empty_place_day_period = []
  empty_place = df.query("subject == '体育'")
  for day_period in empty_place[["day","period"]].apply(tuple, axis=1):
    empty_place_idx = empty_place.query(f"day == '{day_period[0]}' and period == {day_period[1]}").index
    if len(empty_place_idx) >= limit:
      empty_place_day_period.append(day_period)
  return empty_place_day_period

def set_joint_course(df, subject, joint_class_pairs_list):
  for joint_class_pairs in joint_class_pairs_list:
    # 1つずつクラスのペアを抜き出す
    joint_class_mask = df[["grade","class"]].apply(tuple, axis=1).isin(joint_class_pairs)
    _df = df.loc[joint_class_mask & (df["subject"]==subject),]

    # 共通で空いている日に絞る
    day_period_mask = _df[["day","period"]].apply(tuple, axis=1).unique()
    __df = _df.loc[day_period_mask,]

    if len(__df.index) > 0:
      candidate = __df.sample(n=1)
    else:
      print("No candidate")
      break

    empty_slot_candidate_day = candidate["day"].values[0]
    empty_slot_candidate_period = candidate["period"].values[0]
    idx_tmp = __df.query(f"day == '{empty_slot_candidate_day}' and period == '{empty_slot_candidate_period}'")

    df.loc[idx_tmp, "subject"] = subject
    df.loc[idx_tmp, "teacher"] = subject_dict[g][subject][1]
    df.loc[idx_tmp, "room"] = subject_dict[g][subject][2]
  
  return df


def set_subject(df, subject, err, two_period_course=False, grade_specialize=[1,2,3,4,5,6], period_limit=[1,2,3,4,5,6]):
  success = False
  error = False

  while success == False and error == False:
    for g in grade_specialize:
      for c in class_dict[g]:
        _cnt = 0
        if two_period_course == False:
          num_subject = subject_dict[g][subject][0]
        else:
          num_subject = 1
        while num_subject > _cnt:
          # 教科担当の教員・部屋が埋まっている日のリスト
          scheduled = df.query(f"subject == '{subject}'")
          scheduled_teacher_room = scheduled.query(f"teacher == '{subject_dict[g][subject][1]}' or room == '{subject_dict[g][subject][2]}'")

          if two_period_course == False:
            scheduled_day_period_list = scheduled_teacher_room[["day","period"]].apply(tuple, axis=1)
          else:
            scheduled_day_period_list = empty_place_day_periods(scheduled_teacher_room)
          
          # そのクラスが空いてる日を抜き出す
          if two_period_course == False:
            __empty_slot_candidates = df.loc[(df["grade"] == g) & (df["class"] == c) & (df["period"].isin(period_limit)) & (df["subject"] == ""),]
          else:
            ___empty_slot_candidates = df.loc[(df["grade"] == g) & (df["class"] == c) & (df["period"].isin([1,2,3,5])) & (df["subject"] == ""),]
            __empty_slot_candidates = ___empty_slot_candidates.query(f"day not in {six_periods_days[g]} or period != 5")
          
          # 同じ日に同じ教科が入らないようにする
          self_scheduled_days_list = df.query(f"grade == {g} and `class` == {c} and subject == '{subject}'").day.unique()

          if self_scheduled_days_list == ["月","火","水","木","金"]:
            self_scheduled_days = []
          elif len(self_scheduled_days_list) > 0:
            self_scheduled_days = self_scheduled_days_list
          else:
            self_scheduled_days = []
          
          _empty_slot_candidates = __empty_slot_candidates.query(f"day not in {self_scheduled_days}")
          
          # 候補日を抜き出す
          if two_period_course == False:
            empty_slot_candidates = _empty_slot_candidates.loc[~(_empty_slot_candidates[["day","period"]].apply(tuple, axis=1).isin(scheduled_day_period_list)),]
          else:
            _empty_slot_candidates_next = _empty_slot_candidates.copy()
            _empty_slot_candidates_next.loc[:, "period_next"] = _empty_slot_candidates["period"]+1
            empty_slot_candidates = _empty_slot_candidates.loc[~(_empty_slot_candidates[["day","period"]].apply(tuple, axis=1).isin(scheduled_day_period_list))&
                                                               ~(_empty_slot_candidates_next[["day", "period_next"]].apply(tuple, axis=1).isin(scheduled_day_period_list)),]

          if len(empty_slot_candidates.index)>0:
            empty_slot_candidate = empty_slot_candidates.sample(n=1)
          else:
            print(f"No candidates in {g}-{c}")
            err = True
            error = True
            break

          # 条件を満たすインデックスを取得
          empty_slot_candidate_day = empty_slot_candidate["day"].values[0]
          if two_period_course == False:
            empty_slot_candidate_period = empty_slot_candidate["period"].values[0]
            idx_tmp = df.query(f"grade == {g} and `class` == {c} and day == '{empty_slot_candidate_day}' and period == {empty_slot_candidate_period}").index
          else:
            empty_slot_candidate_period = empty_slot_candidate["period"].values[0]
            empty_slot_candidate_period = empty_slot_candidate["period"].values[0]+1
            idx_tmp = df.query(f"grade == {g} and `class` == {c} and day == '{empty_slot_candidate_day}' and period == {empty_slot_candidate_period}").index
            idx_tmp_next = df.query(f"grade == {g} and `class` == {c} and day == '{empty_slot_candidate_day}' and period == {empty_slot_candidate_period}").index
            idx_tmp.append(idx_tmp_next[0])

          
          df.loc[idx_tmp, "subject"] = subject
          df.loc[idx_tmp, "teacher"] = subject_dict[g][subject][1]
          df.loc[idx_tmp, "room"] = subject_dict[g][subject][2]

          print(f"success in {g}-{c}")
          _cnt += 1

    success = True
    
  return df
