# -*- coding: utf-8 -*-
import sys
import os
from distutils.core import setup
from setuptools import find_packages

#########
# settings
#########

project_var_name = "ensae_projects"
versionPython = "%s.%s" % (sys.version_info.major, sys.version_info.minor)
path = "Lib/site-packages/" + project_var_name
readme = 'README.rst'
history = "HISTORY.rst"
requirements = None

KEYWORDS = [project_var_name, 'hackathon', 'teachings', 'Xavier Dupré']
DESCRIPTION = """Helpers for projects, teachings, events."""
CLASSIFIERS = [
    'Programming Language :: Python :: %d' % sys.version_info[0],
    'Intended Audience :: Developers',
    'Topic :: Scientific/Engineering',
    'Topic :: Education',
    'License :: OSI Approved :: MIT License',
    'Development Status :: 5 - Production/Stable'
]

#######
# data
#######

packages = find_packages('src', exclude='src')
package_dir = {k: "src/" + k.replace(".", "/") for k in packages}
package_data = {
    project_var_name: ["*.xml"],
    project_var_name + ".automation": ["*.r", "*.ico"],
    project_var_name + ".datainc.hackathon_2015_croix_rouge": ["*.enc"],
    project_var_name + ".datainc.search_images": ["*.jpg"],
    project_var_name + ".datainc.seattle_streets": ["*.xlsx"],
    project_var_name + ".datainc.zips": ["*.zip"],
    project_var_name + ".hackathon": ["*.jpg", "*.csv"],
}

############
# functions
############


def ask_help():
    return "--help" in sys.argv or "--help-commands" in sys.argv


def is_local():
    file = os.path.abspath(__file__).replace("\\", "/").lower()
    if "/temp/" in file and "pip-" in file:
        return False
    from pyquickhelper.pycode.setup_helper import available_commands_list
    return available_commands_list(sys.argv)


def verbose():
    print("---------------------------------")
    print("package_dir =", package_dir)
    print("packages    =", packages)
    print("package_data=", package_data)
    print("current     =", os.path.abspath(os.getcwd()))
    print("---------------------------------")

##########
# version
##########


if is_local() and not ask_help():
    def write_version():
        from pyquickhelper.pycode import write_version_for_setup
        return write_version_for_setup(__file__)

    write_version()

    versiontxt = os.path.join(os.path.dirname(__file__), "version.txt")
    if os.path.exists(versiontxt):
        with open(versiontxt, "r") as f:
            lines = f.readlines()
        subversion = "." + lines[0].strip("\r\n ")
        if subversion == ".0":
            raise Exception("Git version is wrong: '{0}'.".format(subversion))
    else:
        raise FileNotFoundError(versiontxt)
else:
    # when the module is installed, no commit number is displayed
    subversion = ""

if "upload" in sys.argv and not subversion and not ask_help():
    # avoid uploading with a wrong subversion number
    raise Exception(
        "Git version is empty, cannot upload, is_local()={0}".format(is_local()))

##############
# common part
##############

if os.path.exists(readme):
    with open(readme, "r", encoding='utf-8-sig') as f:
        long_description = f.read()
else:
    long_description = ""
if os.path.exists(history):
    with open(history, "r", encoding='utf-8-sig') as f:
        long_description += f.read()

if "--verbose" in sys.argv:
    verbose()

if is_local():
    import pyquickhelper
    logging_function = pyquickhelper.get_fLOG()
    logging_function(OutputPrint=True)
    from pyquickhelper.pycode import process_standard_options_for_setup
    r = process_standard_options_for_setup(
        sys.argv, __file__, project_var_name,
        unittest_modules=["pyquickhelper"],
        github_owner='sdpython',
        requirements=["pyquickhelper", "jyquickhelper", "manydataapi",
                      "pyensae", "pyrsslocal", "pymyinstall",
                      "mlinsights", "pandas_streaming"],
        additional_notebook_path=["pyquickhelper", "jyquickhelper", "manydataapi",
                                  "pyensae", "pyrsslocal", "pymyinstall", "papierstat",
                                  "lightmlrestapi", "mlinsights", "pandas_streaming"],
        additional_local_path=["pyquickhelper", "jyquickhelper", "manydataapi",
                               "pyensae", "pyrsslocal", "pymyinstall", "papierstat",
                               "lightmlrestapi", "mlinsights", "pandas_streaming"],
        copy_add_ext=["enc", 'jpg'], fLOG=logging_function, layout=['html'],
        covtoken=("ad448134-a962-480b-85c6-a899999575d5", "'_UT_39_std' in outfile"))
    if not r and not ({"bdist_msi", "sdist",
                       "bdist_wheel", "publish", "publish_doc", "register",
                       "upload_docs", "bdist_wininst", "build_ext"} & set(sys.argv)):
        raise Exception("unable to interpret command line: " + str(sys.argv))
else:
    r = False

if not r:
    if len(sys.argv) in (1, 2) and sys.argv[-1] in ("--help-commands",):
        from pyquickhelper.pycode import process_standard_options_for_setup_help
        process_standard_options_for_setup_help(sys.argv)
    from pyquickhelper.pycode import clean_readme
    try:
        from ensae_projects import __version__ as sversion
    except ImportError:
        sversion = None
    long_description = clean_readme(long_description)
    setup(
        name=project_var_name,
        version=sversion,
        author='Xavier Dupré',
        author_email='xavier.dupre@gmail.com',
        license="MIT",
        url="http://www.xavierdupre.fr/app/ensae_projects/helpsphinx/index.html",
        download_url="https://github.com/sdpython/ensae_projects/",
        description=DESCRIPTION,
        long_description=long_description,
        keywords=KEYWORDS,
        classifiers=CLASSIFIERS,
        packages=packages,
        package_dir=package_dir,
        package_data=package_data,
        setup_requires=["pyquickhelper"],
        install_requires=[
            "pyquickhelper>=1.9", "pyensae", "pymyinstall",
            "scikit-learn", "pyrsslocal", "pandas", "numpy",
            "matplotlib", "jupyter", "manydataapi", "mlinsights"],
    )
