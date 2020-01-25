import pytest

@pytest.mark.vcr
def test_vcrtest(dataproxy):
    seq = dataproxy.get_sequence("NC_000013.11",50_000_000,50_000_050)
    assert len(seq) == 50
    assert seq == "TTAGGTGTTTAGATGATTTCTAAGATGCTTTTAAGCCCAGTATTTCTATT"
