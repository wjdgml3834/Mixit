resource "azurerm_resource_group" "example" {
  name     = "mixit-740144f4"
  location = "westeurope"
}

resource "azurerm_service_plan" "example" {
  name                = "app-serviceplan-mixit"
  resource_group_name = azurerm_resource_group.example.name
  location            = azurerm_resource_group.example.location
  os_type             = "Linux"
  sku_name            = "S1"
}

resource "azurerm_linux_web_app" "example" {
  name                = "website-740144f4"
  resource_group_name = azurerm_resource_group.example.name
  location            = azurerm_service_plan.example.location
  service_plan_id     = azurerm_service_plan.example.id
  https_only          = true

  site_config { 
    application_stack {
      python_version = "3.11"
    }
  }
  app_settings = {
    "SCM_DO_BUILD_DURING_DEPLOYMENT" = true
    "ApotheekApiUrl" = format("%s%s",azurerm_linux_web_app.ApotheekApi.name,".azurewebsites.net")
    "PatientApiUrl" = format("%s%s",azurerm_linux_web_app.PatientApi.name,".azurewebsites.net")
  }
}

resource "azurerm_linux_web_app" "ApotheekApi" {
  name                = "ApotheekApi-840144f4"
  resource_group_name = azurerm_resource_group.example.name
  location            = azurerm_service_plan.example.location
  service_plan_id     = azurerm_service_plan.example.id
  https_only          = true

  site_config { 
    app_command_line = "gunicorn -w 2 -k uvicorn.workers.UvicornWorker main:app"
    application_stack {
      python_version = "3.11"
    }
  }
  app_settings = {
    "SCM_DO_BUILD_DURING_DEPLOYMENT" = true
    "WEBSITE_WEBDEPLOY_USE_SCM" = true
    "ApotheekApiDatabaseName" = azurerm_key_vault_secret.ApotheekApiDatabaseName.value
    "ApotheekApiDatabaseUsername" = azurerm_key_vault_secret.ApotheekApiDatabaseUsername.value
    "ApotheekApiDatabasePassword" = azurerm_key_vault_secret.ApotheekApiDatabaseName.value
    # "WEBSITE_RUN_FROM_PACKAGE"= 1
  }
}

resource "azurerm_linux_web_app" "PatientApi" {
  name                = "PatientApi-940144f4"
  resource_group_name = azurerm_resource_group.example.name
  location            = azurerm_service_plan.example.location
  service_plan_id     = azurerm_service_plan.example.id
  https_only          = true

  site_config { 
    app_command_line = "gunicorn -w 2 -k uvicorn.workers.UvicornWorker main:app"
    application_stack {
      python_version = "3.11"
    }
  }
  app_settings = {
    "SCM_DO_BUILD_DURING_DEPLOYMENT" = true
    "WEBSITE_WEBDEPLOY_USE_SCM" = true
    "PatientApiDatabaseName" = azurerm_key_vault_secret.PatientApiDatabaseName.value
    "PatientApiDatabaseUsername" = azurerm_key_vault_secret.PatientApiDatabaseUsername.value
    "PatientApiDatabasePassword" = azurerm_key_vault_secret.PatientApiDatabasePassword.value
    # "WEBSITE_RUN_FROM_PACKAGE"= 1
  }
}

resource "random_password" "sql_admin_password" {
  length  = 20
  special = true
  min_numeric = 1
  min_upper   = 1
  min_lower   = 1
  min_special = 1
}

resource "azurerm_mssql_server" "PatientServer" {
  name                         = "patient-server"
  resource_group_name          = azurerm_resource_group.example.name
  location                     = azurerm_resource_group.example.location
  version                      = "12.0"
  administrator_login          = "sqladmin1"
  administrator_login_password = azurerm_key_vault_secret.DatabaseSqladminPW.value
}

resource "azurerm_mssql_database" "PatientDatabase" {
  name                = "Patient-db"
  server_id           = azurerm_mssql_server.PatientServer.id
}

resource "azurerm_mssql_server" "ApotheekServer" {
  name                         = "apotheek-server"
  resource_group_name          = azurerm_resource_group.example.name
  location                     = azurerm_resource_group.example.location
  version                      = "12.0"
  administrator_login          = "sqladmin2"
  administrator_login_password = azurerm_key_vault_secret.DatabaseSqladminPW.value
}

