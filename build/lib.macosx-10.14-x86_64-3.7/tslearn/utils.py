"""
The :mod:`tslearn.utils` module includes various utilities.
"""

import numpy, mpmath, math,os,sys
from decimal import *

__author__ = 'Romain Tavenard romain.tavenard[at]univ-rennes2.fr'

def write_discretized_dataset(datasets,class_arrays,output_file_str):
    dirname = os.path.abspath(os.path.dirname(sys.argv[0]))
    file_location =  dirname + "/" + output_file_str
    train_test_str = ["_TRAIN_DISCRETIZED","_TEST_DISCRETIZED"]
    for u in range(0,2):
        file_location = file_location + train_test_str[u]
        with open(file_location, "w") as myfile:
            for i in range(0,len(datasets[u])):
                for j in range(0,len(datasets[u][i])):
                    myfile.write(str(i+1) + " " + str(j+1) + " " + str(class_arrays[u][i]) + " " + datasets[u][i][j] + "\n")
    return

def multivar_final_symbolic_representation(dataset,variables,alphabet):
    symbol_increment = 0
    symbolic_association_dict = {}
    for i in range(0,len(dataset)):
        for j in range(0,len(dataset[i])):
            if dataset[i][j] in symbolic_association_dict:
                dataset[i][j] = symbolic_association_dict[dataset[i][j]]
            else:
                symbolic_association_dict[dataset[i][j]] = str(symbol_increment)
                dataset[i][j] = symbolic_association_dict[dataset[i][j]]
                symbol_increment = symbol_increment + 1
    return


def my_covariance_matrix(data,variables_size):
    cov_matrix = mpmath.matrix(variables_size)
    #cov_matrix = numpy.zeros((variables_size,variables_size))

    for i in range(0,variables_size):
        #diagonal!
        cov_matrix[i,i] = mpmath.mpf(my_variance(data[i]))
        for j in range(0,variables_size):
            cov_matrix[i,j] = cov_funct(data[i],data[j])
            #matrix is simmetric!
            cov_matrix[j,i] = cov_matrix[i,j]
    return cov_matrix

def my_variance(vect):
    #mexer no vect?
    vect_mean = my_mean(vect)
    for i in range(0,len(vect)):
        vect[i] = mpmath.mpf(vect[i] - vect_mean)
    return mpmath.fsum(vect**2)/mpmath.mpf(len(vect))

def cov_funct(vect1,vect2):
    vect1_mean = my_mean(vect1)
    vect2_mean = my_mean(vect2)
    for i in range(0,len(vect1)):
        vect1[i] = mpmath.mpf(vect1[i] - vect1_mean)
        vect2[i] = mpmath.mpf(vect2[i] - vect2_mean)
    return mpmath.fsum(my_vector_multp(vect1,vect2))/mpmath.mpf(len(vect1))
    #return mpmath.mpf(my_mean(my_vector_multp(vect1,vect2)) - (my_mean(vect1)*my_mean(vect2)))


def my_vector_multp(vect1,vect2):
    returnvect = []
    for j in range(0,len(vect1)):
        returnvect.append(mpmath.mpf(vect1[j])*mpmath.mpf(vect2[j]))
    return returnvect


def my_mean(vect):
    sum = mpmath.mpf(0)
    for j in range(0,len(vect)):
        sum = sum + mpmath.mpf(vect[j])
    return mpmath.mpf(sum/mpmath.mpf(len(vect)))


#running for several atributes
def separate_atributes_dataset(X,variables_size):

    return_vector=[]
    for j in range(0,variables_size):
        atribute = []
        for ts in X:
            help=[]
            for element in ts:
                help.append(element[j])
            atribute.append(numpy.array(help))
        return_vector.append(atribute)
    return return_vector


def _arraylike_copy(arr):
    """Duplicate content of arr into a numpy array.

     Examples
     --------
     >>> X_npy = numpy.array([1, 2, 3])
     >>> numpy.alltrue(_arraylike_copy(X_npy) == X_npy)
     True
     >>> _arraylike_copy(X_npy) is X_npy
     False
     >>> numpy.alltrue(_arraylike_copy([1, 2, 3]) == X_npy)
     True
     """
    if type(arr) != numpy.ndarray:
        return numpy.array(arr)
    else:
        return arr.copy()


def bit_length(n):
    """Returns the number of bits necessary to represent an integer in binary, excluding the sign and leading zeros.

    This function is provided for Python 2.6 compatibility.

    Examples
    --------
    >>> bit_length(0)
    0
    >>> bit_length(2)
    2
    >>> bit_length(1)
    1
    """
    k = 0
    try:
        if n > 0:
            k = n.bit_length()
    except AttributeError:  # In Python2.6, bit_length does not exist
        k = 1 + int(numpy.log2(abs(n)))
    return k


