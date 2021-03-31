import logging

from .ModelExperimentBase import ModelExperimentBase
from .MTFSupporting import ModelExperimentBaseError, ExperimentOption

logger = logging.getLogger("mtf_logger")


class SupervisedModelExperiment(ModelExperimentBase):

    def __init__(self, model_name, debug_skips_preprop_steps):
        """Exactly the same as ModelExperimentBase but contains additional attributes that may be helpful in a supervised learning  
        context
        Args:
            model_name (str): Name of the experiment. If inheriting this class, this variable should not be perminently defined.
            debug_skips_preprop_steps (bool): Defines whether self.preprocessing_debug replaces self.preprocessing_steps or follows it 
            when running in debug model. If set to True, the self.preprocessing_debug will replace self.preprocessing_steps. 
            This attribute is designed to be perminently set wherever the preprocessing steps are defined.
        """
        super().__init__(model_name, debug_skips_preprop_steps)
        self.y_true_train = None
        self.y_pred_train = None
        self.X_train = None
        self.y_true_test = None
        self.y_pred_test = None
        self.X_test = None



