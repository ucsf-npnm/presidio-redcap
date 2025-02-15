# presidio-redcap
An interface for retrieving behavioral survey data from Redcap.

This toolbox is compatible with REDCap projects configured for PRESIDIO. 
Support is provided for projects with the following naming scheme:
`PR##: [Pre-]Stage #` and `PR##: Follow-Up`

Projects labeled with `DEPRECATED` are not supported by this tool.

## How to setup this toolbox
1. Verify that you have user access to PRESIDIO-related Redcap projects by
logging into your [UCSF REDCap](https://redcap.ucsf.edu) account.
2. Request API key for each project that follows the supported naming scheme.
  Within a project, API key may be requested and retrieved as follows: `Left Menu Bar > Applications > API`
  Note: A separate IT request will need to be submitted for each project.
3. Setup your local PRESIDIO REDCap Config (on the machine where this tool will be used).
  a. Copy the `./assets/presidio_redcap.json` file to a local, private directory of your choice.
    Mac/Linux users may consider the `~/.config/` directory.
  b. In the JSON file:
      i. Add the PRESIDIO subject ID (e.g. PR01) to the `NAME` field.
      ii. Add each API key string copied from REDCap in the comma-separated `API_KEYS` list.
      iii. Create a separate nested entry for each subject ID within this file.
  c. Set the environment variable `PRESIDIO_REDCAP` to the path of the JSON file.
    ```
    export PRESIDIO_REDCAP="$HOME/.config/presidio_redcap.json"
    ```
    Consider adding the above line to your `~/.bashrc` file.
4. Install the package into your Python environment.
  ```
  pip install git+ssh://git@github.com/ucsf-npnm/presidio-redcap.git
  ```

## Usage
```
from presidio_redcap.database import RedcapDB
rcdb = RedcapDB()
print(rcdb.projects)  # display subject IDs and associated projects

df_survey = rcdb.agg_subject('PR01')  # data concatenated across all projects
df_meta = rcdb.agg_field_meta('PR01') # field metadata across all projects
```