def to_time_series(ts,remove_nans=False):
    """Transforms a time series so that it fits the format used in ``tslearn`` models.

    Parameters
    ----------
    ts : array-like
        The time series to be transformed.
    remove_nans : bool (default: False)
        Whether trailing NaNs at the end of the time series should be removed or not

    Returns
    -------
    numpy.ndarray of shape (sz, d)
        The transformed time series.

    Example
    -------
    >>> to_time_series([1, 2]) # doctest: +NORMALIZE_WHITESPACE
    array([[ 1.],
           [ 2.]])
    >>> to_time_series([1, 2, numpy.nan]) # doctest: +NORMALIZE_WHITESPACE
    array([[ 1.],
           [ 2.],
           [ nan]])
    >>> to_time_series([1, 2, numpy.nan], remove_nans=True) # doctest: +NORMALIZE_WHITESPACE
    array([[ 1.],
           [ 2.]])

    See Also
    --------
    to_time_series_dataset : Transforms a dataset of time series
    """
    ts_out = _arraylike_copy(ts)
    if ts_out.ndim == 1:
        ts_out = ts_out.reshape((-1, 1))
    if ts_out.dtype != numpy.float:
        ts_out = ts_out.astype(numpy.float)
    if remove_nans:
        ts_out = ts_out[:len(ts)]
    return ts_out

#running for several atributes
def to_time_series_dataset(dataset,variables_size=1,dtype=numpy.float):
    """Transforms a time series dataset so that it fits the format used in ``tslearn`` models.

    Parameters
    ----------
    dataset : array-like
        The dataset of time series to be transformed.
    dtype : data type (default: numpy.float)
        Data type for the returned dataset.

    Returns
    -------
    numpy.ndarray of shape (n_ts, sz, d) or array of numpy.ndarray of shape (sz_i, d)
        The transformed dataset of time series. Represented as a list of numpy arrays if equal_size is False.

    Example
    -------
    >>> to_time_series_dataset([[1, 2]]) # doctest: +NORMALIZE_WHITESPACE
    array([[[ 1.],
            [ 2.]]])
    >>> to_time_series_dataset([[1, 2], [1, 4, 3]]) # doctest: +NORMALIZE_WHITESPACE
    array([[[  1.],
            [  2.],
            [ nan]],
    <BLANKLINE>
           [[  1.],
            [  4.],
            [  3.]]])

    See Also
    --------
    to_time_series : Transforms a single time series
    """
    if variables_size==1:
        if numpy.array(dataset[0]).ndim == 0:
            dataset = [dataset]
        n_ts = len(dataset)
        max_sz = max([ts_size(to_time_series(ts)) for ts in dataset])
        d = to_time_series(dataset[0]).shape[1]
        dataset_out = numpy.zeros((n_ts, max_sz, d), dtype=dtype) + numpy.nan
        for i in range(n_ts):
            ts = to_time_series(dataset[i], remove_nans=True)
            dataset_out[i, :ts.shape[0]] = ts
        return dataset_out
    else:
        return_vector=[]
        for j in range(0,variables_size):
            if numpy.array(dataset[j][0]).ndim == 0:
                dataset[j] = [dataset[j]]
            n_ts = len(dataset[j])
            max_sz = len(dataset[j][0])
            d = to_time_series(dataset[j][0],2).shape[1]
            dataset_out = numpy.zeros((n_ts, max_sz, d), dtype=dtype) + numpy.nan
            for i in range(n_ts):
                ts = to_time_series(dataset[j][i], remove_nans=True)
                dataset_out[i, :ts.shape[0]] = ts
            return_vector.append(dataset_out)

        return return_vector


def timeseries_to_str(ts, fmt="%.18e"):
    """Transforms a time series to its representation as a string (used when saving time series to disk).

    Parameters
    ----------
    ts : array-like
        Time series to be represented.
    fmt : string (default: "%.18e")
        Format to be used to write each value.

    Returns
    -------
    string
        String representation of the time-series.

    Examples
    --------
    >>> timeseries_to_str([1, 2, 3, 4], fmt="%.1f")  # doctest: +NORMALIZE_WHITESPACE
    '1.0 2.0 3.0 4.0'
    >>> timeseries_to_str([[1, 3], [2, 4]], fmt="%.1f")  # doctest: +NORMALIZE_WHITESPACE
    '1.0 2.0|3.0 4.0'

    See Also
    --------
    load_timeseries_txt : Load time series from disk
    str_to_timeseries : Transform a string into a time series
    """
    ts_ = to_time_series(ts)
    dim = ts_.shape[1]
    s = ""
    for d in range(dim):
        s += " ".join([fmt % v for v in ts_[:, d]])
        if d < dim - 1:
            s += "|"
    return s


