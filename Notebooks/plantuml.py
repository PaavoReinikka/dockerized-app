import subprocess
import os

class PlantUML:
    def processes_file(self, filename, code):
        with open(filename, "w") as f:
            f.write("@startuml\n")
            f.write(code)
            f.write("\n@enduml\n")
        jar_path = os.path.expanduser("~/plantuml.jar")
        subprocess.run(["java", "-jar", jar_path, "-tpng", filename])
