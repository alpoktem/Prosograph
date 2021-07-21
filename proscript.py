import os
import sys
import csv
import json

END = "<END>"
COPY = "Prosograph"
FLOAT_FORMATTING="{0:.4f}"

class Word(object):
	def __init__(self):
		self.id = ""
		self.word = None
		#timing parameters
		self.duration = 0.0				    #seconds
		self.end_time = 0.0					#seconds
		self.start_time = 0.0				#seconds
		self.pause_before = 0.0  			#seconds
		self.pause_after = 0.0				#seconds
		#speech rate parameters
		self.speech_rate_phon = -1			
		self.speech_rate_normalized = -1
		#acoustic parameters
		self.f0_contour = []
		self.i0_contour = []
		self.f0_contour_xaxis = []
		self.i0_contour_xaxis = [] 
		self.f0_contour_evened = []
		self.i0_contour_evened = []
		self.f0_contour_semitones = []
		self.i0_contour_semitones = []
		self.f0_mean = 0.0
		self.i0_mean = 0.0
		self.f0_mean_hz = 0.0
		self.i0_mean_db = 0.0
		self.f0_slope = 0.0
		self.i0_slope = 0.0
		self.f0_median = 0.0
		self.i0_median = 0.0
		self.f0_sd = 0.0
		self.i0_sd = 0.0
		self.f0_range = 0.0
		self.i0_range = 0.0
		#linguistic parameters
		self.pos = "NA"
		self.punctuation_before = ""
		self.punctuation_after = ""
		#Prosograph variables
		self.word_box_topleft = (0,0)
		self.word_box_bottomright = (0,0)
		self.selected = False
		#references
		self.segment_ref = None

	def memory_address(self):
		return hex(id(self))

	def get_value(self, property_name):
		if hasattr(self, property_name):
			value = getattr(self, property_name)
			return value
		else:
			return None

	def set_value(self, property_name, new_value, given_as_string = False):
		if hasattr(self, property_name):
			if not given_as_string:
				setattr(self, property_name, new_value)
			else:
				if "word" in property_name or "punctuation" in property_name or "pos" in property_name or "id" in property_name:
					setattr(self, property_name, new_value)
				elif "contour" in property_name:
					arr_rep = json.loads(new_value)
					setattr(self, property_name, arr_rep)
				else:
					float_rep = float(new_value)
					setattr(self, property_name, float_rep)

class Segment(object):
	def __init__(self):
		self.start_time = -1.0
		self.end_time = -1.0
		self.transcript = ""
		self.id = ""
		self.speaker_id = ""
		self.word_list = []
		self.word_aligned = False
		self.proscript_ref = None
		self.needs_split_at = []

	def add_word(self, word):
		word.segment_ref = self
		self.word_list.append(word)
		if self.proscript_ref:
			self.proscript_ref.word_list.append(word)

	def get_last_word(self):
		if len(self.word_list) > 0:
			return self.word_list[-1]
		else:
			return None

	def get_no_of_words(self):
		return len(self.word_list)

	def to_string(self):
		#print("segment id: %s"%self.id)
		print("%s (%s): %.2f-%.2f"%(self.id, self.speaker_id, self.start_time, self.end_time))
		print("transcript: %s"%self.transcript)

	def get_value(self, property_name):
		if hasattr(self, property_name):
			value = getattr(self, property_name)
			return value
		else:
			return None

	def set_value(self, property_name, new_value):
		if hasattr(self, property_name):
			setattr(self, property_name, new_value)

	def get_duration(self):
		#if time values are set:
		duration = self.end_time - self.start_time
		return max(0.0, duration)
		#if not:
		#calculate from last word and first word

	def add_end_token(self, punc_before = ""):
		end_word = Word()
		end_word.word = END
		end_word.punctuation_before = punc_before
		self.add_word(end_word)

