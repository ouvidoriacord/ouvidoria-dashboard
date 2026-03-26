import pandas as pd
import json
from datetime import datetime

SEC_MAP = {
    'Administra': 'Administração',
    'Cultura, t': 'Cultura e Turismo',
    'Obras': 'Obras',
    'Meio Ambie': 'Meio Ambiente',
    'Desenvolvi': 'Desenvolvimento Econômico',
    'Governo': 'Governo',
    'Educação': 'Educação',
    'SAAE': 'SAAE',
    'Justiça': 'Justiça',
    'Segurança': 'Segurança Pública',
    'Finanças': 'Finanças',
    'Saúde': 'Saúde',
    'Serviços': 'Serviços Públicos'
}

df = pd.read_excel('Dash.xlsx', sheet_name='Dash')
df['Data de Criação'] = pd.to_datetime(df['Data de Criação'], errors='coerce')
df['Status'] = df['Status'].astype(str).str.strip().replace('Em andamento', 'Em Andamento')
df['Dentro/Fora Prazo'] = df['Dentro/Fora Prazo'].astype(str).str.strip()

records = []
for _, r in df.iterrows():
    dt = r['Data de Criação']
    mes = dt.strftime('%Y-%m') if pd.notna(dt) else '—'
    dc  = dt.strftime('%d/%m/%Y') if pd.notna(dt) else '—'
    sec = str(r.get('Secretaria', ''))
    status = str(r.get('Status', '—'))
    prazo  = str(r.get('Dentro/Fora Prazo', '—'))
    if prazo in ('nan', 'None', ''): prazo = '—'
    if status in ('nan', 'None', ''): status = '—'
    records.append({
        'protocolo':  str(r.get('Protocolo', '')),
        'tipo':       str(r.get('Manifestação', '—')),
        'assunto':    str(r.get('Assuntos', '—')),
        'secretaria': SEC_MAP.get(sec, sec),
        'mes':        mes,
        'status':     status,
        'prazo':      prazo,
        'dataCriacao': dc
    })

with open('dados.json', 'w', encoding='utf-8') as f:
    json.dump(records, f, ensure_ascii=False)

print(f"✅ {len(records)} registros convertidos para dados.json")
