#ライブラリのインポート
import pandas as pd
import numpy as np

################## Part1. Input information ###################

########### Classes ###############
grade_list = [1,2,3,4,5,6]
first_grade_class_num = 3 #1年生のクラス数
second_grade_class_num = 3 #2年生のクラス数
third_grade_class_num = 3 #3年生のクラス数
fourth_grade_class_num = 3 #4年生のクラス数
fifth_grade_class_num = 3 #5年生のクラス数
sixth_grade_class_num = 3 #6年生のクラス数

#学年ごとのクラス数(default)
class_dict = {1:range(1,first_grade_class_num+1),
              2:range(1,second_grade_class_num+1),
              3:range(1,third_grade_class_num+1),
              4:range(1,fourth_grade_class_num+1),
              5:range(1,fifth_grade_class_num+1),
              6:range(1,sixth_grade_class_num+1)} 

# クラスごとの担任
class_teacher_list = []
class_teacher_dict = {}
for grade in grade_list:
    class_teacher_dict[grade] = {}
    for cls in class_dict[grade]:
        class_teacher_list.append(f"{grade}-{cls}担任")
        class_teacher_dict[grade][cls] = f"{grade}-{cls}担任" #担任の学年を辞書に格納

# クラスごとの教室
class_room_list = []
class_room_dict = {}
for grade in grade_list:
    class_room_dict[grade] = {}
    for cls in class_dict[grade]:
        class_room_list.append(f"{grade}-{cls}教室")
        class_room_dict[grade][cls] = f"{grade}-{cls}教室"

########### Subjects ###############
subject_list = ["英語","算数","国語","理科","社会","図工","音楽","体育","家庭科","総合","学活・道徳","生活","書写"] #教科名
# multi_period_subject_list = ["体育","理科","総合"] #2コマ連続授業の教科名

########### Day-Period ###############
week = ["月","火","水","木","金"]
period_list = [1,2,3,4,5,6]

# 学年ごとの5時間授業の日のリスト
first_grade_5_hour_day = ["月","火","水","木","金"]
second_grade_5_hour_day = ["月","火","木","金"]
third_grade_5_hour_day = ["月","水","木","金"]
fourth_grade_5_hour_day = ["月"]
fifth_grade_5_hour_day = ["月"]
sixth_grade_5_hour_day = ["月"]

grade_5_hour_day_dict = {
    1: first_grade_5_hour_day,
    2: second_grade_5_hour_day,
    3: third_grade_5_hour_day,
    4: fourth_grade_5_hour_day,
    5: fifth_grade_5_hour_day,
    6: sixth_grade_5_hour_day
}

########### Teachers ###############
_teacher_list = ["英語教員","理科教員","音楽教員","家庭科教員","書写教員", "算数教員"]

teacher_list = class_teacher_list + _teacher_list #教員リスト

########### Rooms ###############
_room_list = ["理科室","音楽室","図工室","家庭科室","体育館"] #特別教室リスト

room_list = class_room_list + _room_list #教室リスト

############ Grade-Class-Subject to Teacher-Room #############
#必要授業数(default value)
subject_dict = {
    1:{
        "英語":1,
        "算数":3,
        "国語":5,
        "理科":0,
        "社会":0,
        "図工":2,
        "音楽":2,
        "体育":2,
        "家庭科":0,
        "総合":0,
        "学活・道徳":1,
        "生活":2,
        "書写":0},
    2:{
        "英語":1,
        "算数":3,
        "国語":5,
        "理科":0,
        "社会":0,
        "図工":2,
        "音楽":2,
        "体育":2,
        "家庭科":0,
        "総合":0,
        "学活・道徳":1,
        "生活":2,
        "書写":0},
    3:{
        "英語":1,
        "算数":3,
        "国語":5,
        "理科":2,
        "社会":2,
        "図工":2,
        "音楽":2,
        "体育":2,
        "家庭科":0,
        "総合":2,
        "学活・道徳":1,
        "生活":0,
        "書写":1},
    4:{
        "英語":1,
        "算数":3,
        "国語":5,
        "理科":2,
        "社会":2,
        "図工":2,
        "音楽":2,
        "体育":2,
        "家庭科":0,
        "総合":2,
        "学活・道徳":1,
        "生活":0,
        "書写":1},
    5:{
        "英語":2,
        "算数":3,
        "国語":3,
        "理科":2,
        "社会":2,
        "図工":1,
        "音楽":1,
        "体育":3,
        "家庭科":2,
        "総合":2,
        "学活・道徳":1,
        "生活":0,
        "書写":1},
    6:{
        "英語":2,
        "算数":3,
        "国語":3,
        "理科":2,
        "社会":2,
        "図工":1,
        "音楽":1,
        "体育":3,
        "家庭科":2,
        "総合":2,
        "学活・道徳":1,
        "生活":0,
        "書写":1}
    }

