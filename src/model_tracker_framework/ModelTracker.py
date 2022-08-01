import logging
import os

import pandas as pd

logger = logging.getLogger("mtf_logger")


class ModelTracker:
    
    def __init__(self):
        """Class representing a 'model tracker'. 
        self.rows is a list dictionaries where each dictionary is of the form 
        {column_name: value} and each dictionary represents an individual 
        experiment
        self.column_names is a list of unique column_name value from self.rows
        
        """
        self.rows = []
        self.column_names = []

    def _get_check_consistent_col_names(self, new_row_col_names:list, 
                                        force_columns:bool=False) -> set:
        """Method is used check whether the column names provided in 
        new_row_col_names are consistent with the current names housed in 
        self.column_names. The method raises an exception if the new column 
        names don't align unless force_columns is set to True, in which case a 
        warning is provided.
        

        Args:
            new_row_col_names (list): List of column names to check
            force_columns (bool, optional): Option to force new column names in 
            and avoid exception. Defaults to False.

        Returns:
            set: The column names provided in new_row_col_names that are not 
            already in self.column_names
        """
        miss_frm_exst_col = set(self.column_names) - set(new_row_col_names)
        miss_frm_exst_col_wrn = "Column names {} already exist in the tracker however are missing from the new row".format(miss_frm_exst_col)
        nw_col_names = set(new_row_col_names) - set(self.column_names)
        nw_col_names_wrn = "{} are new column names in the row that are not already in the tracker".format(nw_col_names)
        if len(self.column_names) > 0:
            # Only check if column names are not empty
            if force_columns:
                if len(miss_frm_exst_col) > 0:
                    logger.warning(miss_frm_exst_col_wrn)
                if len(nw_col_names) > 0:
                    logger.warning(nw_col_names_wrn)
            else:
                assert(len(miss_frm_exst_col) == 0), miss_frm_exst_col_wrn
                assert(len(nw_col_names) == 0), nw_col_names_wrn
        return nw_col_names

    def update_tracker_w_dict(self, row_dict:dict, force_columns:bool=False):
        """Updates the self.rows and self.column_names with the new values 
        provided in row_dict

        Args:
            row_dict (dict): dictionary containing {column:values} to be added 
            to the tracker
            force_columns (bool, optional): Option to force new column names in 
            and avoid exception. Defaults to False.
        """

        new_row_col_names = [col for col in row_dict.keys()]
        nw_col_names = self._get_check_consistent_col_names(
            new_row_col_names=new_row_col_names, force_columns=force_columns)
        if len(nw_col_names) > 0:
            self.column_names += nw_col_names
        self.rows.append(row_dict)

    def tracker_to_pandas_df(self)->pd.DataFrame:
        """Converts the values stored in self.rows and returns in the form of a 
        dataframe

        Returns:
            pd.DataFrame: Dataframe containing the values in self.rows
        """
        dict_df = pd.DataFrame.from_dict(self.rows)
        return dict_df

    def tracker_to_csv(self, csv_dir:str, **kwargs):
        """Saves the tracker i.e. values in self.rows as a csv. This is performed 
        via pandas. kwargs should contain options defined in 
        pd.DataFrame.to_csv()
        

        Args:
            csv_dir (str): File location of where to save the output csv
        """
        dict_df = self.tracker_to_pandas_df()
        dict_df.to_csv(csv_dir, **kwargs)

    def import_existing_pandas_df_tracker(self, exstng_track_df:pd.DataFrame, **kwargs):
        """Takes as an input a dataframe representing and model tracker and 
        updates self with values from the dataframe. kwargs should refer to 
        updating options defined in self.update_tracker_w_dict
        

        Args:
            exstng_track_df (pd.DataFrame): Pandas dataframe representing a 
            model tracker
        """
        exstng_track_dict = exstng_track_df.to_dict("records")
        for row in exstng_track_dict:
            self.update_tracker_w_dict(row, **kwargs)

    def import_existing_csv_tracker(self, existing_tracker_path:str, imprt_kwargs:dict = {}, rd_csv_kwargs:dict = {}):
        """Takes as an input a csv representing and model tracker and updates 
        self with values from the csv. This is performed via pandas. 

        Args:
            existing_tracker_path (str): File location of the csv tracker
            imprt_kwargs (dict): kwargs to provide to 
            self.import_existing_pandas_df_tracker. Defaults to {}.
            rd_csv_kwargs (dict): kwargs to provide to pd.read_csv. 
            Defaults to {}.
        """
        exstng_track_df = pd.read_csv(existing_tracker_path, **rd_csv_kwargs)
        self.import_existing_pandas_df_tracker(exstng_track_df, **imprt_kwargs)

    def update_existing_csv_tracker(self, existing_tracker_path:str, 
                                    imprt_kwargs:dict = {}, 
                                    rd_csv_kwargs:dict = {}, 
                                    wrt_csv_kwargs:dict = {}):
        """Imports a csv file representing a model tracker, updates it with the 
        observations captured in self and re-writes the csv

        Args:
            existing_tracker_path (str): File location of the csv tracker
            imprt_kwargs (dict, optional): kwargs to provide to 
            self.import_existing_pandas_df_tracker. Defaults to {}.
            rd_csv_kwargs (dict, optional): kwargs to provide to pd.read_csv. 
            Defaults to {}.
            wrt_csv_kwargs (dict, optional): kwargs to provide to 
            pd.DataFrame.to_csv. Defaults to {}.
        """
        self.import_existing_csv_tracker(
            existing_tracker_path=existing_tracker_path, 
            imprt_kwargs=imprt_kwargs, rd_csv_kwargs=rd_csv_kwargs)
        self.tracker_to_csv(existing_tracker_path, index=False, 
                            **wrt_csv_kwargs)

    def tracker_to_json(self, json_dir:str, **kwargs):
        """Saves the tracker i.e. values in self.rows as a json. This is 
        performed via pandas. kwargs should contain options defined in 
        pd.DataFrame.to_json()

        Args:
            json_dir (str): File location of where to save the output json
        """
        dict_df = self.tracker_to_pandas_df()
        dict_df.to_json(json_dir, **kwargs)

    def import_existing_json_tracker(self, existing_tracker_path:str, 
                                     imprt_kwargs:dict = {}, 
                                     rd_json_kwargs:dict = {}):
        """Takes as an input a json representing and model tracker and updates 
        self with values from the json. This is performed via pandas.

        Args:
            existing_tracker_path (str): File location of the csv tracker
            imprt_kwargs (dict, optional): kwargs to provide to 
            self.import_existing_pandas_df_tracker. Defaults to {}.
            rd_json_kwargs (dict, optional): kwargs to provide to pd.read_json. 
            Defaults to {}.
        """
        exstng_track_df = pd.read_json(existing_tracker_path, **rd_json_kwargs)
        self.import_existing_pandas_df_tracker(exstng_track_df, **imprt_kwargs)

    def update_existing_json_tracker(self, existing_tracker_path: str, 
                                     imprt_kwargs: dict = {},
    rd_json_kwargs:dict = {}, wrt_json_kwargs: dict = {}):
        """Imports a json file representing a model tracker, updates it with the 
        observations captured in self and re-writes the json

        Args:
            existing_tracker_path (str): File location of the csv tracker
            imprt_kwargs (dict, optional): kwargs to provide to 
            self.import_existing_pandas_df_tracker. Defaults to {}.
            rd_json_kwargs (dict, optional): kwargs to provide to pd.read_json. 
            Defaults to {}.
            wrt_json_kwargs (dict, optional): kwargs to provide to 
            pd.DataFrame.to_json. Defaults to {}.
        """
        self.import_existing_json_tracker(
            existing_tracker_path=existing_tracker_path, 
            imprt_kwargs=imprt_kwargs, rd_json_kwargs=rd_json_kwargs)
        self.tracker_to_json(existing_tracker_path, **wrt_json_kwargs)

    @staticmethod
    def check_tracker_exists(existing_tracker_path: str) -> bool:
        """Confirms whether a file exists.

        Args:
            existing_tracker_path (str): Location of file to check

        Returns:
            bool: Returns True if file exists else returns False
        """
        return os.path.isfile(existing_tracker_path)

