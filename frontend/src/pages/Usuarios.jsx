import { useEffect, useState } from 'react'
import { api } from '../services/api'
import Sidebar from '../components/Sidebar'
import Header from '../components/Header'

function Usuarios() {
  const [usuarios, setUsuarios] = useState([])
  const [form, setForm] = useState({ nome: '', username: '', email: '', cargo: 'Funcionário', senha: '' })
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    buscarUsuarios()
  }, [])

  async function buscarUsuarios() {
    setLoading(true)
    try {
      const response = await api.get('/usuarios')
      setUsuarios(response.data)
    } catch (error) {
      console.error(error)
    } finally {
      setLoading(false)
    }
  }

  async function criarUsuario(event) {
    event.preventDefault()
    try {
      await api.post('/usuarios', form)
      setForm({ nome: '', username: '', email: '', cargo: 'Funcionário', senha: '' })
      buscarUsuarios()
    } catch (error) {
      console.error(error)
      alert('Erro ao criar usuário')
    }
  }

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100">
      <div className="flex min-h-screen flex-col lg:flex-row">
        <Sidebar />
        <main className="flex-1 p-5 lg:p-8">
          <Header />
          <div className="mt-6 grid gap-6 xl:grid-cols-[1fr_0.9fr]">
            <section className="glass-card p-6">
              <h1 className="text-2xl font-semibold">Equipe de Usuários</h1>
              <p className="mt-2 text-slate-400">Gerencie perfis e cargos do seu time.</p>
              <form className="mt-6 space-y-4" onSubmit={criarUsuario}>
                <div className="grid gap-4 lg:grid-cols-2">
                  <input
                    value={form.nome}
                    onChange={(e) => setForm((prev) => ({ ...prev, nome: e.target.value }))}
                    placeholder="Nome completo"
                    className="rounded-3xl border border-slate-800 bg-slate-950 px-4 py-3 text-slate-100 shadow-soft focus:border-blue-500 focus:outline-none focus:ring-2 focus:ring-blue-500/20"
                  />
                  <input
                    value={form.username}
                    onChange={(e) => setForm((prev) => ({ ...prev, username: e.target.value }))}
                    placeholder="Usuário"
                    className="rounded-3xl border border-slate-800 bg-slate-950 px-4 py-3 text-slate-100 shadow-soft focus:border-blue-500 focus:outline-none focus:ring-2 focus:ring-blue-500/20"
                  />
                </div>
                <div className="grid gap-4 lg:grid-cols-2">
                  <input
                    value={form.email}
                    onChange={(e) => setForm((prev) => ({ ...prev, email: e.target.value }))}
                    placeholder="Email"
                    className="rounded-3xl border border-slate-800 bg-slate-950 px-4 py-3 text-slate-100 shadow-soft focus:border-blue-500 focus:outline-none focus:ring-2 focus:ring-blue-500/20"
                  />
                  <select
                    value={form.cargo}
                    onChange={(e) => setForm((prev) => ({ ...prev, cargo: e.target.value }))}
                    className="rounded-3xl border border-slate-800 bg-slate-950 px-4 py-3 text-slate-100 shadow-soft focus:border-blue-500 focus:outline-none focus:ring-2 focus:ring-blue-500/20"
                  >
                    <option value="Admin">Admin</option>
                    <option value="Gerente">Gerente</option>
                    <option value="Funcionário">Funcionário</option>
                  </select>
                </div>
                <input
                  type="password"
                  value={form.senha}
                  onChange={(e) => setForm((prev) => ({ ...prev, senha: e.target.value }))}
                  placeholder="Senha"
                  className="rounded-3xl border border-slate-800 bg-slate-950 px-4 py-3 text-slate-100 shadow-soft focus:border-blue-500 focus:outline-none focus:ring-2 focus:ring-blue-500/20"
                />
                <button className="w-full rounded-3xl bg-blue-600 px-5 py-3 text-sm font-semibold text-white transition hover:bg-blue-500">
                  Criar usuário
                </button>
              </form>
            </section>
            <section className="glass-card p-6">
              <h2 className="text-xl font-semibold">Usuários ativos</h2>
              <div className="mt-5 space-y-3">
                {loading ? (
                  <p className="text-slate-400">Carregando usuários...</p>
                ) : usuarios.length === 0 ? (
                  <p className="text-slate-400">Nenhum usuário encontrado.</p>
                ) : (
                  usuarios.map((usuario) => (
                    <div key={usuario.id} className="rounded-3xl border border-slate-800 bg-slate-950/90 p-4 shadow-soft">
                      <div className="flex items-center justify-between gap-4">
                        <div>
                          <p className="font-semibold text-slate-100">{usuario.nome}</p>
                          <p className="text-sm text-slate-400">{usuario.usuario} • {usuario.cargo}</p>
                        </div>
                        <span className="rounded-full bg-slate-800 px-3 py-1 text-xs uppercase tracking-[0.16em] text-slate-300">{usuario.cargo}</span>
                      </div>
                      <p className="mt-3 text-sm text-slate-400">{usuario.email}</p>
                    </div>
                  ))
                )}
              </div>
            </section>
          </div>
        </main>
      </div>
    </div>
  )
}

export default Usuarios