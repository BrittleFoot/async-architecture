# Schema Registry for Popug Jira



## Installation

### Dev

```bash
pip install -e .
```

### Prod
```bash
pip install .
```

## Usage

### Add new schema

#### Example 1: Add new event schema

Lets assume we want to add new event schema for `user_quacked` event.

```python
# Create new pydantic model in jirapogug.schema.account.v1

class UserQucacked(V1Base):
    __event_name__ = 'user.quacked'

    loud: bool
```

Add new schema to `jirapopug.schema.json`

```python

from jirapopug.schema import account

DataType = [
    ...,
    account.v1.UserQucacked,
]
```

#### Example 2: Add new schema version

Lets assume we want to add new version for `user.quacked` event.

```python
# Create new pydantic model in jirapogug.schema.account.v2

class UserQucacked(V2Base):
    __event_name__ = 'user.quacked'

    loud: float # now we want to store loudness as float instead of bool

```

Add new schema to `jirapopug.schema.json`

```python

from jirapopug.schema import account

DataType = [
    ...,
    account.v2.UserQucacked,
]
```
