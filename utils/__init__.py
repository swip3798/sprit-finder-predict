def pad(num):
    num = str(num)
    if len(num) < 2:
        return "0" + num
    return num

from .batch_iterator import BatchIterator, BatchIteratorSingle

def get_input_target(df):
    inputs = df.iloc[:, :-1]
    targets = df.iloc[:, -1:]
    return inputs, targets