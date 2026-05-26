import { useEffect, useState } from 'react'
import { api } from '../services/api'
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, CartesianGrid, Legend } from 'recharts'

function GraficoMovimentacoes() {
  const [dados, setDados] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    buscarDados()
  }, [])

  async function buscarDados() {
    try {
      setLoading(true)
      const response = await api.get('/grafico/movimentacoes')
      setDados(response.data || [])
    } catch (error) {
      console.error('Erro ao buscar movimentações:', error)
      setDados([])
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="glass-card flex flex-col p-6" style={{ minHeight: '450px' }}>
      <div className="flex items-center justify-between gap-3">
        <div>
          <p className="text-sm uppercase tracking-[0.3em] text-slate-400">Análise</p>
          <h2 className="mt-2 text-2xl font-semibold text-slate-100">Movimentações por tipo</h2>
        </div>
      </div>
      <div className="mt-6 flex-1" style={{ minHeight: '350px', display: 'flex' }}>
        {loading ? (
          <div className="flex h-full w-full items-center justify-center text-slate-400">Carregando...</div>
        ) : dados && dados.length > 0 ? (
          <ResponsiveContainer width="100%" height="100%">
            <BarChart data={dados} margin={{ top: 10, right: 20, left: -20, bottom: 0 }}>
              <CartesianGrid strokeDasharray="3 3" stroke="#334155" />
              <XAxis dataKey="tipo" stroke="#94a3b8" />
              <YAxis stroke="#94a3b8" />
              <Tooltip formatter={(value) => `${value} unidades`} />
              <Legend wrapperStyle={{ color: '#94a3b8' }} />
              <Bar dataKey="total" fill="#38bdf8" radius={[12, 12, 0, 0]} />
            </BarChart>
          </ResponsiveContainer>
        ) : (
          <div className="flex h-full w-full items-center justify-center text-slate-400">Sem dados disponíveis</div>
        )}
      </div>
    </div>
  )
}

export default GraficoMovimentacoes
