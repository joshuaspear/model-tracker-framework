
class ModelExperimentBaseError(Exception):
    pass


class ExperimentOption:
    """An attempt to enforce static typing. Used in the ModelExperimentBase
    """
    def __init__(self, exp_option):
        if exp_option not in ["overwrite", "duplicate", None]:
            raise TypeError("Values should only be one of overwrite, duplicate or None")
        self.exp_option = exp_option

    def __repr__(self):
        return str(self.exp_option)
