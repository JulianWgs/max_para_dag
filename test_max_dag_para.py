import networkx as nx
from max_dag_para import max_dag_para


def test_01():
    g = nx.DiGraph()

    g.add_edge("A", "B")
    g.add_edge("A", "C")
    g.add_edge("A", "D")

    g.add_edge("C", "N")

    g.add_edge("B", "E")
    g.add_edge("E", "H")
    g.add_edge("H", "M")
    g.add_edge("B", "F")
    g.add_edge("F", "H")

    g.add_edge("N", "I")
    g.add_edge("N", "J")
    g.add_edge("N", "K")
    g.add_edge("I", "M")
    g.add_edge("J", "M")
    g.add_edge("K", "M")

    g.add_edge("D", "N")
    g.add_edge("D", "O")
    g.add_edge("D", "G")

    g.add_edge("G", "L")
    g.add_edge("O", "L")
    g.add_edge("L", "M")

    assert max_dag_para(g) == 7


def test_02():
    g = nx.DiGraph()

    g.add_edge("A", "B")
    g.add_edge("A", "C")
    g.add_edge("A", "D")

    g.add_edge("B", "E")
    g.add_edge("C", "E")
    g.add_edge("D", "F")

    g.add_edge("E", "G")
    g.add_edge("E", "H")
    g.add_edge("F", "I")
    g.add_edge("F", "H")

    g.add_edge("G", "J")
    g.add_edge("H", "J")
    g.add_edge("I", "J")

    assert max_dag_para(g) == 4


def test_03():
    g = nx.DiGraph()

    g.add_edge("A", "B")
    g.add_edge("A", "C")
    g.add_edge("A", "D")
    g.add_edge("A", "E1")
    g.add_edge("E1", "E")

    g.add_edge("B", "G")
    g.add_edge("C", "G")
    g.add_edge("D", "G")

    g.add_edge("E", "H")
    g.add_edge("F", "H")
    g.add_edge("E", "F")

    g.add_edge("G", "J")
    g.add_edge("G", "I")
    g.add_edge("I", "J")
    g.add_edge("H", "J")

    assert max_dag_para(g) == 5