########################################

# 5時間授業の日を考慮
info_list = []
for grade in grade_list:
    for cls in class_dict[grade]:
      for day in week:
        for _period in period:
          if grade == 1 and _period != 6:
            info_list.append([grade,cls,day,_period])
          elif grade == 2 and (day == "水" or _period != 6):
            info_list.append([grade,cls,day,_period])
          elif grade == 3 and (day == "火" or _period != 6):
            info_list.append([grade,cls,day,_period])
          elif grade > 3 and (day == "月" and _period != 6):
            info_list.append([grade,cls,day,_period])
          elif grade > 3 and (day != "月"):
            info_list.append([grade,cls,day,_period])

df = pd.DataFrame(info_list,columns=["grade","class","day","period"])
df["subject"] = ""

# 1. 学活・道徳の授業は、全学年・全クラスにおいて月曜1限に行われる。（担任が教室で行う）
gakkatsu_idx = df.query("day == '月' and period == 1").index
df.loc[gakkatsu_idx,"subject"] = "学活・道徳"

# 2. 総合の授業は3年生が火曜日、4年生が木曜日、5年生が水曜日、6年生が金曜日の5,6限に行われる（担任が教室で行う）
sougou_dict = {3:"火", 4:"木", 5:"水", 6:"金"}
sougou_idx = []
for sougou_grd, sougou_day in sougou_dict.items():
    _sougou_idx56 = df.query(f"grade == {sougou_grd} and day == '{sougou_day}' and period >= 5").index
    for _sougou_idx in _sougou_idx56:
        sougou_idx.append(_sougou_idx)
df.loc[sougou_idx,"subject"] = "総合"

# 3. 体育の授業
# 3-1. 1~4年の合同授業の場合を除き、体育館は全学年全クラス問わず2クラスしか使えない。
# 3-2. 1~4年の体育は、各学年の全クラス合同授業1コマとその他の日の1コマの週2コマ行われる（後半は3-4）。（担任が体育館で行う）
import random
df1 = df.copy()
# cnt_all = 0
# err = False
# while cnt_all <500 and err == False:
grade_multi_class_taiiku = [1,2,3,4]
multi_class_taiiku_idx = []
for g in grade_multi_class_taiiku:
  empty_slot_candidate = df1.query(f"grade == {g} and subject == ''").sample(n=1)
  empty_slot_candidate_day = empty_slot_candidate["day"].values[0]
  empty_slot_candidate_period = empty_slot_candidate["period"].values[0]
  for c in class_dict[g]:
    idx_tmp = df1.query(f"grade == {g} and `class` == {c} and day == '{empty_slot_candidate_day}' and period == {empty_slot_candidate_period}").index[0]
    df1.loc[idx_tmp, "subject"] = "体育"
    multi_class_taiiku_idx.append(idx_tmp)

def empty_place_day_periods(df, limit=2):
  empty_place_day_period = []
  for day_period in df[["day","period"]].apply(tuple, axis=1):
    empty_place_idx = df.query(f"day == '{day_period[0]}' and period == {day_period[1]}").index
    if len(empty_place_idx) >= limit:
      empty_place_day_period.append(day_period)
  return empty_place_day_period

df2 = df1.copy()

