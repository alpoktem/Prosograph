import cPickle
import codecs
import config
import random

randomColorVals = [0, 20, 50, 75, 100, 125, 150, 175, 200, 225, 250]
numRandomColorVals = 11

def setup():
    size(config.WINDOW_WIDTH, config.WINDOW_HEIGHT)
    ellipseMode(CENTER)

    global dataset
    with open(config.DATASET, 'rb') as f:
        dataset = cPickle.load(f)
        
    global dataset_size
    dataset_size = len(dataset[config.word_key])

    global font
    font = createFont(config.FONT_TYPE, config.TEXT_SIZE, True)
    textFont(font)  
    textAlign(LEFT)
    
    global draw_from_word_no
    draw_from_word_no = 0
    
    initializeColors()
    initializeDrawOrNot()
    initializeMinMaxOfFeatures()
    
def initializeDrawOrNot():
    #initialize drawOrNot arrays for features (this is written for later)
    global point_features_drawOrNot_dict
    point_features_drawOrNot_dict = createDrawOrNotDict(config.point_feature_keys)
    global line_features_drawOrNot_dict
    line_features_drawOrNot_dict = createDrawOrNotDict(config.line_feature_keys)
    global curve_features_drawOrNot_dict
    curve_features_drawOrNot_dict = createDrawOrNotDict(config.curve_feature_keys)
    global percentage_features_drawOrNot_dict
    percentage_features_drawOrNot_dict = createDrawOrNotDict(config.percentage_feature_keys)
    
def initializeMinMaxOfFeatures():
    minFeatureVal = 0
    global maxFeatureVal
    maxFeatureVal = 0
    
    for featureName in config.point_feature_keys:
        minFeatureVal = min(minFeatureVal, min(dataset[featureName]))
        maxFeatureVal = max(maxFeatureVal, max(dataset[featureName]))
    for featureName in config.line_feature_keys:
        minFeatureVal = min(minFeatureVal, min(dataset[featureName]))
        maxFeatureVal = max(maxFeatureVal, max(dataset[featureName]))
    for featureName in config.curve_feature_keys:
        minFeatureVal = min(minFeatureVal, min(dataset[featureName]))
        maxFeatureVal = max(maxFeatureVal, max(dataset[featureName]))
        
    maxFeatureVal = max(abs(minFeatureVal), abs(maxFeatureVal))
    
def fitFeatureValueToBoxRange(value, boxSize):
    return int(value/maxFeatureVal * boxSize)
    
def initializeColors():
    #initialize colors for drawing features
    #if config.point_feature_keys:
    global point_features_colors_dict
    point_features_colors_dict = createColorDict(config.point_feature_keys)
    global line_features_colors_dict
    line_features_colors_dict = createColorDict(config.line_feature_keys)
    global curve_features_colors_dict
    curve_features_colors_dict = createColorDict(config.curve_feature_keys)
    global percentage_features_colors_dict
    percentage_features_colors_dict = createColorDict(config.percentage_feature_keys)

def createColorDict(featureList):
    dict = { feature : [randomColorVals[random.randrange(0, numRandomColorVals)], 
                        randomColorVals[random.randrange(0, numRandomColorVals)],
                        randomColorVals[random.randrange(0, numRandomColorVals)]] for feature in featureList }
    return dict

def createDrawOrNotDict(featureList):
    #all set to draw
    dict = { feature : 1 for feature in featureList }
    return dict

def createMinMaxDict(featureList):
    global dataset
    dict = {featureName: (min(dataset[featureName]), max(dataset[featureName])) for featureName in featureList}
    return dict

