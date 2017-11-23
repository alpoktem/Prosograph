# Prosograph
A Visualizer for prosodically annotated speech corpora written in Processing. Prosograph lets visualize a prosodically annotated speech corpus on a large scale. An example of a view:

[[https://github.com/alpoktem/Prosograph/blob/master/saved-frames/batchfrom-0.tif]]

In the `dataset` directory you can find sample data. Data is encoded as python dictionaries and stored as pickle files.  

Visual configurations are set in `config.py`.

Data specific configurations are set in  `dataconfig_xxx.py` and imported in the main script `Prosograph.pyde`. Which data file to read is specified in data configuration file in the `DATASET` variable. 

More information on the tool can be found in [our publication](http://hdl.handle.net/10230/32719).

# Keyboard shortcuts:
* N - skip ahead 20 words 
* B - skip back 20 words
* S - save current view as image to disk
* C - re-randomize colours
* X - Exit

# Citing
This software is published in Interspeech 2017.

	@inproceedings{prosograph,
		author = {Alp Oktem and Mireia Farrus and Leo Wanner},
		title = {Prosograph: a tool for prosody visualisation of large speech corpora},
		booktitle = {Proceedings of the 18th Annual Conference of the International Speech Communication Association (INTERSPEECH)},
		year = {2017},
		address = {Stockholm, Sweden}
	}