# 3-3. 5,6年の体育は、2コマ連続授業とその他の日の1コマ授業の週3コマ行われる(後半は3-4)（担任が体育館で行う）
grade_2period_taiiku = [5,6]
success_multi_period_taiiku = False
cnt_multi_period_taiiku = 0
while success_multi_period_taiiku == False and cnt_multi_period_taiiku < 500:
  for g in grade_2period_taiiku:
    for c in class_dict[g]:
      # 体育館が空いてない日にちと時間のリスト
      empty_taiiku_place = df2.query("subject == '体育'")
      empty_taiiku_place_day_period_list = empty_place_day_periods(empty_taiiku_place)

      # 体育館が使える日の1日目の候補を取得(1日目と2日目が空いてない日に含まれていないかチェック)
      __empty_slot_candidate = df2.query(f"grade == {g} and `class` == {c} and period in [1,2,3,5] and subject == '' and subject != '総合'")
      _empty_slot_candidate = __empty_slot_candidate.query(f"day != '月' or period != 5")
      _empty_slot_candidate_next = _empty_slot_candidate.copy()
      _empty_slot_candidate_next.loc[:, "period_next"] = _empty_slot_candidate["period"]+1

      empty_slot_candidate = _empty_slot_candidate.loc[~(_empty_slot_candidate[["day","period"]].apply(tuple, axis=1).isin(empty_taiiku_place_day_period_list))&
                                                       ~(_empty_slot_candidate_next[["day", "period_next"]].apply(tuple, axis=1).isin(empty_taiiku_place_day_period_list)),].sample(n=1)
      empty_slot_candidate_day = empty_slot_candidate["day"].values[0]
      empty_slot_candidate_period = empty_slot_candidate["period"].values[0]
      empty_slot_candidate_period_plus = empty_slot_candidate["period"].values[0]+1
      idx_tmp1 = df2.query(f"grade == {g} and `class` == {c} and day == '{empty_slot_candidate_day}' and period == {empty_slot_candidate_period}").index
      idx_tmp2 = df2.query(f"grade == {g} and `class` == {c} and day == '{empty_slot_candidate_day}' and period == {empty_slot_candidate_period_plus} and subject==''").index

      # print((empty_slot_candidate_day,empty_slot_candidate_period_plus))
      if len(idx_tmp2) > 0:
        df2.loc[idx_tmp1, "subject"] = "体育"
        df2.loc[idx_tmp2, "subject"] = "体育"
        print(f"success in {g}-{c}")
      else:
        cnt_multi_period_taiiku += 1
        if cnt_multi_period_taiiku == 500:
          print("No candidates in 5-2")
          break
        continue
    success_multi_period_taiiku = True

# 4-1. 5,6年理科2連続授業
df3 = df2.copy()
grade_2period_rika = [5,6]
success_multi_period_rika = False
cnt_multi_period_rika = 0
while success_multi_period_rika == False and cnt_multi_period_rika < 500:
  for g in grade_2period_rika:
    for c in class_dict[g]:
      # 理科室が空いてない日にちと時間のリスト
      empty_rika_place = df3.query("subject == '理科'")
      empty_rika_place_day_period_list = empty_rika_place[["day","period"]].apply(tuple, axis=1)

      # 理科室が使える日の1日目の候補を取得(1日目と2日目が空いてない日に含まれていないかチェック)
      __empty_slot_candidate = df3.query(f"grade == {g} and `class` == {c} and period in [1,2,3,5] and subject == ''")
      _empty_slot_candidate = __empty_slot_candidate.query(f"day != '月' or period != 5")
      _empty_slot_candidate_next = _empty_slot_candidate.copy()
      _empty_slot_candidate_next.loc[:, "period_next"] = _empty_slot_candidate["period"]+1

      empty_slot_candidate = _empty_slot_candidate.loc[~(_empty_slot_candidate[["day","period"]].apply(tuple, axis=1).isin(empty_rika_place_day_period_list))&
                                                       ~(_empty_slot_candidate_next[["day", "period_next"]].apply(tuple, axis=1).isin(empty_rika_place_day_period_list)),].sample(n=1)
      empty_slot_candidate_day = empty_slot_candidate["day"].values[0]
      empty_slot_candidate_period = empty_slot_candidate["period"].values[0]
      empty_slot_candidate_period_plus = empty_slot_candidate["period"].values[0]+1
      idx_tmp1 = df3.query(f"grade == {g} and `class` == {c} and day == '{empty_slot_candidate_day}' and period == {empty_slot_candidate_period}").index
      idx_tmp2 = df3.query(f"grade == {g} and `class` == {c} and day == '{empty_slot_candidate_day}' and period == {empty_slot_candidate_period_plus} and subject==''").index

      # print((empty_slot_candidate_day,empty_slot_candidate_period_plus))
      if len(idx_tmp2) > 0:
        df3.loc[idx_tmp1, "subject"] = "理科"
        df3.loc[idx_tmp2, "subject"] = "理科"
        print(f"success in {g}-{c}")
      else:
        cnt_multi_period_rika += 1
        if cnt_multi_period_rika == 500:
          print(f"No candidates in {g}-{c}")
          break
        continue
    success_multi_period_rika = True


# 5. 英語の授業
# 5-1. 英語の授業は2~5限の間に、英語教員が各教室で行う必要がある(3,4,5,6年)
period_limit_eng = [2,3,4,5]
grade_eng_specialize = [3,4,5,6]
df4 = df3.copy()

