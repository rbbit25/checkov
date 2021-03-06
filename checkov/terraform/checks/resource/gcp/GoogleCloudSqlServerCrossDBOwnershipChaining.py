from checkov.common.models.enums import CheckResult, CheckCategories
from checkov.terraform.checks.resource.base_resource_check import BaseResourceCheck


class GoogleCloudSqlServerCrossDBOwnershipChaining(BaseResourceCheck):
    def __init__(self):
        name = "Ensure SQL database 'cross db ownership chaining' flag is set to 'off'"
        check_id = "CKV_GCP_58"
        supported_resources = ['google_sql_database_instance']
        categories = [CheckCategories.GENERAL_SECURITY]
        super().__init__(name=name, id=check_id, categories=categories, supported_resources=supported_resources)

    def scan_resource_conf(self, conf):
        """
            Looks for google_sql_database_instance which prevents cross ownerships on SQL DBs::
            :param
            conf: google_sql_database_instance
            configuration
            :return: < CheckResult >
        """
        if 'database_version' in conf.keys():
            key = conf['database_version'][0]
            if 'SQLSERVER' in key:
                if 'settings' in conf.keys():
                    for attribute in conf['settings'][0]:
                        if attribute == 'database_flags':
                            for flag in conf['settings'][0]['database_flags']:
                                if (flag['name'][0] == 'cross db ownership chaining') and (flag['value'][0] == 'on'):
                                    return CheckResult.FAILED
        return CheckResult.PASSED


check = GoogleCloudSqlServerCrossDBOwnershipChaining()