def str_to_timeseries(ts_str):
    """Reads a time series from its string representation (used when loading time series from disk).

    Parameters
    ----------
    ts_str : string
        String representation of the time-series.

    Returns
    -------
    numpy.ndarray
        Represented time-series.

    Examples
    --------
    >>> str_to_timeseries("1 2 3 4")  # doctest: +NORMALIZE_WHITESPACE
    array([[ 1.],
           [ 2.],
           [ 3.],
           [ 4.]])
    >>> str_to_timeseries("1 2|3 4")  # doctest: +NORMALIZE_WHITESPACE
    array([[ 1., 3.],
           [ 2., 4.]])

    See Also
    --------
    load_timeseries_txt : Load time series from disk
    timeseries_to_str : Transform a time series into a string
    """
    dimensions = ts_str.split("|")
    ts = [dim_str.split(" ") for dim_str in dimensions]
    return to_time_series(numpy.transpose(ts))


def save_timeseries_txt(fname, dataset, fmt="%.18e"):
    """Writes a time series dataset to disk.

    Parameters
    ----------
    fname : string
        Path to the file in which time series should be written.
    dataset : array-like
        The dataset of time series to be saved.
    fmt : string (default: "%.18e")
        Format to be used to write each value.

    See Also
    --------
    load_timeseries_txt : Load time series from disk
    """
    fp = open(fname, "wt")
    for ts in dataset:
        fp.write(timeseries_to_str(ts, fmt=fmt) + "\n")
    fp.close()


def load_timeseries_txt(fname):
    """Loads a time series dataset from disk.

    Parameters
    ----------
    fname : string
        Path to the file from which time series should be read.

    Returns
    -------
    numpy.ndarray or array of numpy.ndarray
        The dataset of time series.

    Examples
    --------
    >>> dataset = to_time_series_dataset([[1, 2, 3, 4], [1, 2, 3]])
    >>> save_timeseries_txt("tmp-tslearn-test.txt", dataset)
    >>> reloaded_dataset = load_timeseries_txt("tmp-tslearn-test.txt")
    >>> [numpy.alltrue((ts0[:ts_size(ts0)] - ts1[:ts_size(ts1)]) < 1e-6) for ts0, ts1 in zip(dataset, reloaded_dataset)]
    [True, True]
    >>> dataset = to_time_series_dataset([[1, 2, 4], [1, 2, 3]])
    >>> save_timeseries_txt("tmp-tslearn-test.txt", dataset)
    >>> reloaded_dataset = load_timeseries_txt("tmp-tslearn-test.txt")
    >>> [numpy.alltrue((ts0 - ts1) < 1e-6) for ts0, ts1 in zip(dataset, reloaded_dataset)]
    [True, True]

    See Also
    --------
    save_timeseries_txt : Save time series to disk
    """
    dataset = []
    fp = open(fname, "rt")
    for row in fp.readlines():
        ts = str_to_timeseries(row)
        dataset.append(ts)
    fp.close()
    return to_time_series_dataset(dataset)


def check_equal_size(dataset):
    """Check if all time series in the dataset have the same size.

    Parameters
    ----------
    dataset: array-like
        The dataset to check.

    Returns
    -------
    bool
        Whether all time series in the dataset have the same size.

    Examples
    --------
    >>> check_equal_size([[1, 2, 3], [4, 5, 6], [5, 3, 2]])
    True
    >>> check_equal_size([[1, 2, 3, 4], [4, 5, 6], [5, 3, 2]])
    False
    """
    dataset_ = to_time_series_dataset(dataset)
    sz = -1
    for ts in dataset_:
        if sz < 0:
            sz = ts_size(ts)
        else:
            if sz != ts_size(ts):
                return False
    return True


def ts_size(ts):
    """Returns actual time series size.

    Final timesteps that have NaN values for all dimensions will be removed from the count.

    Parameters
    ----------
    ts : array-like
        A time series.

    Returns
    -------
    int
        Actual size of the time series.

    Examples
    --------
    >>> ts_size([1, 2, 3, numpy.nan])
    3
    >>> ts_size([[1, 2], [2, 3], [3, 4], [numpy.nan, 2], [numpy.nan, numpy.nan]])
    4
    """

    ts_ = to_time_series(ts)
    sz = ts_.shape[0]
    while not numpy.any(numpy.isfinite(ts_[sz - 1])):
        sz -= 1
    return sz

#single var mean value
def ts_mean_single_var(ts):
    mean = 0
    for element in ts:
        mean = element + mean
    return mean / len(ts)

#multiple var on same final array
def ts_mean_multiple_var(ts,variables_size):

    return_vector = []
    for j in range(0,variables_size):
        mean = 0
        for element in ts:
            mean = element[j] +  mean
        mean = mean / len(ts)
        return_vector.append(mean)
    return return_vector
