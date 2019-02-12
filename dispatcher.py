import os
import pandas as pd


__author__ = "ContraxSuite, LLC; LexPredict, LLC"
__copyright__ = "Copyright 2015-2018, ContraxSuite, LLC"
__license__ = "https://github.com/LexPredict/lexpredict-legan-dictionary/blob/master/LICENSE"
__version__ = "1.0.7"
__maintainer__ = "LexPredict, LLC"
__email__ = "support@contraxsuite.com"


class Source(object):
    """
    Simple wrapper to get access to the repo's data from paths collection attributes chain like
    >>> collection.multi.geopolitical.geopolitical_divisions_csv.as_df
    """
    def __init__(self, name='root', title=None, path=None):
        self._name = name
        self._title = title
        self._file_name, self._file_ext = os.path.splitext(name)
        self._path = path
        self._is_dir = os.path.isdir(path) if path else None
        self._is_file = os.path.isfile(path) if path else None

    def __str__(self):
        return '<Source: name="{}"; path="{}">'.format(self._name, self._path)

    def __repr__(self):
        return self.__str__()

    @property
    def as_str(self):
        if self._is_file:
            with open(self._path, 'r') as f:
                return f.read()

    @property
    def as_df(self):
        if self._is_file:
            if self._file_ext == '.csv':
                return pd.read_csv(self._path)
            elif '.xls' in self._file_ext:
                return pd.read_excel(self._path)
            elif self._file_ext == '.json':
                return pd.read_json(self._path)


source_paths = [os.path.join(path, name)
                for path, _, files in os.walk('./')
                for name in files
                if os.path.split(path)[1] and not path.startswith('./.')]


collection = Source()


for source_path in source_paths:
    source_path_tokens = source_path.split('/')[1:]
    current_item = collection
    for path_token in source_path_tokens:
        token_title = path_token.replace('.', '_')
        if not hasattr(current_item, token_title):
            path = os.path.join(source_path.split(path_token)[0], path_token)
            new_item = Source(name=path_token, title=token_title, path=path)
            setattr(current_item, token_title, new_item)
        current_item = getattr(current_item, token_title)
