import json
class BodyResponse:
    def __init__(self):
        self.categories = self.get_categories()

    def get_categories(self):
        return {
            "data": {
                "Networking": [
                    {
                        "actionName": "AZURECreateLandingZoneArguments",
                        "category": "Networking"
                    },
                    {
                        "actionName": "AWSTemplateVpcProdArguments",
                        "category": "Networking"
                    },
                    {
                        "actionName": "GCPCreateNetworkFullArguments",
                        "category": "Networking"
                    },
                    {
                        "actionName": "AZURECreateVnetNonProdArguments",
                        "category": "Networking"
                    },
                    {
                        "actionName": "AWSTemplateVpcNonProd",
                        "category": "Networking"
                    },
                    {
                        "actionName": "AZURECreateVnetProdArguments",
                        "category": "Networking"
                    }
                ],
                "Load Balancing": [
                    {
                        "actionName": "AWSCreateLoadBalancerFullArgumentsV2",
                        "category": "Load Balancing"
                    },
                    {
                        "actionName": "AZURECreateAppGatewayArguments",
                        "category": "Load Balancing"
                    }
                ],
                "Compute": [
                    {
                        "actionName": "AZURECreateVMArguments",
                        "category": "Compute"
                    },
                    {
                        "actionName": "AWSTemplateEc2InstanceProdArguments",
                        "category": "Compute"
                    }
                ],
                "Containers": [
                    {
                        "actionName": "AWSK8SClusterFullArguments",
                        "category": "Containers"
                    },
                    {
                        "actionName": "AksCreateNonManagedClusterArguments",
                        "category": "Containers"
                    },
                    {
                        "actionName": "AksCreateManagedClusterArguments",
                        "category": "Containers"
                    },
                    {
                        "actionName": "AWSK8SNginxServiceFullArguments",
                        "category": "Containers"
                    }
                ],
                "DataBase": [
                    {
                        "actionName": "",
                        "category": "DataBase"
                    },
                    {
                        "actionName": "",
                        "category": "DataBase"
                    }
                ]
            }
        }
