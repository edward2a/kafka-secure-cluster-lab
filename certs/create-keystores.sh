#!/bin/bash

# TODO: Migrate to use PKCS12 (.p12) key stores as recommended by keytool

# Gotta love java...

if ! which keytool &>/dev/null; then
    echo "ERROR: keytool is not present."
    exit 1
fi

if [ ! -d stores ]; then
    mkdir stores
fi

if [ -z "${ENV}" ]; then
    read -t 120 -p "\n\tEnvironment name?: " ENV
fi

# TODO: Use external password source
STORE_PASS="${STORE_PASS:-sooThai+taeXo2Eosiege3yu}"

# Create trustore for CA
[ ! -f stores/truststore.p12 ] || rm -f stores/truststore.p12
openssl pkcs12 -export -nokeys -in certs/${ENV}/ca/ca-cert.pem -out stores/truststore.p12 -name "${ENV}.rrm.local-ca" -password pass:"${STORE_PASS}"

[ ! -f stores/truststore.jks ] || rm -f stores/truststore.jks
keytool -importcert -alias kds-ca -file certs/${ENV}/ca/ca-cert.pem -trustcacerts -noprompt -keystore stores/truststore.jks -storepass "${STORE_PASS}"


# Create server key store
[ ! -f stores/keystore-server.p12 ] || rm -f stores/keystore-server.p12
openssl pkcs12 -export -in certs/${ENV}/server-cert.pem -inkey certs/${ENV}/server-key.pem -out stores/keystore-server.p12 -name "*.kds.${ENV}.rrm.local" -password pass:"${STORE_PASS}"

[ ! -f stores/keystore-server.jks ] || rm -f stores/keystore-server.jks
keytool -importkeystore -destkeystore stores/keystore-server.jks -srckeystore stores/keystore-server.p12 -deststorepass "${STORE_PASS}" -srcstorepass "${STORE_PASS}" -srcalias "*.kds.${ENV}.rrm.local" -destalias "*.kds.${ENV}.rrm.local"
