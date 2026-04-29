# Sem Aperreio - Sistema de Controle de Gastos

Sistema de controle de gastos financeiros com previsão usando Inteligência Artificial.

## 🚀 Stack Tecnológico

### Backend
- **Django 4.2** - Framework web
- **Django REST Framework** - API REST
- **SQLite** - Banco de dados
- **Scikit-learn** - Machine Learning
- **Pandas** - Manipulação de dados

### Frontend
- **Vue 3** - Framework JavaScript
- **Vite** - Build tool
- **PrimeVue** - Componentes UI
- **CSS3** - Estilização

## 📋 Funcionalidades

- ✅ Cadastro de gastos com categorias
- ✅ Validação robusta de dados
- ✅ Previsão de gastos com IA
- ✅ Interface responsiva e moderna
- ✅ Tratamento de erros amigável
- ✅ Loading states e feedback visual
- ✅ Filtros e ordenação
- ✅ Segurança com variáveis de ambiente

## 🔧 Instalação

### Pré-requisitos
- Python 3.8+
- Node.js 16+
- npm ou yarn

### Backend

1. **Criar ambiente virtual**
```bash
cd backend
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

2. **Instalar dependências**
```bash
pip install -r requirements.txt
```

3. **Configurar variáveis de ambiente**
```bash
cp .env.example .env
# Edite o arquivo .env com suas configurações
```

4. **Migrar banco de dados**
```bash
python manage.py makemigrations
python manage.py migrate
```

5. **Treinar modelo de IA (opcional)**
```bash
python treinar_modelo.py
```

6. **Iniciar servidor**
```bash
python manage.py runserver
```

### Frontend

1. **Instalar dependências**
```bash
cd frontend
npm install
```

2. **Configurar variáveis de ambiente**
```bash
# Criar arquivo .env.local
echo "VITE_API_URL=http://127.0.0.1:8000" > .env.local
```

3. **Iniciar servidor de desenvolvimento**
```bash
npm run dev
```

## 🌐 URLs de Acesso

- **Frontend**: http://localhost:5173
- **Backend API**: http://localhost:8000/api/
- **Admin Django**: http://localhost:8000/admin/

## 📚 Endpoints da API

### Gastos
- `GET /api/gastos/` - Listar todos os gastos
- `POST /api/gastos/` - Criar novo gasto
- `GET /api/gastos/{id}/` - Detalhes do gasto
- `PUT /api/gastos/{id}/` - Atualizar gasto
- `DELETE /api/gastos/{id}/` - Excluir gasto

### Previsão
- `POST /api/prever/` - Prever gasto do mês

### Parâmetros de Filtro
- `?categoria=alimentacao` - Filtrar por categoria
- `?data_inicio=2024-01-01` - Data inicial
- `?data_fim=2024-12-31` - Data final
- `?limite=50` - Limitar resultados

## 🔒 Segurança

- ✅ Variáveis de ambiente configuradas
- ✅ CORS configurado para produção
- ✅ Validação de inputs no backend
- ✅ Headers de segurança em produção
- ✅ SQL injection prevention
- ✅ XSS protection

## 📱 Categorias Disponíveis

- Alimentação 🍔
- Transporte 🚗
- Moradia 🏠
- Saúde 🏥
- Educação 📚
- Lazer 🎮
- Outros 📦

## 🚀 Deploy

### Backend (Produção)
1. Configure as variáveis de ambiente no servidor
2. Defina `DEBUG=False` no `.env`
3. Configure `ALLOWED_HOSTS` e `CORS_ALLOWED_ORIGINS`
4. Execute `collectstatic`
5. Use servidor WSGI (Gunicorn, uWSGI)

### Frontend (Produção)
1. Configure `VITE_API_URL` para o URL de produção
2. Execute `npm run build`
3. Sirva os arquivos estáticos com Nginx ou similar

## 🤝 Contribuindo

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/nova-feature`)
3. Commit suas mudanças (`git commit -am 'Add nova feature'`)
4. Push para a branch (`git push origin feature/nova-feature`)
5. Abra um Pull Request

## 📝 Licença

Este projeto está sob licença MIT.

## 🐛 Problemas Conhecidos

- Modelo de IA usa dados fixos (precisa de retreinamento com dados reais)
- Não há autenticação implementada
- Cache não está configurado

## 🔮 Próximos Passos

- [ ] Implementar autenticação JWT
- [ ] Adicionar gráficos e dashboard
- [ ] Implementar cache com Redis
- [ ] Melhorar modelo de IA com dados reais
- [ ] Adicionar exportação de dados
- [ ] Implementar PWA
- [ ] Adicionar testes automatizados
