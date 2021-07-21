import csv
from collections import defaultdict
import codecs
import config
import proscript
import json
import os
import random
from proscript import Proscript, Segment, Word
import dataconfig_ted as dataconfig   #Specify here which dataconfig you want to use

add_library('minim')

randomColorVals = [0, 20, 50, 75, 100, 125, 150, 175, 200, 225, 250]
numRandomColorVals = 11

def get_file_list(data_source, extension='.csv'):
    if not os.path.isdir(data_source):
        files = [data_source]
    else:
        files = os.listdir(data_source)
        files.sort() 
        files = [os.path.join(data_source, fn) for fn in files if fn.endswith(extension)]
    return files

def load_dataset():
    global dataset
    global dataset_id
    global no_of_samples
    if dataset_id == '-1':
        dataset = get_file_list(dataconfig.DATASET)
        no_of_samples = len(dataset)
        print("Displaying dataset. (Size: " + str(no_of_samples) + ")")
    elif dataset_id in dataconfig.dataset_tags.keys():
        dataset = get_file_list(dataconfig.DATASET, '.' + dataset_id + '.csv')
        no_of_samples = len(dataset)
        print("Displaying dataset " + dataset_id + ": " + dataconfig.dataset_tags[dataset_id] + " (Size: " + str(no_of_samples) + ")")
    else:
        print("No dataset exists with that index")
        no_of_samples = 0

def setup():
    size(config.WINDOW_WIDTH, config.WINDOW_HEIGHT)
    ellipseMode(CENTER)
    
    global minim
    minim = Minim(this)
    
    global groove
    groove = None
    
    global dataset_id
    if len(dataconfig.dataset_tags) > 0:
        dataset_id = '0'
    else:
        dataset_id = '-1'
    
    load_dataset()

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
    
    global drawn_words
    drawn_words = []
    
    global select_range
    select_range = -1
    
    initializeColors()
    initializeDrawOrNot()

def initializeDrawOrNot():
    #initialize drawOrNot arrays for features (this is written for later)
    global point_features_drawOrNot_dict
    point_features_drawOrNot_dict = createDrawOrNotDict(dataconfig.point_feature_keys)
    global line_features_drawOrNot_dict
    line_features_drawOrNot_dict = createDrawOrNotDict(dataconfig.line_feature_keys)
    global curve_features_drawOrNot_dict
    curve_features_drawOrNot_dict = createDrawOrNotDict(dataconfig.curve_feature_keys)
    global evened_curve_features_drawOrNot_dict
    evened_curve_features_drawOrNot_dict = createDrawOrNotDict(dataconfig.evened_curve_feature_keys)
    global percentage_features_drawOrNot_dict
    percentage_features_drawOrNot_dict = createDrawOrNotDict(dataconfig.percentage_feature_keys)
    global binary_feature_drawOrNot_dict
    binary_feature_drawOrNot_dict = createDrawOrNotDict([dataconfig.binary_feature_key])
    
def initializeColors():
    #initialize colors for drawing features
    global point_features_colors_dict
    point_features_colors_dict = createColorDict(dataconfig.point_feature_keys)
    global line_features_colors_dict
    line_features_colors_dict = createColorDict(dataconfig.line_feature_keys)
    global curve_features_colors_dict
    curve_features_colors_dict = createColorDict(dataconfig.curve_feature_keys)
    global evened_curve_features_colors_dict
    evened_curve_features_colors_dict = createColorDict(dataconfig.evened_curve_feature_keys)
    global percentage_features_colors_dict
    percentage_features_colors_dict = createColorDict(dataconfig.percentage_feature_keys)
    if dataconfig.binary_feature_key :
        global binary_feature_colors_dict
        binary_feature_colors_dict = { dataconfig.binary_feature_key : [config.WORD_BOX_LIT_COLOR[0], 
                            config.WORD_BOX_LIT_COLOR[1],
                            config.WORD_BOX_LIT_COLOR[2],
                            config.WORD_BOX_LIT_COLOR[3]]}

def getRandomColor():
    return [randomColorVals[random.randrange(0, numRandomColorVals)], 
            randomColorVals[random.randrange(0, numRandomColorVals)],
            randomColorVals[random.randrange(0, numRandomColorVals)],
            255]

