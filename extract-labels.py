import os

# Define default module and chip labels as global variables
# Update the list in the repository settings when a new chip is introduced
DEFAULT_CHIP_LABELS = os.environ.get("CHIP_LIST")

# Get the value of CI_MERGE_REQUEST_LABELS from the environment
CI_MERGE_REQUEST_LABELS = os.environ.get("CI_MERGE_REQUEST_LABELS")

if CI_MERGE_REQUEST_LABELS:
    # Remove the "Release" label if it exists
    CI_MERGE_REQUEST_LABELS = ",".join(label for label in CI_MERGE_REQUEST_LABELS.split(",") if label != "Release")

def extract_labels():
    if not CI_MERGE_REQUEST_LABELS:
        # Scenario 1: If no module or chip label is selected,
        # build main__LANGUAGE.tex files in all CHIP_SERIES folders
        MODULE_LABELS = 'main'
        CHIP_LABELS = DEFAULT_CHIP_LABELS
        print(f"No MR labels provided. Use default module labels={MODULE_LABELS} and chip labels={CHIP_LABELS}")
    else:
        LABELS = CI_MERGE_REQUEST_LABELS.split(",")
        MODULE_LABELS = ''
        CHIP_LABELS = ''
        # Scenario 2: If both module and chip labels are selected,
        # build the specific MODULE_NAME__LANGUAGE.tex files
        # in the specific CHIP_SERIES folders
        for LABEL in LABELS:
            # Check if label is not in chip labels,
            # or not partially matches chip labels
            if LABEL not in DEFAULT_CHIP_LABELS.split(","):
                MODULE_LABELS += f",{LABEL}"
            else:
                CHIP_LABELS += f",{LABEL}"

        # Remove leading commas if they exist
        MODULE_LABELS = MODULE_LABELS.lstrip(',')
        CHIP_LABELS = CHIP_LABELS.lstrip(',')

        # Scenario 3: If no module label is selected
        # but a chip label is selected,
        # build main__LANGUAGE.tex files in the specific CHIP_SERIES folder
        if not MODULE_LABELS:
            MODULE_LABELS = 'main'

        if not CHIP_LABELS:
            print("Please provide a chip label.")

        print(f"Extract module labels={MODULE_LABELS} and chip labels={CHIP_LABELS}")

    # Export MODULE_LABELS and CHIP_LABELS as environment variables
    with open("labels.env", "w") as env_file:
        env_file.write(f"MODULE_LABELS={MODULE_LABELS}\n")
        env_file.write(f"CHIP_LABELS={CHIP_LABELS}\n")

if __name__ == "__main__":
    extract_labels()
