# Reading string output

Wrapper objects have compact string representations for logs and debugging.
Read an `<invalid:…>` marker as an invariant violation: the object preserves
malformed data, but that field is not valid.

```python
from frequenz.client.common.metrics import InvalidBounds
from frequenz.client.common.types import InvalidLatitude

latitude = InvalidLatitude(value=999.0)
bounds = InvalidBounds(lower=10, upper=5)

print(latitude)  # <invalid:999.00>
print(bounds)  # <invalid:[10,5]>
```

[`InvalidLatitude`][frequenz.client.common.types.InvalidLatitude] keeps an
out-of-range latitude, while
[`InvalidBounds`][frequenz.client.common.metrics.InvalidBounds] keeps a
malformed pair of bounds. [`InvalidLongitude`][frequenz.client.common.types.InvalidLongitude]
and [`InvalidCountryCode`][frequenz.client.common.types.InvalidCountryCode]
use the same marker. See [validity in the type](validity-in-the-type.md) to
handle these values.

An unexpected raw number without `<invalid:…>` means something different: the
data is well-formed, but this client version does not recognize it yet. For
example, [`UnrecognizedElectricalComponent`][frequenz.client.common.microgrid.electrical_components.UnrecognizedElectricalComponent]
prints a suffix shaped like `:category=<int>`, and
[`UnrecognizedBattery`][frequenz.client.common.microgrid.electrical_components.UnrecognizedBattery]
prints `:type=<int>`. Those plain values are forward-compatible unknown data,
not invalid data. See [enum-or-int fields](enum-or-int-fields.md) for handling
that case.

Use these strings for human inspection and logging, not programmatic parsing.
Use the typed fields and accessors for application logic instead.
