from trivy_script_project.parser import parser
from trivy_script_project.classes.custom_exception import FileExtensionNotSupported
from trivy_script_project.root_dependency_finder import find_root_dependency, get_reverse_dependency_map
import sys

if __name__ == '__main__':
    # 1. Take in a filename, check what type of file extension is it between json and html
    # if json, check if it cyclonedx structure or not (but let's assume it is for now)
    # if html, go to step 2 with html extension in mind
    # otherwise, output unknown or unsupported file extension and exit
    # 2. Parse the file and extract the data
    # Data needed:
    # Parent Dependency: such as Axios, Nuxt/Auth
    # Child Dependency: dependency that Parent dependency relies on, like follows-redirect that Axios used
    # Version: version of the dependency, in format of <current version:fixed version>
    # 3. Output, profited

    # Extra: If you can make an auto-update to fixed version of all dependencies as an argument flag
    #   then that would be nice
    filename = sys.argv[1]

    try:
        parser(filename)
    except FileExtensionNotSupported as e:
        print(e)
    except FileNotFoundError:
        print(f"{filename} cannot be found, Please double check your file path or whether the file exists")
    except IndexError:
        print("Missing an argument for a report file, please provide a report file")
    except Exception as e:
        print("Unknown Exception Occured:")
        print(e)
