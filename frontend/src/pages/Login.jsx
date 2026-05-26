import { useState } from 'react'
import { useNavigate, useLocation, Link } from 'react-router-dom'
import { api } from '../services/api'
import { useAuth } from '../context/AuthContext'
import { Lock, Mail, UserCircle, ShieldCheck } from 'lucide-react'

function Login() {
  const navigate = useNavigate()
  const location = useLocation()
  const { login } = useAuth()
  const [usuario, setUsuario] = useState('')
  const [senha, setSenha] = useState('')
  const [erro, setErro] = useState('')
  const [lembrar, setLembrar] = useState(true)

  async function fazerLogin(e) {
    e.preventDefault()
    setErro('')

    try {
      const response = await api.post('/login', {
        usuario,
        senha,
      })
      login(response.data.token, response.data.usuario)
      const from = location.state?.from?.pathname || '/dashboard'
      navigate(from, { replace: true })
    } catch (error) {
      setErro(error.response?.data?.erro || 'Falha no login. Verifique suas credenciais.')
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
                EstoQ+ (Controle de Estoque)
              </p>
            </div>
            <h1 className="text-5xl font-bold leading-tight text-slate-50">
              Acesse seu painel <span className="bg-gradient-to-r from-blue-400 to-blue-600 bg-clip-text text-transparent">empresarial</span>
            </h1>
            <p className="max-w-md text-lg text-slate-400">Sistema moderno de controle de estoque com autenticação segura, relatórios avançados e interface futurista.</p>
          </div>

          <div className="grid gap-4 sm:grid-cols-2 pt-4">
            <div className="group rounded-2xl border border-slate-800/50 bg-slate-900/40 p-6 backdrop-blur-sm transition-all duration-300 hover:border-blue-500/30 hover:bg-slate-800/40 hover:shadow-xl hover:shadow-blue-500/5">
              <div className="mb-4 inline-block rounded-xl bg-blue-500/10 p-3 group-hover:bg-blue-500/20 transition-colors">
                <ShieldCheck size={20} className="text-blue-400" />
              </div>
              <h3 className="font-semibold text-slate-100 mb-2">Seguro</h3>
              <p className="text-sm text-slate-400">JWT encriptado e sessão persistente com recuperação segura.</p>
            </div>

            <div className="group rounded-2xl border border-slate-800/50 bg-slate-900/40 p-6 backdrop-blur-sm transition-all duration-300 hover:border-blue-500/30 hover:bg-slate-800/40 hover:shadow-xl hover:shadow-blue-500/5">
              <div className="mb-4 inline-block rounded-xl bg-blue-500/10 p-3 group-hover:bg-blue-500/20 transition-colors">
                <UserCircle size={20} className="text-blue-400" />
              </div>
              <h3 className="font-semibold text-slate-100 mb-2">Premium</h3>
              <p className="text-sm text-slate-400">Design elegante inspirado em dashboards SaaS profissionais.</p>
            </div>
          </div>
        </section>

        {/* Right Section - Login Form */}
        <main className="w-full max-w-md animate-fade-in">
          <div className="rounded-3xl border border-slate-700/50 bg-gradient-to-br from-slate-900/80 to-slate-900/40 p-8 backdrop-blur-xl shadow-2xl shadow-blue-500/5 transition-all duration-300 hover:border-slate-600/50 hover:shadow-2xl hover:shadow-blue-500/10">
            <div className="mb-8 space-y-3">
              <p className="text-sm font-medium text-blue-400">Bem-vindo de volta</p>
              <h2 className="text-3xl font-bold text-slate-50">Login</h2>
              <p className="text-slate-400">Digite suas credenciais para acessar o painel.</p>
            </div>

            <form className="space-y-5" onSubmit={fazerLogin}>
              <label className="block group">
                <span className="mb-3 flex items-center gap-2 text-sm font-medium text-slate-300 group-focus-within:text-blue-400 transition-colors">
                  <Mail size={16} className="text-blue-400" />
                  Usuário ou email
                </span>
                <input
                  value={usuario}
                  onChange={(e) => setUsuario(e.target.value)}
                  className="w-full rounded-2xl border border-slate-700 bg-slate-800/50 px-4 py-3 text-slate-100 placeholder-slate-500 shadow-inner transition-all duration-300 focus:border-blue-500 focus:bg-slate-800 focus:outline-none focus:ring-2 focus:ring-blue-500/30 hover:border-slate-600"
                  placeholder="admin@empresa.com ou admin"
                  autoComplete="username"
                  required
                />
              </label>

              <label className="block group">
                <span className="mb-3 flex items-center gap-2 text-sm font-medium text-slate-300 group-focus-within:text-blue-400 transition-colors">
                  <Lock size={16} className="text-blue-400" />
                  Senha
                </span>
                <input
                  value={senha}
                  onChange={(e) => setSenha(e.target.value)}
                  type="password"
                  className="w-full rounded-2xl border border-slate-700 bg-slate-800/50 px-4 py-3 text-slate-100 placeholder-slate-500 shadow-inner transition-all duration-300 focus:border-blue-500 focus:bg-slate-800 focus:outline-none focus:ring-2 focus:ring-blue-500/30 hover:border-slate-600"
                  placeholder="••••••••"
                  autoComplete="current-password"
                  required
                />
              </label>

              <div className="flex items-center justify-between gap-4 text-sm">
                <label className="inline-flex items-center gap-2 cursor-pointer group">
                  <input
                    type="checkbox"
                    checked={lembrar}
                    onChange={(e) => setLembrar(e.target.checked)}
                    className="h-4 w-4 rounded border-slate-600 bg-slate-800 text-blue-500 transition-all focus:ring-blue-500/30 cursor-pointer"
                  />
                  <span className="text-slate-400 group-hover:text-slate-300 transition-colors">Lembrar de mim</span>
                </label>
                <button 
                  type="button" 
                  className="text-blue-400 transition-all duration-300 hover:text-blue-300 hover:underline font-medium"
                >
                  Recuperar senha
                </button>
              </div>

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
                Entrar no painel
              </button>
            </form>

            <div className="mt-8 space-y-4 border-t border-slate-700/50 pt-6">
              <p className="text-center text-sm text-slate-500">
                Não tem conta?{' '}
                <Link to="/cadastro" className="font-semibold text-blue-400 transition-all hover:text-blue-300 hover:underline">
                  Criar cadastro
                </Link>
              </p>
              <p className="text-center text-xs text-slate-600">
                Suas credenciais são protegidas com criptografia JWT
              </p>
            </div>
          </div>
        </main>
      </div>
    </div>
  )
}

export default Login
