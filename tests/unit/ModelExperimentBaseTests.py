import model_tracker_framework as mtf
import unittest
import json
import collections
import pandas as pd
import os
from sklearn.linear_model import SGDClassifier
from sklearn.metrics import precision_score, recall_score

class UnitTstExp(mtf.ModelExperimentBase):
    
    def __init__(self, model_name, debug_skips_preprop_steps) -> None:
        super().__init__(model_name, debug_skips_preprop_steps)
        self.train_df = None
        self.test_df = None
        self.model = None
        
    def preprocessing_steps(self):
        df = pd.read_csv("tests/unit/unit_test_data.csv")
        df = df[["Age", "Na_to_K", "Drug"]]
        self.train_df = df.iloc[:-2]
        self.test_df = df.iloc[-2:]
        
    def preprocessing_debug(self):
        self.preprop_df = preprop_df.iloc[0:5]
        
    def train_model(self):
        self.model = SGDClassifier()
        self.model.fit(X=self.train_df[["Age", "Na_to_K"]], 
                       y=self.train_df["Drug"])
        
    def evaluate_model(self):
        test_pred = self.model.predict(self.test_df[["Age", "Na_to_K"]])
        self.results["recall"] = recall_score(self.test_df["Drug"], test_pred, 
                                             average="micro")
        self.results["precision"] = precision_score(self.test_df["Drug"], test_pred, 
                                                   average="micro")
        




