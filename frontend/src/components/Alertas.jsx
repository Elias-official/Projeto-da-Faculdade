import { useEffect, useState } from 'react'
import { api } from '../services/api'
import { AlertTriangle, Package, TrendingDown } from 'lucide-react'

function Alertas() {
  const [produtos, setProdutos] = useState([])

  useEffect(() => {
    buscarAlertas()
  }, [])

  async function buscarAlertas() {
    try {
      const response = await api.get('/produtos')
      setProdutos(response.data.filter((item) => item.status !== 'Estoque normal').slice(0, 5))
    } catch (error) {
      console.error(error)
    }
  }

  return (
    <div className="glass-card p-6">
      <div className="flex items-center justify-between gap-4">
        <div>
          <p className="text-sm uppercase tracking-[0.3em] text-slate-400">Alertas</p>
          <h2 className="mt-2 text-2xl font-semibold text-slate-100">Reforçar estoque</h2>
        </div>
        <div className="rounded-3xl bg-amber-500/10 p-3 text-amber-300 shadow-soft">
          <AlertTriangle size={20} />
        </div>
      </div>
      <div className="mt-6 space-y-4">
        {produtos.length === 0 ? (
          <div className="rounded-3xl border border-slate-800 bg-slate-950/90 p-4 text-slate-400">Nenhum alerta no momento.</div>
        ) : (
          produtos.map((produto) => (
            <div key={produto.id} className="rounded-3xl border border-slate-800 bg-slate-950/90 p-4 shadow-soft">
              <div className="flex items-center justify-between gap-4">
                <div>
                  <p className="text-sm text-slate-400">{produto.codigo}</p>
                  <p className="text-lg font-semibold text-slate-100">{produto.produto}</p>
                </div>
                <span className={`inline-flex rounded-full px-3 py-1 text-xs font-semibold ${produto.status.includes('Crítico') ? 'bg-red-500/15 text-red-300' : 'bg-yellow-500/15 text-yellow-300'}`}>
                  {produto.status}
                </span>
              </div>
              <div className="mt-4 grid gap-3 sm:grid-cols-2 text-sm text-slate-400">
                <div className="flex items-center gap-2">
                  <Package size={16} />
                  <span>{produto.categoria}</span>
                </div>
                <div className="flex items-center gap-2">
                  <TrendingDown size={16} />
                  <span>{produto.estoque_atual} em estoque</span>
                </div>
              </div>
            </div>
          ))
        )}
      </div>
    </div>
  )
}

export default Alertas