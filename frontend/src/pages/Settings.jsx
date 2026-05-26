import Sidebar from '../components/Sidebar'
import Header from '../components/Header'
import { useAuth } from '../context/AuthContext'

function Settings() {
  const { user, logout } = useAuth()

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100">
      <div className="flex min-h-screen flex-col lg:flex-row">
        <Sidebar />
        <main className="flex-1 p-5 lg:p-8">
          <Header />
          <div className="mt-6 space-y-6">
            <section className="glass-card p-6">
              <div className="flex flex-col gap-6 lg:flex-row lg:items-center lg:justify-between">
                <div>
                  <h1 className="text-2xl font-semibold">Configurações</h1>
                  <p className="mt-2 text-slate-400">Dados da sua conta e preferências do sistema.</p>
                </div>
                <button
                  onClick={logout}
                  className="rounded-3xl bg-red-500 px-5 py-3 text-sm font-semibold text-white transition hover:bg-red-400"
                >
                  Sair do sistema
                </button>
              </div>
            </section>
            <section className="glass-card p-6">
              <h2 className="text-xl font-semibold">Perfil do usuário</h2>
              <div className="mt-6 grid gap-4 lg:grid-cols-2">
                <div className="rounded-3xl border border-slate-800 bg-slate-950/90 p-5 shadow-soft">
                  <p className="text-sm uppercase tracking-[0.3em] text-slate-500">Nome</p>
                  <p className="mt-2 text-lg font-semibold text-slate-100">{user?.nome || '---'}</p>
                </div>
                <div className="rounded-3xl border border-slate-800 bg-slate-950/90 p-5 shadow-soft">
                  <p className="text-sm uppercase tracking-[0.3em] text-slate-500">Cargo</p>
                  <p className="mt-2 text-lg font-semibold text-slate-100">{user?.cargo || '---'}</p>
                </div>
                <div className="rounded-3xl border border-slate-800 bg-slate-950/90 p-5 shadow-soft">
                  <p className="text-sm uppercase tracking-[0.3em] text-slate-500">Email</p>
                  <p className="mt-2 text-lg font-semibold text-slate-100">{user?.email || '---'}</p>
                </div>
                <div className="rounded-3xl border border-slate-800 bg-slate-950/90 p-5 shadow-soft">
                  <p className="text-sm uppercase tracking-[0.3em] text-slate-500">Último login</p>
                  <p className="mt-2 text-lg font-semibold text-slate-100">{user?.ultimo_login ? new Date(user.ultimo_login).toLocaleString('pt-BR') : '---'}</p>
                </div>
              </div>
            </section>
          </div>
        </main>
      </div>
    </div>
  )
}

export default Settings