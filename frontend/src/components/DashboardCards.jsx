import { useEffect, useState } from 'react'
import { TrendingUp, Package, AlertTriangle, DollarSign } from 'lucide-react'
import { api } from '../services/api'

const cards = [
  {
    label: 'Total Produtos',
    key: 'total_produtos',
    icon: Package,
    accent: 'from-blue-600 to-slate-900',
    suffix: '',
  },
  {
    label: 'Estoque Baixo',
    key: 'estoque_baixo',
    icon: AlertTriangle,
    accent: 'from-yellow-500 to-slate-900',
    suffix: '',
  },
  {
    label: 'Itens em estoque',
    key: 'estoque_total',
    icon: TrendingUp,
    accent: 'from-green-500 to-slate-900',
    suffix: '',
  },
  {
    label: 'Valor total',
    key: 'valor_estoque',
    icon: DollarSign,
    accent: 'from-blue-500 to-slate-900',
    suffix: 'R$',
  },
]

function DashboardCards() {
  const [dados, setDados] = useState({})

  useEffect(() => {
    buscarDashboard()
  }, [])

  async function buscarDashboard() {
    try {
      const response = await api.get('/dashboard')
      setDados(response.data)
    } catch (error) {
      console.error(error)
    }
  }

  return (
    <div className="grid gap-6 xl:grid-cols-4">
      {cards.map((card) => {
        const Icon = card.icon
        return (
          <div key={card.key} className="glass-card p-6 transition hover:-translate-y-1 hover:shadow-glow">
            <div className="flex items-center justify-between gap-4">
              <div>
                <p className="text-sm uppercase tracking-[0.3em] text-slate-400">{card.label}</p>
                <h2 className="mt-4 text-3xl font-semibold text-slate-100">
                  {card.key === 'valor_estoque'
                    ? `R$ ${Number(dados[card.key] ?? 0).toLocaleString('pt-BR', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}`
                    : `${dados[card.key] ?? 0}`}
                </h2>
              </div>
              <div className={`rounded-3xl bg-gradient-to-br ${card.accent} p-4 text-white`}>
                <Icon size={22} />
              </div>
            </div>
            <p className="mt-4 text-sm text-slate-400">+12% este mês</p>
          </div>
        )
      })}
    </div>
  )
}

export default DashboardCards
