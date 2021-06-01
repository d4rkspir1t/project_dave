import itertools
import pandas as pd
import random

df = pd.read_csv('src_data/nagyobbikszar.csv', parse_dates=True)
# print(df.head(5))
print(df.columns)

df_sub = df[['Onset_periodic_intrial', 'Onset_nonperiodic_intrial',
             'Onset_periodic_absolute', 'Onset_nonperiodic_absolute',
             'Clause', 'Beat_inclause', 'Cymbal_nonh', 'Tone1_nonh', 'Tone2_nonh']]
print(df_sub.head(5))
print(df_sub.columns)
# exit()


def full_time_calculator(onsets):
    full_onsets = []
    for idx, onset in enumerate(onsets):
        full_timestamp = onset + 2*idx
        full_onsets.append(full_timestamp)
    return full_onsets


def calc_dicts():
    p_dict = {}
    np_dict = {}
    clause = 0

    for idx, row in df_sub.iterrows():
        # print(idx)
        # print(row[0], row[1], int(row[5]))
        beat = int(row[5])
        if beat not in p_dict.keys():
            p_dict[beat] = []
        p_dict[beat].append(float(row[0]))

        if clause not in np_dict.keys():
            np_dict[clause] = []
        np_dict[clause].append(float(row[1]))

        if (idx + 1) % 8 == 0:
            clause += 1

    return p_dict, np_dict


def beat_distributor(bam, ctbm):
    for beat in range(1, 9):
        try:
            clauses = random.sample(bam[beat], 5)
        except:
            # print('ERROR', beat, bam[beat])
            continue
        for clause in clauses:
            ctbm[clause] = beat
            if beat < 8:
                for key in range(beat+1, 9):
                    if clause in bam[key]:
                        bam[key].remove(clause)
    # print(clause_to_beat_map)
    safety_check = {}
    for key in sorted(ctbm.keys()):
        beat = ctbm[key]
        # print(key, beat)
        if beat not in safety_check.keys():
            safety_check[beat] = 0
        safety_check[beat] += 1
    complete_list = True
    for val in safety_check:
        if val != 8:
            complete_list = False
    return ctbm, complete_list


def calc_ctt_matches():
    c_mathes = {}
    t1_matches = {}
    t2_matches = {}
    remaining_clauses = [*range(1, 65)]
    clause_to_beat_map = {}
    beat_availability_map = {}

    for idx, row in df_sub.iterrows():
        # print(idx, clause, row[4], row[5], row[6], row[7], row[8])
        clause = int(row[4])
        cplace = int(row[6])
        t1place = int(row[7])
        t2place = int(row[8])
        if cplace not in c_mathes.keys():
            c_mathes[cplace] = []
        if t1place not in t1_matches.keys():
            t1_matches[t1place] = []
        if t2place not in t2_matches.keys():
            t2_matches[t2place] = []

        if clause not in c_mathes[cplace]:
            c_mathes[cplace].append(clause)
        if clause not in t1_matches[t1place]:
            t1_matches[t1place].append(clause)
        if clause not in t2_matches[t2place]:
            t2_matches[t2place].append(clause)

    # print(t1_matches)
    for key, val in c_mathes.items():
        clause = random.choice(val)
        for t1key, t1val in t1_matches.items():
            if clause in t1val:
                t1val.remove(clause)
        for t2key, t2val in t2_matches.items():
            if clause in t2val:
                t2val.remove(clause)
        if clause in remaining_clauses:
            remaining_clauses.remove(clause)
        print(key, clause)
        clause_to_beat_map[clause] = key
    print('----')
    for key, val in t1_matches.items():
        clause = random.choice(val)
        for t2key, t2val in t2_matches.items():
            if clause in t2val:
                t2val.remove(clause)
        if clause in remaining_clauses:
            remaining_clauses.remove(clause)
        print(key, clause)
        clause_to_beat_map[clause] = key
    print('----')
    for key, val in t2_matches.items():
        clause = random.choice(val)
        if clause in remaining_clauses:
            remaining_clauses.remove(clause)
        print(key, clause)
        clause_to_beat_map[clause] = key
    # print(t1_matches)
    # print(t2_matches)
    print(remaining_clauses, len(remaining_clauses))

    for idx, row in df_sub.iterrows():
        # print(idx, clause, row[4], row[5], row[6], row[7], row[8])
        clause = int(row[4])
        beat_in_clause = int(row[5])
        cplace = int(row[6])
        t1place = int(row[7])
        t2place = int(row[8])
        match_with = beat_in_clause == cplace or beat_in_clause == t1place or beat_in_clause == t2place
        # print(match_with)
        if clause not in clause_to_beat_map.keys() and not match_with:
            if beat_in_clause not in beat_availability_map.keys():
                beat_availability_map[beat_in_clause] = []
            beat_availability_map[beat_in_clause].append(clause)
    # print(beat_availability_map)


    # val_rarity = {}
    # for key, val in beat_availability_map.items():
    #     print(key, len(val), val)
    #     for clause in val:
    #         if clause not in val_rarity.keys():
    #             val_rarity[clause] = 0
    #         val_rarity[clause] += 1
    # print(val_rarity)
    all_delegated = False
    trial = 0
    while not all_delegated:
        trial += 1
        print('TRIAL', trial)
        ctbm, success = beat_distributor(beat_availability_map.copy(), clause_to_beat_map.copy())
        if success:
            all_delegated = True

    full_ctbm = {**clause_to_beat_map, **ctbm}
    for key in sorted(full_ctbm.keys()):
        beat = full_ctbm[key]
        print(key, beat)
    return c_mathes, t1_matches, t2_matches


