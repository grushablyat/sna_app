# This gist is a small example of how to use gephi from Jython
# IT IS INCOMPLETE - see below
#
# this is a small include offering only a minimal subset of shortcuts
# for a couple of Gephi Toolkit controllers. use it at your own risks.
#
# usage:
#
#  1. save this file to gephi.py
#  2. download the gephi toolkit and put it in your java classpath
#  3. from your python app, do:
#
#    from gephi import ProjectController
#    ProjectController().newProject()
#    workspace = ProjectController().getCurrentWorkspace()
#    print workspace
#

import sys
sys.path.append("C:\\Program Files\\gephi_toolkit\\gephi-toolkit-0.10.0-all.jar")

# lookup# some boilerplate code to make life easier
ProjectController().newProject()
from org.openide.util import Lookup
lookup = Lookup.getDefault().lookup

# packages
import org.gephi.project.api as project
import org.gephi.data.attributes.api as attributes
import org.gephi.filters.api as filters
import org.gephi.graph.api as graph
import org.gephi.io.exporter.api as exporter
import org.gephi.io.generator.api as generator
import org.gephi.io.importer.api as importer
import org.gephi.layout.api as layout
import org.gephi.partition.api as partition
import org.gephi.preview as preview
import org.gephi.project.api as project
import org.gephi.ranking.api as ranking
import org.gephi.statistics as statistics
import org.gephi.utils as utils

# controllers
def ProjectController():
    return lookup(project.ProjectController)
def ExportController():
    return lookup(exporter.ExportController)
def ImportController():
    return lookup(importer.ImportController)
def GraphController():
    return lookup(graph.GraphController)

# add more boilerplate interfaces if needed