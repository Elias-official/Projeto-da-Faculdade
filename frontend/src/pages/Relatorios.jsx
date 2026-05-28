import { useState } from 'react'
import { Download, FileText, Table, File } from 'lucide-react'
import { api } from '../services/api'
import Sidebar from '../components/Sidebar'
import Header from '../components/Header'

function Relatorios() {
  const [downloadType, setDownloadType] = useState('')
  const [loading, setLoading] = useState(false)
  const [success, setSuccess] = useState(false)

  async function handleDownload(path, label) {
    setDownloadType(label)
    setLoading(true)
    try {
      const response = await api.get(path, { responseType: 'blob' })
      const url = window.URL.createObjectURL(new Blob([response.data]))
      const link = document.createElement('a')
      link.href = url
      const filename = response.headers['content-disposition']?.split('filename=')[1]?.replace(/"/g, '') || `relatorio_${Date.now()}`
      link.setAttribute('download', filename)
      document.body.appendChild(link)
      link.click()
      link.remove()
      window.URL.revokeObjectURL(url)
      setSuccess(true)
      setTimeout(() => setSuccess(false), 3000)
    } catch (error) {
      console.error(error)
      alert('Erro ao gerar relatório. Verifique sua conexão.')
    } finally {
      setDownloadType('')
      setLoading(false)
    }
  }

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100">
      <div className="flex min-h-screen flex-col lg:flex-row">
        <Sidebar />
        <main className="flex-1 p-5 lg:p-8">
          <Header />
          <div className="mt-8 space-y-8">
            {/* Seção Produtos */}
            <section className="glass-card p-8 border border-slate-800/50">
              <div className="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between mb-6">
                <div>
                  <h2 className="text-2xl font-bold text-slate-100 flex items-center gap-2">
                    <FileText className="w-6 h-6 text-blue-400" />
                    Relatório de Produtos
                  </h2>
                  <p className="mt-2 text-sm text-slate-400">Exporte dados de produtos em diferentes formatos com timestamp automático.</p>
                </div>
              </div>
              <div className="grid gap-4 sm:grid-cols-3">
                <button
                  onClick={() => handleDownload('/relatorios/produtos/csv', 'Produtos CSV')}
                  disabled={loading || downloadType === 'Produtos CSV'}
                  className="group rounded-2xl border border-slate-700 bg-slate-900/40 px-6 py-6 text-left shadow-lg transition hover:border-blue-500 hover:bg-slate-900 disabled:opacity-50 disabled:cursor-not-allowed"
                >
                  <div className="flex items-center gap-3 mb-3">
                    <Table className="w-5 h-5 text-blue-400 group-hover:text-blue-300" />
                    <span className="text-sm font-semibold text-slate-300">CSV</span>
                  </div>
                  <p className="text-sm text-slate-400 group-hover:text-slate-300">Planilha de Texto</p>
                  {downloadType === 'Produtos CSV' && <p className="mt-2 text-xs text-blue-400 animate-pulse">Gerando...</p>}
                </button>

                <button
                  onClick={() => handleDownload('/relatorios/produtos/xlsx', 'Produtos XLSX')}
                  disabled={loading || downloadType === 'Produtos XLSX'}
                  className="group rounded-2xl border border-slate-700 bg-slate-900/40 px-6 py-6 text-left shadow-lg transition hover:border-emerald-500 hover:bg-slate-900 disabled:opacity-50 disabled:cursor-not-allowed"
                >
                  <div className="flex items-center gap-3 mb-3">
                    <File className="w-5 h-5 text-emerald-400 group-hover:text-emerald-300" />
                    <span className="text-sm font-semibold text-slate-300">Excel</span>
                  </div>
                  <p className="text-sm text-slate-400 group-hover:text-slate-300">Arquivo XLSX</p>
                  {downloadType === 'Produtos XLSX' && <p className="mt-2 text-xs text-emerald-400 animate-pulse">Gerando...</p>}
                </button>

                <button
                  onClick={() => handleDownload('/relatorios/produtos/pdf', 'Produtos PDF')}
                  disabled={loading || downloadType === 'Produtos PDF'}
                  className="group rounded-2xl border border-slate-700 bg-slate-900/40 px-6 py-6 text-left shadow-lg transition hover:border-red-500 hover:bg-slate-900 disabled:opacity-50 disabled:cursor-not-allowed"
                >
                  <div className="flex items-center gap-3 mb-3">
                    <Download className="w-5 h-5 text-red-400 group-hover:text-red-300" />
                    <span className="text-sm font-semibold text-slate-300">PDF</span>
                  </div>
                  <p className="text-sm text-slate-400 group-hover:text-slate-300">Arquivo PDF</p>
                  {downloadType === 'Produtos PDF' && <p className="mt-2 text-xs text-red-400 animate-pulse">Gerando...</p>}
                </button>
              </div>
            </section>

            {/* Seção Movimentações */}
            <section className="glass-card p-8 border border-slate-800/50">
              <div className="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between mb-6">
                <div>
                  <h2 className="text-2xl font-bold text-slate-100 flex items-center gap-2">
                    <FileText className="w-6 h-6 text-purple-400" />
                    Relatório de Movimentações
                  </h2>
                  <p className="mt-2 text-sm text-slate-400">Histórico completo de entrada e saída de produtos.</p>
                </div>
              </div>
              <div className="grid gap-4 sm:grid-cols-3">
                <button
                  onClick={() => handleDownload('/relatorios/movimentacoes/csv', 'Movimentações CSV')}
                  disabled={loading || downloadType === 'Movimentações CSV'}
                  className="group rounded-2xl border border-slate-700 bg-slate-900/40 px-6 py-6 text-left shadow-lg transition hover:border-blue-500 hover:bg-slate-900 disabled:opacity-50 disabled:cursor-not-allowed"
                >
                  <div className="flex items-center gap-3 mb-3">
                    <Table className="w-5 h-5 text-blue-400 group-hover:text-blue-300" />
                    <span className="text-sm font-semibold text-slate-300">CSV</span>
                  </div>
                  <p className="text-sm text-slate-400 group-hover:text-slate-300">Planilha de Texto</p>
                  {downloadType === 'Movimentações CSV' && <p className="mt-2 text-xs text-blue-400 animate-pulse">Gerando...</p>}
                </button>

                <button
                  onClick={() => handleDownload('/relatorios/movimentacoes/xlsx', 'Movimentações XLSX')}
                  disabled={loading || downloadType === 'Movimentações XLSX'}
                  className="group rounded-2xl border border-slate-700 bg-slate-900/40 px-6 py-6 text-left shadow-lg transition hover:border-emerald-500 hover:bg-slate-900 disabled:opacity-50 disabled:cursor-not-allowed"
                >
                  <div className="flex items-center gap-3 mb-3">
                    <File className="w-5 h-5 text-emerald-400 group-hover:text-emerald-300" />
                    <span className="text-sm font-semibold text-slate-300">Excel</span>
                  </div>
                  <p className="text-sm text-slate-400 group-hover:text-slate-300">Arquivo XLSX</p>
                  {downloadType === 'Movimentações XLSX' && <p className="mt-2 text-xs text-emerald-400 animate-pulse">Gerando...</p>}
                </button>

                <button
                  onClick={() => handleDownload('/relatorios/movimentacoes/pdf', 'Movimentações PDF')}
                  disabled={loading || downloadType === 'Movimentações PDF'}
                  className="group rounded-2xl border border-slate-700 bg-slate-900/40 px-6 py-6 text-left shadow-lg transition hover:border-red-500 hover:bg-slate-900 disabled:opacity-50 disabled:cursor-not-allowed"
                >
                  <div className="flex items-center gap-3 mb-3">
                    <Download className="w-5 h-5 text-red-400 group-hover:text-red-300" />
                    <span className="text-sm font-semibold text-slate-300">PDF</span>
                  </div>
                  <p className="text-sm text-slate-400 group-hover:text-slate-300">Arquivo PDF</p>
                  {downloadType === 'Movimentações PDF' && <p className="mt-2 text-xs text-red-400 animate-pulse">Gerando...</p>}
                </button>
              </div>
            </section>

            {/* Feedback de Sucesso */}
            {success && (
              <div className="rounded-2xl border border-emerald-500/30 bg-emerald-500/10 p-4 text-sm text-emerald-200 backdrop-blur-sm animate-pulse">
                <div className="flex items-center gap-2">
                  <div className="h-2 w-2 rounded-full bg-emerald-400"></div>
                  Arquivo baixado com sucesso! ✓
                </div>
              </div>
            )}
          </div>
        </main>
      </div>
    </div>
  )
}

export default Relatorios