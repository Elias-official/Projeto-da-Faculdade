import { useEffect, useState } from 'react'
import { api } from '../services/api'
import { PieChart, Pie, Cell, ResponsiveContainer, Tooltip, Legend } from 'recharts'

const COLORS = ['#38bdf8', '#60a5fa', '#818cf8', '#a78bfa', '#c084fc', '#f472b6']
const RADIAN = Math.PI / 180

function GraficoCategorias() {
  const [dados, setDados] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    buscarDados()
  }, [])

  const total = dados.reduce((sum, item) => sum + Number(item.total || 0), 0)

  const renderCustomizedLabel = ({ cx, cy, midAngle, innerRadius, outerRadius, percent }) => {
    const radius = innerRadius + (outerRadius - innerRadius) * 0.5
    const x = cx + radius * Math.cos(-midAngle * RADIAN)
    const y = cy + radius * Math.sin(-midAngle * RADIAN)

    return (
      <text x={x} y={y} fill="#f8fafc" textAnchor={x > cx ? 'start' : 'end'} dominantBaseline="central" fontSize={10}>
        {`${(percent * 100).toFixed(0)}%`}
      </text>
    )
  }

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
                outerRadius={90} 
                innerRadius={45} 
                paddingAngle={2}
                label={renderCustomizedLabel}
                labelLine={false}
              >
                {dados.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                ))}
              </Pie>
              <Tooltip 
                formatter={(value) => `${value} itens`}
                labelFormatter={(label) => `${label}`}
                contentStyle={{
                  backgroundColor: '#1e293b',
                  border: '1px solid #475569',
                  borderRadius: '8px',
                  color: '#f1f5f9'
                }}
              />
              <Legend formatter={(value, entry) => {
                const percent = total ? ((entry.payload.total / total) * 100).toFixed(1) : '0.0'
                return `${value} • ${percent}%`
              }} />
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
