from __future__ import annotations

from rest_framework import serializers

from apps.operations.models import CsvOperationJob


class FilterValueField(serializers.Field):
    def to_internal_value(self, data):
        if isinstance(data, (dict, list)):
            raise serializers.ValidationError(
                "Filter value must be a string, number, or boolean."
            )
        return data

    def to_representation(self, value):
        return value


class FilterConditionSerializer(serializers.Serializer):
    field = serializers.CharField(max_length=255, allow_blank=False)
    operator = serializers.ChoiceField(
        choices=(
            "eq",
            "neq",
            "contains",
            "gt",
            "gte",
            "lt",
            "lte",
        )
    )
    value = FilterValueField()


class PerformOperationRequestSerializer(serializers.Serializer):
    file_id = serializers.IntegerField(min_value=1)
    operation = serializers.ChoiceField(choices=CsvOperationJob.Operation.choices)
    column = serializers.CharField(required=False, allow_blank=False)
    filters = FilterConditionSerializer(many=True, required=False)

    def validate(self, attrs):
        operation = attrs["operation"]
        column = attrs.get("column")
        filters = attrs.get("filters")

        if operation == CsvOperationJob.Operation.UNIQUE and not column:
            raise serializers.ValidationError(
                {"column": "This field is required for unique operation."}
            )

        if operation == CsvOperationJob.Operation.FILTER:
            raw_filters = self.initial_data.get("filters", None)
            if raw_filters is None or (
                isinstance(raw_filters, list) and len(raw_filters) == 0
            ):
                raise serializers.ValidationError(
                    {"filters": "This field is required for filter operation."}
                )

            # Preserve nested validation errors when `filters` is provided but invalid.
            if filters is None:
                return attrs

        return attrs


class TaskStatusQuerySerializer(serializers.Serializer):
    task_id = serializers.CharField(max_length=255, allow_blank=False)
    n = serializers.IntegerField(
        required=False, min_value=1, max_value=1000, default=100
    )


class OperationTaskPathSerializer(serializers.Serializer):
    task_id = serializers.CharField(max_length=255, allow_blank=False)
