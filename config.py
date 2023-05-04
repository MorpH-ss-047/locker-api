SCOPES = ["https://www.googleapis.com/auth/androidmanagement"]
SERVICE_ACCOUNT_FILE = "json/refab-emi-locker-5d6e113c8448.json"
ENTERPRISE_NAME = "enterprises/LC02ws5cs6"
BASE_POLICY_NAME = ENTERPRISE_NAME + "/policies/"


POLICY_JSON = """
{
  "applications": [
    {
      "packageName": "com.apptimates.apptimatelocker",
      "installType": "REQUIRED_FOR_SETUP",
      "delegatedScopes": [
          "MANAGED_CONFIGURATIONS",
          "BLOCK_UNINSTALL",
          "PERMISSION_GRANT",
          "PACKAGE_ACCESS",
          "ENABLE_SYSTEM_APP",
          "NETWORK_ACTIVITY_LOGS",
          "SECURITY_LOGS"
        ],
      "defaultPermissionPolicy": "GRANT",
      "permissionGrants": [
        {
          "permission": "android.Manifest.permission.READ_PRIVILEGED_PHONE_STATE",
          "policy": "GRANT"
        },
        {
          "permission":  "android.Manifest.permission.ACCESS_FINE_LOCATION",
          "policy": "GRANT"
        },
        {
          "permission":  "android.Manifest.permission.ACCESS_COARSE_LOCATION",
          "policy": "GRANT"
        },
        {
          "permission":  "android.Manifest.permission.READ_PHONE_STATE",
          "policy": "GRANT"
        },
        {
          "permission":  "android.Manifest.permission.CALL_PHONE",
          "policy": "GRANT"
        }
      ],
      "autoUpdateMode": "AUTO_UPDATE_HIGH_PRIORITY"
    },
    {
      "packageName": "com.apptimates.noteefy",
      "installType": "PREINSTALLED"
    }
  ],
  "advancedSecurityOverrides": {
     "developerSettings": "DEVELOPER_SETTINGS_DISABLED"
  },
  "playStoreMode": "BLACKLIST",
  "factoryResetDisabled" : "true"
}
"""