success_eng = False
cnt_eng = 0
while success_eng == False and cnt_eng < 500:
  for g in grade_eng_specialize:
    for c in class_dict[g]:
      cnt_ = 0
      while subject_dict[g]["英語"] > cnt_:
        # 英語教員が空いている日のリスト
        scheduled_eng = df4.query("subject == '英語'")
        scheduled_eng_day_period_list = scheduled_eng[["day","period"]].apply(tuple, axis=1)

        # 英語教員が使える日を抜き出す
        __empty_slot_candidate = df4.loc[(df4["grade"] == g) & (df4["class"] == c) & (df4["period"].isin(period_limit_eng)) & (df4["subject"] == ""),]

        self_scheduled_day = df4.query(f"grade == {g} and `class` == {c} and subject == '英語'").day
        if len(self_scheduled_day) > 0:
          self_scheduled_day = self_scheduled_day.values[0]
        else:
          self_scheduled_day = ""
        _empty_slot_candidate = __empty_slot_candidate.query(f"day != '{self_scheduled_day}'")
        empty_slot_candidate = _empty_slot_candidate.loc[~(_empty_slot_candidate[["day","period"]].apply(tuple, axis=1).isin(scheduled_eng_day_period_list)),].sample(n=1)
        empty_slot_candidate_day = empty_slot_candidate["day"].values[0]
        empty_slot_candidate_period = empty_slot_candidate["period"].values[0]
        idx_tmp = df4.query(f"grade == {g} and `class` == {c} and day == '{empty_slot_candidate_day}' and period == {empty_slot_candidate_period}").index

        if len(idx_tmp) > 0:
          df4.loc[idx_tmp, "subject"] = "英語"
          print(f"success in {g}-{c}")
          cnt_ += 1
        else:
          cnt_eng += 1
          if cnt_eng == 500:
            print(f"No candidates in {g}-{c}")
            break
          continue
    success_eng = True

# 6. 音楽の授業
# 6-1. 3~6年の音楽は、音楽室で音楽教員が行う。
# 6-2. 音楽の授業は2~5限の間に行われる
period_limit_music = [2,3,4,5]
grade_music_specialize = [3,4,5,6]
df5 = df4.copy()

success_music = False
cnt_music = 0
while success_music == False and cnt_music < 500:
  for g in grade_music_specialize:
    for c in class_dict[g]:
      cnt_ = 0
      while subject_dict[g]["音楽"] > cnt_:
        # 音楽教員が空いている日のリスト
        scheduled_music = df5.query("subject == '音楽'")
        scheduled_music_day_period_list = scheduled_music[["day","period"]].apply(tuple, axis=1)

        # 音楽教員が使える日を抜き出す
        __empty_slot_candidate = df5.loc[(df5["grade"] == g) & (df5["class"] == c) & (df5["period"].isin(period_limit_music)) & (df5["subject"] == ""),]

        scheduled_day = df5.query(f"grade == {g} and `class` == {c} and subject == '音楽'").day
        if len(scheduled_day) > 0:
          scheduled_day = scheduled_day.values[0]
        else:
          scheduled_day = ""
        _empty_slot_candidate = __empty_slot_candidate.query(f"day != '{scheduled_day}'")
        empty_slot_candidate = _empty_slot_candidate.loc[~(_empty_slot_candidate[["day","period"]].apply(tuple, axis=1).isin(scheduled_music_day_period_list)),].sample(n=1)
        empty_slot_candidate_day = empty_slot_candidate["day"].values[0]
        empty_slot_candidate_period = empty_slot_candidate["period"].values[0]
        idx_tmp = df5.query(f"grade == {g} and `class` == {c} and day == '{empty_slot_candidate_day}' and period == {empty_slot_candidate_period}").index

        if len(idx_tmp) > 0:
          df5.loc[idx_tmp, "subject"] = "音楽"
          print(f"success in {g}-{c}")
          cnt_ += 1
        else:
          cnt_music += 1
          if cnt_music == 500:
            print(f"No candidates in {g}-{c}")
            break
          continue
    success_music = True

# 7. 算数の授業
# 7-1. 1~5年の算数の授業は、4限までに6年の算数は5限までに、各教室で行う必要がある。
period_limit_math_dict = {
    1:[1,2,3,4], 2:[1,2,3,4], 3:[1,2,3,4], 4:[1,2,3,4], 5:[1,2,3,4], 6:[1,2,3,4,5]
}

