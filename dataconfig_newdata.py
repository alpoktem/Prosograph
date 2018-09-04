#DATASET = "/Users/alp/phdCloud/playground/Prosograph/newdata/spk01f_01.csv"
#DATASET = "/Users/alp/Desktop/proscripter_test/alp/alp_1.csv"
#DATASET="/Users/alp/phdCloud/playground/proscripter_test/journal/sent34.csv"
#DATASET = "/Users/alp/phdCloud/playground/parsing_ws/ted_data/sample_proscripts"
#DATASET = "/Users/alp/Documents/Corpora/ted_data/punkProse_corpus/compiled/0001.csv"
#DATASET = "/Users/alp/Desktop/proscripter_test/whaddya"
DATASET = "/Users/alp/phdCloud/playground/punkProse_asr-demo/rec"
dataset_tags = {'0':'raw' ,'1':'word only', '2':'word+POS+pause+f0.mean'}

#DATASET = "/Users/alp/Movies/heroes/corpus/heroes_s2_7_mini/spa-eng/segments_eng"
#dataset_tags = {}

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
evened_curve_feature_keys = ['f0_contour_semitones']
percentage_feature_keys = [] 

minFeatureVal = -10
maxFeatureVal = 10
