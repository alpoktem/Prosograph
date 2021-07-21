DATASET = "/Users/alp/Documents/phdCloud/playground/Prosograph/data/ted"  #Change this to the exact location of the dataset
dataset_tags = {}

word_key = 'word'  
punctuation_before_key = 'punctuation_before'
draw_punctuation = True
pause_before_key = 'pause_before'
draw_pause_boxes = True
word_duration_key = '' 
draw_word_duration = False
binary_feature_key = ''
label_feature_key = 'pos'
draw_label_feature = False

draw_feature_line = True
point_feature_keys = ['i0_mean']
line_feature_keys = ['f0_mean']
curve_feature_keys = ['f0_contour', 'i0_contour']
curve_axis_keys = ['f0_contour_xaxis', 'i0_contour_xaxis']
evened_curve_feature_keys = []
percentage_feature_keys = [] 

minFeatureVal = -10
maxFeatureVal = 10

color_dict = {'f0_mean': [75, 150, 225, 255], 'i0_mean': [150, 100, 175, 255]}
