from __future__ import absolute_import
from flytekit.common.types import helpers as _type_helpers, base_sdk_types as _base_sdk_types
from flytekit.models import literals as _literals, types as _model_types
from flytekit.sdk import types as _sdk_types


def test_python_std_to_sdk_type():
    o = _type_helpers.python_std_to_sdk_type(_sdk_types.Types.Integer)
    assert o.to_flyte_literal_type().simple == _model_types.SimpleType.INTEGER

    o = _type_helpers.python_std_to_sdk_type([_sdk_types.Types.Boolean])
    assert o.to_flyte_literal_type().collection_type.simple == _model_types.SimpleType.BOOLEAN


def test_get_sdk_type_from_literal_type():
    o = _type_helpers.get_sdk_type_from_literal_type(_model_types.LiteralType(simple=_model_types.SimpleType.FLOAT))
    assert o == _sdk_types.Types.Float


def test_infer_sdk_type_from_literal():
    o = _type_helpers.infer_sdk_type_from_literal(
        _literals.Literal(scalar=_literals.Scalar(primitive=_literals.Primitive(string_value="abc")))
    )
    assert o == _sdk_types.Types.String

    o = _type_helpers.infer_sdk_type_from_literal(
        _literals.Literal(scalar=_literals.Scalar(none_type=_literals.Void()))
    )
    assert o is _base_sdk_types.Void


def test_get_sdk_value_from_literal():
    o = _type_helpers.get_sdk_value_from_literal(
        _literals.Literal(scalar=_literals.Scalar(none_type=_literals.Void()))
    )
    assert o.to_python_std() is None

    o = _type_helpers.get_sdk_value_from_literal(
        _literals.Literal(scalar=_literals.Scalar(none_type=_literals.Void())),
        sdk_type=_sdk_types.Types.Integer
    )
    assert o.to_python_std() is None

    o = _type_helpers.get_sdk_value_from_literal(
        _literals.Literal(scalar=_literals.Scalar(primitive=_literals.Primitive(integer=1))),
        sdk_type=_sdk_types.Types.Integer
    )
    assert o.to_python_std() == 1

    o = _type_helpers.get_sdk_value_from_literal(
        _literals.Literal(
            collection=_literals.LiteralCollection(
                [
                    _literals.Literal(scalar=_literals.Scalar(primitive=_literals.Primitive(integer=1))),
                    _literals.Literal(scalar=_literals.Scalar(none_type=_literals.Void())),
                ]
            )
        )
    )
    assert o.to_python_std() == [1, None]
