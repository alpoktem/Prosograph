import cPickle
import codecs
import config
import random

NUM_BIN = config.no_of_bins_in_curve_features
NUM_WORDS_PER_SAMPLE = config.words_per_sample

randomColorVals = [0, 20, 50, 75, 100, 125, 150, 175, 200, 225, 250]
numRandomColorVals = 11

def read_vocabulary(file_name):
    with codecs.open(file_name, 'r', 'utf-8') as f:
        return iterable_to_dict(f.readlines())

def iterable_to_dict(arr):
    return dict((x.strip(), i) for (i, x) in enumerate(arr))

def wordIds_to_words(arr):
    ret = []
    for index, i in enumerate(arr):
        ret.append(wordId_to_word(i))
    return ret

def wordId_to_word(wordId):
    return inv_vocabulary[wordId]

def setup():
    size(config.WINDOW_WIDTH, config.WINDOW_HEIGHT)
    ellipseMode(CENTER)

    global dataset
    with open(config.DATASET, 'rb') as f:
        dataset = cPickle.load(f)
    print(dataset[0].keys())
        
    #open vocabulary
    word_vocabulary = read_vocabulary(config.VOCABULARY)
    global inv_vocabulary
    inv_vocabulary = {v: k for k, v in word_vocabulary.iteritems()}
    
    global font
    font = createFont(config.FONT_TYPE, config.TEXT_SIZE, True)
    textFont(font)  
    textAlign(LEFT)
    
    global no_of_batches
    no_of_batches = len(dataset) / config.NUM_SAMPLES_PER_SCREEN
    
    print("Number of batches:%d"%no_of_batches)
    global batchNo
    batchNo = 0
    
    initializeColors()
    initializeDrawOrNot()
    
def initializeDrawOrNot():
    #initialize drawOrNot arrays for features (this is written for later)
    global curve_features_drawOrNot_dict
    curve_features_drawOrNot_dict = createDrawOrNotDict(config.curve_feature_keys)
    global line_features_drawOrNot_dict
    line_features_drawOrNot_dict = createDrawOrNotDict(config.line_feature_keys)
    global point_features_drawOrNot_dict
    point_features_drawOrNot_dict = createDrawOrNotDict(config.point_feature_keys)
    global percentage_features_drawOrNot_dict
    percentage_features_drawOrNot_dict = createDrawOrNotDict(config.percentage_feature_keys)

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

