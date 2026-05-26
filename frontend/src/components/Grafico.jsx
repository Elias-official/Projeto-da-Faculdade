import { useEffect, useState } from 'react'
import { PieChart, Pie, Cell, Tooltip, ResponsiveContainer } from 'recharts'
import { apiFetch } from '../services/api'

function Grafico() {
  const [dados, setDados] = useState([])

  useEffect(() => {
    buscarDados()
  }, [])

  async function buscarDados() {
    try {
      const response = await apiFetch('/grafico/categorias')
      const data = await response.json()
      setDados(data)
    } catch (error) {
      console.error(error)
    }
  }

  const COLORS = ['#0088FE', '#00C49F', '#FFBB28', '#FF8042', '#845EC2', '#D65DB1']

  return (
    <div className="chart-box">
      <h2>Produtos por Categoria</h2>
      <div style={{ width: '100%', height: '300px' }}>
        <ResponsiveContainer>
          <PieChart>
            <Pie data={dados} dataKey="total" nameKey="categoria" outerRadius={100} label>
              {dados.map((entry, index) => (
                <Cell key={index} fill={COLORS[index % COLORS.length]} />
              ))}
            </Pie>
            <Tooltip />
          </PieChart>
        </ResponsiveContainer>
      </div>
    </div>
  )
}

export default Grafico
