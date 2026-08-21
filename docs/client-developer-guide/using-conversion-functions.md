# Using conversion functions

Your client library calls a gRPC service and gets back low-level protobuf
messages. The conversion functions this library provides translate those into
the high-level Python wrappers, so the rest of your code — and your users —
work with wrappers instead of protobuf.

## Convert a single message

```python
response = await self._stub.GetMetricSample(request)
return metric_sample_from_proto(response.metric_sample)
```

## Convert a list of messages

```python
response = await self._stub.ListMetricSamples(request)
return [metric_sample_from_proto(s) for s in response.samples]
```

## You don't handle unknown or invalid values here

The conversion function already deals with them: it keeps an enum value your
version doesn't recognize as a plain `int`, and returns an `Invalid*` wrapper
instead of raising when data is malformed. You just return the wrapper.
Deciding what those cases *mean* is up to your users — see the [User Guide](../user-guide/index.md).