grade_math_specialize = [5,6]
df6 = df5.copy()

success_math = False
cnt_math = 0
while success_math == False and cnt_math < 500:
  for g in grade_math_specialize:
    for c in class_dict[g]:
      cnt_ = 0
      while subject_dict[g]["算数"] > cnt_:
        # 算数教員が空いている日のリスト
        scheduled_math = df6.query("subject == '算数'")
        scheduled_math_day_period_list = scheduled_math[["day","period"]].apply(tuple, axis=1)

        # 算数教員が使える日を抜き出す
        __empty_slot_candidate = df6.loc[(df6["grade"] == g) & (df6["class"] == c) & (df6["period"].isin(period_limit_math_dict[g])) & (df6["subject"] == ""),]

        self_scheduled_day = df6.query(f"grade == {g} and `class` == {c} and subject == '算数'").day
        if len(self_scheduled_day) > 0:
          self_scheduled_day = self_scheduled_day.values
        else:
          self_scheduled_day = []
        _empty_slot_candidate = __empty_slot_candidate.loc[~(__empty_slot_candidate["day"].isin(self_scheduled_day)),]
        empty_slot_candidate = _empty_slot_candidate.loc[~(_empty_slot_candidate[["day","period"]].apply(tuple, axis=1).isin(scheduled_math_day_period_list)),].sample(n=1)
        empty_slot_candidate_day = empty_slot_candidate["day"].values[0]
        empty_slot_candidate_period = empty_slot_candidate["period"].values[0]
        idx_tmp = df6.query(f"grade == {g} and `class` == {c} and day == '{empty_slot_candidate_day}' and period == {empty_slot_candidate_period}").index

        if len(idx_tmp) > 0:
          df6.loc[idx_tmp, "subject"] = "算数"
          print(f"success in {g}-{c}")
          cnt_ += 1
        else:
          cnt_math += 1
          if cnt_math == 500:
            print(f"No candidates in {g}-{c}")
            break
          continue
    success_math = True

# 8. 家庭科の授業
# 8-1. 家庭科の授業は家庭科教員が家庭科室で行う

df7 = df6.copy()

success_home = False
cnt_home = 0
while success_home == False and cnt_home < 500:
  for g in grade_list:
    for c in class_dict[g]:
      cnt_ = 0
      while subject_dict[g]["家庭科"] > cnt_:
        # 家庭科教員が空いている日のリスト
        scheduled_home = df7.query("subject == '家庭科'")
        scheduled_home_day_period_list = scheduled_home[["day","period"]].apply(tuple, axis=1)

        # 家庭科教員が使える日を抜き出す
        __empty_slot_candidate = df7.loc[(df7["grade"] == g) & (df7["class"] == c) & (df7["subject"] == ""),]

        self_scheduled_day = df7.query(f"grade == {g} and `class` == {c} and subject == '家庭科'").day
        if len(self_scheduled_day) > 0:
          self_scheduled_day = self_scheduled_day.values
        else:
          self_scheduled_day = []
        _empty_slot_candidate = __empty_slot_candidate.loc[~(__empty_slot_candidate["day"].isin(self_scheduled_day)),]
        empty_slot_candidate = _empty_slot_candidate.loc[~(_empty_slot_candidate[["day","period"]].apply(tuple, axis=1).isin(scheduled_home_day_period_list)),].sample(n=1)
        empty_slot_candidate_day = empty_slot_candidate["day"].values[0]
        empty_slot_candidate_period = empty_slot_candidate["period"].values[0]
        idx_tmp = df7.query(f"grade == {g} and `class` == {c} and day == '{empty_slot_candidate_day}' and period == {empty_slot_candidate_period}").index

        if len(idx_tmp) > 0:
          df7.loc[idx_tmp, "subject"] = "家庭科"
          print(f"success in {g}-{c}")
          cnt_ += 1
        else:
          cnt_home += 1
          if cnt_home == 500:
            print(f"No candidates in {g}-{c}")
            break
          continue
    success_home = True

# 9. 書写の授業
# 9-1. 5,6年は書写教員が書写の授業を各教室で行う
df8 = df7.copy()
grade_shosha_specialize = [5,6]

