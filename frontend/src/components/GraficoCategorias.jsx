import { useEffect, useState } from 'react'
import { api } from '../services/api'
import { PieChart, Pie, Cell, ResponsiveContainer, Tooltip, Legend } from 'recharts'

const COLORS = ['#38bdf8', '#60a5fa', '#818cf8', '#a78bfa', '#c084fc', '#f472b6']

function GraficoCategorias() {
  const [dados, setDados] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    buscarDados()
  }, [])

  async function buscarDados() {
    try {
      setLoading(true)
      const response = await api.get('/grafico/categorias')
      setDados(response.data || [])
    } catch (error) {
      console.error('Erro ao buscar categorias:', error)
      setDados([])
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="glass-card flex flex-col p-6" style={{ minHeight: '450px' }}>
      <div className="flex items-center justify-between gap-3">
        <div>
          <p className="text-sm uppercase tracking-[0.3em] text-slate-400">Gráfico</p>
          <h2 className="mt-2 text-2xl font-semibold text-slate-100">Produtos por categoria</h2>
        </div>
      </div>
      <div className="mt-6 flex-1" style={{ minHeight: '350px', display: 'flex' }}>
        {loading ? (
          <div className="flex h-full w-full items-center justify-center text-slate-400">Carregando...</div>
        ) : dados && dados.length > 0 ? (
          <ResponsiveContainer width="100%" height="100%">
            <PieChart>
              <Pie 
                data={dados} 
                dataKey="total" 
                nameKey="categoria" 
                outerRadius={80} 
                innerRadius={40} 
                paddingAngle={2}
                label={({ categoria, total }) => `${categoria}: ${total}`}
              >
                {dados.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                ))}
              </Pie>
              <Tooltip 
                formatter={(value) => `${value} itens`}
                contentStyle={{
                  backgroundColor: '#1e293b',
                  border: '1px solid #475569',
                  borderRadius: '8px',
                  color: '#f1f5f9'
                }}
              />
              <Legend />
            </PieChart>
          </ResponsiveContainer>
        ) : (
          <div className="flex h-full w-full items-center justify-center text-slate-400">Sem dados disponíveis</div>
        )}
      </div>
    </div>
  )
}

export default GraficoCategorias
