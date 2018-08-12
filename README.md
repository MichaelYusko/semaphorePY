# SemaphoreCI Python client


[![Build Status](https://semaphoreci.com/api/v1/michaelyusko/semaphorepy/branches/develop/badge.svg)](https://semaphoreci.com/michaelyusko/semaphorepy)


A python3.6+ wrapper for fast and easy SemaphoreCI API

### Version
```
0.1.4
```

### Installation
```
pip install semaphorePY
```

### Guide
```
# Create a instance of Semaphore client
from semaphore.client import Semaphore
semaphore = Semaphore('YOUR-AUTH-TOKEN-HERE')

# Returns all available an organizations
# For more details see, all available resources
semaphore.organization.list()
```

### All available resources
   * Organization
   * Configuration file
   * Secrets
   * Teams
   * Projects
   * Users