class Proscript(object):
	def __init__(self):
		self.segment_list = []
		self.word_list = []		#same words as in segments. used for easy indexing
		self.features_extracted = False
		#self.word_list = []
		self.word_feature_set = ["start_time", "end_time", "duration", "pause_before", "pause_after", "pos", "punctuation_before", "punctuation_after", "speech_rate_phon", "f0_mean", "i0_mean", "f0_range", "i0_range", "f0_contour_semitones", "i0_contour_semitones"]
		self.duration = -1.0
		self.speaker_ids = []
		self.speaker_textgrid_files = [] #textgrid file for each speaker, aligned with self.speaker_ids
		self.textgrid_file = ""
		self.audio_file = ""
		self.id = ""
		self.xml_file = ""
		self.words_csv_path = ""
		self.segments_csv_path = ""
		self.speaker_f0_means = []
		self.speaker_i0_means = []

	def as_dict(self):
		p_as_dict = {column:[] for column in ["word"] + self.word_feature_set}
		for word in self.word_list:
			for key in p_as_dict:
				p_as_dict[key].append(word.get_value(key))
		return p_as_dict

	def populate_speaker_ids(self):
		for segment in self.segment_list:
			if segment.speaker_id not in self.speaker_ids:
				self.speaker_ids.append(segment.speaker_id)

	def repopulate_word_list(self):
		self.word_list = []
		for segment in self.segment_list:
			for word in segment.word_list:
				self.word_list.append(word)

	def get_speaker_textgrid_file(self, speaker_id):
		index = self.speaker_ids.index(speaker_id)
		return self.speaker_textgrid_files[index]

	def add_segment(self, segment):
		segment.proscript_ref = self
		self.segment_list.append(segment)
		self.word_list += segment.word_list

	def get_last_segment(self):
		if self.get_no_of_segments() > 0:
			return self.segment_list[-1]
		else:
			return None

	def get_value(self, property_name):
		if hasattr(self, property_name):
			value = getattr(self, property_name)
			return value
		else:
			return None

	def get_last_word(self):
		if self.get_no_of_words() > 0:
			return self.word_list[-1]
		else:
			return None

	def get_speaker_segments(self, speaker_id):
		speaker_segments = []
		for segment in self.segment_list:
			if segment.speaker_id == speaker_id:
				speaker_segments.append(segment)
		return speaker_segments

	def get_segment_by_index(self, segment_index):
		try:
			return self.segment_list[segment_index]
		except:
			return None

	def get_word_by_index(self, word_index):
		try:
			return self.word_list[word_index]
		except:
			return None

	def get_no_of_segments(self):
		return len(self.segment_list)

	def get_no_of_words(self):
		return len(self.word_list)

	def to_csv(self, csv_filename, word_feature_set=[], segment_feature_set=[], delimiter="|"):
		if not word_feature_set:
			word_feature_set = ["id"] + self.word_feature_set
		with open(csv_filename, 'w') as f:
			w = csv.writer(f, delimiter=delimiter)
			rowIds = ['word'] + segment_feature_set + word_feature_set
			w.writerow(rowIds)
			for segment in self.segment_list:
				for word in segment.word_list:
					row = [word.word]
					row += [segment.get_value(feature_id) for feature_id in segment_feature_set]
					row += [word.get_value(feature_id) for feature_id in word_feature_set]
					w.writerow(row) 
		self.words_csv_path = csv_filename

	def segments_to_csv(self, csv_filename, segment_feature_set=[], delimiter="|"):
		with open(csv_filename, 'w') as f:
			w = csv.writer(f, delimiter=delimiter)
			rowIds = segment_feature_set
			w.writerow(rowIds)
			for segment in self.segment_list:
				row = [segment.get_value(feature_id) for feature_id in segment_feature_set]
				w.writerow(row) 
		self.segments_csv_path = csv_filename

	def add_end_token(self, punc_before=""):
		end_word = Word()
		end_word.word = END
		end_word.punctuation_before = punc_before
		self.get_last_segment().add_word(end_word)

	def get_speaker_means(self):
		features = ['f0_mean_hz', 'i0_mean_db']
		for feature_type in features:
			speaker_mean_for_feature = {speaker_id:0.0 for speaker_id in self.speaker_ids}
			for speaker_id in self.speaker_ids:
				measurement_count = 0
				for speaker_segment in self.get_speaker_segments(speaker_id):
					for word in speaker_segment.word_list:
						values = word.get_value(feature_type)
						if not type(values) == list:
							values = [values]
						for measurement in values:
							if measurement > 0.0:
								measurement_count += 1
								speaker_mean_for_feature[speaker_id] += measurement
				if measurement_count > 0:
					speaker_mean_for_feature[speaker_id] /= measurement_count
					speaker_mean_for_feature[speaker_id] = float(FLOAT_FORMATTING.format(speaker_mean_for_feature[speaker_id]))
				else:
					if 'f0' in feature_type:
						speaker_mean_for_feature[speaker_id] = 150 #An average value
					elif 'i0' in feature_type:
						speaker_mean_for_feature[speaker_id] = 55 #An average value

			if 'f0' in feature_type:
				self.speaker_f0_means = speaker_mean_for_feature	
			elif 'i0' in feature_type:
				self.speaker_i0_means = speaker_mean_for_feature	

			print("%s speaker means"%self.id)
			print("%s-%s speaker means:\n%s"%(self.id, feature_type, speaker_mean_for_feature))

	def get_word_id_list(self):
		word_id_list = []
		for word in self.word_list:
			word_id_list.append(word.id)
		return word_id_list

	def clear_content(self):
		self.segment_list = []
		self.word_list = []

	def from_file(self, csv_filename, proscript_id=None, audio_file=None, search_audio=False, delimiter="|"):
		self.clear_content()
		if proscript_id:
			self.id = proscript_id
		else:
			self.id = os.path.splitext(os.path.basename(csv_filename))[0]

		if audio_file:
			self.audio_file = audio_file
		elif search_audio:
			audio_file = os.path.join(os.path.dirname(csv_filename), self.id + '.wav')
			if os.path.isfile(audio_file):
				self.audio_file = audio_file

		with open(csv_filename) as f:
			reader = csv.DictReader(f, delimiter=delimiter) # read rows into a dictionary format

			row_count = 0
			curr_seg = Segment()
			for row in reader: # read a row as {column1: value1, column2: value2,...}
				row_count += 1
				try:
					word_id = row["id"]
				except:
					word_id = "%s.seg0.word%i"%(self.id, row_count)
				segment_id = word_id.split('.')[1]
				segment_id = segment_id.replace('segment', '')
				try:	
					spk_id = row["spk_id"]
					if not spk_id in self.speaker_ids:
						self.speaker_ids.append(spk_id)
				except:
					spk_id = "s1"
					if not spk_id in self.speaker_ids:
						self.speaker_ids.append(spk_id)

				#read word
				word = Word()
				for key in row.keys():
					try:
						word.set_value(key, row[key], given_as_string=True)
					except:
						pass
				if not segment_id == curr_seg.id:	#belongs to new segment
					if not curr_seg.id == "": #don't add the first empty segment
						self.add_segment(curr_seg)
					curr_seg = Segment()
					curr_seg.id = segment_id
					curr_seg.speaker_id = spk_id

				curr_seg.add_word(word)
			self.add_segment(curr_seg)
		self.words_csv_path = csv_filename

	def from_dict(self, proscript_as_dict, proscript_id=None, audio_file=None):
		self.clear_content()
		if proscript_id:
			self.id = proscript_id
		if audio_file:
			self.audio_file = audio_file

		no_of_words = len(proscript_as_dict['word'])

		curr_seg = Segment()
		for index in range(no_of_words): 
			try:
				word_id = proscript_as_dict["id"][index]
				segment_id = word_id.split('.')[1]
				segment_id = segment_id.replace('segment', '')
			except:
				word_id = 'w0'
				segment_id = 's0'
			try:	
				spk_id = proscript_as_dict["spk_id"][index]
				if not spk_id in self.speaker_ids:
					self.speaker_ids.append(spk_id)
			except:
				spk_id = "s1"
				if not spk_id in self.speaker_ids:
					self.speaker_ids.append(spk_id)

			#read word
			word = Word()
			for key in proscript_as_dict.keys():
				try:
					word.set_value(key, proscript_as_dict[key][index])
				except:
					pass
			if not segment_id == curr_seg.id:	#belongs to new segment
				if not curr_seg.id == "": #don't add the first empty segment
					self.add_segment(curr_seg)
				curr_seg = Segment()
				curr_seg.id = segment_id
				curr_seg.speaker_id = spk_id
			curr_seg.add_word(word)

		self.add_segment(curr_seg)