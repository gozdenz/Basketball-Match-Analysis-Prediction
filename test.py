from basketbol_maç_analizi_ve_tahmini import compare_teams , get_team_score ,search_team
def test_compare_teams():
    result = compare_teams("Galatasaray", "Fenerbahçe")
    assert result == "Fenerbahçe takımı daha yüksek kazanma olasılığına sahip.", f"Test failed. Result: {result}"

    result = compare_teams("Anadolu Efes", "Büyükçekmece")
    assert result == "Anadolu Efes takımı daha yüksek kazanma olasılığına sahip.", f"Test failed. Result: {result}"


def test_get_team_score():
    result = get_team_score("Galatasaray", "Fenerbahçe")
    assert result == "Galatasaray: 22,\nFenerbahçe: 28", f"Test failed. Result: {result}"

    result = get_team_score("Anadolu Efes", "Büyükçekmece")
    assert result == "Anadolu Efes: 25,\nBüyükçekmece: 20", f"Test failed. Result: {result}"

def test_search_team():
    result = search_team("Galatasaray ")
    assert result == (465, 40, 92, 40) , f"Test failed . Result:{result}"
    result = search_team("Fenerbahçe ")
    assert result == (517, 41, 93, 45) , f"Test failed . Result:{result}"
    result = search_team("Anadolu Efes ")
    assert result == (490, 34, 90, 41) , f"Test failed . Result:{result}"
    result = search_team("Büyükçekmece ")
    assert result == (465, 49, 88, 42) , f"Test failed . Result:{result}"


test_search_team()
test_compare_teams()
test_get_team_score()