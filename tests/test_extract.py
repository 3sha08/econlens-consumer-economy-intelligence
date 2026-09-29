from econlens.extract import fetch_indicator

class FakeResponse:
    def raise_for_status(self): pass
    def json(self):
        return [{'page':1, 'pages':1}, [{
            'countryiso3code':'IND', 'date':'2023', 'value':None,
            'country':{'value':'India'}}]]

class FakeSession:
    def get(self, url, params, timeout):
        assert 'FP.CPI.TOTL.ZG' in url
        assert params['format'] == 'json'
        assert timeout == 30
        return FakeResponse()

def test_fetch_parses_missing_data_without_imputation():
    frame = fetch_indicator('FP.CPI.TOTL.ZG', session=FakeSession())
    assert frame.shape[0] == 1
    assert frame.loc[0, 'value'] is None
    assert frame.loc[0, 'country_code'] == 'IND'
