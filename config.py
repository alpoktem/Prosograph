#ProsViz file to store constants

#data file paths
DATASET="dataset/SAMPLETED.pickle"
VOCABULARY="dataset/vocabulary"

#constants
PUNC_CODES = {0: '?', 1: '!', 2: '', 3: ',', 4: '-', 5: ':', 6: ';', 7: '.'}
DIR_SAVED_FRAMES = "saved-frames"

#look constants
#WINDOW_WIDTH = 1280   #full screen
#WINDOW_HEIGHT = 650   #full screen
LEGEND_BOX_SIZE = 20
LEGEND_HEIGHT = 30
LEGEND_TEXT_SIZE = 12
TEXT_SIZE = 20
JUMP_TO_FEATURE_LINE_OFFSET = int(TEXT_SIZE * 2.5)
JUMP_TO_TEXTLINE_OFFSET = int(TEXT_SIZE * 1.5)

NUM_SAMPLES_PER_SCREEN = 3

WINDOW_WIDTH = 1280
#WINDOW_HEIGHT = 650
WINDOW_HEIGHT = (NUM_SAMPLES_PER_SCREEN * (JUMP_TO_FEATURE_LINE_OFFSET + JUMP_TO_TEXTLINE_OFFSET)) + LEGEND_HEIGHT
TEXT_SPACE_WIDTH = TEXT_SIZE / 10 
POINT_VALUE_MARKER_SIZE = TEXT_SIZE / 5
PERCENTAGE_VALUE_MARKER_SIZE = TEXT_SIZE / 3
PAUSE_AMPLIFICATION= TEXT_SIZE / 4
WORD_AMPLIFICATION = TEXT_SIZE * 3 #!!!!
FONT_TYPE = "Arial"

WORD_BOX_COLOR=[0, 100, 255, 107]
WORD_BOX_LIT_COLOR=[47, 211, 199, 107]  #color if it has a binary-value 1

#feature names in the dataset
#all_feature_names = ['pause', 'word', 'bins.f0', 'mean.f0', 'jump.f0', 'med.f0', 'mean.i0', 'bins.i0', 'sd.f0', 'slope.f0', 'punctuation']
word_key = 'word'    #integer value which has the corresponding text in the vocabulary
punctuation_after_key = 'punctuation'    #integer that corresponds to a punctuation mark in PUNC_CODES
pause_after_key = 'pause'       #this corresponds to silence after the word. a space will be put before
word_duration_key = '' 
binary_feature_key = 'word_stress'
#word_duration_key = 'duration'      #if this value exists words will be stretched according to their duration

point_feature_keys = ['sd.f0', 'med.f0']
#point_feature_keys = []
line_feature_keys = ['mean.f0', 'mean.i0']
curve_feature_keys = ['bins.f0']

#percentage_feature_keys = ['accent']
percentage_feature_keys = []

no_of_bins_in_curve_features = 10
words_per_sample = 50