class ModelTrackerTests(unittest.TestCase):
    
    #model_exp = UnitTstExp(model_name="unit_tst_exp",
    #                        debug_skips_preprop_steps=False)

    def test_preprocessing_debug_skips(self):
        model_exp_true_skip = UnitTstExp(model_name="unit_tst_exp",
                                         debug_skips_preprop_steps=True)
        # When running in debug we should expect only preprocessing_debug to run which should raise an error
        self.assertRaises(NameError, lambda:model_exp_true_skip.preprocessing(debug=True))
        
        # When running in non debug we should expect the processed data to be in the self.train_df and self.test_df attributes
        model_exp_true_skip.preprocessing(debug=False)
        self.assertEqual(model_exp_true_skip.train_df.shape, (7, 3))
        self.assertEqual(model_exp_true_skip.test_df.shape, (2, 3))

    
    def test_preprocessing_debug_no_skips(self):
        model_exp = UnitTstExp(model_name="unit_tst_exp", debug_skips_preprop_steps=False)
        # When running in debug we should expect the train set to have 3 rows and test to have 2
        self.assertRaises(NameError, lambda:model_exp.preprocessing(debug=True))
        
        # When running in debug we should expect the train set to have 7 rows and test to have 2
        model_exp.preprocessing(debug=False)
        self.assertEqual(model_exp.train_df.shape, (7, 3))
        self.assertEqual(model_exp.test_df.shape, (2, 3))
        
    def test_run_experiment(self):
        model_exp = UnitTstExp(model_name="unit_tst_exp", debug_skips_preprop_steps=False)
        # 1. debug false, overwrite, new tracker
        # Expected output:
        model_exp.run_experiment(existing_tracker_path="tests/unit/model_tracker_run_experiment.json",
                                 debug=False,
                                 exp_description = "tests/unit", parent_sv_dir = "tests/unit", 
                                 dupe_model_nms=mtf.ExperimentOption("overwrite"))
        
        json_tracker = pd.read_json("tests/unit/model_tracker_run_experiment.json")
        self.assertEqual(json_tracker["model_name"].iloc[0], "unit_tst_exp")
        self.assertTrue("precision" in json_tracker.columns)
        self.assertTrue("recall" in json_tracker.columns)
        self.assertEqual(json_tracker["experiment_description"].iloc[0], "tests/unit")
        self.assertEqual(json_tracker["output_save_location"].iloc[0], "tests/unit/unit_tst_exp")
        self.assertTrue(os.path.exists("tests/unit/unit_tst_exp"))
        
        
        # 2. debug true, overwrite, existing tracker
        self.assertRaises(NameError, lambda:model_exp.run_experiment(existing_tracker_path="tests/unit/model_tracker_run_experiment.json",
                                                                     debug=True,
                                                                     exp_description = "tests/unit", 
                                                                     parent_sv_dir = "tests/unit/",
                                                                     dupe_model_nms=mtf.ExperimentOption("overwrite")))
        
        # 3. debug false, overwrite, existing tracker
        model_exp.run_experiment(existing_tracker_path="tests/unit/model_tracker_run_experiment.json",
                            debug=False,
                            exp_description = "tests/unit", parent_sv_dir = "tests/unit/", 
                            dupe_model_nms=mtf.ExperimentOption("overwrite")) 
        
        json_tracker = pd.read_json("tests/unit/model_tracker_run_experiment.json")
        self.assertEqual(json_tracker["model_name"].iloc[0], "unit_tst_exp")
        self.assertTrue("precision" in json_tracker.columns)
        self.assertTrue("recall" in json_tracker.columns)
        self.assertEqual(json_tracker["experiment_description"].iloc[0], "tests/unit")
        self.assertEqual(json_tracker["output_save_location"].iloc[0], "tests/unit/unit_tst_exp")
        self.assertEqual(json_tracker.shape[0], 1)
        self.assertTrue(os.path.exists("tests/unit/unit_tst_exp"))

        
        # 4. debug false, duplicate, existing tracker
        model_exp.run_experiment(existing_tracker_path="tests/unit/model_tracker_run_experiment.json",
                                 debug=False,
                                 exp_description = "tests/unit", parent_sv_dir = "tests/unit/", 
                                 dupe_model_nms=mtf.ExperimentOption("duplicate"))

        json_tracker = pd.read_json("tests/unit/model_tracker_run_experiment.json")
        
        self.assertEqual(json_tracker["model_name"].iloc[1], "unit_tst_exp")
        self.assertTrue("precision" in json_tracker.columns)
        self.assertTrue("recall" in json_tracker.columns)
        self.assertEqual(json_tracker["experiment_description"].iloc[1], "tests/unit")
        self.assertEqual(json_tracker["output_save_location"].iloc[1], "tests/unit/unit_tst_exp_1")
        self.assertTrue(os.path.exists("tests/unit/unit_tst_exp"))
        self.assertTrue(os.path.exists("tests/unit/unit_tst_exp_1"))

        
        # 5. debug false, overwrite with multiple runs, existing tracker
        # Expect all runs of that model to be removed
        model_exp.run_experiment(existing_tracker_path="tests/unit/model_tracker_run_experiment.json",
                    debug=False,
                    exp_description = "tests/unit", parent_sv_dir = "tests/unit/", 
                    dupe_model_nms=mtf.ExperimentOption("overwrite")) 
        
        json_tracker = pd.read_json("tests/unit/model_tracker_run_experiment.json")
        self.assertEqual(json_tracker["model_name"].iloc[0], "unit_tst_exp")
        self.assertTrue("precision" in json_tracker.columns)
        self.assertTrue("recall" in json_tracker.columns)
        self.assertEqual(json_tracker["experiment_description"].iloc[0], "tests/unit")
        self.assertEqual(json_tracker["output_save_location"].iloc[0], "tests/unit/unit_tst_exp")
        self.assertEqual(json_tracker.shape[0], 1)
        self.assertTrue(os.path.exists("tests/unit/unit_tst_exp"))
        self.assertTrue(not os.path.exists("tests/unit/unit_tst_exp_1"))

    
if __name__ == '__main__':
    try:
        unittest.main()
    finally:
        # Clean up tests
        os.removedirs("tests/unit/unit_tst_exp")
        os.remove("tests/unit/model_tracker_run_experiment.json")