success_shosha = False
cnt_shosha = 0
while success_shosha == False and cnt_shosha < 500:
  for g in grade_shosha_specialize:
    for c in class_dict[g]:
      cnt_ = 0
      while subject_dict[g]["書写"] > cnt_:
        # 書写教員が空いている日のリスト
        scheduled_shosha = df8.query("subject == '書写'")
        scheduled_shosha_day_period_list = scheduled_shosha[["day","period"]].apply(tuple, axis=1)

        # 書写教員が使える日を抜き出す
        __empty_slot_candidate = df8.loc[(df8["grade"] == g) & (df8["class"] == c) & (df8["subject"] == ""),]

        self_scheduled_day = df8.query(f"grade == {g} and `class` == {c} and subject == '書写'").day
        if len(self_scheduled_day) > 0:
          self_scheduled_day = self_scheduled_day.values
        else:
          self_scheduled_day = []
        _empty_slot_candidate = __empty_slot_candidate.loc[~(__empty_slot_candidate["day"].isin(self_scheduled_day)),]
        empty_slot_candidate = _empty_slot_candidate.loc[~(_empty_slot_candidate[["day","period"]].apply(tuple, axis=1).isin(scheduled_shosha_day_period_list)),].sample(n=1)
        empty_slot_candidate_day = empty_slot_candidate["day"].values[0]
        empty_slot_candidate_period = empty_slot_candidate["period"].values[0]
        idx_tmp = df8.query(f"grade == {g} and `class` == {c} and day == '{empty_slot_candidate_day}' and period == {empty_slot_candidate_period}").index

        if len(idx_tmp) > 0:
          df8.loc[idx_tmp, "subject"] = "書写"
          print(f"success in {g}-{c}")
          cnt_ += 1
        else:
          cnt_shosha += 1
          if cnt_shosha == 500:
            print(f"No candidates in {g}-{c}")
            break
          continue
    success_shosha = True

# 3-4. 1~4年と5,6年の残りの授業

df9 = df8.copy()
success_another_period = False
cnt_another_period = 0
while success_another_period == False and cnt_another_period < 500:
  for g in grade_list:
    for c in class_dict[g]:
      # 体育館が空いてない日にちと時間のリスト
      empty_taiiku_place = df9.query("subject == '体育'")
      empty_taiiku_place_day_period_list = empty_place_day_periods(empty_taiiku_place)

      # 体育館が使える日の1日目の候補を取得
      __empty_slot_candidate = df9.query(f"grade == {g} and `class` == {c} and subject == ''")
      scheduled_day = df9.query(f"grade == {g} and `class` == {c} and subject == '体育'").day.values[0]
      _empty_slot_candidate = __empty_slot_candidate.query(f"day != '{scheduled_day}'")
      empty_slot_candidate = _empty_slot_candidate.loc[~(_empty_slot_candidate[["day","period"]].apply(tuple, axis=1).isin(empty_taiiku_place_day_period_list)),].sample(n=1)
      empty_slot_candidate_day = empty_slot_candidate["day"].values[0]
      empty_slot_candidate_period = empty_slot_candidate["period"].values[0]
      idx_tmp = df9.query(f"grade == {g} and `class` == {c} and day == '{empty_slot_candidate_day}' and period == {empty_slot_candidate_period}").index

      if len(idx_tmp) > 0:
        df9.loc[idx_tmp, "subject"] = "体育"
        print(f"success in {g}-{c}")
      else:
        cnt_another_period += 1
        if cnt_another_period == 500:
          print("No candidates in 5-2")
          break
      success_another_period = True

# 4-2. 3,4年理科週2
df10 = df9.copy()

success_another_rika = False
cnt_another_rika = 0
while success_another_rika == False and cnt_another_rika < 500:
  for g in [3,4]:
    for c in class_dict[g]:
      cnt_ = 0
      while subject_dict[g]["理科"] > cnt_:
        # 理科教員が空いている日のリスト
        scheduled_another_rika = df10.query("subject == '理科'")
        scheduled_another_rika_day_period_list = scheduled_another_rika[["day","period"]].apply(tuple, axis=1)

        # 理科教員が使える日を抜き出す
        __empty_slot_candidate = df10.loc[(df10["grade"] == g) & (df10["class"] == c) & (df10["subject"] == ""),]

        self_scheduled_day = df10.query(f"grade == {g} and `class` == {c} and subject == '理科'").day
        if len(self_scheduled_day) > 0:
          self_scheduled_day = self_scheduled_day.values
        else:
          self_scheduled_day = []
        _empty_slot_candidate = __empty_slot_candidate.loc[~(__empty_slot_candidate["day"].isin(self_scheduled_day)),]
        empty_slot_candidate = _empty_slot_candidate.loc[~(_empty_slot_candidate[["day","period"]].apply(tuple, axis=1).isin(scheduled_another_rika_day_period_list)),].sample(n=1)
        empty_slot_candidate_day = empty_slot_candidate["day"].values[0]
        empty_slot_candidate_period = empty_slot_candidate["period"].values[0]
        idx_tmp = df10.query(f"grade == {g} and `class` == {c} and day == '{empty_slot_candidate_day}' and period == {empty_slot_candidate_period}").index

        if len(idx_tmp) > 0:
          df10.loc[idx_tmp, "subject"] = "理科"
          print(f"success in {g}-{c}")
          cnt_ += 1
        else:
          cnt_another_rika += 1
          if cnt_another_rika == 500:
            print(f"No candidates in {g}-{c}")
            break
          continue
    success_another_rika = True

