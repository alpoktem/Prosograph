DATASET = "/Users/alp/Movies/heroes/corpus/heroes_s2_1/spa-eng/segments_eng"
dataset_tags = {}

word_key = 'word'    #integer value which has the corresponding text in the vocabulary
punctuation_before_key = 'punctuation_before'
draw_punctuation = True
pause_before_key = 'pause_before'
draw_pause_boxes = True
word_duration_key = '' 
draw_word_duration = False
binary_feature_key = ''
label_feature_key = 'pos'
draw_label_feature = True

draw_feature_line = True
point_feature_keys = ['i0_mean']
line_feature_keys = ['f0_mean']
curve_feature_keys = []
curve_axis_keys = []
evened_curve_feature_keys = []
percentage_feature_keys = [] 

minFeatureVal = -15
maxFeatureVal = 15