def createColorDict(featureList):
    dict = { feature : getRandomColor() if feature not in dataconfig.color_dict else dataconfig.color_dict[feature] for feature in featureList if feature }
    return dict

def createDrawOrNotDict(featureList):
    #all set to draw
    dict = { feature : 1 for feature in featureList }
    return dict

def triangleSimple(x, y, w, h):
    # A wrapper for standard triangle() command. 
    # triangleSimple has the lower left corner as x,y 
    triangle(x,y, x+w/2, y-h, x+w, y)
    
def fitFeatureValueToBoxRange(value, boxSize, maxFeatureVal=None):
    if maxFeatureVal == None:
        maxFeatureVal = dataconfig.maxFeatureVal
    return int(value/maxFeatureVal * boxSize)

def drawSample(sample, start_drawing_from, no_of_words, draw_from_Y=0):
    global select_range
    strokeWeight(0.5)
    brushX = 0
    brushY = draw_from_Y
    break_free = False
    wordBoundingBoxHeight = config.TEXT_SIZE + 4
    
    word_line_skip = config.PERCENTAGE_FEATURE_MARK_SIZE
    if dataconfig.label_feature_key:
        label_line_skip = wordBoundingBoxHeight + 1
        feature_line_skip = label_line_skip + config.LABEL_FEATURE_TEXT_SIZE + 1 + wordBoundingBoxHeight 
    else:
        label_line_skip = wordBoundingBoxHeight
        feature_line_skip = label_line_skip + 1 + wordBoundingBoxHeight 
    new_line_skip = feature_line_skip + wordBoundingBoxHeight + 1
    
    for index in range(start_drawing_from, no_of_words):
        word = sample.get_word_by_index(index).word
        if dataconfig.draw_pause_boxes:
            pause_duration = sample.get_word_by_index(index).pause_before
        else:
            pause_duration = 0
        #get punctuation coming before the current word and after previous word
        punctuation = ''
        if dataconfig.draw_punctuation:
            if index-1 in range(start_drawing_from, no_of_words):
                punctuation += sample.get_word_by_index(index-1).punctuation_after
            punctuation += sample.get_word_by_index(index).punctuation_before

        #calculate word width, see if it fits in current line
        textFont(font)
        if dataconfig.draw_word_duration:
            wordGraphicWidth = int(sample.get_word_by_index(index).duration * textWidth(word))
        else:
            wordGraphicWidth = int(textWidth(word)) 
        #see if still on the screen horizontally, if not skip to next line
        if brushX + wordGraphicWidth >= config.WINDOW_WIDTH - config.RIGHT_AXIS_LENGTH:
            brushX = 0
            brushY += new_line_skip
        #see if new can line fit on the screen vertically, if not stop drawing new words
        if not brushY + wordBoundingBoxHeight * 3 <= config.WINDOW_HEIGHT - config.LEGEND_HEIGHT:
            break_free = True
            break
        
        #Drawing the word and all its properties
        global drawn_words
        drawn_words.append(sample.get_word_by_index(index))
        drawn_word_index = len(drawn_words) - 1
        brushY += word_line_skip
        
        #draw pause/puncuation box between words
        writePunctuation = False
        if pause_duration > 0:
            interword_box_width = int(pause_duration * config.PAUSE_AMPLIFICATION) + 2
            fill(config.PAUSE_BOX_COLOR[0],config.PAUSE_BOX_COLOR[1],config.PAUSE_BOX_COLOR[2], config.PAUSE_BOX_COLOR[3])
            if not punctuation == '':
                puncGraphicWidth = int(textWidth(punctuation)) 
                fill(config.PUNC_PAUSE_BOX_COLOR[0],config.PUNC_PAUSE_BOX_COLOR[1],config.PUNC_PAUSE_BOX_COLOR[2], config.PUNC_PAUSE_BOX_COLOR[3])
                writePunctuation = True
        elif not punctuation == '':
            puncGraphicWidth = int(textWidth(punctuation)) 
            interword_box_width = textWidth(punctuation) + 2
            fill(config.PUNC_BOX_COLOR[0],config.PUNC_BOX_COLOR[1],config.PUNC_BOX_COLOR[2], config.PUNC_BOX_COLOR[3])
            writePunctuation = True
        else:
            interword_box_width = 0
        stroke(0) 
        strokeWeight(1)
        rect(brushX, brushY, interword_box_width, wordBoundingBoxHeight)
        if writePunctuation:
            fill(0)
            text(punctuation, brushX + interword_box_width / 2 - puncGraphicWidth/2, brushY + config.TEXT_SIZE)
        brushX += interword_box_width
        
        #draw word bounding box
        stroke(0)
        strokeWeight(1)
        if not select_range == -1 and drawn_word_index >= select_range[0] and drawn_word_index <= select_range[1]:
            fill(config.WORD_BOX_LIT_COLOR[0],config.WORD_BOX_LIT_COLOR[1],config.WORD_BOX_LIT_COLOR[2], config.WORD_BOX_LIT_COLOR[3])
        else:
            fill(config.WORD_BOX_COLOR[0],config.WORD_BOX_COLOR[1],config.WORD_BOX_COLOR[2], config.WORD_BOX_COLOR[3])
        wordBoxStartX = brushX
        wordBoxWidth = wordGraphicWidth + 2
        wordBoxEndX = wordBoxStartX + wordBoxWidth
        wordBoxHeight = config.TEXT_SIZE + 4
        rect(wordBoxStartX, brushY, wordBoxWidth, wordBoxHeight)
        #write word inside
        fill(0)
        text(word, brushX + 1, brushY + config.TEXT_SIZE)
        #store coordinates in the sample
        sample.get_word_by_index(index).word_box_topleft = (wordBoxStartX, brushY)
        sample.get_word_by_index(index).word_box_bottomright = (wordBoxStartX + wordBoxWidth, brushY + wordBoxHeight)
        
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
        if dataconfig.draw_label_feature:
            label = sample.get_word_by_index(index).get_value(dataconfig.label_feature_key)
            textFont(font_label)
            brushY += label_line_skip
            label_graphic_width = textWidth(label) 
            fill(0)
            label_X = wordBoxStartX + (wordBoxEndX - wordBoxStartX)/2 - label_graphic_width/2
            text(label, label_X, brushY + config.LABEL_FEATURE_TEXT_SIZE)
            
            brushY -= label_line_skip #back to word line
        
        brushX += wordGraphicWidth + 2 # + config.TEXT_SPACE_WIDTH
            
        #draw features line below words
        brushY += feature_line_skip
        #draw the zero line
        stroke(150, 150, 150)
        strokeWeight(0)
        line(0,brushY, config.WINDOW_WIDTH - config.RIGHT_AXIS_LENGTH, brushY)
        #draw line features
        for line_feature_name in dataconfig.line_feature_keys:
            if line_features_drawOrNot_dict[line_feature_name]:
                strokeWeight(1.5)
                stroke(line_features_colors_dict[line_feature_name][0],
                    line_features_colors_dict[line_feature_name][1],
                    line_features_colors_dict[line_feature_name][2])
                value = sample.get_word_by_index(index).get_value(line_feature_name)
                rangedValue = fitFeatureValueToBoxRange(value, wordBoundingBoxHeight, config.MAX_SEMITONE)
                line(wordBoxStartX, brushY - rangedValue, wordBoxEndX, brushY - rangedValue)
    
        #draw curve features
        for curve_feature_name in dataconfig.curve_feature_keys:
            if curve_features_drawOrNot_dict[curve_feature_name]:
                strokeWeight(1)
                stroke(curve_features_colors_dict[curve_feature_name][0],
                    curve_features_colors_dict[curve_feature_name][1],
                    curve_features_colors_dict[curve_feature_name][2])
                for contour_index, x_percentage in enumerate(sample.get_word_by_index(index).get_value(curve_feature_name + '_xaxis')):
                    value = sample.get_word_by_index(index).get_value(curve_feature_name)[contour_index]
                    binX = round((wordBoxEndX - wordBoxStartX) * x_percentage / 100)
                    pointLocX = wordBoxStartX + binX
                    rangedValue = fitFeatureValueToBoxRange(value, wordBoundingBoxHeight, config.MAX_HZ)
                    if contour_index > 0:
                        line(prev_LocX, brushY - prev_rangedValue, pointLocX, brushY - rangedValue)
                    prev_LocX = pointLocX
                    prev_rangedValue = rangedValue
        
        #draw evened curve features
        for evened_curve_feature_name in dataconfig.evened_curve_feature_keys:
            if evened_curve_features_drawOrNot_dict[evened_curve_feature_name]:
                strokeWeight(1)
                stroke(evened_curve_features_colors_dict[evened_curve_feature_name][0],
                    evened_curve_features_colors_dict[evened_curve_feature_name][1],
                    evened_curve_features_colors_dict[evened_curve_feature_name][2])
                
                contour = sample.get_word_by_index(index).get_value(evened_curve_feature_name)
                axis =  list(range(0,len(contour)))    #MAKE THIS SMARTER. 
                for contour_index, x_percentage in enumerate(axis):
                    value = contour[contour_index]
                    binX = round((wordBoxEndX - wordBoxStartX) * x_percentage / len(contour))
                    pointLocX = wordBoxStartX + binX
                    rangedValue = fitFeatureValueToBoxRange(value, wordBoundingBoxHeight, config.MAX_SEMITONE)
                    if contour_index > 0:
                        line(prev_LocX, brushY - prev_rangedValue, pointLocX, brushY - rangedValue)
                    prev_LocX = pointLocX
                    prev_rangedValue = rangedValue
        
        #draw point features
        for point_feature_name in dataconfig.point_feature_keys:
            strokeWeight(1)
            stroke(point_features_colors_dict[point_feature_name][0],
                point_features_colors_dict[point_feature_name][1],
                point_features_colors_dict[point_feature_name][2])
            fill(point_features_colors_dict[point_feature_name][0],
                point_features_colors_dict[point_feature_name][1],
                point_features_colors_dict[point_feature_name][2])
            value = sample.get_word_by_index(index).get_value(point_feature_name)
            rangedValue = fitFeatureValueToBoxRange(value, wordBoundingBoxHeight, config.MAX_SEMITONE)
            pointLocX = wordBoxStartX + (wordBoxEndX - wordBoxStartX)/2
            ellipse(pointLocX, brushY - rangedValue, config.POINT_VALUE_MARKER_SIZE, config.POINT_VALUE_MARKER_SIZE)    
        brushY -= feature_line_skip + word_line_skip #back to word line
    
    if not break_free:
        draw_from_Y = brushY + new_line_skip
        return draw_from_Y
    else:
        return -1

