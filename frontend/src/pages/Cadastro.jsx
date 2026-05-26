import { useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { api } from '../services/api'
import { User, Mail, Shield, Key } from 'lucide-react'

function Cadastro() {
  const navigate = useNavigate()
  const [form, setForm] = useState({ nome: '', username: '', email: '', cargo: 'Funcionário', senha: '', confirmar: '' })
  const [erro, setErro] = useState('')

  async function criarConta(event) {
    event.preventDefault()
    setErro('')

    if (form.senha !== form.confirmar) {
      setErro('As senhas não coincidem.')
      return
    }

    try {
      await api.post('/register', {
        nome: form.nome,
        username: form.username,
        email: form.email,
        cargo: form.cargo,
        senha: form.senha,
      })
      navigate('/login')
    } catch (error) {
      setErro(error.response?.data?.erro || 'Erro ao criar conta.')
    }
  }

  return (
    <div className="relative min-h-screen overflow-hidden bg-gradient-to-br from-slate-950 via-slate-950 to-slate-900 px-4 py-8 text-slate-100">
      {/* Background elements */}
      <div className="pointer-events-none absolute -right-40 top-20 h-80 w-80 rounded-full bg-blue-600/5 blur-3xl"></div>
      <div className="pointer-events-none absolute -left-40 bottom-40 h-96 w-96 rounded-full bg-blue-500/5 blur-3xl"></div>

      <div className="relative mx-auto flex max-w-6xl flex-col gap-8 lg:flex-row lg:items-center lg:justify-between">
        {/* Left Section - Info */}
        <section className="space-y-6">
          <div className="space-y-4 animate-fade-in">
            <div className="inline-block">
              <p className="rounded-full bg-blue-500/10 px-4 py-2 text-sm uppercase tracking-[0.3em] text-blue-400 font-semibold border border-blue-500/20">
                Novo Cadastro
              </p>
            </div>
            <h1 className="text-5xl font-bold leading-tight text-slate-50">
              Crie sua conta <span className="bg-gradient-to-r from-blue-400 to-blue-600 bg-clip-text text-transparent">corporativa</span>
            </h1>
            <p className="max-w-md text-lg text-slate-400">Cadastre-se para começar a controlar estoque, movimentações e relatórios em um painel premium.</p>
          </div>

          <div className="grid gap-4 sm:grid-cols-2 pt-4">
            <div className="group rounded-2xl border border-slate-800/50 bg-slate-900/40 p-6 backdrop-blur-sm transition-all duration-300 hover:border-blue-500/30 hover:bg-slate-800/40 hover:shadow-xl hover:shadow-blue-500/5">
              <div className="mb-4 inline-block rounded-xl bg-blue-500/10 p-3 group-hover:bg-blue-500/20 transition-colors">
                <Shield size={20} className="text-blue-400" />
              </div>
              <h3 className="font-semibold text-slate-100 mb-2">Seguro</h3>
              <p className="text-sm text-slate-400">Acesso protegido com autenticação JWT encriptada.</p>
            </div>

            <div className="group rounded-2xl border border-slate-800/50 bg-slate-900/40 p-6 backdrop-blur-sm transition-all duration-300 hover:border-blue-500/30 hover:bg-slate-800/40 hover:shadow-xl hover:shadow-blue-500/5">
              <div className="mb-4 inline-block rounded-xl bg-blue-500/10 p-3 group-hover:bg-blue-500/20 transition-colors">
                <User size={20} className="text-blue-400" />
              </div>
              <h3 className="font-semibold text-slate-100 mb-2">Profissional</h3>
              <p className="text-sm text-slate-400">Suporte a cargos e permissões para equipe operacional.</p>
            </div>
          </div>
        </section>

        {/* Right Section - Register Form */}
        <main className="w-full max-w-md animate-fade-in">
          <div className="rounded-3xl border border-slate-700/50 bg-gradient-to-br from-slate-900/80 to-slate-900/40 p-8 backdrop-blur-xl shadow-2xl shadow-blue-500/5 transition-all duration-300 hover:border-slate-600/50 hover:shadow-2xl hover:shadow-blue-500/10">
            <div className="mb-8 space-y-3">
              <p className="text-sm font-medium text-blue-400">Novo usuário</p>
              <h2 className="text-3xl font-bold text-slate-50">Cadastro</h2>
              <p className="text-slate-400">Preencha seus dados para criar sua conta.</p>
            </div>

            <form className="space-y-5" onSubmit={criarConta}>
              <label className="block group">
                <span className="mb-3 flex items-center gap-2 text-sm font-medium text-slate-300 group-focus-within:text-blue-400 transition-colors">
                  <User size={16} className="text-blue-400" />
                  Nome completo
                </span>
                <input
                  value={form.nome}
                  onChange={(e) => setForm({ ...form, nome: e.target.value })}
                  className="w-full rounded-2xl border border-slate-700 bg-slate-800/50 px-4 py-3 text-slate-100 placeholder-slate-500 shadow-inner transition-all duration-300 focus:border-blue-500 focus:bg-slate-800 focus:outline-none focus:ring-2 focus:ring-blue-500/30 hover:border-slate-600"
                  placeholder="Seu nome completo"
                  required
                />
              </label>

              <label className="block group">
                <span className="mb-3 flex items-center gap-2 text-sm font-medium text-slate-300 group-focus-within:text-blue-400 transition-colors">
                  <Mail size={16} className="text-blue-400" />
                  Email corporativo
                </span>
                <input
                  type="email"
                  value={form.email}
                  onChange={(e) => setForm({ ...form, email: e.target.value })}
                  className="w-full rounded-2xl border border-slate-700 bg-slate-800/50 px-4 py-3 text-slate-100 placeholder-slate-500 shadow-inner transition-all duration-300 focus:border-blue-500 focus:bg-slate-800 focus:outline-none focus:ring-2 focus:ring-blue-500/30 hover:border-slate-600"
                  placeholder="email@empresa.com"
                  required
                />
              </label>

              <label className="block group">
                <span className="mb-3 flex items-center gap-2 text-sm font-medium text-slate-300 group-focus-within:text-blue-400 transition-colors">
                  <Shield size={16} className="text-blue-400" />
                  Usuário
                </span>
                <input
                  value={form.username}
                  onChange={(e) => setForm({ ...form, username: e.target.value })}
                  className="w-full rounded-2xl border border-slate-700 bg-slate-800/50 px-4 py-3 text-slate-100 placeholder-slate-500 shadow-inner transition-all duration-300 focus:border-blue-500 focus:bg-slate-800 focus:outline-none focus:ring-2 focus:ring-blue-500/30 hover:border-slate-600"
                  placeholder="seu_usuario"
                  required
                />
              </label>

              <label className="block group">
                <span className="mb-3 flex items-center gap-2 text-sm font-medium text-slate-300 group-focus-within:text-blue-400 transition-colors">
                  <Key size={16} className="text-blue-400" />
                  Senha
                </span>
                <input
                  type="password"
                  value={form.senha}
                  onChange={(e) => setForm({ ...form, senha: e.target.value })}
                  className="w-full rounded-2xl border border-slate-700 bg-slate-800/50 px-4 py-3 text-slate-100 placeholder-slate-500 shadow-inner transition-all duration-300 focus:border-blue-500 focus:bg-slate-800 focus:outline-none focus:ring-2 focus:ring-blue-500/30 hover:border-slate-600"
                  placeholder="••••••••"
                  required
                />
              </label>

              <label className="block group">
                <span className="mb-3 flex items-center gap-2 text-sm font-medium text-slate-300 group-focus-within:text-blue-400 transition-colors">
                  <Key size={16} className="text-blue-400" />
                  Confirmar senha
                </span>
                <input
                  type="password"
                  value={form.confirmar}
                  onChange={(e) => setForm({ ...form, confirmar: e.target.value })}
                  className="w-full rounded-2xl border border-slate-700 bg-slate-800/50 px-4 py-3 text-slate-100 placeholder-slate-500 shadow-inner transition-all duration-300 focus:border-blue-500 focus:bg-slate-800 focus:outline-none focus:ring-2 focus:ring-blue-500/30 hover:border-slate-600"
                  placeholder="Repita a senha"
                  required
                />
              </label>

              {erro && (
                <div className="rounded-2xl border border-red-500/30 bg-red-500/10 px-4 py-3 text-sm text-red-200 backdrop-blur-sm animate-pulse">
                  <div className="flex items-center gap-2">
                    <div className="h-2 w-2 rounded-full bg-red-400"></div>
                    {erro}
                  </div>
                </div>
              )}

              <button 
                className="w-full rounded-2xl bg-gradient-to-r from-blue-600 to-blue-500 px-5 py-3 text-sm font-bold text-white shadow-lg shadow-blue-600/30 transition-all duration-300 hover:shadow-blue-600/50 hover:shadow-xl hover:from-blue-500 hover:to-blue-400 focus:outline-none focus:ring-2 focus:ring-blue-500/50 active:scale-95"
              >
                Criar conta
              </button>
            </form>

            <div className="mt-8 space-y-4 border-t border-slate-700/50 pt-6">
              <p className="text-center text-sm text-slate-500">
                Já possui conta?{' '}
                <Link to="/login" className="font-semibold text-blue-400 transition-all hover:text-blue-300 hover:underline">
                  Entrar
                </Link>
              </p>
              <p className="text-center text-xs text-slate-600">
                Todos os dados são encriptados e seguros
              </p>
            </div>
          </div>
        </main>
      </div>
    </div>
  )
}

export default Cadastro