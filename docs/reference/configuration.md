# Configuration

The Sonetel SDK provides configuration options to customize its behavior, including HTTP connection settings, retry behavior, and logging.

## Configure Function

The `configure()` function allows you to customize the SDK's behavior:

```python
import sonetel

sonetel.configure(
    timeout=(3.05, 60),
    max_retries=3,
    backoff_factor=0.3,
    pool_connections=10,
    pool_maxsize=10,
    log_level="INFO"
)
```

### Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `timeout` | `float` or `tuple(float, float)` | `(3.05, 60)` | Request timeout in seconds. Can be a single float or a tuple of (connect_timeout, read_timeout) |
| `max_retries` | `int` | `3` | Maximum number of retries for failed requests |
| `backoff_factor` | `float` | `0.3` | Backoff factor for retries (exponential backoff) |
| `pool_connections` | `int` | `10` | Number of connection pools to cache |
| `pool_maxsize` | `int` | `10` | Maximum number of connections to save in the pool |
| `log_level` | `str` | `None` | Logging level (DEBUG, INFO, WARNING, ERROR) |

## Session Management

The SDK uses connection pooling to improve performance by reusing HTTP connections. This reduces the overhead of establishing new connections for each request.

### Benefits

- **Reduced Latency**: Reusing connections eliminates the need for TCP handshakes and TLS negotiations for each request
- **Improved Throughput**: Connection pooling allows for more efficient use of resources
- **Automatic Retries**: Failed requests are automatically retried with exponential backoff
- **Resource Cleanup**: Connections are properly closed when your program exits

### Retry Behavior

The SDK automatically retries failed requests with the following characteristics:

- Retries are performed for server errors (HTTP 500, 502, 503, 504)
- Exponential backoff is used to avoid overwhelming the server
- The backoff formula is: `{backoff factor} * (2 ** ({number of total retries} - 1))`
- With the default backoff factor of 0.3, the retry delays would be:
  - 1st retry: 0.3s
  - 2nd retry: 0.6s
  - 3rd retry: 1.2s

## Logging

The SDK uses Python's standard logging module. You can configure the log level using the `log_level` parameter in the `configure()` function.

```python
import sonetel

# Enable debug logging
sonetel.configure(log_level="DEBUG")
```

You can also configure logging manually:

```python
import logging

# Configure the root logger
logging.basicConfig(level=logging.INFO)

# Or configure just the sonetel logger
logging.getLogger('sonetel').setLevel(logging.DEBUG)
```

## Example Usage

```python
import sonetel
import logging

# Configure the SDK with custom settings
sonetel.configure(
    timeout=(5, 60),
    max_retries=5,
    backoff_factor=0.5,
    pool_connections=20,
    pool_maxsize=20,
    log_level="DEBUG"
)

# Then use the SDK as normal
user = os.environ.get('sonetelUsername')
pswd = os.environ.get('sonetelPassword')
auth = sonetel.Auth(username=user, password=pswd)