# 5-2. 1,2年は担任が各クラスの教室で行う
df11 = df10.copy()
success_another_eng = False
cnt_another_eng = 0
while success_another_eng == False and cnt_another_eng < 500:
  for g in grade_list:
    if g not in grade_eng_specialize:
      for c in class_dict[g]:
        cnt_ = 0
        while subject_dict[g]["英語"] > cnt_:
          # そのクラスが空いてる日を抜き出す
          _empty_slot_candidate = df11.loc[(df11["grade"] == g) & (df11["class"] == c) & (df11["subject"] == ""),]

          self_scheduled_day = df11.query(f"grade == {g} and `class` == {c} and subject == '英語'").day
          if len(self_scheduled_day) > 0:
            self_scheduled_day = self_scheduled_day.values
          else:
            self_scheduled_day = []
          empty_slot_candidate = _empty_slot_candidate.loc[~(_empty_slot_candidate["day"].isin(self_scheduled_day)),].sample(n=1)
          empty_slot_candidate_day = empty_slot_candidate["day"].values[0]
          empty_slot_candidate_period = empty_slot_candidate["period"].values[0]
          idx_tmp = df11.query(f"grade == {g} and `class` == {c} and day == '{empty_slot_candidate_day}' and period == {empty_slot_candidate_period}").index
          if len(idx_tmp) > 0:
            df11.loc[idx_tmp, "subject"] = "英語"
            print(f"success in {g}-{c}")
            cnt_ += 1
          else:
            cnt_another_eng += 1
            if cnt_another_eng == 500:
              print(f"No candidates in {g}-{c}")
              break
            continue
      success_another_eng = True

# 6-3. 1,2年は担任が各クラスの教室で行う
df12 = df11.copy()
success_another_music = False
cnt_another_music = 0
while success_another_music == False and cnt_another_music < 500:
  for g in grade_list:
    if g not in grade_music_specialize:
      for c in class_dict[g]:
        cnt_ = 0
        while subject_dict[g]["音楽"] > cnt_:
          # そのクラスが空いてる日を抜き出す
          _empty_slot_candidate = df12.loc[(df12["grade"] == g) & (df12["class"] == c) & (df12["subject"] == ""),]

          self_scheduled_day = df12.query(f"grade == {g} and `class` == {c} and subject == '音楽'").day
          if len(self_scheduled_day) > 0:
            self_scheduled_day = self_scheduled_day.values
          else:
            self_scheduled_day = []
          empty_slot_candidate = _empty_slot_candidate.loc[~(_empty_slot_candidate["day"].isin(self_scheduled_day)),].sample(n=1)
          empty_slot_candidate_day = empty_slot_candidate["day"].values[0]
          empty_slot_candidate_period = empty_slot_candidate["period"].values[0]
          idx_tmp = df12.query(f"grade == {g} and `class` == {c} and day == '{empty_slot_candidate_day}' and period == {empty_slot_candidate_period}").index
          if len(idx_tmp) > 0:
            df12.loc[idx_tmp, "subject"] = "音楽"
            print(f"success in {g}-{c}")
            cnt_ += 1
          else:
            cnt_another_music += 1
            if cnt_another_music == 500:
              print(f"No candidates in {g}-{c}")
              break
            continue
      success_another_music = True

