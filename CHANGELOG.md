## 0.1.0 (2022-04-28)

### Fix

- ensure that nanmax ignores nans over max

### Feat

- define survey items, collections, and templates for Presidio surveys
- created class to extract project records and construct dataframe from RedCap interface
- add method for indexing and retrieving subjects from RedcapSecrets

## 0.0.1 (2022-04-17)

### Fix

- reset version and create initial tag to facilitate cz bump

## 0.0.0 (2022-04-17)

### Fix

- **pyproject.toml**: typo reference to src project
- cz version_files was incorrectly defined

### Feat

- class RedcapSecrets to parse user-specific JSON configuration
- **py.typed**: added typed annotations for the project
- enforce commitizen commits

### Perf

- enable dataclass decorator to impose json structure