def drawLegend():    
    legendY = config.WINDOW_HEIGHT - config.LEGEND_HEIGHT
    fill(0)
    stroke(0)
    textFont(font)
    strokeWeight(1)
    rect(0, legendY, config.WINDOW_WIDTH, config.LEGEND_HEIGHT)
    
    brushX = config.LEGEND_HEIGHT
    brushY = legendY + config.LEGEND_HEIGHT / 2
    brushX = drawFeatureLegend(dataconfig.line_feature_keys, line_features_drawOrNot_dict, line_features_colors_dict, brushX, brushY, "line")
    brushX = drawFeatureLegend(dataconfig.curve_feature_keys, curve_features_drawOrNot_dict, curve_features_colors_dict, brushX, brushY, "line")
    brushX = drawFeatureLegend(dataconfig.evened_curve_feature_keys, evened_curve_features_drawOrNot_dict, evened_curve_features_colors_dict, brushX, brushY, "line")
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

def drawSampleset(start_drawing_from_sample, start_drawing_from_word):
    Y_offset=0
    global drawn_words
    drawn_words = []
    
    for sample_no in range(start_drawing_from_sample, no_of_samples):
        sample_file = dataset[sample_no]
        print('reading %s'%sample_file)
        sample_proscript = Proscript()
        sample_proscript.from_file(sample_file, search_audio=True)
        #print('audio file', sample_proscript.audio_file)
        #print(sample_proscript.id)
        
        global no_of_words
        no_of_words = sample_proscript.get_no_of_words()
        Y_offset = drawSample(sample_proscript, start_drawing_from_word, no_of_words, Y_offset)
        if Y_offset == -1:
            break
    
