import subprocess
import os
import shutil
import glob
from setuptools import setup
from setuptools.command.build_py import build_py as _build_py

class CustomBuild(_build_py):
    def run(self):
        # Detect platform and use the correct gradlew wrapper
        gradlew = 'gradlew.bat' if os.name == 'nt' else './gradlew'

        try:
            # Step 1: Call gradlew clean to ensure a clean build
            subprocess.check_call([gradlew, 'clean'])

            # Step 2: Call gradlew shadowJar task to build corese-python JAR file
            subprocess.check_call([gradlew, 'shadowJar'])

            # Step 3: Call gradlew downloadCorese task to download the corese-core JAR file
            subprocess.check_call([gradlew, 'downloadCorese'])

            # Step 2: Copy the JAR file(s) from the Gradle build directory to the resources directory
            jar_source = os.path.join('build', 'libs')  # Adjust this path if necessary
            jar_destination = os.path.join('resources')

            # Create destination directory if it doesn't exist
            os.makedirs(os.path.dirname(jar_destination), exist_ok=True)

            jar_files = glob.glob(os.path.join(jar_source, '*.jar'))  # Find all JAR files
            for jar_file in jar_files:
                shutil.copy(jar_file, jar_destination)
                print(f"Copied {jar_file} to {jar_destination}")

        except subprocess.CalledProcessError as e:
            print(f"Gradle task failed with error: {e}")
            raise

        # Continue with the normal build process
        super().run()

setup(
    cmdclass={
        'build_py': CustomBuild,
    },
)
