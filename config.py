#ProsViz file to store constants

#data file paths
DATASET="dataset/0001.pickle"

#constants
DIR_SAVED_FRAMES = "saved-frames"

#LOOK CONSTANTS
#how much content to fit
NUM_WORDS_TO_SKIP_ON_PAGE_TURN = 20
#sizes
TEXT_SIZE = 20
LEGEND_BOX_SIZE = TEXT_SIZE
LEGEND_HEIGHT = int(TEXT_SIZE * 1.6)
LEGEND_TEXT_SIZE = int(TEXT_SIZE * 0.6)
JUMP_TO_FEATURE_LINE_OFFSET = int(TEXT_SIZE * 2.5)
JUMP_TO_TEXTLINE_OFFSET = int(TEXT_SIZE * 1.5)
WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 600
TEXT_SPACE_WIDTH = TEXT_SIZE / 10 
POINT_VALUE_MARKER_SIZE = TEXT_SIZE / 5
PERCENTAGE_VALUE_MARKER_SIZE = TEXT_SIZE / 3
PAUSE_AMPLIFICATION= TEXT_SIZE / 4
WORD_AMPLIFICATION = TEXT_SIZE * 3 #!!!!
EMPTY_SPACE_BTW_TEXT_FEATURES = 5
FONT_TYPE = "Arial"
RIGHT_AXIS_LENGTH=30

#colors
WORD_BOX_COLOR=[0, 100, 255, 107]
WORD_BOX_LIT_COLOR=[47, 211, 199, 107]  #color if it has a binary-value 1

#feature names in the dataset
#all_feature_names = ['pause', 'word', 'bins.f0', 'mean.f0', 'jump.f0', 'med.f0', 'mean.i0', 'bins.i0', 'sd.f0', 'slope.f0', 'punctuation']
word_key = 'word'    #integer value which has the corresponding text in the vocabulary
punctuation_before_key = 'punctuation'
#punctuation_after_key = 'punctuation'    #integer that corresponds to a punctuation mark in PUNC_CODES
pause_before_key = 'pause'       #this corresponds to silence after the word. a space will be put before
word_duration_key = '' 
binary_feature_key = ''
#word_duration_key = 'duration'      #if this value exists words will be stretched according to their duration

point_feature_keys = ['range.f0', 'range.i0']
line_feature_keys = ['mean.f0', 'mean.i0']
curve_feature_keys = []

percentage_feature_keys = []

no_of_bins_in_curve_features = 10
words_per_line = 30