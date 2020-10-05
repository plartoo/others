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


class NullValueFoundError(QAError):
    """
    Raised when there is any NULL/NaN value is
    found in the given dataframe (entire dataframe
    or just within a few given columns).
    """
    pass


class EmptyStringFoundError(QAError):
    """
    Raised when there is an empty string (blank)
    in a given column of the dataframe.
    """
    pass


class InvalidValueFoundError(QAError):
    """
    Raised when there is a value that is invalid
    in the data.
    """
    pass


class ValueComparisonError(QAError):
    """
    Raised when there is value in one column
    does not match corresponding value in
    another column of the dataframe.
    """
    pass


class LessThanThresholdValueFoundError(QAError):
    """
    Raised when there is value that is less than
    the given threshold value found in a given
    column of the dataframe.
    """
    pass


class InsufficientNumberOfColumnsError(QAError):
    """
    Raised when the number of columns found 
    in the data is less than expected.  
    """
    pass


class ColumnListMismatchError(QAError):
    """
    Raised when the column name found is unexpected.
    """
    pass

class UnexpectedColumnNameFoundError(QAError):
    """
    Raised when the column name found is unexpected.
    """
    pass


class UnexpectedColumnValuesFoundError(QAError):
    """
    Raised when value(s) in a given column is(are) unexpected.
    """
    pass


class QA_Reference_Data_Outdated(QAError):
    """
    Raised when the reference data we use in the QA process
    is outdated (say, more than 6 months old) and need
    updating.
    """
    pass