def drawWords(start_drawing_from):
    strokeWeight(0.5)
    brushX = 0
    brushY = 3
    wordBoundingBoxSize = config.TEXT_SIZE + 4

    for index in range(start_drawing_from, dataset_size):
        pause_duration = dataset[config.pause_before_key][index]
        punctuation = dataset[config.punctuation_before_key][index]
        word = dataset[config.word_key][index]
        
        #calculate word width
        if config.word_duration_key:
            wordGraphicWidth = int(dataset[config.word_duration_key][index] * textWidth(word))
        else:
            wordGraphicWidth = textWidth(word) 
        #see if still on the screen horizontally, if not skip to next line
        if brushX + wordGraphicWidth >= config.WINDOW_WIDTH - config.RIGHT_AXIS_LENGTH:
            brushX = 0
            brushY += 3 * wordBoundingBoxSize + 2*config.EMPTY_SPACE_BTW_TEXT_FEATURES
        #see if new can line fit on the screen vertically, if not stop drawing new words
        if not brushY + wordBoundingBoxSize * 3 <= config.WINDOW_HEIGHT - config.LEGEND_HEIGHT:
            break
        
        pause_box_width = int(pause_duration * config.PAUSE_AMPLIFICATION)
        if pause_box_width > 0: #pause
            pause_rect_x = brushX - 1
            pause_rect_y = brushY - 1
            pause_rect_width = pause_box_width + 1
            pause_rect_height = config.TEXT_SIZE + 4
            fill(255,200,0, 107)
            stroke(0)
            rect(pause_rect_x, pause_rect_y, pause_rect_width, pause_rect_height)  # bu pause uzunlugunda olacak
            if not punctuation == '':
                fill(0)
                if pause_rect_width < textWidth(punctuation):
                    punctuation_x = pause_rect_x - 1
                else:
                    punctuation_x = pause_rect_x + pause_rect_width/2 - 1
                text(punctuation, punctuation_x, brushY + config.TEXT_SIZE)
            brushX += pause_box_width + 1
        elif not punctuation == '':
            punctuationWidth = textWidth(punctuation)
            fill(255,0,0,107)
            stroke(0)
            rect(brushX - 1, brushY - 1, punctuationWidth + 2, wordBoundingBoxSize) 
            fill(0)
            text(punctuation, brushX, brushY + config.TEXT_SIZE)
            brushX += textWidth(punctuation) + 2 #+ config.TEXT_SPACE_WIDTH
        
        #draw word bounding box
        stroke(0)
        if config.binary_feature_key and dataset[config.binary_feature_key][index]:
            fill(config.WORD_BOX_LIT_COLOR[0],config.WORD_BOX_LIT_COLOR[1],config.WORD_BOX_LIT_COLOR[2], config.WORD_BOX_LIT_COLOR[3])
        else:
            fill(config.WORD_BOX_COLOR[0],config.WORD_BOX_COLOR[1],config.WORD_BOX_COLOR[2], config.WORD_BOX_COLOR[3])
        wordBoxStartX = brushX - 1
        wordBoxEndX = brushX - 1 + wordGraphicWidth + 2
        rect(brushX - 1, brushY - 1, wordGraphicWidth + 2, config.TEXT_SIZE + 4)
        #write word
        fill(0)
        text(word, brushX, brushY + config.TEXT_SIZE)
        brushX += wordGraphicWidth + 2 # + config.TEXT_SPACE_WIDTH
        
        #draw features line below words
        brushY += 2*wordBoundingBoxSize + config.EMPTY_SPACE_BTW_TEXT_FEATURES
        #draw the zero line
        stroke(0)
        line(0,brushY, config.WINDOW_WIDTH - config.RIGHT_AXIS_LENGTH, brushY)
        #draw line features
        for line_feature_name in config.line_feature_keys:
            if line_features_drawOrNot_dict[line_feature_name]:
                
                stroke(line_features_colors_dict[line_feature_name][0],
                    line_features_colors_dict[line_feature_name][1],
                    line_features_colors_dict[line_feature_name][2])
                
                value = dataset[line_feature_name][index]
                rangedValue = fitFeatureValueToBoxRange(value, wordBoundingBoxSize)
                line(wordBoxStartX, brushY - rangedValue, wordBoxEndX, brushY - rangedValue)
    
        #draw curve features
        for curve_feature_name in config.curve_feature_keys:
            if curve_features_drawOrNot_dict[curve_feature_name]:
                
                stroke(curve_features_colors_dict[curve_feature_name][0],
                    curve_features_colors_dict[curve_feature_name][1],
                    curve_features_colors_dict[curve_feature_name][2])
                
                bin_length_in_x = (wordBoxEndX - wordBoxStartX) / config.no_of_bins_in_curve_features
                curr_bin_offset = 0
                for bin_no in range(config.no_of_bins_in_curve_features):
                    startBinX = wordBoxStartX + curr_bin_offset
                    endBinX = wordBoxStartX + curr_bin_offset + bin_length_in_x
                    value = sample[curve_feature_name][i][bin_no]
                    rangedValue = fitFeatureValueToBoxRange(value, wordBoundingBoxSize)
                    line(startBinX, brushY - rangedValue, endBinX, brushY - rangedValue)
                    curr_bin_offset += bin_length_in_x
        #draw point features
        for point_feature_name in config.point_feature_keys:
            stroke(point_features_colors_dict[point_feature_name][0],
                point_features_colors_dict[point_feature_name][1],
                point_features_colors_dict[point_feature_name][2])
            fill(point_features_colors_dict[point_feature_name][0],
                point_features_colors_dict[point_feature_name][1],
                point_features_colors_dict[point_feature_name][2])
            value = dataset[point_feature_name][index]
            rangedValue = fitFeatureValueToBoxRange(value, wordBoundingBoxSize)
            pointLocX = wordBoxStartX + (wordBoxEndX - wordBoxStartX)/2
            ellipse(pointLocX, brushY - rangedValue, config.POINT_VALUE_MARKER_SIZE, config.POINT_VALUE_MARKER_SIZE)    
        brushY -= 2*wordBoundingBoxSize + config.EMPTY_SPACE_BTW_TEXT_FEATURES #back to word line
    noLoop()

