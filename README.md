# unifi-zabbix-multi-site-monitoring
Projeto Monitoramento dos Aps e Swichs Unifi no Zabbix 
# Zabbix UniFi Multi-Site Monitoring

Template e script para monitoramento de dispositivos UniFi (Access Points e Switches) em múltiplos sites através do Zabbix.

## Características

- Monitoramento de múltiplos sites UniFi
- Descoberta automática de dispositivos (APs e Switches)
- Métricas de disponibilidade por site
- Dashboard com visualização honeycomb
- Alertas configuráveis para dispositivos offline

## Dispositivos Suportados

- **Access Points (UAP)**: Todos os modelos UniFi
- **Switches (USW)**: Todos os modelos UniFi

## Métricas Coletadas

### Por Site:
- Total de dispositivos
- Dispositivos online/offline
- Percentual de disponibilidade
- Total de APs vs Switches

### Por Dispositivo:
- Status (Online/Offline)
- Endereço IP
- Modelo
- Versão do firmware
- Uptime
- Resumo formatado para dashboards

## Pré-requisitos

- Zabbix Server 6.0+
- Python 3.6+
- Biblioteca `requests` para Python
- Acesso ao UniFi Controller
- Usuário dedicado no UniFi Controller para monitoramento

## Instalação

### 1. Script Python

Copie o script para o diretório de scripts externos do Zabbix:

```bash
sudo cp zbx_unifi_ap_status.py /usr/lib/zabbix/externalscripts/
sudo chmod +x /usr/lib/zabbix/externalscripts/zbx_unifi_ap_status.py
sudo chown zabbix:zabbix /usr/lib/zabbix/externalscripts/zbx_unifi_ap_status.py
```

### 2. Dependências Python

```bash
pip3 install requests
```

### 3. Template Zabbix

1. No Zabbix Web Interface: **Configuration → Templates → Import**
2. Selecione o arquivo `template_unifi_multi_site.xml`
3. Marque "Update existing" se já existir
4. Clique em "Import"

## Configuração

### 1. UniFi Controller

Crie um usuário dedicado no UniFi Controller:
- Username: `zabbix`
- Password: `zabbix` (ou personalize no script)
- Role: Read-only Admin

### 2. Script Python

Edite as configurações no arquivo `zbx_unifi_ap_status.py`:

```python
# Configurações UniFi
UNIFI_HOST = "https://SEU_CONTROLLER_IP:8443"
USERNAME = "zabbix"
PASSWORD = "sua_senha"

# Mapeamento de sites
SITE_MAP = {
    "Default": "default",
    "Branch Office": "abc123def456",
    "Warehouse": "def456ghi789"
}
```

### 3. Hosts no Zabbix

Para cada site UniFi, crie um host:

```
Host name: UniFi-BranchOffice
Visible name: UniFi - Branch Office
Host groups: UniFi Sites
Templates: Template UniFi Multi-Site
Macros:
  {$UNIFI_SITE} = "Branch Office"
```

## Uso

### Dashboard

Crie widgets usando os itens Summary para visualização:

- **Widget Honeycomb**: Use item pattern `Device *: Summary`
- **Gráficos**: Use os itens de contagem e disponibilidade
- **Tabelas**: Filtre por tags `summary=dashboard`

### Alertas

O template inclui triggers pré-configurados:

- Dispositivos offline
- Baixa disponibilidade (<90%)
- Disponibilidade crítica (<70%)

## Estrutura dos Dados

### Item Summary (para dashboards):
Formato: `Nome | IP | Status | Tipo | Modelo`
Exemplo: `Office AP-01 | 192.168.1.100 | Online | AP | UAP-AC-PRO`

### Métricas disponíveis:
- `unifi.devices.total` - Total de dispositivos
- `unifi.devices.online` - Dispositivos online
- `unifi.devices.offline` - Dispositivos offline
- `unifi.devices.availability` - Percentual de disponibilidade
- `unifi.devices.total.ap` - Total de Access Points
- `unifi.devices.total.switch` - Total de Switches

## Troubleshooting

```bash
# Teste manual
sudo -u zabbix /usr/lib/zabbix/externalscripts/zbx_unifi_ap_status.py "Default"
```

### Sem descoberta de dispositivos:
1. Verifique Latest Data se o item Raw Data tem conteúdo
2. Execute discovery rule manualmente
3. Verifique se a macro {$UNIFI_SITE} está correta

### Widget sem dados:
1. Confirme se os itens Summary existem em Latest Data
2. Use item pattern: `Device *: Summary`
3. Ou use item tags: `summary=dashboard`

## Estrutura do Projeto

```
unifi-zabbix-monitoring/
├── README.md
├── TROUBLESHOOTING.md
├── LICENSE
├── zbx_unifi_ap_status.py
├── template_unifi_multi_site.xml
├── install.sh
├── config.example.py
└── screenshots/
    ├── dashboard_example.png
    └── widget_config.png
```

## Contribuindo

1. Faça fork do projeto
2. Crie uma branch para sua feature
3. Commit suas mudanças
4. Faça push para a branch
5. Abra um Pull Request

## Licença

Este projeto está licenciado sob a licença MIT - veja o arquivo LICENSE para detalhes.

## Suporte

Para suporte e dúvidas:
- Abra uma issue no GitHub
- Consulte a documentação do Zabbix
- Verifique os logs do Zabbix Server para debugging
