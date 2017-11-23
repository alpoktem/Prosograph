import cPickle
import codecs
import config
import dataconfig_ted as dataconfig
import random

randomColorVals = [0, 20, 50, 75, 100, 125, 150, 175, 200, 225, 250]
numRandomColorVals = 11

def setup():
    size(config.WINDOW_WIDTH, config.WINDOW_HEIGHT)
    ellipseMode(CENTER)

    global dataset
    with open(dataconfig.DATASET, 'rb') as f:
        dataset = cPickle.load(f)
    
    if not dataconfig.DATA_IS_SAMPLED:
        global no_of_words
        no_of_words = len(dataset[dataconfig.word_key])
    else:
        global no_of_samples
        no_of_samples = len(dataset)
    
    global draw_from_word_no  #in the case of unsampled continous data
    draw_from_word_no = 0
    
    global draw_from_sample_no
    draw_from_sample_no = 0
    
    global font
    font = createFont(config.FONT_TYPE, config.TEXT_SIZE, True)
    textAlign(LEFT)
    
    global font_label
    font_label = createFont(config.FONT_TYPE, config.LABEL_FEATURE_TEXT_SIZE, True)
    textAlign(LEFT)
    
    initializeColors()
    initializeDrawOrNot()
    initializeMinMaxOfFeatures()  #ACHTUNG
    
def initializeDrawOrNot():
    #initialize drawOrNot arrays for features (this is written for later)
    global point_features_drawOrNot_dict
    point_features_drawOrNot_dict = createDrawOrNotDict(dataconfig.point_feature_keys)
    global line_features_drawOrNot_dict
    line_features_drawOrNot_dict = createDrawOrNotDict(dataconfig.line_feature_keys)
    global curve_features_drawOrNot_dict
    curve_features_drawOrNot_dict = createDrawOrNotDict(dataconfig.curve_feature_keys)
    global percentage_features_drawOrNot_dict
    percentage_features_drawOrNot_dict = createDrawOrNotDict(dataconfig.percentage_feature_keys)
    global binary_feature_drawOrNot_dict
    binary_feature_drawOrNot_dict = createDrawOrNotDict([dataconfig.binary_feature_key])
    
#TODO: this function doesn't work for sampled data
def initializeMinMaxOfFeatures():
    global minFeatureVal
    minFeatureVal = 0
    global maxFeatureVal
    maxFeatureVal = 0
    
    for featureName in dataconfig.point_feature_keys:
        minFeatureVal = min(minFeatureVal, min(dataset[featureName]))
        maxFeatureVal = max(maxFeatureVal, max(dataset[featureName]))
    for featureName in dataconfig.line_feature_keys:
        minFeatureVal = min(minFeatureVal, min(dataset[featureName]))
        maxFeatureVal = max(maxFeatureVal, max(dataset[featureName]))
    #for featureName in dataconfig.curve_feature_keys:
    #    minFeatureVal = min(minFeatureVal, min(dataset[featureName]))
    #    maxFeatureVal = max(maxFeatureVal, max(dataset[featureName]))
    
    maxFeatureVal = max(abs(minFeatureVal), abs(maxFeatureVal))
    
def fitFeatureValueToBoxRange(value, boxSize):
    global maxFeatureVal
    return int(value/maxFeatureVal * boxSize)
    
def initializeColors():
    #initialize colors for drawing features
    #if config.point_feature_keys:
    global point_features_colors_dict
    point_features_colors_dict = createColorDict(dataconfig.point_feature_keys)
    global line_features_colors_dict
    line_features_colors_dict = createColorDict(dataconfig.line_feature_keys)
    global curve_features_colors_dict
    curve_features_colors_dict = createColorDict(dataconfig.curve_feature_keys)
    global percentage_features_colors_dict
    percentage_features_colors_dict = createColorDict(dataconfig.percentage_feature_keys)
    if dataconfig.binary_feature_key :
        global binary_feature_colors_dict
        binary_feature_colors_dict = { dataconfig.binary_feature_key : [config.WORD_BOX_LIT_COLOR[0], 
                            config.WORD_BOX_LIT_COLOR[1],
                            config.WORD_BOX_LIT_COLOR[2],
                            config.WORD_BOX_LIT_COLOR[3]]}

def createColorDict(featureList):
    dict = { feature : [randomColorVals[random.randrange(0, numRandomColorVals)], 
                        randomColorVals[random.randrange(0, numRandomColorVals)],
                        randomColorVals[random.randrange(0, numRandomColorVals)],
                        255] for feature in featureList }
    return dict

def createDrawOrNotDict(featureList):
    #all set to draw
    dict = { feature : 1 for feature in featureList }
    return dict

