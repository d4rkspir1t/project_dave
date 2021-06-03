import cv2
import numpy as np
import pandas as pd
import os
import shutil


clear_img = 'src_vid_images/izgray.png'
onset_img = 'src_vid_images/iznotonlygray.png'
db_paths = []
for _, _, files in os.walk('c_onset_output', topdown=True):
    # print(files)
    for f in files:
        file_path = os.path.join('c_onset_output', f)
        db_paths.append(file_path)

for part_file in db_paths:
    df = pd.read_csv(part_file, parse_dates=True)
    # part_no = part_file.split('_')[-1].split('.')[0]
    part_no = part_file.split('_')[-2]
    # print(df.head(5))
    # print(df.columns)
    # vid_col_labels = [
    #                 ['hch_beats', 'hch_onsets', 'hch_onsets_abs'],
    #                 ['hhc_beats', 'hhc_onsets', 'hhc_onsets_abs'],
    #                 ['nhp_beats', 'nhp_onsets', 'nhp_onsets_abs'],
    #                 ['nhnp_beats', 'nhnp_onsets', 'nhnp_onsets_abs']]
    vid_col_labels = [
        ['nhp_beats_const', 'nhp_onsets_const', 'nhp_onsets_abs_const'],
        ['nhnp_beats_const', 'nhnp_onsets_const', 'nhnp_onsets_abs_const']]

    # vid_paths = ['vid_out/hch', 'vid_out/hhc', 'vid_out/nhp', 'vid_out/nhnp']
    vid_paths = ['vidc_out/nhpC', 'vidc_out/nhnpC']
    # skip_array = [0, 1, 2]
    for idx, vid_col in enumerate(vid_col_labels):
        # if idx in skip_array:
        #     continue
        tmp_df = df[vid_col]
        # print(tmp_df.head(5))
        # print(tmp_df.columns)
        onsets = tmp_df[vid_col[2]].tolist()
        print(onsets)

        img_path_array = []
        active_onset = False
        onset_end = 0
        onset_id_track = 0
        for fr in range(0, 128*200):
            if onset_id_track < len(onsets):
                if fr == int(onsets[onset_id_track]*100*2):
                    # print('trigger')
                    onset_id_track += 1
                    active_onset = True
                    onset_end = fr+40
            if fr >= onset_end and active_onset:
                active_onset = False

            if active_onset:
                img_path_array.append(onset_img)
            else:
                img_path_array.append(clear_img)
        # print(img_path_array)
        # print(img_path_array[162:250])
        vid_path = '%s_%s.avi' % (vid_paths[idx], part_no)

        print('Making writer')
        img = cv2.imread(img_path_array[0])
        height, width, layers = img.shape
        size = (width, height)

        out = cv2.VideoWriter(vid_path, cv2.VideoWriter_fourcc(*'DIVX'), 200, size)
        print('Starting writer')
        c = 0
        for img_path in img_path_array:
            c += 1
            if c % 12500 == 0:
                print('%d/%d' % (c, len(img_path_array)))
            img = cv2.imread(img_path)
            height, width, layers = img.shape
            size = (width, height)
            out.write(img)

        out.release()
        print('Done with %s (%dth)' % (part_no, idx))
        # if idx == 0:
        #     new_path = '%s_%s.avi' % (vid_paths[1], part_no)
        #     shutil.copy(vid_path, new_path)
        # break
    # break
