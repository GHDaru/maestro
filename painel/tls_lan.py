"""CA própria da LAN ("Maestro LAN CA") e certificado do servidor (spec 069, ADR-001).

    python painel/tls_lan.py painel/dados/tls --ip 192.168.15.12 --dns ola-webhook.ghdaru.com.br

Gera em <pasta>: ca.key e ca.crt (10 anos, reaproveitados se já existirem), servidor.key e
servidor.crt (1 ano, SAN de IP e DNS) e maestro-lan-ca.crt (cópia pública da CA, para o n8n).
As chaves privadas nunca saem da pasta, que está no .gitignore.
"""
from __future__ import annotations

import argparse
import datetime as dt
import ipaddress
import os
import shutil

from cryptography import x509
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.x509.oid import ExtendedKeyUsageOID, NameOID


def _grava_chave(caminho, chave):
    with open(caminho, "wb") as f:
        f.write(chave.private_bytes(serialization.Encoding.PEM, serialization.PrivateFormat.PKCS8,
                                    serialization.NoEncryption()))


def _grava_cert(caminho, cert):
    with open(caminho, "wb") as f:
        f.write(cert.public_bytes(serialization.Encoding.PEM))


def gera(pasta: str, ips: list[str], dns: list[str], dias_servidor: int = 365) -> dict:
    os.makedirs(pasta, exist_ok=True)
    agora = dt.datetime.now(dt.timezone.utc)
    ca_key_p, ca_crt_p = os.path.join(pasta, "ca.key"), os.path.join(pasta, "ca.crt")
    if os.path.exists(ca_key_p) and os.path.exists(ca_crt_p):
        ca_key = serialization.load_pem_private_key(open(ca_key_p, "rb").read(), None)
        ca_crt = x509.load_pem_x509_certificate(open(ca_crt_p, "rb").read())
    else:
        ca_key = ec.generate_private_key(ec.SECP256R1())
        nome = x509.Name([x509.NameAttribute(NameOID.COMMON_NAME, "Maestro LAN CA"),
                          x509.NameAttribute(NameOID.ORGANIZATION_NAME, "Hindiana / Maestro")])
        ca_crt = (x509.CertificateBuilder().subject_name(nome).issuer_name(nome).public_key(ca_key.public_key())
                  .serial_number(x509.random_serial_number()).not_valid_before(agora - dt.timedelta(minutes=5))
                  .not_valid_after(agora + dt.timedelta(days=3650))
                  .add_extension(x509.BasicConstraints(ca=True, path_length=0), critical=True)
                  .add_extension(x509.KeyUsage(digital_signature=True, key_cert_sign=True, crl_sign=True, content_commitment=False,
                                               key_encipherment=False, data_encipherment=False, key_agreement=False,
                                               encipher_only=False, decipher_only=False), critical=True)
                  .add_extension(x509.SubjectKeyIdentifier.from_public_key(ca_key.public_key()), critical=False)
                  .sign(ca_key, hashes.SHA256()))
        _grava_chave(ca_key_p, ca_key)
        _grava_cert(ca_crt_p, ca_crt)
    srv_key = ec.generate_private_key(ec.SECP256R1())
    san = [x509.IPAddress(ipaddress.ip_address(i)) for i in ips] + [x509.DNSName(d) for d in dns]
    cn = dns[0] if dns else ips[0]
    srv_crt = (x509.CertificateBuilder().subject_name(x509.Name([x509.NameAttribute(NameOID.COMMON_NAME, cn)]))
               .issuer_name(ca_crt.subject).public_key(srv_key.public_key()).serial_number(x509.random_serial_number())
               .not_valid_before(agora - dt.timedelta(minutes=5)).not_valid_after(agora + dt.timedelta(days=dias_servidor))
               .add_extension(x509.SubjectAlternativeName(san), critical=False)
               .add_extension(x509.BasicConstraints(ca=False, path_length=None), critical=True)
               .add_extension(x509.ExtendedKeyUsage([ExtendedKeyUsageOID.SERVER_AUTH]), critical=False)
               .add_extension(x509.AuthorityKeyIdentifier.from_issuer_public_key(ca_key.public_key()), critical=False)
               .sign(ca_key, hashes.SHA256()))
    _grava_chave(os.path.join(pasta, "servidor.key"), srv_key)
    _grava_cert(os.path.join(pasta, "servidor.crt"), srv_crt)
    shutil.copyfile(ca_crt_p, os.path.join(pasta, "maestro-lan-ca.crt"))
    return {"ca": ca_crt_p, "servidor": os.path.join(pasta, "servidor.crt"),
            "validade_servidor": srv_crt.not_valid_after_utc.isoformat(), "san": ips + dns}


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("pasta")
    ap.add_argument("--ip", action="append", default=[])
    ap.add_argument("--dns", action="append", default=[])
    a = ap.parse_args()
    r = gera(a.pasta, a.ip, a.dns)
    print(f"certificado do servidor válido até {r['validade_servidor'][:10]}, SAN {', '.join(r['san'])}")
    print(f"CA pública para o n8n: {os.path.join(a.pasta, 'maestro-lan-ca.crt')}")