def createMinMaxDict(featureList):
    global dataset
    dict = {featureName: (min(dataset[featureName]), max(dataset[featureName])) for featureName in featureList}
    return dict

def triangleSimple(x, y, w, h):
    # A wrapper for standard triangle() command. 
    # triangleSimple has the lower left corner as x,y 
    triangle(x,y, x+w/2, y-h, x+w, y)

def drawSample(sample, start_drawing_from, no_of_words, draw_from_Y=0):
    print(sample)
    strokeWeight(0.5)
    brushX = 0
    brushY = draw_from_Y
    wordBoundingBoxHeight = config.TEXT_SIZE + 4
    
    #fix this coming madafaka
    word_line_skip = config.PERCENTAGE_FEATURE_MARK_SIZE
    if dataconfig.label_feature_key:
        label_line_skip = wordBoundingBoxHeight + 1
        feature_line_skip = label_line_skip + config.LABEL_FEATURE_TEXT_SIZE + 1 + wordBoundingBoxHeight 
    else:
        label_line_skip = wordBoundingBoxHeight
        feature_line_skip = label_line_skip + 1 + wordBoundingBoxHeight 
    new_line_skip = feature_line_skip + wordBoundingBoxHeight + 1
    
    for index in range(start_drawing_from, no_of_words):
        if dataconfig.pause_before_key:
            pause_duration = sample[dataconfig.pause_before_key][index]
        else:
            pause_duration = 0
        punctuation = sample[dataconfig.punctuation_before_key][index]
        word = sample[dataconfig.word_key][index]
        
        #calculate word width, see if it fits in current line
        textFont(font)
        if dataconfig.word_duration_key:
            wordGraphicWidth = int(sample[dataconfig.word_duration_key][index] * textWidth(word))
        else:
            wordGraphicWidth = int(textWidth(word)) 
        #see if still on the screen horizontally, if not skip to next line
        if brushX + wordGraphicWidth >= config.WINDOW_WIDTH - config.RIGHT_AXIS_LENGTH:
            brushX = 0
            brushY += new_line_skip
        #see if new can line fit on the screen vertically, if not stop drawing new words
        if not brushY + wordBoundingBoxHeight * 3 <= config.WINDOW_HEIGHT - config.LEGEND_HEIGHT:
            break
        
        brushY += word_line_skip
        
        #draw pause/puncuation box between words
        writePunctuation = False
        if pause_duration > 0:
            interword_box_width = int(pause_duration * config.PAUSE_AMPLIFICATION) + 2
            fill(255,200,0, 107)
            if not punctuation == '':
                writePunctuation = True
        elif not punctuation == '':
            interword_box_width = textWidth(punctuation) + 2
            fill(255,0,0,107)
            writePunctuation = True
        else:
            interword_box_width = 0
        stroke(0) 
        strokeWeight(1)
        rect(brushX, brushY, interword_box_width, wordBoundingBoxHeight)
        if writePunctuation:
            fill(0)
            text(punctuation, brushX + interword_box_width / 2 - 2, brushY + config.TEXT_SIZE + 2)
        brushX += interword_box_width
        
        #draw word bounding box
        stroke(0)
        strokeWeight(1)
        if dataconfig.binary_feature_key and sample[dataconfig.binary_feature_key][index]:
            fill(config.WORD_BOX_LIT_COLOR[0],config.WORD_BOX_LIT_COLOR[1],config.WORD_BOX_LIT_COLOR[2], config.WORD_BOX_LIT_COLOR[3])
        else:
            fill(config.WORD_BOX_COLOR[0],config.WORD_BOX_COLOR[1],config.WORD_BOX_COLOR[2], config.WORD_BOX_COLOR[3])
        wordBoxStartX = brushX
        wordBoxWidth = wordGraphicWidth + 2
        wordBoxEndX = wordBoxStartX + wordBoxWidth
        wordBoxHeight = config.TEXT_SIZE + 4
        rect(wordBoxStartX, brushY, wordBoxWidth, wordBoxHeight)
        #write word
        fill(0)
        text(word, brushX + 1, brushY + config.TEXT_SIZE)
        
        #draw percentage features 
        for percentage_feature_name in dataconfig.percentage_feature_keys:
            if percentage_features_drawOrNot_dict[percentage_feature_name]:
                for mark_at_percentage in sample[percentage_feature_name][index]:
                    if mark_at_percentage >= 0 and mark_at_percentage <= 100: 
                        markX = wordBoxStartX + (wordBoxEndX - wordBoxStartX) * mark_at_percentage / 100
                        markY = brushY #cuidado
                        
                        #print(mark_at_percentage)
                        #print("%i, %i, %i"%(wordBoxStartX, markX, wordBoxEndX))
                        
                        stroke(percentage_features_colors_dict[percentage_feature_name][0],
                            percentage_features_colors_dict[percentage_feature_name][1],
                            percentage_features_colors_dict[percentage_feature_name][2])
                        fill(percentage_features_colors_dict[percentage_feature_name][0],
                            percentage_features_colors_dict[percentage_feature_name][1],
                            percentage_features_colors_dict[percentage_feature_name][2])
                        
                        triangleSimple(markX, markY, config.PERCENTAGE_FEATURE_MARK_SIZE, config.PERCENTAGE_FEATURE_MARK_SIZE)
            
        
        #draw label feature just below word
        if dataconfig.label_feature_key and sample[dataconfig.label_feature_key][index]:
            textFont(font_label)
            brushY += label_line_skip
            label = sample[dataconfig.label_feature_key][index]
            label_graphic_width = textWidth(label) 
            fill(0)
            label_X = wordBoxStartX + (wordBoxEndX - wordBoxStartX)/2 - label_graphic_width/2
            text(label, label_X, brushY + config.LABEL_FEATURE_TEXT_SIZE)
            
            brushY -= label_line_skip #back to word line
        
        brushX += wordGraphicWidth + 2 # + config.TEXT_SPACE_WIDTH
            
        #draw features line below words
        brushY += feature_line_skip
        #draw the zero line
        stroke(0)
        strokeWeight(0)
        line(0,brushY, config.WINDOW_WIDTH - config.RIGHT_AXIS_LENGTH, brushY)
        #draw line features
        for line_feature_name in dataconfig.line_feature_keys:
            if line_features_drawOrNot_dict[line_feature_name]:
                
                strokeWeight(1.5)
                stroke(line_features_colors_dict[line_feature_name][0],
                    line_features_colors_dict[line_feature_name][1],
                    line_features_colors_dict[line_feature_name][2])
                
                value = sample[line_feature_name][index]
                rangedValue = fitFeatureValueToBoxRange(value, wordBoundingBoxHeight)
                line(wordBoxStartX, brushY - rangedValue, wordBoxEndX, brushY - rangedValue)
    
        #draw curve features
        for curve_feature_name in dataconfig.curve_feature_keys:
            if curve_features_drawOrNot_dict[curve_feature_name]:
                
                strokeWeight(1)
                stroke(curve_features_colors_dict[curve_feature_name][0],
                    curve_features_colors_dict[curve_feature_name][1],
                    curve_features_colors_dict[curve_feature_name][2])
                
                bin_length_in_x = (wordBoxEndX - wordBoxStartX) / config.NO_OF_BINS_IN_CURVE_FEATURES
                curr_bin_offset = 0
                for bin_no in range(config.NO_OF_BINS_IN_CURVE_FEATURES):
                    startBinX = wordBoxStartX + curr_bin_offset
                    endBinX = wordBoxStartX + curr_bin_offset + bin_length_in_x
                    value = sample[curve_feature_name][index][bin_no]
                    rangedValue = fitFeatureValueToBoxRange(value, wordBoundingBoxHeight)
                    line(startBinX, brushY - rangedValue, endBinX, brushY - rangedValue)
                    curr_bin_offset += bin_length_in_x
        #draw point features
        for point_feature_name in dataconfig.point_feature_keys:
            strokeWeight(1)
            stroke(point_features_colors_dict[point_feature_name][0],
                point_features_colors_dict[point_feature_name][1],
                point_features_colors_dict[point_feature_name][2])
            fill(point_features_colors_dict[point_feature_name][0],
                point_features_colors_dict[point_feature_name][1],
                point_features_colors_dict[point_feature_name][2])
            value = sample[point_feature_name][index]
            rangedValue = fitFeatureValueToBoxRange(value, wordBoundingBoxHeight)
            pointLocX = wordBoxStartX + (wordBoxEndX - wordBoxStartX)/2
            ellipse(pointLocX, brushY - rangedValue, config.POINT_VALUE_MARKER_SIZE, config.POINT_VALUE_MARKER_SIZE)    
        brushY -= feature_line_skip + word_line_skip #back to word line
    
    draw_from_Y = brushY + new_line_skip
    return draw_from_Y

