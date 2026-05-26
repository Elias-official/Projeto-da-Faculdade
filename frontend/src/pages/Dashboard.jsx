import { useEffect, useState } from 'react'
import Sidebar from '../components/Sidebar'
import Header from '../components/Header'
import DashboardCards from '../components/DashboardCards'
import GraficoCategorias from '../components/GraficoCategorias'
import GraficoMovimentacoes from '../components/GraficoMovimentacoes'
import Alertas from '../components/Alertas'
import UltimasMovimentacoes from '../components/UltimasMovimentacoes'
import LowStockTable from '../components/LowStockTable'
import { api } from '../services/api'

function Dashboard() {
  const [lowStock, setLowStock] = useState([])

  useEffect(() => {
    buscarEstoqueBaixo()
  }, [])

  async function buscarEstoqueBaixo() {
    try {
      const response = await api.get('/produtos')
      setLowStock(response.data.filter((produto) => produto.status !== 'Estoque normal').slice(0, 5))
    } catch (error) {
      console.error(error)
    }
  }

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100">
      <div className="flex min-h-screen flex-col lg:flex-row">
        <Sidebar />
        <main className="flex-1 p-5 lg:p-8">
          <Header />

          <section className="space-y-6 pt-6">
            <DashboardCards />

            <div className="grid gap-6 xl:grid-cols-[1.45fr_0.95fr]">
              <div className="space-y-6">
                <div className="grid gap-6 xl:grid-cols-2" style={{ alignItems: 'stretch' }}>
                  <GraficoCategorias />
                  <GraficoMovimentacoes />
                </div>
              </div>
              <div className="space-y-6">
                <Alertas />
                <UltimasMovimentacoes />
              </div>
            </div>

            <div className="grid gap-6 xl:grid-cols-[1.6fr_1fr]">
              <LowStockTable produtos={lowStock} />
              <div className="glass-card p-6">
                <div className="flex items-center justify-between gap-3">
                  <div>
                    <p className="text-sm uppercase tracking-[0.3em] text-slate-400">Status do sistema</p>
                    <h2 className="mt-2 text-2xl font-semibold text-slate-100">Saúde do ERP</h2>
                  </div>
                </div>
                <div className="mt-6 space-y-4">
                  <div className="rounded-3xl border border-slate-800 bg-slate-950/90 p-4 shadow-soft">
                    <p className="text-sm text-slate-400">Sistema Online</p>
                    <p className="mt-2 text-lg font-semibold text-slate-100">Conectado</p>
                  </div>
                  <div className="rounded-3xl border border-slate-800 bg-slate-950/90 p-4 shadow-soft">
                    <p className="text-sm text-slate-400">Banco de dados</p>
                    <p className="mt-2 text-lg font-semibold text-slate-100">OK</p>
                  </div>
                  <div className="rounded-3xl border border-slate-800 bg-slate-950/90 p-4 shadow-soft">
                    <p className="text-sm text-slate-400">Backup</p>
                    <p className="mt-2 text-lg font-semibold text-slate-100">27/05 02:00</p>
                  </div>
                </div>
              </div>
            </div>
          </section>
        </main>
      </div>
    </div>
  )
}

export default Dashboard