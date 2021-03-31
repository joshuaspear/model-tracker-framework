import os
import pathlib

from model_tracker_framework import ExperimentOption
from model_tracker_framework.SupervisedModelExperiment import SupervisedModelExperiment
import numpy as np
import pandas as pd

from sklearn.ensemble import ExtraTreesClassifier
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import LabelEncoder, OneHotEncoder
from sklearn.model_selection import train_test_split



# This only for the purposes of this example, for ease of running.
curr_dir = pathlib.Path(__file__).parent.absolute()
data_path = os.path.join(curr_dir, "drug200.csv")
if not os.path.isfile(data_path):
    print("Cannot find drug200.csv, attempting to download from kaggle")
    try:
        import kaggle
        print("Downloading dataset from kaggle")
        kaggle.api.authenticate()
        kaggle.api.dataset_download_files('prathamtripathi/drug-classification', path=curr_dir, unzip=True)
    except ModuleNotFoundError:
        print("""kaggle module not installed. 
        To automatically download the required data, install the kaggle module. 
        Else manually download the data from the following link (https://www.kaggle.com/prathamtripathi/drug-classification) 
        and place in the same directory as this python file """)

# Creating 
model_output_dir = os.path.join(curr_dir, "model_output")
if not os.path.exists(model_output_dir):
    print("Creating model_output directory at: {}".format(model_output_dir))
    os.makedirs(model_output_dir)


class ModelExperimentProject(SupervisedModelExperiment):
    # Ordinarily this should be split out into a seperate .py file
    def __init__(self, model_name):
        super().__init__(model_name, debug_skips_preprop_steps=False)
        self.model = None
        self.cat_x_vars = ["sex", "bp", "cholesterol"]

    def preprocessing_steps(self):
        input_df = pd.read_csv(os.path.join(curr_dir, "drug200.csv"))
        input_df.columns = input_df.columns.str.lower()
        y = input_df["drug"]
        le = LabelEncoder()
        y = le.fit_transform(y)
        X = input_df.drop(columns=["drug"])
        X_cat = X[self.cat_x_vars]
        ohe = OneHotEncoder(sparse=False)
        X_cat = ohe.fit_transform(X_cat)
        X_cat = pd.DataFrame(X_cat)
        X_num = X.drop(columns=self.cat_x_vars)
        X = pd.merge(X_cat, X_num, left_index=True, right_index=True)
        self.X_train, self.X_test, self.y_true_train, self.y_true_test = train_test_split(
            X, y, test_size=0.2, random_state=42)

    def preprocessing_debug(self, debug_prop=0.1):
        # Simple debug - just take 10% of the input dataset
        self.y_true_train = self.y_true_train[0:round(self.y_true_train.shape[0]*debug_prop)]
        self.y_true_test = self.y_true_test[0:round(self.y_true_test.shape[0]*debug_prop)]
        self.X_train = self.X_train.iloc[0:round(self.X_train.shape[0]*debug_prop)]
        self.X_test = self.X_test.iloc[0:round(self.X_test.shape[0]*debug_prop)]

    def evaluate_model(self):
        self.y_pred_test = self.model.predict(self.X_test)
        self.results["test_accuracy"] = accuracy_score(self.y_true_test, self.y_pred_test)
        self.y_pred_train = self.model.predict(self.X_train)
        self.results["train_accuracy"] = accuracy_score(self.y_true_train, self.y_pred_train)


class ModelExperiment1(ModelExperimentProject):

    def __init__(self, model_name):
        super().__init__(model_name)
        

    def train_model(self):
        model = ExtraTreesClassifier()
        model.fit(self.X_train, self.y_true_train)
        self.model = model
        

if __name__ == "__main__":
    exp1 = ModelExperiment1("Experiment_1")
    exp1.run_experiment(
        existing_tracker_path=os.path.join(curr_dir, "model_tracker.json"),
        exp_description="Test experiment", 
        # Need to work out how to make these relative!
        parent_sv_dir = os.path.join(curr_dir, "model_output"),
        dupe_model_nms=ExperimentOption("overwrite"), debug=False)