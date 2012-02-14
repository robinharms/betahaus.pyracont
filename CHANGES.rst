0.1a3
-----

- Typo on code caused description to be stored under the wrong attribute of
  the schema when using createSchema. [robinharms]

0.1a2
-----

- If title and descriptions are specified for the schema factory, also transfer
  them to the schema itself. (Colander Schemas are transfered to Schema nodes on
  construction, which enables title and description) [sassur]

0.1a1
-----

- Exception raised when custom accessors or mutators created a loop. [robinharms]
- Exposing field_storage as a public attribute should remove the need to
  the switch to override custom accessors / mutators. So it has been removed.
  Hopefully this will make it easier to use. [robinharms]

0.1a
----

- Initial version
