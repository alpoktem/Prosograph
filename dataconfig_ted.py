#data file paths
DATASET="dataset/0001.pcl"
DATA_IS_SAMPLED=False

#feature names in the dataset
#all_feature_names = ['pause', 'word', 'bins.f0', 'mean.f0', 'jump.f0', 'med.f0', 'mean.i0', 'bins.i0', 'sd.f0', 'slope.f0', 'punctuation']
word_key = 'word'    #integer value which has the corresponding text in the vocabulary
punctuation_before_key = 'punctuation'
pause_before_key = 'pause'       #this corresponds to silence before the word. a space will be put before
word_duration_key = '' 
binary_feature_key = ''
#word_duration_key = 'duration'      #if this value exists words will be stretched according to their duration
label_feature_key = ''

draw_feature_line = True
point_feature_keys = []
point_feature_keys = ['range.i0']
line_feature_keys = ['mean.i0']
#line_feature_keys = ['mean.i0']
curve_feature_keys = []
percentage_feature_keys = []