def drawLegend():    
    legendY = config.WINDOW_HEIGHT - config.LEGEND_HEIGHT
    fill(0)
    stroke(0)
    rect(0, legendY, config.WINDOW_WIDTH, config.LEGEND_HEIGHT)
    
    brushX = config.LEGEND_HEIGHT
    brushY = legendY + config.LEGEND_HEIGHT / 2
    brushX = drawFeatureLegend(config.line_feature_keys, line_features_drawOrNot_dict, line_features_colors_dict, brushX, brushY, "line")
    brushX = drawFeatureLegend(config.curve_feature_keys, curve_features_drawOrNot_dict, curve_features_colors_dict, brushX, brushY, "line")
    brushX = drawFeatureLegend(config.point_feature_keys, point_features_drawOrNot_dict, point_features_colors_dict, brushX, brushY, "point")

def drawFeatureLegend(feature_keys, drawOrNot_dict, colors_dict, brushX, brushY, markType):
    if feature_keys:
        ellipseMode(CENTER)
        for feature_name in feature_keys:
            if drawOrNot_dict[feature_name]:
                if markType == "point":
                    fill(colors_dict[feature_name][0],
                        colors_dict[feature_name][1],
                        colors_dict[feature_name][2])
                    stroke(colors_dict[feature_name][0],
                        colors_dict[feature_name][1],
                        colors_dict[feature_name][2])
                    ellipse(brushX, brushY, config.LEGEND_BOX_SIZE, config.LEGEND_BOX_SIZE)
                    brushX += config.LEGEND_BOX_SIZE/2
                    fill(255)
                    text(" : " + feature_name, brushX, brushY + config.LEGEND_TEXT_SIZE/2)
                    brushX += textWidth(" : " + feature_name) + config.LEGEND_TEXT_SIZE * 1.3
                elif markType == "line":
                    stroke(colors_dict[feature_name][0],
                        colors_dict[feature_name][1],
                        colors_dict[feature_name][2])
                    strokeWeight(3)
                    line(brushX, brushY, brushX + config.LEGEND_BOX_SIZE, brushY)
                    brushX += config.LEGEND_BOX_SIZE
                    fill(255)
                    text(" : " + feature_name, brushX, brushY + config.LEGEND_TEXT_SIZE/2)
                    brushX += textWidth(" : " + feature_name) + config.LEGEND_TEXT_SIZE * 1.3
                else:
                    "You shouldn't be here"
                
        brushX += config.LEGEND_TEXT_SIZE * 2
    return brushX
    
def draw():
    background(255)
    drawWords(draw_from_word_no)
    drawLegend()

def keyPressed():
    global draw_from_word_no
    global dataset_size
    global draw_from_word_no
    if key == 'N' or key == 'n':
        if draw_from_word_no + config.NUM_WORDS_TO_SKIP_ON_PAGE_TURN < dataset_size:
            draw_from_word_no += config.NUM_WORDS_TO_SKIP_ON_PAGE_TURN
            loop()
        else:
            print("end of data")
    if key == 'B' or key == 'b':
        if draw_from_word_no - config.NUM_WORDS_TO_SKIP_ON_PAGE_TURN >= 0:
            draw_from_word_no -= config.NUM_WORDS_TO_SKIP_ON_PAGE_TURN
            loop()
        else:
            print("at the beginning of data")      
    if key == 'X' or key == 'x':
        print("exiting")
        exit()
    if key == 'S' or key == 's':
        saveFrame("%s/batchfrom-%i.tif"%(config.DIR_SAVED_FRAMES, draw_from_word_no))
        print("Saved frame to %s/batchfrom-%i.tif"%(config.DIR_SAVED_FRAMES, draw_from_word_no))
    if key == 'C' or key == 'c':
        initializeColors()
        loop()