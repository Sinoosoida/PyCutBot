def get_new_frame_codes(cuts, frame_codes):
    new_frame_codes = []

    pos_in_cuts = -1
    deleted_frames_num = 0

    def serve_frame_code(_frame_code, _pos_in_cuts, _deleted_frames_num):
        if _frame_code < cuts[0][0]:
            return _frame_code, _pos_in_cuts, _deleted_frames_num
        if cuts[_pos_in_cuts][0] <= _frame_code <= cuts[_pos_in_cuts][1]:
            print('IN CUT')
            print(f'_pos_in_cuts: {_pos_in_cuts, cuts[_pos_in_cuts][0] - 1}')
            return max(0, cuts[_pos_in_cuts][0] - 1 - _deleted_frames_num), _pos_in_cuts, _deleted_frames_num
        if _frame_code > cuts[-1][1]:
            print('FINAL')
            return _frame_code - _deleted_frames_num, _pos_in_cuts, _deleted_frames_num
        if not (cuts[_pos_in_cuts][1] < _frame_code < cuts[_pos_in_cuts + 1][0]):
            print('REC')
            return serve_frame_code(_frame_code, _pos_in_cuts + 1,
                                    _deleted_frames_num + cuts[_pos_in_cuts][1] - cuts[_pos_in_cuts][0] + 1)
        # _deleted_frames_num += cuts[_pos_in_cuts][1] - cuts[_pos_in_cuts][0] + 1
        # print(cuts[_pos_in_cuts][1], cuts[_pos_in_cuts + 1][0])
        return _frame_code - _deleted_frames_num - (
                cuts[_pos_in_cuts][1] - cuts[_pos_in_cuts][0] + 1), _pos_in_cuts, _deleted_frames_num

    for frame_code in frame_codes:
        print(f'frame code:{frame_code}')
        new_frame_code, pos_in_cuts, deleted_frames_num = serve_frame_code(frame_code, pos_in_cuts, deleted_frames_num)
        print(f'new frame code: {new_frame_code}, '
              f'pos in cuts: {pos_in_cuts}, '
              f'del num: {deleted_frames_num}')
        print('-' * 20)
        new_frame_codes.append(new_frame_code)
    return new_frame_codes
