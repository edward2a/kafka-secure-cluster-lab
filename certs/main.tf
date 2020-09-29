locals {
  o               = "Real ReadMe Ltd."
  ou              = "ITS"
  city            = "London"
  province        = "Essex"
  country         = "GB"
  dns_parent_zone = "rrm.local"
}


module "kds_ca" {
  source = "github.com/edward2a/tf-module-tls-certificate?ref=v0.1.0"

  type                  = "SELF_SIGNED"
  algorithm             = "ECDSA"
  ecdsa_curve           = "P384"
  is_ca_certificate     = true
  validity_period_hours = 87600

  common_name         = "rrm-kdsf-ca"
  organization        = local.o
  organizational_unit = local.ou
  locality            = local.city
  province            = local.province
  country             = local.country
  allowed_uses = [
    "any_extended",
    "digital_signature",
    "key_encipherment",
    "data_encipherment",
    "cert_signing",
    "crl_signing",
    "ocsp_signing",
    "server_auth"
  ]
}

module "kds" {
  source = "github.com/edward2a/tf-module-tls-certificate?ref=v0.1.0"

  ca_private_key_pem = module.kds_ca.private_key_pem
  ca_cert_pem        = module.kds_ca.cert_pem
  allowed_uses = [
    "server_auth"
  ]

  type             = "LOCAL"
  algorithm        = "ECDSA"
  ecdsa_curve      = "P384"
  ca_key_algorithm = "ECDSA"

  common_name         = "*.kds.${var.env}.${local.dns_parent_zone}"
  organization        = local.o
  organizational_unit = local.ou
  locality            = local.city
  province            = local.province
  country             = local.country
  dns_names = [
    "*.kds.${var.env}.${local.dns_parent_zone}",
  ]
}
