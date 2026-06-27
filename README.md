# 🛡️ Autodefesa Brasil — Painéis de Gestão

Painéis gerados automaticamente via GitHub Actions e publicados no Netlify.

## 📁 Estrutura do repositório

```
autodefesa-painel/
├── index.html                    ← Hub de entrada (gerado automaticamente)
├── hub_index.html                ← Template do hub (NÃO APAGAR)
├── painel_os.html                ← Painel de OS (gerado automaticamente)
├── painel_pagamentos.html        ← Painel Financeiro (gerado automaticamente)
├── gerar_painel.py               ← Script do Painel de OS
├── gerar_painel_pagamentos.py    ← Script do Painel Financeiro
├── OIP__1_.webp                  ← Logo Autodefesa Brasil
├── dados/
│   ├── painel_de_OSS.xlsx        ← ⬅️ SUBSTITUA AQUI para atualizar OS
│   └── BASE_DE_DADOS_SANKHYA_-_PAGAMENTOS.xlsx  ← ⬅️ SUBSTITUA AQUI para atualizar Financeiro
└── .github/
    └── workflows/
        └── gerar_paineis.yml     ← Automação GitHub Actions
```

## 🔄 Como atualizar os painéis

### Opção 1 — Pelo GitHub Desktop (mais fácil)
1. Exporte o Excel novo do Sankhya
2. Substitua o arquivo dentro da pasta `dados/`
3. Abra o GitHub Desktop
4. Escreva qualquer mensagem no campo Summary (ex: `atualiza excel junho`)
5. Clique **Commit to main** → **Push origin**
6. O GitHub Actions roda automaticamente e o Netlify publica em ~1 minuto ✅

### Opção 2 — Pelo GitHub.com (sem instalar nada)
1. Acesse seu repositório em github.com
2. Clique na pasta `dados/`
3. Clique no arquivo Excel → clique no ícone de lápis ✏️ → **"Upload files"**
4. Arraste o novo Excel
5. Clique **Commit changes**
6. Pronto — automação roda sozinha ✅

## ⚙️ Como conectar o Netlify

1. No Netlify → **Add new site** → **Import an existing project**
2. Escolha **GitHub** → selecione este repositório
3. Build command: deixe **em branco**
4. Publish directory: deixe **em branco** (ou `.`)
5. Clique **Deploy** ✅

## ⚠️ Importante

- Não apague o arquivo `hub_index.html` — ele é o template da página inicial
- O nome dos arquivos Excel pode variar, mas deve começar com `painel_de_OSS` ou `BASE_DE_DADOS`
- O logo `OIP__1_.webp` deve permanecer na raiz do repositório
