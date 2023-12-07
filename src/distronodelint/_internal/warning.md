# warning

`warning` is a special type of internal rule that is used to report generic
runtime warnings found during execution. As stated by its name, they are not
counted as errors, so they do not influence the final outcome.

- `warning[raw-non-string]` indicates that you are using
  `[raw](https://docs.distronode.com/distronode/latest/collections/distronode/builtin/raw_module.html#distronode-collections-distronode-builtin-raw-module)`
  module with non-string arguments, which is not supported by Distronode.
