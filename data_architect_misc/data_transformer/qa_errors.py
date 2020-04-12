import transform_errors


class QAError(transform_errors.TransformError):
    """Base class for QA-related exceptions."""

    def __str__(self):
        return f"\nERROR: QA => {''.join(self.args)}"


class ColumnCountError(QAError):
    """
    Raised when the number of columns in a dataframe
    is not according to expectation
    """
    pass


class PossibleDuplicateError(QAError):
    """
    Raised when there is a possibility of duplicate values
    in a given column. This should alert the programmer to
    check the values in the column again and apply necessary
    mapping to remove the duplicate values.
    """
    pass


class NaNFoundError(QAError):
    """
    Raised when there is any nan value in the given
    the dataframe (entire dataframe or just within a
    column).
    """
    pass


class EmptyStringFoundError(QAError):
    """
    Raised when there is an empty string in a given
    column of the dataframe.
    """
    pass


class LessThanThresholdValueFoundError(QAError):
    """
    Raised when there is value that is less than
    the given threshold value found in a given
    column of the dataframe.
    """
    pass
