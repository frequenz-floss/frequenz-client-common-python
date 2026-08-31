# Typed IDs

Use typed IDs when you work with microgrids and their resources. Instead of
plain integers, the library gives you distinct types such as
[`MicrogridId`][frequenz.client.common.microgrid.MicrogridId],
[`ElectricalComponentId`][frequenz.client.common.microgrid.electrical_components.ElectricalComponentId],
[`SensorId`][frequenz.client.common.microgrid.sensors.SensorId], and
[`EnterpriseId`][frequenz.client.common.microgrid.EnterpriseId]. This makes an
ID self-describing when you print it and lets a type checker catch using a
sensor ID where a microgrid ID is expected.

```python
from frequenz.client.common.microgrid import MicrogridId
from frequenz.client.common.microgrid.sensors import SensorId

microgrid_id = MicrogridId(123)
same_microgrid_id = MicrogridId(123)
sensor_id = SensorId(123)

print(microgrid_id)  # MID123
print(microgrid_id == same_microgrid_id)  # True
print(microgrid_id == sensor_id)  # False

ids = {microgrid_id, same_microgrid_id, sensor_id}
print(len(ids))  # 2

names = {microgrid_id: "Rooftop microgrid"}
print(names[MicrogridId(123)])  # Rooftop microgrid
```

Construct an ID from its numeric value. IDs of the same type and value compare
equal, so you can use them as dictionary keys or set members. IDs with the
same number but different types are not equal.

The printed prefix identifies the kind of ID: `MID` for a microgrid, `CID` for
an electrical component, `SID` for a sensor, and `EID` for an enterprise. All
of these types are based on [`BaseId`][frequenz.core.id.BaseId].
