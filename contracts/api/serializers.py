from rest_flex_fields import FlexFieldsModelSerializer

from contracts.models import Contract, ContractRequest, SoloContract


class ContractSerializer(FlexFieldsModelSerializer):

    class Meta:
        model = Contract
        exclude = ()
        read_only_fields = ('id', 'agency', 'create_at', 'update_at')
        expandable_fields = {
            'agency': ('agencies.api.serializers.AgencySerializer', {'many': False, 'read_only': True}),
            'requests': ('contracts.api.serializers.ContractRequestSerializer', {'many': True, 'read_only': True}),
        }


class ContractRequestSerializer(FlexFieldsModelSerializer):

    class Meta:
        model = ContractRequest
        exclude = ()
        read_only_fields = ('id', 'profile', 'contract', 'create_at', 'update_at')
        expandable_fields = {
            'profile': ('profiles.api.serializers.ProfileSerializer', {'many': False, 'read_only': True}),
            'contract': ('contracts.api.serializers.ContractSerializer', {'many': False, 'read_only': True}),
        }


class ProfileContractRequestSerializer(ContractRequestSerializer):

    class Meta(ContractRequestSerializer.Meta):
        read_only_fields = (
            *ContractRequestSerializer.Meta.read_only_fields,
            'status', 'money_offer_currency', 'money_offer', 'director_notes'
        )


class AgencyContractRequestSerializer(ContractRequestSerializer):

    class Meta(ContractRequestSerializer.Meta):
        read_only_fields = (
            *ContractRequestSerializer.Meta.read_only_fields,
            'model_notes'
        )


class SoloContractSerializer(FlexFieldsModelSerializer):

    class Meta:
        model = SoloContract
        exclude = ()
        read_only_fields = ('id', 'profile', 'agency', 'create_at', 'update_at')
        expandable_fields = {
                'profile': ('profiles.api.serializers.ProfileSerializer', {'many': False, 'read_only': True}),
                'agency': ('agencies.api.serializers.AgencySerializer', {'many': False, 'read_only': True}),
        }


class ProfileSoloContractSerializer(SoloContractSerializer):

    class Meta(SoloContractSerializer.Meta):
        read_only_fields = (
            *SoloContractSerializer.Meta.read_only_fields,
            'industry', 'title', 'description', 'guidelines', 'restrictions', 'money_offer_currency', 'money_offer',
            'start_at', 'require_travel_inboard', 'require_travel_outboard', 'num_of_days', 'city', 'country',
            'address',  'status'
        )


class AgencySoloContractSerializer(SoloContractSerializer):

    class Meta(SoloContractSerializer.Meta):
        read_only_fields = (
            *SoloContractSerializer.Meta.read_only_fields,
            'model_notes'
        )
