import model_tracker_framework as mtf
import unittest
import json
import collections
import pandas as pd
import os


#valid_col_names = ['test_accuracy', 'train_accuracy', 'model_name', 'experiment_description', 'prev_run_notes', 'train_time_strt', 'train_time_end', 'output_save_location']
#valid_values = [0.975, 1.0, 'Experiment_1', 'Test experiment', '', '01/04/2021 17:24:30', '01/04/2021 17:24:30', '/Users/ukjspear1/Documents/Personal/kaggle_tings/misc_repos/model_tracker_framework/examples/model_output/Experiment_1']

class ModelTrackerTests(unittest.TestCase):

    # Tests for update_tracker_w_dict
    def test_update_tracker_w_dict_no_force(self):
        with open('tests/unit/model_tracker.json') as json_file:
            tracker_dict = json.load(json_file)
        tracker_dict = {k:tracker_dict[k]['0'] for k in tracker_dict.keys()}    
        model_tracker = mtf.ModelTracker()
        model_tracker.column_names.append("test_col")
        self.assertRaises(AssertionError, 
                          lambda:model_tracker.update_tracker_w_dict(row_dict=tracker_dict, 
                                                                     force_columns=False))
    def test_update_tracker_w_dict_no_force_new_col(self):
        with open('tests/unit/model_tracker.json') as json_file:
            tracker_dict = json.load(json_file)
        tracker_dict = {k:tracker_dict[k]['0'] for k in tracker_dict.keys()}    
        model_tracker = mtf.ModelTracker()
        model_tracker.column_names.append("test_col")
        self.assertRaises(AssertionError, 
                          lambda:model_tracker.update_tracker_w_dict(row_dict=tracker_dict, 
                                                                     force_columns=False))
    
    def test_update_tracker_w_dict_no_force_ms_col(self):
        with open('tests/unit/model_tracker.json') as json_file:
            tracker_dict = json.load(json_file)
        tracker_dict = {k:tracker_dict[k]['0'] for k in tracker_dict.keys()} 
        model_tracker = mtf.ModelTracker()
        model_tracker.column_names = list(tracker_dict.keys())
        model_tracker.column_names.remove("test_accuracy")
        self.assertRaises(AssertionError, 
                          lambda:model_tracker.update_tracker_w_dict(row_dict=tracker_dict, 
                                                                     force_columns=False))

    def test_update_tracker_w_dict_force(self):
        with open('tests/unit/model_tracker.json') as json_file:
            tracker_dict = json.load(json_file)
        tracker_dict = {k:tracker_dict[k]['0'] for k in tracker_dict.keys()}    
        model_tracker = mtf.ModelTracker()
        model_tracker.update_tracker_w_dict(row_dict=tracker_dict, 
                                            force_columns=True)

        sorted_model_tracker_cols = model_tracker.column_names.copy()
        sorted_model_tracker_cols.sort()
        sorted_tracker_dict_keys = list(tracker_dict.keys()).copy()
        sorted_tracker_dict_keys.sort()

        sorted_tracker_dict = collections.OrderedDict(sorted(tracker_dict.items()))
        sorted_tracker_rows = collections.OrderedDict(sorted(model_tracker.rows[0].items()))

        self.assertEquals(sorted_model_tracker_cols, sorted_tracker_dict_keys)
        self.assertEquals(sorted_tracker_rows, sorted_tracker_dict)
                
    # Tests tracker_to_pandas_df
    def test_tracker_to_pandas_df(self):
        pandas_tracker = pd.read_json('tests/unit/model_tracker.json')
        model_tracker = mtf.ModelTracker()
        model_tracker.import_existing_pandas_df_tracker(
            exstng_track_df=pandas_tracker)
        pandas_tracker_out = model_tracker.tracker_to_pandas_df()
        self.assertTrue(all(pandas_tracker_out == pandas_tracker))
    
    
    # Tests tracker_to_csv
    def test_tracker_to_csv(self):
        pandas_tracker = pd.read_json('tests/unit/model_tracker.json')
        model_tracker = mtf.ModelTracker()
        model_tracker.import_existing_pandas_df_tracker(
            exstng_track_df=pandas_tracker)
        model_tracker.tracker_to_csv('tests/unit/model_tracker_csv_tst.csv', 
                                     index=False)
        pandas_csv_tracker = pd.read_csv('tests/unit/model_tracker_csv_tst.csv')
        self.assertTrue(all(pandas_csv_tracker == pandas_tracker))
       
    # Tests import_existing_pandas_df_tracker
    def test_import_existing_pandas_df_tracker(self):
        pandas_tracker = pd.read_json('tests/unit/model_tracker.json')
        model_tracker = mtf.ModelTracker()
        model_tracker.import_existing_pandas_df_tracker(
            exstng_track_df=pandas_tracker)
        model_tracker.column_names.sort()
        pandas_cols = list(pandas_tracker.columns)
        pandas_cols.sort()
        
        model_tracker_row = list(model_tracker.rows[0].values())
        model_tracker_row = [str(i) for i in model_tracker_row]
        model_tracker_row.sort()
        pandas_row = list(pandas_tracker.iloc[0])
        pandas_row = [str(i) for i in pandas_row]
        pandas_row.sort()

        self.assertEquals(model_tracker.column_names, pandas_cols)
        self.assertEquals(model_tracker_row, pandas_row)

    
    # Tests import_existing_csv_tracker
    def test_import_existing_csv_tracker(self):
        pandas_csv_tracker = pd.read_csv('tests/unit/model_tracker.csv')
        model_tracker = mtf.ModelTracker()
        model_tracker.import_existing_csv_tracker(existing_tracker_path='tests/unit/model_tracker.csv')
        model_tracker.column_names.sort()
        pandas_cols = list(pandas_csv_tracker.columns)
        pandas_cols.sort()
        model_tracker_row = list(model_tracker.rows[0].values())
        model_tracker_row = [str(i) for i in model_tracker_row]
        model_tracker_row.sort()
        pandas_row = list(pandas_csv_tracker.iloc[0])
        pandas_row = [str(i) for i in pandas_row]
        pandas_row.sort()
        self.assertEquals(model_tracker.column_names, pandas_cols)
        self.assertEquals(model_tracker_row, pandas_row)


    # Tests update_existing_csv_tracker
    def tests_update_existing_csv_tracker(self):
        model_tracker = mtf.ModelTracker()
        model_tracker.import_existing_csv_tracker(existing_tracker_path='tests/unit/model_tracker.csv')
        
        model_tracker_cols = ['test_accuracy', 'train_accuracy', 'model_name', 'experiment_description', 'prev_run_notes', 'train_time_strt', 'train_time_end', 'output_save_location']
        model_tracker_values = [0.975, 1.0, 'Experiment_1', 'Test experiment', '', '01/04/2021 17:24:30', '01/04/2021 17:24:30', '/Users/ukjspear1/Documents/Personal/kaggle_tings/misc_repos/model_tracker_framework/examples/model_output/Experiment_1']
        model_tracker.column_names = model_tracker_cols
        model_tracker.rows.append({k:v for k,v in zip(model_tracker_cols, model_tracker_values)})
        
        model_tracker.update_existing_csv_tracker(existing_tracker_path="tests/unit/model_tracker_updt_tst.csv")
        updt_tracker = pd.read_csv("tests/unit/model_tracker_updt_tst.csv")
        
        self.assertTrue(updt_tracker.shape[0], 2)
        self.assertTrue(updt_tracker.shape[1], 8)
    
    # Tests tracker_to_json   
    def test_tracker_to_json(self):
        pandas_tracker = pd.read_json('tests/unit/model_tracker.json')
        model_tracker = mtf.ModelTracker()
        model_tracker.import_existing_pandas_df_tracker(
            exstng_track_df=pandas_tracker)
        model_tracker.tracker_to_json('tests/unit/model_tracker_json_tst.json')
        pandas_json_tracker = pd.read_json('tests/unit/model_tracker_json_tst.json')
        os.remove("tests/unit/model_tracker_json_tst.json")
        self.assertTrue(all(pandas_json_tracker == pandas_tracker))


    # Tests import_existing_json_tracker 
    def test_import_existing_json_tracker(self):
        pandas_json_tracker = pd.read_json('tests/unit/model_tracker.json')
        model_tracker = mtf.ModelTracker()
        model_tracker.import_existing_json_tracker(existing_tracker_path='tests/unit/model_tracker.json')
        model_tracker.column_names.sort()
        pandas_cols = list(pandas_json_tracker.columns)
        pandas_cols.sort()
        model_tracker_row = list(model_tracker.rows[0].values())
        model_tracker_row = [str(i) for i in model_tracker_row]
        model_tracker_row.sort()
        pandas_row = list(pandas_json_tracker.iloc[0])
        pandas_row = [str(i) for i in pandas_row]
        pandas_row.sort()
        self.assertEquals(model_tracker.column_names, pandas_cols)
        self.assertEquals(model_tracker_row, pandas_row)


    def tests_update_existing_csv_tracker(self):
        model_tracker = mtf.ModelTracker()
        model_tracker.import_existing_json_tracker(existing_tracker_path='tests/unit/model_tracker.json')
        
        model_tracker_cols = ['test_accuracy', 'train_accuracy', 'model_name', 'experiment_description', 'prev_run_notes', 'train_time_strt', 'train_time_end', 'output_save_location']
        model_tracker_values = [0.975, 1.0, 'Experiment_1', 'Test experiment', '', '01/04/2021 17:24:30', '01/04/2021 17:24:30', '/Users/ukjspear1/Documents/Personal/kaggle_tings/misc_repos/model_tracker_framework/examples/model_output/Experiment_1']
        model_tracker.column_names = model_tracker_cols
        model_tracker.rows.append({k:v for k,v in zip(model_tracker_cols, model_tracker_values)})
        
        model_tracker.update_existing_json_tracker(existing_tracker_path="tests/unit/model_tracker_updt_tst.json")
        updt_tracker = pd.read_json("tests/unit/model_tracker_updt_tst.json")
        
        self.assertTrue(updt_tracker.shape[0], 2)
        self.assertTrue(updt_tracker.shape[1], 8)


if __name__ == '__main__':
    try:
        unittest.main()
    finally:
        # Clean up tests
        os.remove("tests/unit/model_tracker_csv_tst.csv")