import os
import sys

import pytest

import calliope
from calliope import AttrDict


constraint_sets = AttrDict.from_yaml(os.path.join(os.path.dirname(__file__), 'constraint_sets.yaml'))

_defaults_files = {
    k: os.path.join(os.path.dirname(calliope.__file__), 'config', k + '.yaml')
    for k in ['model', 'defaults']
}
defaults = AttrDict.from_yaml(_defaults_files['defaults'])
defaults_model = AttrDict.from_yaml(_defaults_files['model'])


python36_or_higher = pytest.mark.skipif(
    sys.version_info < (3, 6),
    reason="Requires ordered dicts from Python >= 3.6"
)


def build_test_model(override_dict=None, scenario=None, minimal=False):
    this_path = os.path.dirname(__file__)
    model = 'model_minimal.yaml' if minimal is True else 'model.yaml'

    model_location = os.path.join(this_path, 'test_model', model)

    return calliope.Model(
        model_location, override_dict=override_dict,
        scenario=scenario
    )


def check_error_or_warning(error_warning, test_string_or_strings):
    if hasattr(error_warning, 'list'):
        output = ','.join(str(error_warning.list[i]) for i in range(len(error_warning.list)))
    else:
        output = str(error_warning.value)

    if isinstance(test_string_or_strings, list):
        result = all(test_string in output for test_string in test_string_or_strings)
    else:
        result = test_string_or_strings in output

    return result
