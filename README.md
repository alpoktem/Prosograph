# Prosograph
A Visualizer for prosodically annotated speech corpora written in Processing. Prosograph lets visualize a prosodically annotated speech corpus on a large scale. An example of a view can be seen in `saved-frames` folder. 

More information on the tool can be found in [our publication](http://hdl.handle.net/10230/32719).

## Run

Prosograph is written in [Python mode of Processing](http://py.processing.org/). Once you downloaded and installed Processing, put it in Python mode and then open the main script `Prosograph.pyde` to run.

## Data

In the `dataset` directory sample data is provided. Data is encoded as python dictionaries and stored as pickle files.  

Visual configurations are set in `config.py`.

Data specific configurations are set in  `dataconfig_xxx.py` and imported in the main script `Prosograph.pyde`. Which data file to read is specified in the `DATASET` variable of the data configuration file. 

## Keyboard shortcuts:
* N - skip ahead 20 words 
* B - skip back 20 words
* S - save current view as image to disk
* C - re-randomize colours
* X - Exit

## Citing
This software is presented in Interspeech 2017.

	@inproceedings{prosograph,
		author = {Alp Oktem and Mireia Farrus and Leo Wanner},
		title = {Prosograph: a tool for prosody visualisation of large speech corpora},
		booktitle = {Proceedings of the 18th Annual Conference of the International Speech Communication Association (INTERSPEECH)},
		year = {2017},
		address = {Stockholm, Sweden}
	}