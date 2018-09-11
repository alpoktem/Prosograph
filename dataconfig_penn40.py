#data file paths
DATASET="dataset/penn40.pcl"
DATA_IS_SAMPLED=False

#feature names in the dataset
#all_feature_names = ['pause', 'word', 'bins.f0', 'mean.f0', 'jump.f0', 'med.f0', 'mean.i0', 'bins.i0', 'sd.f0', 'slope.f0', 'punctuation']
word_key = 'word'    #integer value which has the corresponding text in the vocabulary
punctuation_before_key = 'punctuation'
binary_feature_key = 'pitch'
label_feature_key = 'tobi'
word_duration_key = '' 
pause_before_key = 'pause'       #this corresponds to silence before the word. a space will be put before

point_feature_keys = ['mean.f0']
line_feature_keys = []
curve_feature_keys = ['contour.f0']
percentage_feature_keys = []