
0.1a4 - 2012-09-05
------------------

- New method to make sure new objects aren't stored with the same name as an
  existing view. Before it was possible to name objects the same way as views. [robinharms]

0.1a3 - 2012-02-14
-------------------

- Typo on code caused description to be stored under the wrong attribute of
  the schema when using createSchema. [robinharms]

0.1a2 - 2012-02-14
------------------

- If title and descriptions are specified for the schema factory, also transfer
  them to the schema itself. (Colander Schemas are transfered to Schema nodes on
  construction, which enables title and description) [sassur]

0.1a1 - 2011-10-14
------------------

- Exception raised when custom accessors or mutators created a loop. [robinharms]
- Exposing field_storage as a public attribute should remove the need to
  the switch to override custom accessors / mutators. So it has been removed.
  Hopefully this will make it easier to use. [robinharms]

0.1a
----

- Initial version
