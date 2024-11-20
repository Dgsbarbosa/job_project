
# Projeto Final - Harvard CS50W

## **Descrição do Projeto**

Este projeto é uma plataforma de gestão de vagas de emprego que permite a candidatos e empresas interagirem de forma eficiente. Empresas podem cadastrar vagas, gerenciá-las, e candidatos podem criar perfis personalizados, salvar vagas de interesse, e se candidatar. A aplicação oferece funcionalidades de filtragem por localização (país, estado, cidade) e tipo de contrato, com foco em usabilidade e escalabilidade.

## **Distinctiveness and Complexity**

### **Distinctiveness**
Este projeto aborda uma solução prática e real no mercado de trabalho, integrando gestão de perfis, cadastro de vagas e interações personalizadas entre candidatos e empresas. Diferencia-se pelo uso extensivo de APIs externas (como CountryStateCity) para gerenciamento de localizações em tempo real, um nível elevado de interatividade com o usuário e a aplicação de padrões modernos de desenvolvimento web com Django.

### **Complexity**
O projeto incorpora:
- **Integração de APIs**: Consumo de uma API externa para preencher automaticamente os dados de localização, garantindo uma experiência otimizada para o usuário.
- **Modelos Relacionais Avançados**: Uso de herança em modelos para simplificar a reutilização de campos comuns, como `Contact` e `Location`.
- **Filtragem e Agrupamento Dinâmicos**: Vagas são agrupadas por data e empresa, otimizando a apresentação de informações para os usuários.
- **Autenticação e Permissões**: As ações críticas (como salvar vagas e gerenciar perfis) exigem autenticação e implementam níveis de permissão diferenciados.
- **Interface Dinâmica**: Interatividade aprimorada com mensagens contextuais e formulários que se adaptam às condições específicas, como visibilidade dinâmica de campos.

## **Estrutura do Projeto**

### **Arquivos Criados**
- **`models.py`**: Define os modelos principais:
  - `CandidateProfile`, `CompanyProfile`, e `Vacancies` herdam estruturas de `Contact` e `Location`.
  - `SaveVacancy` para salvar e gerenciar as vagas preferidas.
- **`views.py`**: Contém as funcionalidades principais, como:
  - Gerenciamento de perfis, empresas, e vagas.
  - Consumo de API para países, estados e cidades.
  - Agrupamento de dados e exibição personalizada.
- **`forms.py`**: Criação de formulários com validação personalizada para perfis e vagas.
- **`urls.py`**: Mapeamento das rotas do aplicativo.
- **Templates HTML**: Interface do usuário, incluindo páginas para cadastro, edição e exibição de vagas e perfis.
- **`requirements.txt`**: Lista de pacotes necessários:
  - Inclui dependências como `Django`, `requests` e `python-decouple`.

## **Como Executar o Aplicativo**

1. **Clone o repositório**:
   ```bash
   git clone <URL_DO_REPOSITORIO>
   cd <DIRETORIO_DO_PROJETO>
   ```

2. **Crie um ambiente virtual**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Em sistemas Unix
   venv\Scripts\activate  # Em sistemas Windows
   ```

3. **Instale as dependências**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Configuração da chave da API**:
   - Crie um arquivo `.env` na raiz do projeto com a seguinte variável:
     ```
     COUNTRYSTATECITY_API_KEY=CHAVE_DA_API
     ```

5. **Aplique as migrações do banco de dados**:
   ```bash
   python manage.py migrate
   ```

6. **Execute o servidor local**:
   ```bash
   python manage.py runserver
   ```

7. **Acesse a aplicação**:
   - Abra o navegador e vá para `http://127.0.0.1:8000`.

## **Informações Adicionais**
- **Usuário Admin**:
  - Email: admin@example.com
  - Senha: `admin123` (troque no ambiente de produção)
- **Testes**:
  - Scripts para testes podem ser criados usando o módulo `unittest` ou `pytest`.

---

Caso tenha outras informações que deseja adicionar ou personalizar, posso adaptar este arquivo para suas necessidades!