resource "azurerm_mssql_database" "ApotheekDatabase" {
  name                = "Apotheek-db"
  server_id           = azurerm_mssql_server.ApotheekServer.id
}

resource "random_pet" "rg_name" {
  prefix = var.resource_group_name_prefix
}

resource "azurerm_resource_group" "rg" {
  name     = var.resource_group_name_prefix
  location = var.resource_group_location
}

data "azurerm_client_config" "current" {}

resource "random_string" "azurerm_key_vault_name" {
  length  = 13
  lower   = true
  numeric = false
  special = false
  upper   = false
}

locals {
  current_user_id = coalesce(var.msi_id, data.azurerm_client_config.current.object_id)
}

resource "azurerm_key_vault" "vault" {
  name                       = local.generated_name
  resource_group_name        = azurerm_resource_group.example.name
  location                   = azurerm_resource_group.example.location
  tenant_id                  = data.azurerm_client_config.current.tenant_id
  sku_name                   = var.sku_name
  soft_delete_retention_days = 7

  access_policy {
    tenant_id = data.azurerm_client_config.current.tenant_id
    object_id = local.current_user_id

    key_permissions    = var.key_permissions
    secret_permissions = var.secret_permissions
  }
  depends_on = [
    azurerm_resource_group.example
  ]
}

resource "random_string" "azurerm_key_vault_key_name" {
  length  = 13
  lower   = true
  numeric = false
  special = false
  upper   = false
}

resource "azurerm_key_vault_key" "key" {
  name = coalesce(var.key_name, "key-${random_string.azurerm_key_vault_key_name.result}")

  key_vault_id = azurerm_key_vault.vault.id
  key_type     = var.key_type
  key_size     = var.key_size
  key_opts     = var.key_ops

  rotation_policy {
    automatic {
      time_before_expiry = "P30D"
    }

    expire_after         = "P90D"
    notify_before_expiry = "P29D"
  }
}
# Azure DB creds
resource "azurerm_key_vault_secret" "DatabaseSqladminPW" {
  name         = "DatabaseSqladminPW"
  value        = random_password.sql_admin_password.result
  key_vault_id = azurerm_key_vault.vault.id
  depends_on = [ azurerm_key_vault.vault ]
}

# API Db creds
resource "azurerm_key_vault_secret" "PatientApiDatabaseName" {
  name         = "PatientApiDatabaseName"
  value        = "zdoorenl2"
  key_vault_id = azurerm_key_vault.vault.id
  depends_on = [ azurerm_key_vault.vault ]
}
resource "azurerm_key_vault_secret" "PatientApiDatabaseUsername" {
  name         = "PatientApiDatabaseUsername"
  value        = "doorenl2"
  key_vault_id = azurerm_key_vault.vault.id
  depends_on = [ azurerm_key_vault.vault ]
}
resource "azurerm_key_vault_secret" "PatientApiDatabasePassword" {
  name         = "PatientApiDatabasePassword"
  value        = "aCieESt0cIy0paMb"
  key_vault_id = azurerm_key_vault.vault.id
  depends_on = [ azurerm_key_vault.vault ]
}
resource "azurerm_key_vault_secret" "ApotheekApiDatabaseName" {
  name         = "ApotheekApiDatabaseName"
  value        = "zhouwelj"
  key_vault_id = azurerm_key_vault.vault.id
  depends_on = [ azurerm_key_vault.vault ]
}
resource "azurerm_key_vault_secret" "ApotheekApiDatabaseUsername" {
  name         = "ApotheekApiDatabaseUsername"
  value        = "houwelj"
  key_vault_id = azurerm_key_vault.vault.id
  depends_on = [ azurerm_key_vault.vault ]
}
resource "azurerm_key_vault_secret" "ApotheekApiDatabasePassword" {
  name         = "ApotheekApiDatabasePassword"
  value        = "oiqie6c50T744G"
  key_vault_id = azurerm_key_vault.vault.id
  depends_on = [ azurerm_key_vault.vault ]
}