def drawLegend():    
    legendY = config.WINDOW_HEIGHT - config.LEGEND_HEIGHT
    fill(0)
    stroke(0)
    strokeWeight(1)
    rect(0, legendY, config.WINDOW_WIDTH, config.LEGEND_HEIGHT)
    
    brushX = config.LEGEND_HEIGHT
    brushY = legendY + config.LEGEND_HEIGHT / 2
    brushX = drawFeatureLegend(dataconfig.line_feature_keys, line_features_drawOrNot_dict, line_features_colors_dict, brushX, brushY, "line")
    brushX = drawFeatureLegend(dataconfig.curve_feature_keys, curve_features_drawOrNot_dict, curve_features_colors_dict, brushX, brushY, "line")
    brushX = drawFeatureLegend(dataconfig.point_feature_keys, point_features_drawOrNot_dict, point_features_colors_dict, brushX, brushY, "point")
    brushX = drawFeatureLegend(dataconfig.percentage_feature_keys, percentage_features_drawOrNot_dict, percentage_features_colors_dict, brushX, brushY, "percentage")
    if dataconfig.binary_feature_key:
        brushX = drawFeatureLegend([dataconfig.binary_feature_key], binary_feature_drawOrNot_dict, binary_feature_colors_dict, brushX, brushY, "binary")