# 7-2. 5,6年の算数の授業は算数教員によって行われる（1~4年は担任が行う）
df13 = df12.copy()
success_another_math = False
cnt_another_math = 0
while success_another_math == False and cnt_another_math < 500:
  for g in grade_list:
    if g not in grade_math_specialize:
      for c in class_dict[g]:
        cnt_ = 0
        while subject_dict[g]["算数"] > cnt_:
          # そのクラスが空いてる日を抜き出す
          _empty_slot_candidate = df13.loc[(df13["grade"] == g) & (df13["class"] == c) & (df13["subject"] == ""),]

          self_scheduled_day = df13.query(f"grade == {g} and `class` == {c} and subject == '算数'").day
          if len(self_scheduled_day) > 0:
            self_scheduled_day = self_scheduled_day.values
          else:
            self_scheduled_day = []
          empty_slot_candidate = _empty_slot_candidate.loc[~(_empty_slot_candidate["day"].isin(self_scheduled_day)),].sample(n=1)
          empty_slot_candidate_day = empty_slot_candidate["day"].values[0]
          empty_slot_candidate_period = empty_slot_candidate["period"].values[0]
          idx_tmp = df13.query(f"grade == {g} and `class` == {c} and day == '{empty_slot_candidate_day}' and period == {empty_slot_candidate_period}").index
          if len(idx_tmp) > 0:
            df13.loc[idx_tmp, "subject"] = "算数"
            print(f"success in {g}-{c}")
            cnt_ += 1
          else:
            cnt_another_math += 1
            if cnt_another_math == 500:
              print(f"No candidates in {g}-{c}")
              break
            continue
      success_another_math = True

# 9-2. 3,4年は担任が書写の授業を各教室で行う
df14 = df13.copy()
success_another_shosha = False
cnt_another_shosha = 0
while success_another_shosha == False and cnt_another_shosha < 500:
  for g in grade_list:
    if g not in grade_shosha_specialize:
      for c in class_dict[g]:
        cnt_ = 0
        while subject_dict[g]["書写"] > cnt_:
          # そのクラスが空いてる日を抜き出す
          _empty_slot_candidate = df14.loc[(df14["grade"] == g) & (df14["class"] == c) & (df14["subject"] == ""),]

          self_scheduled_day = df14.query(f"grade == {g} and `class` == {c} and subject == '書写'").day
          if len(self_scheduled_day) > 0:
            self_scheduled_day = self_scheduled_day.values
          else:
            self_scheduled_day = []
          empty_slot_candidate = _empty_slot_candidate.loc[~(_empty_slot_candidate["day"].isin(self_scheduled_day)),].sample(n=1)
          empty_slot_candidate_day = empty_slot_candidate["day"].values[0]
          empty_slot_candidate_period = empty_slot_candidate["period"].values[0]
          idx_tmp = df14.query(f"grade == {g} and `class` == {c} and day == '{empty_slot_candidate_day}' and period == {empty_slot_candidate_period}").index
          if len(idx_tmp) > 0:
            df14.loc[idx_tmp, "subject"] = "書写"
            print(f"success in {g}-{c}")
            cnt_ += 1
          else:
            cnt_another_shosha += 1
            if cnt_another_shosha == 500:
              print(f"No candidates in {g}-{c}")
              break
            continue
      success_another_shosha = True

normal_subject_list = ["国語","社会","図工","生活"]
df15 = df14.copy()

for subject in normal_subject_list:
  for g in grade_list:
    for c in class_dict[g]:
      cnt_ = 0
      while subject_dict[g][subject] > cnt_:
          # そのクラスが空いてる日を抜き出す
          _empty_slot_candidate = df15.loc[(df15["grade"] == g) & (df15["class"] == c) & (df15["subject"] == ""),]

          self_scheduled_day = df15.query(f"grade == {g} and `class` == {c} and subject == '{subject}'").day
          if len(self_scheduled_day) > 0:
            self_scheduled_day = self_scheduled_day.values
          else:
            self_scheduled_day = []

          empty_slot_candidate = _empty_slot_candidate.loc[~(_empty_slot_candidate["day"].isin(self_scheduled_day)),]
          if len(empty_slot_candidate.index) == 0:
            empty_slot_candidate = _empty_slot_candidate
          empty_slot_candidate_day = empty_slot_candidate["day"].values[0]
          empty_slot_candidate_period = empty_slot_candidate["period"].values[0]
          idx_tmp = df15.query(f"grade == {g} and `class` == {c} and day == '{empty_slot_candidate_day}' and period == {empty_slot_candidate_period}").index
          if len(idx_tmp) > 0:
            df15.loc[idx_tmp, "subject"] = subject
            print(f"success in {g}-{c}")
            cnt_ += 1
          else:
            cnt_another_shosha += 1
            if cnt_another_shosha == 500:
              print(f"No candidates in {g}-{c}")
              break
            continue
      success_another_shosha = True