def draw():
    background(255)
    global draw_from_sample_no
    global draw_from_word_no
    
    drawSampleset(draw_from_sample_no, draw_from_word_no)

    noLoop()
    drawLegend()

def mousePressed():
    global drawn_words
    global select_range
    global minim
    global groove
    click_on_fuera = True
    for index, word in enumerate(drawn_words):
        if mouseX >= word.word_box_topleft[0] and mouseY >= word.word_box_topleft[1] and mouseX <= word.word_box_bottomright[0] and mouseY <= word.word_box_bottomright[1]:
            if select_range == -1:
                select_range = (index,index)
            elif select_range[0] == select_range[1]:
                if not drawn_words[select_range[0]].segment_ref.proscript_ref.id == drawn_words[index].segment_ref.proscript_ref.id:
                    print("Select from the same sample")
                    select_range = (index,index)
                else:
                    if index > select_range[0]:
                        select_range = (select_range[0], index)
                    elif index < select_range[0]:
                        select_range = (index, select_range[0])
            else:
                select_range = (index,index)
            click_on_fuera = False
    if click_on_fuera:
        select_range = -1

    if not select_range == -1:
        print("Selected %s: %s - %s"%(drawn_words[select_range[0]].segment_ref.proscript_ref.id, drawn_words[select_range[0]].word, drawn_words[select_range[1]].word))
        audio_file = drawn_words[select_range[0]].segment_ref.proscript_ref.audio_file
        print("Audio: %s"%audio_file)
        if audio_file:
            groove = minim.loadFile(audio_file)
            groove.setLoopPoints(int(drawn_words[select_range[0]].start_time * 1000), int(drawn_words[select_range[1]].end_time * 1000))
    else:
        print("Selection empty")
        groove = None
        
    loop()
    
