import { useMemo, useState } from 'react'
import { NavLink } from 'react-router-dom'
import {
  LayoutDashboard,
  Box,
  Repeat,
  Users,
  BarChart3,
  Settings,
  LogOut,
  Bell,
} from 'lucide-react'
import { useAuth } from '../context/AuthContext'

const navItems = [
  { label: 'Dashboard', to: '/dashboard', icon: LayoutDashboard },
  { label: 'Produtos', to: '/produtos', icon: Box },
  { label: 'Movimentações', to: '/movimentacoes', icon: Repeat },
  { label: 'Usuários', to: '/usuarios', icon: Users },
  { label: 'Relatórios', to: '/relatorios', icon: BarChart3 },
  { label: 'Configurações', to: '/settings', icon: Settings },
]

function Sidebar() {
  const [collapsed, setCollapsed] = useState(false)
  const { logout } = useAuth()

  const classes = useMemo(
    () =>
      collapsed
        ? 'w-20 overflow-hidden border-r border-slate-800 bg-slate-950/95 transition-all duration-300'
        : 'w-72 border-r border-slate-800 bg-slate-950/95 transition-all duration-300',
    [collapsed]
  )

  return (
    <aside className={`${classes} min-h-screen px-4 py-6`}>
      <div className="flex h-full flex-col justify-between gap-6">
        <div>
          <button
            className="mb-6 inline-flex items-center gap-3 rounded-3xl border border-slate-800 bg-slate-900/90 px-4 py-3 text-slate-100 shadow-soft transition hover:border-blue-500"
            onClick={() => setCollapsed((prev) => !prev)}
          >
            <Bell size={18} />
            {!collapsed && <span className="font-semibold">EstoQ+</span>}
          </button>
          <nav className="space-y-2">
            {navItems.map((item) => {
              const Icon = item.icon
              return (
                <NavLink
                  key={item.to}
                  to={item.to}
                  className={({ isActive }) =>
                    `group flex items-center gap-4 rounded-3xl border border-slate-800 px-4 py-3 text-sm font-medium transition ${
                      isActive
                        ? 'border-blue-400/40 bg-blue-500/10 text-blue-300'
                        : 'border-slate-800 text-slate-300 hover:border-blue-500 hover:bg-slate-900'
                    }`
                  }
                >
                  <Icon size={18} />
                  {!collapsed && item.label}
                </NavLink>
              )
            })}
          </nav>
        </div>
        <button
          onClick={logout}
          className="flex items-center gap-3 rounded-3xl border border-slate-800 bg-slate-900/90 px-4 py-3 text-slate-300 transition hover:border-red-500 hover:bg-red-500/10 hover:text-white"
        >
          <LogOut size={18} />
          {!collapsed && 'Logout'}
        </button>
      </div>
    </aside>
  )
}

export default Sidebar;
