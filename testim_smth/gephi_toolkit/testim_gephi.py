from gephi import ProjectController


ProjectController().newProject()
workspace = ProjectController().getCurrentWorkspace()
print(workspace)
