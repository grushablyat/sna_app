import os
from jpype import getDefaultJVMPath, isJVMStarted, JPackage, startJVM

from config import GEPHI_TOOLKIT_PATH


# Запускаем JVM
if not isJVMStarted():
    startJVM(getDefaultJVMPath(), f"-Djava.class.path={GEPHI_TOOLKIT_PATH}")

# Импортируем Gephi Toolkit
gephi = JPackage("org").gephi

# Создаём проект
project = gephi.project.api.ProjectController.newProject()

# project_controller = gephi.project.api.ProjectController#.newInstance()
# project_controller.newProject()
workspace = project_controller.getCurrentWorkspace()

# Создаём граф
graph_model = gephi.graph.api.GraphModel.newInstance(workspace)
graph = graph_model.getDirectedGraph()

# Добавляем узлы и рёбра
node1 = graph_model.factory().newNode("1")
node1.setLabel("Node A")
node2 = graph_model.factory().newNode("2")
node2.setLabel("Node B")
graph.addNode(node1)
graph.addNode(node2)
edge = graph_model.factory().newEdge(node1, node2)
graph.addEdge(edge)

# # Экспортируем в GEXF
# export_controller = gephi.io.exporter.api.ExportController.newInstance()
# exporter = gephi.io.exporter.plugin.ExporterGEXF()
# export_controller.exportFile(java.io.File("output_toolkit.gexf"), exporter)
#
# print("Граф создан и сохранён в output_toolkit.gexf")