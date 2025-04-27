import graph_tool.all as gt
import matplotlib.cm

gt.seed_rng(47)

g = gt.collection.ns["foodweb_baywet"]

sargs = dict(recs=[g.ep.weight],
             rec_types=["real-exponential"])
state = \
    gt.minimize_nested_blockmodel_dl(g,
                                     state_args=sargs)

state.draw(edge_color=gt.prop_to_size(g.ep.weight,
                                      power=1,
                                      log=True),
           ecmap=(matplotlib.cm.inferno, .6),
           eorder=g.ep.weight,
           edge_pen_width=gt.prop_to_size(g.ep.weight,
                                          1, 4,
                                          power=1,
                                          log=True),
           edge_gradient=[]);