for person_idx in range(120, 180):
    perint_dict, nperint_dict = calc_dicts()
    # NON CONSTRAINED SHUFFLING FOR HCHHHC AND NHP CASES
    # --------------------------------------------------
    hchhhc_sel_beats = []
    hchhhc_onsets = []
    nhp_sel_beats = []
    nhp_onsets = []
    # --------------------------------------------------
    nhnp_sel_beats = []
    nhnp_onsets = []
    nhp_sel_beats_plusconst = []
    nhp_onsets_plusconst = []
    nhnp_sel_beats_plusconst = []
    nhnp_onsets_plusconst = []

    # NON CONSTRAINED SHUFFLING FOR HCHHHC AND NHP CASES
    # --------------------------------------------------
    for key, val in perint_dict.items():
        onset_options = val
        for _ in range(8):
            hchhhc_sel_beats.append(key)
            nhp_sel_beats.append(key)
            hchhhc_onsets.append(onset_options[0])
            nhp_onsets.append(onset_options[0])
    # --------------------------------------------------

    # print(nperint_dict.items())
    beat_list = range(1, 9)
    full_beat_list = list(itertools.chain.from_iterable(itertools.repeat(x, 8) for x in beat_list))
    random.shuffle(full_beat_list)
    print(full_beat_list)
    print(len(nperint_dict.keys()))
    for key, val in nperint_dict.items():
        beat = full_beat_list[key]
        nhnp_sel_beats.append(beat)
        nhnp_onsets.append(val[beat-1])

    # NON CONSTRAINED SHUFFLING FOR HCHHHC AND NHP CASES
    # --------------------------------------------------
    hchhhc_zip = list(zip(hchhhc_sel_beats, hchhhc_onsets))
    random.shuffle(hchhhc_zip)
    hchhhc_sel_beats, hchhhc_onsets = zip(*hchhhc_zip)

    nhp_zip = list(zip(nhp_sel_beats, nhp_onsets))
    random.shuffle(nhp_zip)
    nhp_sel_beats, nhp_onsets = zip(*nhp_zip)
    # --------------------------------------------------

    # NON CONSTRAINED SHUFFLING FOR HCHHHC AND NHP CASES
    # --------------------------------------------------
    print(hchhhc_sel_beats)
    print(hchhhc_onsets)
    print(nhp_sel_beats)
    print(nhp_onsets)
    # --------------------------------------------------
    print(nhnp_sel_beats)
    print(nhnp_onsets)
    print(nhp_sel_beats_plusconst)
    print(nhp_onsets_plusconst)
    print(nhnp_sel_beats_plusconst)
    print(nhnp_onsets_plusconst)

    # NON CONSTRAINED SHUFFLING FOR HCHHHC AND NHP CASES
    # --------------------------------------------------
    hchhhc_onsets_full = full_time_calculator(hchhhc_onsets)
    nhp_onsets_full = full_time_calculator(nhp_onsets)
    print(hchhhc_onsets_full)
    print(nhp_onsets_full)
    # --------------------------------------------------
    nhnp_onsets_full = full_time_calculator(nhnp_onsets)
    nhp_onsets_plusconst_full = full_time_calculator(nhp_onsets_plusconst)
    nhnp_onsets_plusconst_full = full_time_calculator(nhnp_onsets_plusconst)
    print(nhnp_onsets_full)
    print(nhp_onsets_plusconst_full)
    print(nhnp_onsets_plusconst_full)

    calc_ctt_matches()
    exit()

    # NON CONSTRAINED SHUFFLING FOR HCHHHC AND NHP CASES - COMBINE WITH NEXT IF REGENERATING FULL SET
    # --------------------------------------------------
    output_name = 'onset_output/participant_id_%d.csv' % person_idx
    onset_df = pd.DataFrame(
        list(zip(hchhhc_sel_beats, hchhhc_onsets, hchhhc_onsets_full,
                 hchhhc_sel_beats, hchhhc_onsets, hchhhc_onsets_full,
                 nhp_sel_beats, nhp_onsets, nhp_onsets_full,
                 nhnp_sel_beats, nhnp_onsets, nhnp_onsets_full)),
        columns=['hch_beats', 'hch_onsets', 'hch_onsets_abs',
                 'hhc_beats', 'hhc_onsets', 'hhc_onsets_abs',
                 'nhp_beats', 'nhp_onsets', 'nhp_onsets_abs',
                 'nhnp_beats', 'nhnp_onsets', 'nhnp_onsets_abs'])
    # --------------------------------------------------
    # output_name = 'onset_output/participant_id_%d_nhnp.csv' % person_idx
    # onset_df = pd.DataFrame(
    #     list(zip(nhnp_sel_beats, nhnp_onsets, nhnp_onsets_full#,
    #              # nhp_sel_beats_plusconst, nhp_onsets_plusconst, nhp_onsets_plusconst_full,
    #              # nhnp_sel_beats_plusconst, nhnp_onsets_plusconst, nhnp_onsets_plusconst_full
    #              )),
    #     columns=['nhnp_beats', 'nhnp_onsets', 'nhnp_onsets_abs'#,
    #              # 'nhp_beats_const', 'nhp_onsets_const', 'nhp_onsets_abs_const',
    #              # 'nhnp_beats_const', 'nhnp_onsets_const', 'nhnp_onsets_abs_const'
    #              ])
    onset_df.to_csv(output_name, mode='w', index=False, header=True)
    # break
