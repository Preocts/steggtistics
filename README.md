[![Code style:
black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/pre-commit/pre-commit)
[![pre-commit.ci
status](https://results.pre-commit.ci/badge/github/Preocts/steggtistics/main.svg)](https://results.pre-commit.ci/latest/github/Preocts/steggtistics/main)
[![Python
package](https://github.com/Preocts/steggtistics/actions/workflows/python-tests.yml/badge.svg?branch=main)](https://github.com/Preocts/steggtistics/actions/workflows/python-tests.yml)

# st**egg**tistics

Pull from the `{user}/events` public API of GitHub.

### Requirements

- [Python](https://python.org) >= 3.8

## Internal Links

- [Development Installation Guide](docs/development.md)


---

WIP - output to be parsed for metrics

```py
import json
from pathlib import Path
from datetime import datetime

from steggtistics.pull_user import PullUser

save_file = Path(f"temp_{datetime.now().strftime('%Y.%m.%d')}_events.json")

results = PullUser().pull_events("[USERNAME]")

json.dump([r.asdict() for r in results], save_file.open("w"), indent=4)
```
