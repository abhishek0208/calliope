from __future__ import print_function
from __future__ import division

import pytest
import tempfile

import common


class TestModel:
    @pytest.fixture(scope='module')
    def model_one_tech_one_site(self):
        nodes = """
            nodes:
                1:
                    level: 1
                    within:
                    techs: ['ccgt', 'demand']
                    override:
                        ccgt:
                            constraints:
                                e_cap_max: 100
                        demand:
                            constraints:
                                r: -50
            links:
        """
        config_run = """
            input:
                techs: {techs}
                nodes: {nodes}
                path: '{path}'
            output:
                save: false
            subset_t: ['2005-01-01', '2005-01-02']
        """
        with tempfile.NamedTemporaryFile() as f:
            f.write(nodes)
            f.read()
            model = common.simple_model(config_run=config_run,
                                        config_nodes=f.name)
        model.run()
        return model

    def test_one_tech_one_site_solves(self, model_one_tech_one_site):
        model = model_one_tech_one_site
        assert str(model.results.Solution.Status) == 'optimal'

    def test_one_tech_one_site_balanced(self, model_one_tech_one_site):
        model = model_one_tech_one_site
        df = model.get_system_variables()
        assert df['ccgt'].mean() == 50
        assert (df['ccgt'] == -1 * df['demand']).all()

    def test_one_tech_one_site_costs(self, model_one_tech_one_site):
        model = model_one_tech_one_site
        df = model.get_costs()
        assert df.at['lcoe', 'total', 'ccgt'] == 0.1