def drawFeatureLegend(feature_keys, drawOrNot_dict, colors_dict, brushX, brushY, markType):
    if feature_keys:
        ellipseMode(CENTER)
        for feature_name in feature_keys:
            #print(feature_name)
            if drawOrNot_dict[feature_name]:
                if markType == "line":
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
                    #print(colors_dict)
                    #print(feature_name)
                    fill(colors_dict[feature_name][0],
                        colors_dict[feature_name][1],
                        colors_dict[feature_name][2])
                    strokeWeight(1)
                    stroke(colors_dict[feature_name][0],
                        colors_dict[feature_name][1],
                        colors_dict[feature_name][2])
                    if markType == "point":
                        ellipse(brushX, brushY, config.LEGEND_BOX_SIZE, config.LEGEND_BOX_SIZE)
                    elif markType == "percentage":
                        triangleSimple(brushX - config.LEGEND_BOX_SIZE/2, brushY + config.LEGEND_BOX_SIZE/2, config.LEGEND_BOX_SIZE, config.LEGEND_BOX_SIZE)
                    elif markType == "binary":
                        rectMode(CENTER)
                        rect(brushX, brushY, config.LEGEND_BOX_SIZE *1.4, config.LEGEND_BOX_SIZE)
                    brushX += config.LEGEND_BOX_SIZE/2
                    fill(255)
                    text(" : " + feature_name, brushX, brushY + config.LEGEND_TEXT_SIZE/2)
                    brushX += textWidth(" : " + feature_name) + config.LEGEND_TEXT_SIZE * 1.3
                
        brushX += config.LEGEND_TEXT_SIZE * 2
    return brushX

def drawCollection(start_drawing_from):
    Y_offset=0
    for sample_no in range(start_drawing_from, no_of_samples):
        sample = dataset[sample_no]
        no_of_words = len(sample[dataconfig.word_key])
        Y_offset = drawSample(sample, 0, no_of_words, Y_offset)
        
def draw():
    background(255)
    if not dataconfig.DATA_IS_SAMPLED:
        global no_of_words
        drawSample(dataset, draw_from_word_no, no_of_words)
    else:
        global draw_from_sample_no
        drawCollection(draw_from_sample_no)
    
    noLoop()
    drawLegend()

def keyPressed():
    global draw_from_word_no
    global no_of_words
    global draw_from_sample_no
    global no_of_samples
    if key == 'N' or key == 'n':
        if not dataconfig.DATA_IS_SAMPLED:
            if draw_from_word_no + config.NUM_WORDS_TO_SKIP_ON_PAGE_TURN < no_of_words:
                draw_from_word_no += config.NUM_WORDS_TO_SKIP_ON_PAGE_TURN
                loop()
            else:
                print("end of data")
        else:
            if draw_from_sample_no + config.NUM_SAMPLES_TO_SKIP_ON_PAGE_TURN < no_of_samples:
                draw_from_sample_no += config.NUM_SAMPLES_TO_SKIP_ON_PAGE_TURN
                loop()
            else:
                print("end of data")
    if key == 'B' or key == 'b':
        if not dataconfig.DATA_IS_SAMPLED:
            if draw_from_word_no - config.NUM_WORDS_TO_SKIP_ON_PAGE_TURN >= 0:
                draw_from_word_no -= config.NUM_WORDS_TO_SKIP_ON_PAGE_TURN
                loop()
            else:
                print("at the beginning of data")     
        else:
            if draw_from_sample_no - config.NUM_SAMPLES_TO_SKIP_ON_PAGE_TURN >= 0:
                draw_from_sample_no -= config.NUM_SAMPLES_TO_SKIP_ON_PAGE_TURN
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
    if key == 'Q' or key == 'q':
        exit()