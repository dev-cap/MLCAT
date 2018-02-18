import pickle

def save_to_disk(data,file_name):
    """
    A function to save any data structure to a file using pickle module
    :param data: data structure that needs to be saved to disk
    :param file_name: name of the file to be used for saving the data
    :return: null
    """
    with open(file_name, 'wb') as fileObj:
        pickle.dump(data, fileObj)


def load_from_disk(file_name):
    """
    A function to load any data structure from a file 
    :param file_name: name of the file to be used for saving the data
    :return: data structure that exists in the file
    """
    with open(file_name, 'r') as fileObj:
        return fileObj.read()
