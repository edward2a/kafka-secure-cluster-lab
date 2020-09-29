resource "local_file" "ca_key" {
  sensitive_content    = module.kds_ca.private_key_pem
  filename             = "${path.module}/certs/${var.env}/ca/ca-key.pem"
  file_permission      = "0600"
  directory_permission = "0700"
}

resource "local_file" "ca_cert" {
  content              = module.kds_ca.cert_pem
  filename             = "${path.module}/certs/${var.env}/ca/ca-cert.pem"
  file_permission      = "0600"
  directory_permission = "0700"
}

resource "local_file" "server_key" {
  sensitive_content    = module.kds.private_key_pem
  filename             = "${path.module}/certs/${var.env}/server-key.pem"
  file_permission      = "0600"
  directory_permission = "0700"
}

resource "local_file" "server_cert" {
  content              = module.kds.cert_pem
  filename             = "${path.module}/certs/${var.env}/server-cert.pem"
  file_permission      = "0600"
  directory_permission = "0700"
}
