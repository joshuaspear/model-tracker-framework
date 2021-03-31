# model_tracker_framework

An object-orientated framework for tracking machine learning projects. The framework aims to make building and tracking the results of experiments easier. 

Key features:
- Automated tracking of experiments in a way that maximises on the reuse of code but allows for expressive development
- In built 'debug' mode for quickly testing code before running a full scale experiment


In the future, the project aims to implement:
- SQL server integration
- Extend the run_experiment method in the ModelExperimentBase to support more than just json model trackers
- Experiment pipelines
- Extending the debug mode to effect the training process not just preprocessing specifying fewer epochs to run during debug
- Integration with Google Collab to simplify collaboration on Google Collab without having to using notebooks.

Please leave any comments you have on our Gitlab or alternatively contact us directly. 

Thanks

Josh Spear, josh.spear9@gmail.com
Jack Cordery-Redolf, Jackbcordery@gmail.com


## Package overview

The package contains two core classes namely, ModelTracker and ModelExperimentBase, which inherits from ModelTracker. An example has been provided on project's Gitlab. To run the example, download the 'examples' folder from the Gitlab repo and run the ModelExperiment1.py file in a Python environment with the model_tracker_framework installed.


### ModelTracker
The ModelTracker represents a table like structure with the "rows" attribute containing lists of dictionaries of the form {"column name" : "value"} and column_names containing a list of unique colunmn names across the rows. The ModelTracker object contains methods for creating, updating and exporting the ModelTracker to various structures i.e. pandas dataframes, jsons etc. The framework has been developed with the intention of storing experiment results in either a database or as a json/csv file and then ModelTracker object should be used to temporarily update the tracker and then re-write elsewhere.


### ModelExperimentBase
The ModelExperimentBase inherits from the ModelTracker adding  functionality to automatically update the underlying tracker with the results of an experiment. The core functionality is the self.run_experiment method, which performs the following:
1. Creates or imports an existing tracker from json. If the tracker is imported, the methods checks whether an entry with the same self.model_name exists. If it does, depending on what is specified by dupe_model_nms parameter the method either overwrites the entry, duplicates the entry or does nothing
2. Creates relevant output directories
3. If preprocessing steps have been implemented in self.preprocessing_steps, these are run
4. Trains the model using self.train_model
5. Evaluates the model outputs using self.evaluate_model 
6. Updates the tracker and re-save's the json

When running in debug mode, no results will be saved to the underlying tracker and depending on how the debug_skips_preprop_steps attribute has been set, self.preprocessing_debug will run instead of or after self.preprocessing_steps. This provides the flexibility to either run a completely different set of preprocessing steps when debugging or apply some post processing to the original preprocessing steps e.g. directly importing a smaller dataset or just cutting the dataset down.

The run_experiment method assumes results will be included in the self.results attribute in the form {"metric_name": "metric_value"} but no restrictions are placed on which method should update this metric. Similarly, a directory stored in self.model_sv_loc is created to store outputs written to disk for example graphs. 

Special care should be taken when specifying the dupe_model_nms parameter in the self.run_experiment method. Refer to section "MTFSupporting" for further information.


### MTFSupporting 
MTFSupporting contains exception classes and the ExperimentOption class. The ExperimentOption should be used when specifying the "dupe_model_nms" parameter for the self.run_experiment method. This class is an attempt to enforce soem static typing in Python cos statically typed > dynamically typed.  


### SupervisedModelExperiment
The SupervisedModelExperiment class inherits from ModelExperimentBase and provides exactly the same functionilty but provides some attributes which may be useful for running supervised machine learning experiments.