def keyPressed():
    global draw_from_word_no
    global no_of_words
    global draw_from_sample_no
    global no_of_samples
    if key == 'N' or key == 'n':  #next page
        if draw_from_sample_no + config.NUM_SAMPLES_TO_SKIP_ON_PAGE_TURN < no_of_samples:
            draw_from_sample_no += config.NUM_SAMPLES_TO_SKIP_ON_PAGE_TURN
            global select_range
            select_range = -1
            loop()
        elif draw_from_word_no + config.NUM_WORDS_TO_SKIP_ON_PAGE_TURN < no_of_words: 
            draw_from_word_no += config.NUM_WORDS_TO_SKIP_ON_PAGE_TURN
            global select_range
            select_range = -1
            loop()
        else:
            print("end of data")
    if key == 'B' or key == 'b':   #orevious page
        if draw_from_sample_no - config.NUM_SAMPLES_TO_SKIP_ON_PAGE_TURN >= 0:
            draw_from_sample_no -= config.NUM_SAMPLES_TO_SKIP_ON_PAGE_TURN
            global select_range
            select_range = -1
            loop()
        elif draw_from_word_no - config.NUM_WORDS_TO_SKIP_ON_PAGE_TURN >= 0:
            draw_from_word_no -= config.NUM_WORDS_TO_SKIP_ON_PAGE_TURN
            global select_range
            select_range = -1
            loop()
        else:
            print("at the beginning of data")
    if key == 'P' or key == 'p':   #play and pause
        global groove
        global audio_file
        if groove and groove.isPlaying():
            groove.pause()
            groove.rewind()
        elif groove:
            groove.loop(0)
    if key == 'R' or key == 'r':  #refresh view
        global dataset_id
        load_dataset()
        loop()
    if key == 'X' or key == 'x':
        print("exiting")
        exit()
    if key == 'S' or key == 's':
        saveFrame("%s/batchfrom-%i.png"%(config.DIR_SAVED_FRAMES, draw_from_word_no))
        print("Saved frame to %s/batchfrom-%i.png"%(config.DIR_SAVED_FRAMES, draw_from_word_no))
    if key == 'C' or key == 'c':
        initializeColors()
        loop()
    if key == 'Q' or key == 'q':
        exit()
    if key >= '0' and key <= '9':
        global dataset_id
        dataset_id = key
        load_dataset()
        loop()
