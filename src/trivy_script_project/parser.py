from trivy_script_project.classes.custom_exception import FileExtensionNotSupported
from trivy_script_project.root_dependency_finder import (find_root_dependency,
                                                         get_reverse_dependency_map,
                                                         find_root_dependency_sbom,
                                                         get_reverse_dependency_map_sbom)
from trivy_script_project.root_dependency_bfs import bfs
import json


def parser(file_name: str):
    file_extension = file_name.split('.')[-1]
    if len(file_extension) == 1:
        raise FileExtensionNotSupported(file_extension=None)
    elif file_extension == 'json':
        return json_parser(file_name)
    else:
        raise FileExtensionNotSupported(file_extension=file_extension)


def json_parser(file_name: str):
    with (open(file_name, 'r') as file):
        json_data = json.load(file)
        if not isinstance(json_data, dict):
            raise FileExtensionNotSupported(file_extension="json"
                                            ).edit_error_message("The given json file is not of type json or python "
                                                                 "dictionary.")

        else:
            if 'bomFormat' in json_data:
                root_dependency_lst = find_root_dependency_sbom(json_data)
                dependency_mapping = get_reverse_dependency_map_sbom(json_data)
                vulnerability_lst = json_data["vulnerabilities"]
                all_root_vulnerable_dependencies = set()
                for vulnerable_dependency in vulnerability_lst:
                    for affected_dependency in vulnerable_dependency["affects"]:
                        dependency_name = affected_dependency["ref"].split("/")[-1]
                        root_vulnerable_dependencies = bfs(dependency_graph=dependency_mapping,
                                                           root_dependency=root_dependency_lst,
                                                           dependency_key=dependency_name)
                        all_root_vulnerable_dependencies.update(root_vulnerable_dependencies)
                print(all_root_vulnerable_dependencies)
            else:
                root_dependency_lst = find_root_dependency(json_data)
                dependency_mapping = get_reverse_dependency_map(json_data)
                vulnerability_lst = json_data["Results"][0]["Vulnerabilities"]
                all_root_vulnerable_dependencies = set()
                for vulnerable_dependency in vulnerability_lst:
                    root_vulnerable_dependencies = bfs(dependency_graph=dependency_mapping,
                                                       root_dependency=root_dependency_lst,
                                                       dependency_key=vulnerable_dependency["PkgID"])
                    all_root_vulnerable_dependencies.update(root_vulnerable_dependencies)
                print(all_root_vulnerable_dependencies)
