import { useEffect, useState } from 'react'
import { Bell, Search, UserCircle } from 'lucide-react'
import NotificationPanel from './NotificationPanel'
import { useAuth } from '../context/AuthContext'

function Header() {
  const [open, setOpen] = useState(false)
  const [time, setTime] = useState(new Date())
  const { user } = useAuth()

  useEffect(() => {
    const timer = setInterval(() => setTime(new Date()), 1000)
    return () => clearInterval(timer)
  }, [])

  return (
    <header className="glass-card mb-6 flex flex-col gap-6 border border-slate-800 bg-slate-950/95 p-6 shadow-soft sm:flex-row sm:items-center sm:justify-between">
      <div>
        <p className="text-sm uppercase tracking-[0.3em] text-slate-400">Painel</p>
        <h1 className="mt-2 text-3xl font-semibold text-slate-100">Bem-vindo, {user?.nome || 'Visitante'}</h1>
        <p className="mt-2 text-sm text-slate-400">Última atualização: {time.toLocaleString('pt-BR')}</p>
      </div>
      <div className="grid gap-4 sm:grid-flow-col sm:auto-cols-max sm:items-center">
        <div className="inline-flex items-center gap-3 rounded-3xl border border-slate-800 bg-slate-900/80 px-4 py-3 text-slate-300 shadow-soft">
          <Search size={16} className="text-blue-400" />
          <span>{time.toLocaleTimeString('pt-BR')}</span>
        </div>
        <button
          className="inline-flex items-center gap-2 rounded-3xl border border-slate-800 bg-slate-900/80 px-4 py-3 text-slate-300 shadow-soft transition hover:border-blue-500 hover:text-white"
          onClick={() => setOpen((prev) => !prev)}
        >
          <Bell size={18} />
          <span>Notificações</span>
        </button>
        <div className="inline-flex items-center gap-3 rounded-3xl border border-slate-800 bg-slate-900/80 px-4 py-3 text-slate-300 shadow-soft">
          <UserCircle size={20} className="text-blue-400" />
          <div>
            <p className="text-sm font-semibold text-slate-100">{user?.usuario || 'Admin'}</p>
            <p className="text-xs text-slate-500">{user?.cargo || 'Administrador'}</p>
          </div>
        </div>
      </div>
      <NotificationPanel open={open} onClose={() => setOpen(false)} />
    </header>
  )
}

export default Header