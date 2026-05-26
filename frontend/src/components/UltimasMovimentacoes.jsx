import { useEffect, useState } from 'react'
import { api } from '../services/api'
import { ArrowUpRight, ArrowDownRight } from 'lucide-react'

function UltimasMovimentacoes() {
  const [movimentacoes, setMovimentacoes] = useState([])

  useEffect(() => {
    fetchMovimentacoes()
  }, [])

  async function fetchMovimentacoes() {
    try {
      const response = await api.get('/movimentacoes')
      setMovimentacoes(response.data.slice(0, 6))
    } catch (error) {
      console.error(error)
    }
  }

  return (
    <div className="glass-card p-6">
      <div className="flex items-center justify-between gap-3">
        <div>
          <p className="text-sm uppercase tracking-[0.3em] text-slate-400">Últimas movimentações</p>
          <h2 className="mt-2 text-2xl font-semibold text-slate-100">Atividades recentes</h2>
        </div>
      </div>
      <div className="mt-6 space-y-4">
        {movimentacoes.length === 0 ? (
          <p className="text-slate-400">Nenhuma movimentação registrada.</p>
        ) : (
          movimentacoes.map((mov) => {
            const positive = mov.tipo?.toLowerCase().includes('entrada')
            return (
              <div key={mov.id} className="rounded-3xl border border-slate-800 bg-slate-950/90 p-4 shadow-soft">
                <div className="flex items-center justify-between gap-3">
                  <div>
                    <p className="font-semibold text-slate-100">{mov.produto || 'Produto removido'}</p>
                    <p className="text-sm text-slate-400">{new Date(mov.data_movimentacao).toLocaleString('pt-BR')}</p>
                  </div>
                  <span className={`inline-flex items-center gap-2 rounded-full px-3 py-1 text-xs font-semibold ${positive ? 'bg-emerald-500/15 text-emerald-300' : 'bg-red-500/15 text-red-300'}`}>
                    {positive ? <ArrowUpRight size={14} /> : <ArrowDownRight size={14} />}
                    {mov.tipo}
                  </span>
                </div>
                <div className="mt-3 flex items-center justify-between text-sm text-slate-400">
                  <span>Quantidade: {mov.quantidade}</span>
                  <span>Usuário: {mov.usuario_id}</span>
                </div>
              </div>
            )
          })
        )}
      </div>
    </div>
  )
}

export default UltimasMovimentacoes
