# Dicionário de dados

Layout dos microdados não identificados do Novo CAGED (base de movimentação), nomes **como vêm no TXT**.

Fonte: planilha *Layout Não-identificado Novo Caged Movimentação* no FTP
`ftp://ftp.mtps.gov.br/pdet/microdados/NOVO CAGED/` e o pacote [cagedr](https://strategicprojects.github.io/cagedr/reference/caged_layout.html).

O MTE publica o Novo CAGED em **UTF-8**, delimitador `;`, vírgula decimal. Arquivos `CAGEDMOV`, `CAGEDFOR` e `CAGEDEXC` são `.7z`.

| Coluna no arquivo | Nome normalizado | Tipo | Descrição |
| --- | --- | --- | --- |
| competênciamov | competenciamov | int | Mês de referência (AAAAMM) |
| região | regiao | int | Região IBGE |
| uf | uf | int | UF IBGE |
| município | municipio | int | Município IBGE |
| seção | secao | str | Seção CNAE 2.0 |
| subclasse | subclasse | str | Subclasse CNAE 2.0 |
| saldomovimentação | saldomovimentacao | int | **+1 admissão, −1 desligamento** |
| categoria | categoria | int | Categoria do trabalhador |
| cbo2002ocupação | cbo2002ocupacao | int | CBO 2002 |
| graudeinstrução | graudeinstrucao | int | Escolaridade |
| idade | idade | int | Idade |
| horascontratuais | horascontratuais | float | Horas semanais |
| raçacor | racacor | int | Raça/cor |
| sexo | sexo | int | Sexo |
| tipoempregador | tipoempregador | int | Tipo de empregador |
| tipoestabelecimento | tipoestabelecimento | int | Tipo de estabelecimento |
| tipomovimentação | tipomovimentacao | int | Tipo de movimentação |
| tipodedeficiência | tipodedeficiencia | int | Deficiência |
| indtrabintermitente | indtrabintermitente | int | Intermitente |
| indtrabparcial | indtrabparcial | int | Parcial |
| salário | salario | float | Salário mensal declarado |
| tamestabjan | tamestabjan | int | Faixa de emprego em janeiro |
| indicadoraprendiz | indicadoraprendiz | int | Aprendiz |
| origemdainformação | origemdainformacao | int | Origem da informação |
| competênciadec | competenciadec | int | Competência da declaração |
| indicadordeforadoprazo | indicadordeforadoprazo | int | Fora do prazo |
| unidadesaláriocódigo | unidadesalariocodigo | int | Unidade da parte fixa |
| valorsaláriofixo | valorsalariofixo | float | Salário-base (parte fixa) |

Só no arquivo **EXC**: `competênciaexc`, `indicadordeexclusão`.

## Metadados de ingestão (bronze)

| Coluna | Descrição |
| --- | --- |
| _arquivo_origem | Caminho do .7z (ou fixture) |
| _hash_sha256 | SHA-256 do arquivo de origem |
| _data_carga | Timestamp UTC da conversão |
| _tipo_arquivo | MOV, FOR ou EXC |
| _competencia_arquivo | AAAAMM do arquivo baixado |

## Mart `fct_saldo_mensal`

`saldo = sum(saldomovimentacao)` por competência, UF e seção CNAE.
