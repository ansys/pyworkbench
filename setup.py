"""Installation file for the ansys-workbench-core package"""

from datetime import datetime
import os

from ansys.tools.protoc_helper import CMDCLASS_OVERRIDE
import setuptools

# Get the long description from the README file
HERE = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(HERE, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

product = "workbench"
library = "core"
package_info = ["ansys", product, library]
with open(os.path.join(HERE, "src", "ansys", product, library, "VERSION"), encoding="utf-8") as f:
    version = f.read().strip()

package_name = "ansys-workbench-core"
dot_package_name = ".".join(filter(None, package_info))

description = f"Public Python API package for {package_name}, built on {datetime.now().strftime('%H:%M:%S on %d %B %Y')}"  # noqa: E501

if __name__ == "__main__":
    setuptools.setup(
        name=package_name,
        version=version,
        author="ANSYS, Inc.",
        author_email="frank.li@ansys.com",
        description=description,
        long_description=long_description,
        long_description_content_type="text/markdown",
        url=f"https://github.com/ansys-internal/{package_name}",
        license="MIT",
        python_requires=">=3.7",
        install_requires=["grpcio~=1.17", "protobuf~=3.19", "wMI>=1.4.9", "tqdm>=4.65.0"],
        package_dir={"": "src"},
        packages=setuptools.find_namespace_packages("src", include=("ansys.*",)),
        package_data={
            "": ["*.pyi", "py.typed", "VERSION"],
        },
        entry_points={
            "ansys.tools.protoc_helper.proto_provider": [f"{dot_package_name}={dot_package_name}"],
        },
        cmdclass=CMDCLASS_OVERRIDE,
    )
