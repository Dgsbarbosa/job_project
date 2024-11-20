
# Projeto Final - Harvard CS50W

## **Descrição do Projeto**

Este projeto é uma plataforma de gestão de vagas de emprego que permite a candidatos e empresas interagirem de forma eficiente. Empresas podem cadastrar vagas, gerenciá-las,podem abrir e fechar as vagas., e candidatos podem criar perfis personalizados, salvar vagas de interesse, e se candidatar. 
A aplicação oferece funcionalidades de filtragem por localização (país, estado, cidade) e tipo de contrato, com foco em usabilidade e escalabilidade.

## **Distinctiveness and Complexity**

### **Distinctiveness**
Este projeto aborda uma solução prática e real no mercado de trabalho, integrando gestão de perfis, cadastro de vagas e interações personalizadas entre candidatos e empresas. Diferencia-se pelo uso de APIs externas (como CountryStateCity) para gerenciamento de localizações em tempo real, um nível elevado de interatividade com o usuário e a aplicação de padrões modernos de desenvolvimento web com Django.

### **Complexity**
O projeto incorpora:
- **Integração de APIs**: Consumo de uma API externa para preencher automaticamente os dados de localização, garantindo uma experiência otimizada para o usuário.
- **Modelos Relacionais Avançados**: Uso de herança em modelos para simplificar a reutilização de campos comuns, como `Contact` e `Location`.
- **Filtragem e Agrupamento Dinâmicos**: Vagas são agrupadas por data e empresa, otimizando a apresentação de informações para os usuários.
- **Autenticação e Permissões**: As ações críticas (como salvar vagas e gerenciar perfis) exigem autenticação e implementam níveis de permissão diferenciados.
- **Interface Dinâmica**: Interatividade aprimorada com mensagens contextuais e formulários que se adaptam às condições específicas, como visibilidade dinâmica de campos.

## **Estrutura do Projeto**

### **Apps Criados**

#### **2. App: user**

##### Estrutura:
- **`admin.py`**: Configurações do admin para gerenciar perfis de usuários.
- **`apps.py`**: Configuração do app Django.
- **`forms.py`**: Formulários para autenticação e edição de perfis.
- **`models.py`**: Modelos de usuários e perfis personalizados.
- **`tests.py`**: Testes para validação de funcionalidades.
- **`urls.py`**: Rotas específicas para autenticação, edição e visualização de perfis.
- **`utils.py`**: Funções auxiliares, como validação de dados e envio de e-mails de confirmação.
- **`views.py`**: Gerenciamento de usuários, incluindo:
  - Registro de novos usuários.
  - Login e logout.
  - Edição de perfis de candidatos e empresas.
- **`templates/`**: Contém páginas HTML para registro, login, logout, e edição de perfis.

##### Funcionalidades:
- Registro de candidatos e empresas.
- Login e logout.
- Edição de perfis de usuário.
- Redefinição de senha com validação de e-mail.

---

#### **2. App: job**
Este app gerencia o cadastro de vagas e interações entre empresas e candidatos.

##### Estrutura:
   - **`admin.py`**: Configurações para gerenciar vagas e perfis de empresas.
   - **`apps.py`**: Configuração do app Django.
   - **`forms.py`**: Formulários para criação e edição de vagas.
   - **`models.py`**: Modelos para vagas, empresas e candidaturas.
   - **`tests.py`**: Testes para validação de funcionalidades.
   - **`urls.py`**: Rotas específicas para visualização e gerenciamento de vagas.
   - **`views.py`**: Gerenciamento de vagas, incluindo:
   - Cadastro e edição de vagas.
   - Filtragem por localização e tipo de contrato.
   - Exibição dinâmica de vagas agrupadas por data e empresa.
   - **`templates/`**: Contém páginas HTML para cadastro, edição e exibição de vagas.


   - **`requirements.txt`**: Lista de pacotes necessários:
   - Inclui dependências como `Django`, `requests` e `python-decouple`.

### **Funcionalidades Futuras**

   1. **Versão 2**
   - Cadastrar curriculo
   - Vagas compativeis

   2. **Versão 3**
   - Cursos e Certificações
   - Blog

   3. **Versão 4**
   - Login com facebook, google, linkedin
   - Gerador de curriculo

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
         DJANGO_SECRET_KEY=SUA_CHAVE_SECRETA
         COUNTRYSTATECITY_API_KEY=CHAVE_DA_API
         DEBUG=True
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

- **Testes**:
  - Scripts para testes podem ser criados usando o módulo `unittest` ou `pytest`.
