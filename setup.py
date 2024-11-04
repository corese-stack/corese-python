import subprocess
import os
import shutil
from setuptools import setup
from setuptools.command.sdist import sdist as _sdist

class CustomSDist(_sdist):
    def run(self):  

        print("\033[1m****  Running custom sdist... \033[0m")
        print(f"Current directory: {os.getcwd()}")

        def _build_java_libs():            
            # Detect platform and use the correct gradlew wrapper
            gradlew = 'gradlew.bat' if os.name == 'nt' else './gradlew'
            print(f"Using {gradlew} to build corese-python library")

            # Step 1: Call gradlew clean to ensure a clean build
            subprocess.check_call([gradlew, 'clean'])

            # Step 2: Call gradlew shadowJar task to build corese-python JAR file
            subprocess.check_call([gradlew, 'shadowJar'])
            print("corese-python JAR file built successfully")

            # Step 3: Call gradlew downloadCoreseCore task to download the corese-core JAR file
            subprocess.check_call([gradlew, 'downloadCoreseCore'])

            return os.path.join(os.getcwd(), 'build', 'libs')

        src_dir = _build_java_libs()

        # Ensure the destination directory exists
        dest_dir = 'resources'
        os.makedirs(dest_dir, exist_ok=True)
        
        # Copy files from build/libs to resources directory
        for filename in os.listdir(src_dir):
            if filename.endswith('.jar'):
                shutil.copy(os.path.join(src_dir, filename), dest_dir)
        
        # Continue with the normal sdist process
        super().run()        

setup(
    cmdclass={
        'sdist': CustomSDist,
    },
 
    # Same as having
    # [tool.setuptools.data-files] 
    # "share/pycorese" = ["resources/*.jar"]
    # in pyproject.toml
    # Uncomment if prefer to keep everything in one file.

    # data_files=[
    #     ('share/pycorese', glob.glob('resources/*.jar')),  # Include JAR files from the resources directory
    # ],
    # include_package_data=True,
)
