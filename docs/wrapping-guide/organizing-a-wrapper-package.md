# Organizing a wrapper package

A wrapper package keeps public Python types separate from the code that reads
and writes generated protobuf messages. Callers can import and type-check the
wrapper types without depending on generated bindings. The conversion functions
know which protobuf API version they support.

## Put types and converters in separate layers

Give each group of wrapper types a public package. Put its conversion functions
in a versioned `proto/<namespace>/` subpackage. Public type modules must not
import generated protobuf modules. Only conversion modules may import them.

```text
<domain>/
├── __init__.py             # public re-exports and sorted __all__
├── _<thing>.py             # public type in a private implementation module
└── proto/
    └── v1alpha8/
        ├── __init__.py     # public converter re-exports and sorted __all__
        └── _<thing>.py     # generated-message conversion implementation
```

Use a sibling directory such as `proto/v1alpha8/` for each protobuf API version.
When support for a new version is needed, add another sibling directory. Do not
change the existing one. This lets one set of public wrapper types support
several protobuf API versions without exposing generated types.

## Make the package initializer the public surface

Put public types in underscore-prefixed implementation modules and re-export
them from the package initializer. Define an alphabetically sorted `__all__` in
that initializer. This gives callers stable, easy-to-find imports without
making implementation-module paths public. Follow the same rule in each
versioned conversion package.

Internal modules use relative imports from the module that defines a symbol.
Callers import only package-level names, such as
[`Metric`][frequenz.client.common.metrics.Metric], not an underscore module.
This avoids import cycles and makes the supported API clear.

## Name conversion functions by direction and protobuf API version

Name a conversion function `<thing>_from_proto` or `<thing>_to_proto`. Export
it from the matching `proto/<namespace>/` package. The import path, not the
function name, shows which protobuf API version it supports. A `*_from_proto`
function returns a public wrapper type. It can return a documented invalid
wrapper when it must retain malformed protobuf data.

## Preserve semantics in field names and docstrings

Match wrapper field names to protobuf field names by default. Diverge only when
a clear Pythonic improvement preserves or clarifies the field's meaning. Keep
the `_id` suffix for identifiers, even when you drop a redundant entity prefix.
For example, `source_electrical_component_id` can become `source_id`. Use
`_time` for protobuf `_time` and `_timestamp` fields, so names such as
`create_time` stay clear.

In a type whose name ends in `Value`, you may drop a redundant `_value` suffix
if the remaining name stays clear. Docstrings may be shorter or more Pythonic
than generated comments. They must not narrow, broaden, contradict, or change
the meaning of the protobuf field.
