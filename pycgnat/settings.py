# ==========================
# Constants for the project.
# ==========================

# Define the package's version.
# - Is used for indexing and distributing the package
# - Follow the conventions defined by PEP440
__version__ = '1.0b1'

# Define the supported platforms.
# - Uses the same name defined by the file inside 'generator' package
# - Is used for auto calling the 'generate' function at runtime execution
SUPPORTED_PLATFORMS = (
    'routeros',
)
