# Sonetel Python

`sonetel-python` is an open-source library for use with Sonetel's APIs.

It allows you to quickly integrate Sonetel's communication services such as international calls, SMS, voice apps, AI services and much more with projects of any scale.

## Get started

- If you don't have an account, sign up from [sonetel.com](https://app.sonetel.com/register?tag=api-developer&simple=true)
- Install the `sonetel` package using pip.

## Performance Features

The Sonetel SDK includes several performance optimizations:

- **HTTP Session Management**: Uses connection pooling to reduce latency and overhead
- **Automatic Retries**: Retries failed requests with exponential backoff
- **Configurable Settings**: Customize timeouts, retry behavior, and connection pooling
- **Resource Management**: Automatically cleans up resources when your program exits

## Configuration

You can configure the SDK's behavior using the `configure()` function:

```python
import sonetel

# Configure the SDK with custom settings
sonetel.configure(
    timeout=(5, 60),  # (connect_timeout, read_timeout) in seconds
    max_retries=5,    # Maximum number of retries for failed requests
    backoff_factor=0.5,  # Exponential backoff factor
    pool_connections=20,  # Number of connection pools
    pool_maxsize=20,      # Maximum connections per pool
    log_level="DEBUG"     # Logging level (DEBUG, INFO, WARNING, ERROR)
)
```

All parameters are optional and have sensible defaults.
