## Introdução
Os ficheiros que se encontra nesta pasta, devem ser aplicados de modo a garantir, a comunicação com o CA.

### Estrutura

* [pki](./PKI/pki.py): Neste ficheiro é estabelecido a comunicação com CA, e permite assinar o pedido de assinatura certificado.
* [config](./PKI/config.py): Neste ficheiro encontram-se as configurações necessárias para ser estabelecida a comunicação com o CA (ex:. host, portas)
* [ca](./PKI/ca.py): Neste ficheiro é dependências encontram-se as depedências necessárias para o funcionamento do ficheiro [pki](./PKI/pki.py)
* [requirements](./PKI/ca.py): Ficheiro com as depedências necessárias para intalar o pki.

### Comandos

Comando para instalar as dependências do Python necessárias:

```
pip3 install -r requirements.txt
```

