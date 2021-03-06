import src.similarity_rewrite as rw
from collections import defaultdict

from tests.common import write_testq

def test_simple_sim():
    tq = write_testq(['gene', 'chemical_substance', 'disease'],
                     ['increases_transport_of','contributes_to'],
                     [True,True])

    print(tq)
    nqs = rw.similarity_expand(tq)
    assert len(nqs) == 1
    assert len(nqs[0]['nodes']) == 4
    assert len(nqs[0]['edges']) == 3
    assert nqs[0]['edges'][-1]['type'] == 'similar_to'


def test_shortest_sim():
    tq = write_testq(['gene', 'chemical_substance'],
                     ['increases_transport_of'],
                     [True])

    if tq.get('query_graph') is not None:
        tq = tq['query_graph']

    print(tq)
    nqs = rw.similarity_expand(tq)
    assert len(nqs) == 1
    assert len(nqs[0]['nodes']) == 3

def test_double_sim():
    tq = write_testq(['gene', 'chemical_substance', 'disease', 'chemical_substance'],
                     ['increases_transport_of', 'contributes_to', 'treats'],
                     [True, True, False])

    if tq.get('query_graph') is not None:
        tq = tq['query_graph']

    newqueries = rw.similarity_expand(tq)
    assert len(newqueries) == 3
    counts = defaultdict(int)
    for nq in newqueries:
        counts[ (len(nq['nodes']), len(nq['edges']))] += 1
    print(counts)
    #There should be 2 cases where we added one node and 1 case where we added 2
    assert counts[(5,4)] == 2
    assert counts[(6,5)] == 1


def test_node_expansion_linear():
    tq = write_testq(['gene', 'chemical_substance', 'disease'],
                     ['increases_transport_of','contributes_to'],
                     [True,True])

    if tq.get('query_graph') is not None:
        tq = tq['query_graph']

    enode = 'node_1'
    newqueries = rw.apply_node_expansion(tq,enode)
    assert len(newqueries) == 1
    nq = newqueries[0]
    assert len(nq['nodes']) == 4
    assert len(nq['edges']) == 3
    #More detailed testing of the query in test_edge_part_of_node_expansion

def test_node_expansion_end():
    tq = write_testq(['gene', 'disease', 'chemical_substance'],
                     ['gene_to_disease', 'contributes_to'],
                     [True, False])

    if tq.get('query_graph') is not None:
        tq = tq['query_graph']

    enode = 'node_2'
    newqueries = rw.apply_node_expansion(tq, enode)
    assert len(newqueries) == 1
    nq = newqueries[0]
    assert len(nq['nodes']) == 4
    assert len(nq['edges']) == 3
    # More detailed testing of the query in test_edge_part_of_node_expansion

def test_node_expansion_branch():
    """Test expanding the pivot of a Y pattern."""
    tq = write_testq(['gene', 'chemical_substance', 'disease'],
                     ['increases_transport_of', 'contributes_to'],
                     [True, True])

    if tq.get('query_graph') is not None:
        tq = tq['query_graph']

    node3 = {"id": "node_3", "type": 'gene'}
    edge2 = {"id": "edge_2", "type": 'decreases_transport_of', "source_id": "node_3", "target_id": "node_1"}

    tq['nodes'].append(node3)
    tq['edges'].append(edge2)
    enode = 'node_1'
    newqueries = rw.apply_node_expansion(tq, enode)
    assert len(newqueries) == 3
    counts = defaultdict(int)
    for nq in newqueries:
        counts[ (len(nq['nodes']), len(nq['edges']))] += 1
    print(counts)
    #There should be 2 cases where we added one node and 1 case where we added 2
    assert counts[(5,4)] == 2
    assert counts[(6,5)] == 1

def test_edge_part_of_node_expansion():
    tq = write_testq(['gene', 'chemical_substance', 'disease'],
                     ['increases_transport_of', 'contributes_to'],
                     [True, True])

    if tq.get('query_graph') is not None:
        tq = tq['query_graph']

    enode = 'node_1'
    eedge = 'edge_1'
    nq = rw.apply_node_expansion_along_edge(tq, eedge, enode)
    #did we add a node?
    assert len(nq['nodes']) == 4
    #are the node ids all unique?
    assert len(set([n['id'] for n in nq['nodes']])) == 4
    #Did we add an edge?
    assert len(nq['edges']) == 3
    #are the edge ids all unique?
    assert len(set([n['id'] for n in nq['edges']])) == 3
    #But we don't want to have changed tq
    assert len(tq['nodes']) == 3
    assert len(tq['edges']) == 2
    #Check the topology of the new query
    degree = defaultdict(int)
    for e in nq['edges']:
        degree[e['source_id']] += 1
        degree[e['target_id']] += 1
    assert degree['node_0'] == 1
    assert degree['node_1'] == 2
    assert degree['node_2'] == 1
    newnodeid = nq['nodes'][-1]['id']
    assert newnodeid not in ['node_0','node_1','node_2']
    assert degree[newnodeid] == 2

def test_add_sim_node():
    tq = write_testq(['gene', 'chemical_substance', 'disease'],
                     ['increases_transport_of', 'contributes_to'],
                     [True, True])

    if tq.get('query_graph') is not None:
        tq = tq['query_graph']

    rw.add_sim_node('node_1',tq)
    #Now there are 4 nodes
    assert len(tq['nodes']) == 4
    #There are still only 2 edges
    assert len(tq['edges']) == 2
    #There need to be 4 unique node identifiers
    nodeids = set( [n['id'] for n in tq['nodes']])
    assert len(nodeids) == 4

def test_generate_novel_sim_id():
    tq = write_testq(['gene', 'chemical_substance', 'disease'],
                     ['increases_transport_of', 'contributes_to'],
                     [True, True])

    if tq.get('query_graph') is not None:
        tq = tq['query_graph']

    test_node = {}
    test_node['id'] = 'node_0'

    nid = rw.generate_novel_sim_id(test_node,tq)
    original_node_ids = [node['id'] for node in tq['nodes']]
    assert nid not in original_node_ids
    tq['nodes'].append( {'id':nid} )
    nid2 = rw.generate_novel_sim_id(test_node,tq)
    assert nid2 != nid
    original_node_ids2 = [node['id'] for node in tq['nodes']]
    assert nid2 not in original_node_ids2



