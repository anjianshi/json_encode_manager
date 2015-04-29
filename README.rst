JSON encode manager
===================

Python's default json encoder was difficult to extend.
Use this, you can simply register custom encoder, to handle the data types
that default json encoder can't encode.

Usage：

.. code-block:: python

    json_encode_manager = JSONEncodeManager()
    json_encode_manager.register(some_encoder, some_python_type)
    ...
    json.dumps(data, default=json_encode_manager)

For JSONEncodeManager, there are two kinds of `encoder`:
- The first one was `specialized`.
    It can only encode object instance of one specific type or it's subtype.
    The manager will call it only if the type of data matches its register type.

- The other one was `generalized`, called `common_encoder`.
    A common_encoder can encode multiple types of data (eg. tuple and list).

    JSONEncodeManager will pass any type of data to these encoder.
    The encoder should raise a `CantEncodeObjException` exception, if it think this value shouldn't handle by itself.
    System will catch this exception, and pass data to next encoder.

`specialized` encoder has higher priority than `common_encoder`.

System has already define some encoders, in `_predefined_json_encoders` and `_predefined_common_json_encoders`
These encoders will be registered automatically, and has lowest priority of it's kind.
