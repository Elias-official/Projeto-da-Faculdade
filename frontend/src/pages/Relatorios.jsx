import { useState } from 'react'
import { api } from '../services/api'
import Sidebar from '../components/Sidebar'
import Header from '../components/Header'

function Relatorios() {
  const [downloadType, setDownloadType] = useState('')

  async function handleDownload(path, label) {
    setDownloadType(label)
    try {
      const response = await api.get(path, { responseType: 'blob' })
      const url = window.URL.createObjectURL(new Blob([response.data]))
      const link = document.createElement('a')
      link.href = url
      link.setAttribute('download', response.headers['content-disposition']?.split('filename=')[1] || 'relatorio')
      document.body.appendChild(link)
      link.click()
      link.remove()
      window.URL.revokeObjectURL(url)
    } catch (error) {
      console.error(error)
      alert('Erro ao gerar relatório')
    } finally {
      setDownloadType('')
    }
  }

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100">
      <div className="flex min-h-screen flex-col lg:flex-row">
        <Sidebar />
        <main className="flex-1 p-5 lg:p-8">
          <Header />
          <div className="mt-6 space-y-6">
            <section className="glass-card p-6">
              <div className="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
                <div>
                  <h1 className="text-2xl font-semibold">Relatórios</h1>
                  <p className="mt-2 text-slate-400">Exportações sofisticadas em CSV, Excel e PDF.</p>
                </div>
              </div>
              <div className="mt-6 grid gap-4 lg:grid-cols-3">
                <button
                  onClick={() => handleDownload('/relatorios/produtos/csv', 'Produtos CSV')}
                  className="rounded-3xl border border-slate-800 bg-slate-950 px-5 py-5 text-left shadow-soft transition hover:border-blue-500 hover:bg-slate-900"
                >
                  <p className="text-sm text-slate-400">Exportar Produtos</p>
                  <p className="mt-3 text-xl font-semibold text-slate-100">CSV</p>
                </button>
                <button
                  onClick={() => handleDownload('/relatorios/produtos/xlsx', 'Produtos XLSX')}
                  className="rounded-3xl border border-slate-800 bg-slate-950 px-5 py-5 text-left shadow-soft transition hover:border-blue-500 hover:bg-slate-900"
                >
                  <p className="text-sm text-slate-400">Exportar Produtos</p>
                  <p className="mt-3 text-xl font-semibold text-slate-100">Excel</p>
                </button>
                <button
                  onClick={() => handleDownload('/relatorios/produtos/pdf', 'Produtos PDF')}
                  className="rounded-3xl border border-slate-800 bg-slate-950 px-5 py-5 text-left shadow-soft transition hover:border-blue-500 hover:bg-slate-900"
                >
                  <p className="text-sm text-slate-400">Exportar Produtos</p>
                  <p className="mt-3 text-xl font-semibold text-slate-100">PDF</p>
                </button>
              </div>
            </section>
            <section className="glass-card p-6">
              <div className="grid gap-4 lg:grid-cols-3">
                <button
                  onClick={() => handleDownload('/relatorios/movimentacoes/csv', 'Movimentações CSV')}
                  className="rounded-3xl border border-slate-800 bg-slate-950 px-5 py-5 text-left shadow-soft transition hover:border-blue-500 hover:bg-slate-900"
                >
                  <p className="text-sm text-slate-400">Exportar Movimentações</p>
                  <p className="mt-3 text-xl font-semibold text-slate-100">CSV</p>
                </button>
                <button
                  onClick={() => handleDownload('/relatorios/movimentacoes/xlsx', 'Movimentações XLSX')}
                  className="rounded-3xl border border-slate-800 bg-slate-950 px-5 py-5 text-left shadow-soft transition hover:border-blue-500 hover:bg-slate-900"
                >
                  <p className="text-sm text-slate-400">Exportar Movimentações</p>
                  <p className="mt-3 text-xl font-semibold text-slate-100">Excel</p>
                </button>
                <button
                  onClick={() => handleDownload('/relatorios/movimentacoes/pdf', 'Movimentações PDF')}
                  className="rounded-3xl border border-slate-800 bg-slate-950 px-5 py-5 text-left shadow-soft transition hover:border-blue-500 hover:bg-slate-900"
                >
                  <p className="text-sm text-slate-400">Exportar Movimentações</p>
                  <p className="mt-3 text-xl font-semibold text-slate-100">PDF</p>
                </button>
              </div>
            </section>
            {downloadType && <div className="rounded-3xl border border-blue-500/30 bg-blue-500/10 p-4 text-sm text-blue-200">Gerando: {downloadType}</div>}
          </div>
        </main>
      </div>
    </div>
  )
}

export default Relatorios