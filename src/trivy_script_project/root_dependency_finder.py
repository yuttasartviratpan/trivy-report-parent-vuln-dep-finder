import json
from typing import List, Dict


def find_root_dependency(json_data) -> List:
    dependencies_data = json_data["Results"][0]["Packages"]
    root_dependency = []
    for dependency in dependencies_data:
        if 'Indirect' not in dependency:
            root_dependency.append(dependency["ID"])
    return root_dependency


def get_reverse_dependency_map(json_data) -> Dict:
    # {"<PackageName>": ["PackageNameThatDependsOnThisKeyPackage", ...]}
    reversed_dependency_map = dict()

    for package in json_data["Results"][0]["Packages"]:
        package_name = package["ID"]
        if 'DependsOn' in package:
            for dependency in package["DependsOn"]:
                if dependency not in reversed_dependency_map:
                    reversed_dependency_map[dependency] = []
                reversed_dependency_map[dependency].append(package_name)

    return reversed_dependency_map


'''
    The parent dependency (The dependency written in poetry/package.json) is located at the first
    entry of key "dependencies", under the child key "dependsOn".
    If the dependsOn is structured in a uuid format, go on to the next entry, should be there.
    If not, keep going until you actually find a dependency name
    
    What makes a package name?
    pkg:<your package manager>/<package artifact id>/<package name>@<package version>
'''


def find_root_dependency_sbom(json_data) -> List:
    found_parent_dependency = False
    ans_ref = dict()
    reference_index = 0
    dependencies_data = json_data["dependencies"]
    root_dependency = []
    while not found_parent_dependency:
        potential_reference = dependencies_data[reference_index]["dependsOn"]
        package_key = potential_reference[0].split(":")[0]
        if package_key == "pkg":
            ans_ref = dependencies_data[reference_index]
            found_parent_dependency = True
        else:
            reference_index += 1

    for dependency in ans_ref["dependsOn"]:
        dependency_name = dependency.split("/")[-1]
        root_dependency.append(dependency_name)

    return root_dependency


def get_reverse_dependency_map_sbom(json_data) -> Dict:
    # {"<PackageName>": ["PackageNameThatDependsOnThisKeyPackage", ...]}
    reversed_dependency_map = dict()
    dependencies_data = json_data["dependencies"]

    for ref in dependencies_data:
        ref_key = ref["ref"].split(":")[0]
        ref_name = ref["ref"].split("/")[-1]
        if ref_key == "pkg":
            depends_on_lst = ref["dependsOn"]
            for package in depends_on_lst:
                package_name = package.split("/")[-1]
                reversed_dependency_map.setdefault(package_name, list())
                reversed_dependency_map[package_name].append(ref_name)

    return reversed_dependency_map