def drawNextBatch():
    font = createFont(config.FONT_TYPE, config.TEXT_SIZE, True)
    strokeWeight(0.5)
    brushX = 3
    brushY = 3
    
    batchBeginning = batchNo*config.NUM_SAMPLES_PER_SCREEN
    batchEnd = batchNo*config.NUM_SAMPLES_PER_SCREEN + config.NUM_SAMPLES_PER_SCREEN
    print("Showing samples from %d to %d"%(batchBeginning + 1, batchEnd))
    for sample in dataset[batchBeginning:batchEnd]:
        brushX = 0
        wordXs = []
        for idx, word in enumerate(wordIds_to_words(sample[config.word_key])):
            if config.word_duration_key:
                wordGraphicWidth = int(sample[config.word_duration_key][idx] * config.WORD_AMPLIFICATION)
            else:
                wordGraphicWidth = textWidth(word)    
            wordXs.append((brushX, brushX + wordGraphicWidth))
            
            #draw word bounding box
            stroke(0)
            if config.binary_feature_key and sample[config.binary_feature_key][idx]:
                fill(config.WORD_BOX_LIT_COLOR[0],config.WORD_BOX_LIT_COLOR[1],config.WORD_BOX_LIT_COLOR[2], config.WORD_BOX_LIT_COLOR[3])
                rect(brushX - 1, brushY - 1, wordGraphicWidth + 2, config.TEXT_SIZE + 4)
            else:
                fill(config.WORD_BOX_COLOR[0],config.WORD_BOX_COLOR[1],config.WORD_BOX_COLOR[2], config.WORD_BOX_COLOR[3])
                rect(brushX - 1, brushY - 1, wordGraphicWidth + 2, config.TEXT_SIZE + 4)
            
            #write word
            fill(0)
            text(word, brushX, brushY + config.TEXT_SIZE)
            brushX += wordGraphicWidth + 2 # + config.TEXT_SPACE_WIDTH
            
            punctuation_code = sample[config.punctuation_after_key][idx] #punctuation after the word
            pause_length = int(sample[config.pause_after_key][idx] * config.PAUSE_AMPLIFICATION)
            
            if pause_length > 0: #pause
                pause_rect_x = brushX - 1
                pause_rect_y = brushY - 1
                pause_rect_width = pause_length + 1
                pause_rect_height = config.TEXT_SIZE + 4
                fill(255,200,0, 107)
                stroke(0)
                rect(pause_rect_x, pause_rect_y, pause_rect_width, pause_rect_height)  # bu pause uzunlugunda olacak
                if not punctuation_code == 2:
                    punctuation_text = config.PUNC_CODES[punctuation_code]
                    fill(0)
                    if pause_rect_width < textWidth(punctuation_text):
                        punctuation_x = pause_rect_x - 1
                    else:
                        punctuation_x = pause_rect_x + pause_rect_width/2 - 1
                    text(punctuation_text, punctuation_x, brushY + config.TEXT_SIZE)
                brushX += pause_length + 1
            elif not punctuation_code == 2:
                punctuation_text = config.PUNC_CODES[punctuation_code]
                punctuationWidth = textWidth(punctuation_text)
                fill(255,0,0, 107)
                stroke(0)
                rect(brushX - 1, brushY - 1, punctuationWidth + 2, config.TEXT_SIZE + 4) 
                fill(0)
                text(punctuation_text, brushX, brushY + config.TEXT_SIZE)
                brushX += textWidth(punctuation_text) + 2 #+ config.TEXT_SPACE_WIDTH
        bottomWordsY = brushY + config.TEXT_SIZE + 4
        brushY += config.JUMP_TO_FEATURE_LINE_OFFSET #New Line
        
        for i, startEnd in enumerate(wordXs):
            startX = startEnd[0]
            endX = startEnd[1]
            
            #draw line features
            for line_feature_name in config.line_feature_keys:
                if line_features_drawOrNot_dict[line_feature_name]:
                    
                    stroke(line_features_colors_dict[line_feature_name][0],
                         line_features_colors_dict[line_feature_name][1],
                         line_features_colors_dict[line_feature_name][2])
                    
                    value = sample[line_feature_name][i]
                    line(startX, brushY - value, endX, brushY - value)
                    
            #draw curve features
            for curve_feature_name in config.curve_feature_keys:
                if curve_features_drawOrNot_dict[curve_feature_name]:
                    
                    stroke(curve_features_colors_dict[curve_feature_name][0],
                         curve_features_colors_dict[curve_feature_name][1],
                         curve_features_colors_dict[curve_feature_name][2])
                    
                    bin_length_in_x = (endX - startX) / NUM_BIN
                    curr_bin_offset = 0
                    for bin_no in range(config.no_of_bins_in_curve_features):
                        startBinX = startX + curr_bin_offset
                        endBinX = startX + curr_bin_offset + bin_length_in_x
                        value = sample[curve_feature_name][i][bin_no]
                        line(startBinX, brushY - value, endBinX, brushY - value)
                        curr_bin_offset += bin_length_in_x
            #draw point features
            for point_feature_name in config.point_feature_keys:
                stroke(point_features_colors_dict[point_feature_name][0],
                    point_features_colors_dict[point_feature_name][1],
                    point_features_colors_dict[point_feature_name][2])
                fill(point_features_colors_dict[point_feature_name][0],
                    point_features_colors_dict[point_feature_name][1],
                    point_features_colors_dict[point_feature_name][2])
                value = sample[point_feature_name][i]
                pointLocX = startX + (endX - startX)/2
                ellipse(pointLocX, brushY - value, config.POINT_VALUE_MARKER_SIZE, config.POINT_VALUE_MARKER_SIZE)    
            #draw percentage features
            for percentage_feature_name in config.percentage_feature_keys:
                for percentageTime in range(len(sample[percentage_feature_name][i])):
                    print(percentageTime)
                    
                    pointLocX = startX + (endX - startX)/100 * percentageTime
                    pointLocX = startX + 10
                    #rect(pointLocX, brushY, 10,10)
                    plus(pointLocX, 
                             bottomWordsY, 
                             config.PERCENTAGE_VALUE_MARKER_SIZE, 
                             percentage_features_colors_dict[percentage_feature_name][0],
                             percentage_features_colors_dict[percentage_feature_name][1],
                             percentage_features_colors_dict[percentage_feature_name][2],
                             )
    
        brushY += config.JUMP_TO_TEXTLINE_OFFSET #New Line
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
        font = createFont(config.FONT_TYPE, config.LEGEND_TEXT_SIZE, True)
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
                    brushX += textWidth(feature_name) + 40
                elif markType == "line":
                    stroke(colors_dict[feature_name][0],
                        colors_dict[feature_name][1],
                        colors_dict[feature_name][2])
                    strokeWeight(3)
                    line(brushX, brushY, brushX + config.LEGEND_BOX_SIZE, brushY)
                    brushX += config.LEGEND_BOX_SIZE
                    fill(255)
                    text(" : " + feature_name, brushX, brushY + config.LEGEND_TEXT_SIZE/2)
                    brushX += textWidth(feature_name) + 30
                else:
                    "You shouldn't be here"
                
        brushX += 50
        return brushX
    
def draw():
    background(255)
    drawNextBatch()
    drawLegend()
    
# def draw():
#     background(255);
#     noStroke();
    
#     drawPlus(40,40,16, 50,0,255)
    
    
def plus(x, y, sizePlus, r, g, b):
    ellipseMode(CENTER)
    fill(r,g,b)
    stroke(r,g,b)
    ellipse(x,y,sizePlus, sizePlus/3)
    ellipse(x+1,y,sizePlus/3, sizePlus)

def keyPressed():
    global batchNo
    if key == 'N' or key == 'n':
        if batchNo < no_of_batches - 1:
            batchNo += 1
            loop()
        else:
            print("last batch")
    if key == 'B' or key == 'b':
        if batchNo > 0:
            batchNo -= 1
            loop()
        else:
            print("first batch")        
    if key == 'X' or key == 'x':
        print("exiting")
        exit()
    if key == 'S' or key == 's':
        saveFrame("%s/batch-%i.tif"%(config.DIR_SAVED_FRAMES, batchNo))
        print("Saved frame to %s/batch-%i.tif"%(config.DIR_SAVED_FRAMES, batchNo))
    if key == 'C' or key == 'c':
        initializeColors()
        loop()