import pm4py
from pm4py.objects.process_tree.obj import Operator

# Based on Carmona et al, p 223-224 (https://doi.org/10.1007/978-3-319-99414-7)
def max_node_degree(net):
    # Idea: How many neighbors does the node with the most neighbors have? -> Can be a sign for complexity due to multiple branches
    neighbors = {}
    for arc in net.arcs:
        neighbors.setdefault(arc.source, set()).add(arc.target)
        neighbors.setdefault(arc.target, set()).add(arc.source)
    return max(len(nodes) for nodes in neighbors.values())


def max_gateway_depth(node):
    # Idea: Nested gateways are an indicator for a complex model and makes it hard to understand
    is_gateway = node.operator is not None and node.operator != Operator.SEQUENCE
    return int(is_gateway) + max((max_gateway_depth(child) for child in node.children), default=0)


def evaluate_model(log, model):
    net, im, fm = model
    try:
        depth = max_gateway_depth(pm4py.convert_to_process_tree(net, im, fm))
    except ValueError:  # net is not block-structured, so it has no nesting depth
        depth = float('nan')
    fitness = pm4py.fitness_token_based_replay(log, net, im, fm)
    return {
        'Fitness': fitness['log_fitness'],
        'Perfect_Fit_Share': fitness['perc_fit_traces'] / 100,
        'Precision': pm4py.precision_token_based_replay(log, net, im, fm),
        'Generalization': pm4py.generalization_tbr(log, net, im, fm),
        'Simplicity': pm4py.simplicity_petri_net(net, im, fm, variant="arc_degree"),
        'Simplicity_NodeDegree': max_node_degree(net),
        'Simplicity_Depth': depth,
    }
